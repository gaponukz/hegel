import dataclasses

import pytest

from src.application.dto import AllThesises, CreateArticle
from src.application.errors import ApplicationError
from src.application.persistent import DialecticalGraph, UnitOfWork
from src.domain.entities import AntithesisArticle, SynthesisArticle, ThesisArticle
from src.domain.value_objects import RelationType


@dataclasses.dataclass
class _ThesiseDTO(CreateArticle):
    rating: int


class MemoryDialecticalGraphDialecticalGraph(DialecticalGraph):
    def __init__(self):
        self._data: dict[int, _ThesiseDTO] = {}

    async def add_article(self, dto: CreateArticle) -> int:
        article = _ThesiseDTO(
            author_id=dto.author_id,
            title=dto.title,
            text=dto.text,
            relations=dto.relations,
            rating=0,
        )
        article_id = id(article)

        self._data[article_id] = article

        return article_id

    async def get_article(self, article_id: int) -> AllThesises:
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

        if article.relations[0].type == RelationType.ANTITHESIS:
            kwargs["refer_to"] = article.relations[0].to_id
            return AntithesisArticle(**kwargs)  # type: ignore

        elif all(
            rel.type
            in [RelationType.THESIS_SYNTHESIS, RelationType.ANTITHESIS_SYNTHESIS]
            for rel in article.relations
        ):
            for rel in article.relations:
                if rel.type == RelationType.THESIS_SYNTHESIS:
                    kwargs["thesis_id"] = rel.to_id

                elif rel.type == RelationType.ANTITHESIS_SYNTHESIS:
                    kwargs["antithesis_id"] = rel.to_id

            return SynthesisArticle(**kwargs)  # type: ignore

        raise ApplicationError(f"Article(id={article_id}) has unknown type")

    async def update_article(self, thesis: AllThesises) -> None:
        article = self._data.get(thesis.id)

        if article is None:
            raise ApplicationError(f"Article(id={thesis.id} not found)")

        article.rating = thesis.rating

    async def is_antithesis(self, thesis_id: int, antithesis_id: int) -> bool:
        antithesis = self._data.get(antithesis_id)

        if antithesis is None:
            raise ApplicationError(f"Article(id={antithesis_id} not found)")

        if not antithesis.relations:
            return False

        return (
            antithesis.relations[0].to_id == thesis_id
            and antithesis.relations[0].type == RelationType.ANTITHESIS
        )

    def __contains__(self, article_id: int):
        return article_id in self._data


class MemoryUnitOfWork(UnitOfWork):
    def __init__(self):
        self._repository = MemoryDialecticalGraphDialecticalGraph()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    @property
    def repository(self):
        return self._repository


@pytest.fixture
def uow():
    return MemoryUnitOfWork()
