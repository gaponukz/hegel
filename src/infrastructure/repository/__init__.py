import typing

from neo4j import AsyncSession, AsyncTransaction

from src.application.dto import AllThesises, CreateArticle, GetArticleInputDTO
from src.application.persistent import DialecticalGraph, UnitOfWork
from src.domain.value_objects import RelationType


class Neo4jThesisRepository(DialecticalGraph):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_article(self, dto: CreateArticle) -> str:
        kwargs: dict[str, typing.Any] = {
            "title": dto.title,
            "text": dto.text,
            "author_id": dto.author_id,
        }

        if not dto.relations:
            query = "CREATE (t:Thesis {uuid: randomUUID(), title: $title, text: $text, author_id: $author_id, rating: 0}) RETURN t.uuid AS thesis_id"

        elif (
            len(dto.relations) == 1 and dto.relations[0].type == RelationType.ANTITHESIS
        ):
            kwargs["thesis_id"] = dto.relations[0].to_id
            query = "MATCH (t:Thesis) WHERE t.uuid = $thesis_id CREATE (at:Thesis {uuid: randomUUID(), title: $title, text: $text, author_id: $author_id, rating: 0})-[:ANTITHESIS]->(t) RETURN at.uuid AS thesis_id"

        elif len(dto.relations) == 2 and all(
            RelationType.is_synthesis(rel.type) for rel in dto.relations
        ):
            kwargs["thesis_id"] = [
                rel
                for rel in dto.relations
                if rel.type == RelationType.THESIS_SYNTHESIS
            ][0].to_id
            kwargs["antithesis_id"] = [
                rel
                for rel in dto.relations
                if rel.type == RelationType.ANTITHESIS_SYNTHESIS
            ][0].to_id

            query = "MATCH (t:Thesis), (at:Thesis) WHERE t.uuid = $thesis_id AND at.uuid = $antithesis_id CREATE (st:Thesis {uuid: randomUUID(), title: $title, text: $text, author_id: $author_id, rating: 0})-[:THESIS_SYNTHESIS]->(t), (st)-[:ANTITHESIS_SYNTHESIS]->(at) RETURN st.uuid AS thesis_id"

        result = await self._session.run(query, **kwargs)
        record = await result.single(strict=True)

        return record["thesis_id"]

    async def get_article(self, dto: GetArticleInputDTO) -> AllThesises:
        raise NotImplementedError

    async def update_article(self, thesis: AllThesises) -> None:
        raise NotImplementedError

    async def is_antithesis(self, thesis_id: str, antithesis_id: str) -> bool:
        raise NotImplementedError


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
