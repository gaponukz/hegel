import dataclasses
import uuid

import pytest

from src.application.dto import (
    AllThesises,
    CreateArticle,
    GetArticleInputDTO,
    GetArticleOutputDTO,
    ViewArticleRelation,
)
from src.application.errors import ApplicationError
from src.application.persistent import DialecticalGraph, UnitOfWork
from src.domain.entities import AntithesisArticle, SynthesisArticle, ThesisArticle
from src.domain.value_objects import ArticleType, RelationType


@dataclasses.dataclass
class _ThesiseDTO(CreateArticle):
    rating: int


class MemoryDialecticalGraphDialecticalGraph(DialecticalGraph):
    def __init__(self):
        self._data: dict[str, _ThesiseDTO] = {}

    async def add_article(self, dto: CreateArticle) -> str:
        article = _ThesiseDTO(
            author_id=dto.author_id,
            title=dto.title,
            text=dto.text,
            relations=dto.relations,
            rating=0,
        )
        article_id = str(uuid.uuid4())

        self._data[article_id] = article

        return article_id

    async def get_article(self, article_id: str) -> AllThesises:
        article = self._data.get(article_id)

        if article is None:
            raise ApplicationError(f"Article(id={article_id} not found)")

        kwargs = {
            "id": article_id,
            "author_id": article.author_id,
            "title": article.title,
            "text": article.text,
            "rating": article.rating,
        }

        if not article.relations:
            return ThesisArticle(**kwargs)  # type: ignore

        elif len(article.relations) == 1:
            kwargs["thesis_id"] = article.relations[0].to_id
            return AntithesisArticle(**kwargs)  # type: ignore

        elif len(article.relations) == 2:
            for rel in article.relations:
                if rel.type == RelationType.THESIS_SYNTHESIS:
                    kwargs["thesis_id"] = rel.to_id

                elif rel.type == RelationType.ANTITHESIS_SYNTHESIS:
                    kwargs["antithesis_id"] = rel.to_id

            return SynthesisArticle(**kwargs)  # type: ignore

        raise ApplicationError(f"Article(id={article_id}) has unknown type")

    async def get_article_for_view(
        self, dto: GetArticleInputDTO
    ) -> GetArticleOutputDTO:
        article = await self.get_article(dto.article_id)
        output = GetArticleOutputDTO(
            id=article.id,
            type=dto.article_type,
            author_id=article.author_id,
            title=article.title,
            text=article.text,
            rating=article.rating,
            relations=[],
        )

        if dto.article_type == ArticleType.THESIS:
            return output

        if isinstance(article, AntithesisArticle):
            thesis = await self.get_article(article_id=article.thesis_id)
            output.relations.append(
                ViewArticleRelation(
                    to_id=thesis.id,
                    to_name=thesis.title,
                    type=RelationType.ANTITHESIS,
                )
            )

        elif isinstance(article, SynthesisArticle):
            thesis = await self.get_article(article_id=article.thesis_id)
            antithesis = await self.get_article(article_id=article.antithesis_id)

            output.relations.append(
                ViewArticleRelation(
                    to_id=thesis.id,
                    to_name=thesis.title,
                    type=RelationType.THESIS_SYNTHESIS,
                )
            )

            output.relations.append(
                ViewArticleRelation(
                    to_id=antithesis.id,
                    to_name=antithesis.title,
                    type=RelationType.ANTITHESIS_SYNTHESIS,
                )
            )

        return output

    async def update_article(self, thesis: AllThesises) -> None:
        article = self._data.get(thesis.id)

        if article is None:
            raise ApplicationError(f"Article(id={thesis.id} not found)")

        article.rating = thesis.rating

    async def is_antithesis(self, thesis_id: str, antithesis_id: str) -> bool:
        antithesis = self._data.get(antithesis_id)

        if antithesis is None:
            raise ApplicationError(f"Article(id={antithesis_id} not found)")

        if not antithesis.relations:
            return False

        return (
            antithesis.relations[0].to_id == thesis_id
            and antithesis.relations[0].type == RelationType.ANTITHESIS
        )

    async def is_article_exists(self, article_id: str) -> bool:
        return article_id in self._data


class MemoryUnitOfWork(UnitOfWork):
    def __init__(self):
        self._repository = MemoryDialecticalGraphDialecticalGraph()
        self.executed_in_transaction = False

    async def __aenter__(self):
        self.executed_in_transaction = True
        return self

    async def __aexit__(self, *args):
        pass

    @property
    def repository(self):
        return self._repository


@pytest.fixture
def uow():
    return MemoryUnitOfWork()
