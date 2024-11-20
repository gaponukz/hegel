import typing

from neo4j import AsyncSession, AsyncTransaction, Record

from src.application.dto import (
    AllThesises,
    CreateArticle,
    GetArticleInputDTO,
    GetArticleOutputDTO,
    Relation,
    ViewArticleRelation,
)
from src.application.errors import ArticleNotFoundError
from src.application.persistent import DialecticalGraph, UnitOfWork
from src.domain.entities import AntithesisArticle, SynthesisArticle, ThesisArticle
from src.domain.value_objects import ArticleType, RelationType
from src.infrastructure.repository import queries


class Neo4jThesisRepository(DialecticalGraph):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_article(self, dto: CreateArticle) -> str:
        kwargs: dict[str, typing.Any] = {
            "title": dto.title,
            "text": dto.text,
            "author_id": dto.author_id,
        }

        article_type = self._get_article_type_from_relations(dto.relations)

        if article_type == ArticleType.THESIS:
            query = queries.CREATE_THESIS

        elif article_type == ArticleType.ANTITHESIS:
            query = queries.CREATE_ANTITHESIS
            kwargs["thesis_id"] = dto.relations[0].to_id

        elif article_type == ArticleType.SYNTHESIS:
            query = queries.CREATE_SYNTHESIS
            kwargs["thesis_id"] = self._get_thesis_id_from_synthesis(
                dto.relations, RelationType.THESIS_SYNTHESIS
            )
            kwargs["antithesis_id"] = self._get_thesis_id_from_synthesis(
                dto.relations, RelationType.ANTITHESIS_SYNTHESIS
            )

        result = await self._session.run(query, **kwargs)
        record = await result.single(strict=True)

        return record["thesis_id"]

    async def get_article(self, article_id: str) -> AllThesises:
        result = await self._session.run(queries.GET_THESIS_BY_ID, thesis_id=article_id)
        record = await result.single()

        if record is None or record["selected"] is None:
            raise ArticleNotFoundError(article_id)

        kwargs, atype = self._parse_kwargs_from_record(record)

        cls = {
            ArticleType.THESIS: ThesisArticle,
            ArticleType.ANTITHESIS: AntithesisArticle,
            ArticleType.SYNTHESIS: SynthesisArticle,
        }[atype]

        return cls(**kwargs)

    async def get_article_for_view(
        self, dto: GetArticleInputDTO
    ) -> GetArticleOutputDTO:
        result = await self._session.run(
            queries.GET_THESIS_BY_ID, thesis_id=dto.article_id
        )
        record = await result.single()

        if record is None or record["selected"] is None:
            raise ArticleNotFoundError(dto.article_id)

        kwargs, atype = self._parse_kwargs_from_record(record)

        if atype != dto.article_type:
            raise ArticleNotFoundError(f"{dto.article_id}")

        output = GetArticleOutputDTO(
            id=kwargs["id"],
            author_id=kwargs["author_id"],
            title=kwargs["title"],
            text=kwargs["text"],
            rating=kwargs["rating"],
            type=dto.article_type,
            relations=[],
        )
        if dto.article_type == ArticleType.THESIS:
            return output

        if dto.article_type == ArticleType.ANTITHESIS:
            output.relations.append(
                ViewArticleRelation(
                    to_id=record["antithesis_thesis"]["uuid"],
                    to_name=record["antithesis_thesis"]["title"],
                    type=RelationType.ANTITHESIS,
                )
            )

        elif dto.article_type == ArticleType.SYNTHESIS:
            output.relations.append(
                ViewArticleRelation(
                    to_id=record["synthesis_thesis"]["uuid"],
                    to_name=record["synthesis_thesis"]["title"],
                    type=RelationType.THESIS_SYNTHESIS,
                )
            )

            output.relations.append(
                ViewArticleRelation(
                    to_id=record["synthesis_antithesis"]["uuid"],
                    to_name=record["synthesis_antithesis"]["title"],
                    type=RelationType.ANTITHESIS_SYNTHESIS,
                )
            )

        return output

    async def update_article(self, thesis: AllThesises) -> None:
        result = await self._session.run(
            queries.UPDATE_THESIS_BY_ID,
            thesis_id=thesis.id,
            rating=thesis.rating,
            text=thesis.text,
            title=thesis.title,
        )
        record = await result.single()

        if record is None or not record["exists"]:
            raise ArticleNotFoundError(thesis.id)

    async def is_antithesis(self, thesis_id: str, antithesis_id: str) -> bool:
        result = await self._session.run(
            queries.CHECK_ANTITHESIS_RELATIONS,
            thesis_id=thesis_id,
            antithesis_id=antithesis_id,
        )
        record = await result.single()

        return record is not None and record["exists"]

    @classmethod
    def _get_article_type_from_relations(cls, relations: list[Relation]) -> ArticleType:
        if not relations:
            return ArticleType.THESIS

        if len(relations) == 1 and relations[0].type == RelationType.ANTITHESIS:
            return ArticleType.ANTITHESIS

        return ArticleType.SYNTHESIS

    @classmethod
    def _get_thesis_id_from_synthesis(
        cls, relations: list[Relation], _type: RelationType
    ) -> str:
        assert _type != RelationType.ANTITHESIS
        return [rel for rel in relations if rel.type == _type][0].to_id

    @classmethod
    def _parse_kwargs_from_record(cls, record: Record) -> tuple[dict, ArticleType]:
        atype = ArticleType.THESIS
        kwargs = {
            "id": record["selected"]["uuid"],
            "author_id": record["selected"]["author_id"],
            "title": record["selected"]["title"],
            "text": record["selected"]["text"],
            "rating": record["selected"]["rating"],
        }

        if record["antithesis_thesis"] is not None:
            atype = ArticleType.ANTITHESIS
            kwargs["refer_to"] = record["antithesis_thesis"]["uuid"]

        elif (
            record["synthesis_thesis"] is not None
            and record["synthesis_antithesis"] is not None
        ):
            atype = ArticleType.SYNTHESIS
            kwargs["thesis_id"] = record["synthesis_thesis"]["uuid"]
            kwargs["antithesis_id"] = record["synthesis_antithesis"]["uuid"]

        return kwargs, atype


class Neo4jThesisUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = Neo4jThesisRepository(session)
        self._transaction: typing.Optional[AsyncTransaction] = None

    async def __aenter__(self) -> UnitOfWork:
        self._transaction = await self._session.begin_transaction()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._transaction is None:
            return

        if exc_type is None:
            await self._transaction.commit()
        else:
            await self._transaction.rollback()

    @property
    def repository(self) -> Neo4jThesisRepository:
        return self._repository
