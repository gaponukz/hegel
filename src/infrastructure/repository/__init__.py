import typing

from neo4j import AsyncSession, AsyncTransaction

from src.application.dto import (
    AllThesises,
    CreateArticle,
    GetArticleInputDTO,
    GetArticleOutputDTO,
    Relation,
)
from src.application.persistent import DialecticalGraph, UnitOfWork
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

        query = queries.CREATE_THESIS
        article_type = self._get_article_type_from_relations(dto.relations)

        if article_type == ArticleType.THESIS:
            query = queries.CREATE_THESIS

        elif article_type == ArticleType.ANTITHESIS:
            kwargs["thesis_id"] = dto.relations[0].to_id
            query = queries.CREATE_ANTITHESIS

        elif article_type == ArticleType.SYNTHESIS:
            kwargs["thesis_id"] = self._get_thesis_id_from_synthesis(
                dto.relations, RelationType.THESIS_SYNTHESIS
            )
            kwargs["antithesis_id"] = self._get_thesis_id_from_synthesis(
                dto.relations, RelationType.ANTITHESIS_SYNTHESIS
            )

            query = queries.CREATE_SYNTHESIS

        result = await self._session.run(query, **kwargs)
        record = await result.single(strict=True)

        return record["thesis_id"]

    async def get_article(self, article_id: str) -> AllThesises:
        raise NotImplementedError

    async def get_article_for_view(
        self, dto: GetArticleInputDTO
    ) -> GetArticleOutputDTO:
        raise NotImplementedError

    async def update_article(self, thesis: AllThesises) -> None:
        raise NotImplementedError

    async def is_antithesis(self, thesis_id: str, antithesis_id: str) -> bool:
        raise NotImplementedError

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
