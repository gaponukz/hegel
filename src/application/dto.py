import dataclasses
import typing

from typing_extensions import TypeAlias

from src.domain.entities import AntithesisArticle, SynthesisArticle, ThesisArticle
from src.domain.value_objects import ArticleType, RelationType

AllThesises: TypeAlias = typing.Union[
    ThesisArticle, AntithesisArticle, SynthesisArticle
]


@dataclasses.dataclass
class _BasePublishArticleInputDTO:
    author_id: int
    title: str
    text: str


@dataclasses.dataclass
class PublishThesisArticleInputDTO(_BasePublishArticleInputDTO):
    pass


@dataclasses.dataclass
class PublishAntithesisArticleInputDTO(_BasePublishArticleInputDTO):
    thesis_id: str


@dataclasses.dataclass
class PublishSynthesisArticleInputDTO(_BasePublishArticleInputDTO):
    thesis_id: str
    antithesis_id: str


@dataclasses.dataclass
class PublishArticleOutputDTO:
    id: str


@dataclasses.dataclass
class RateArticleInputDTO:
    article_id: str
    is_positive: bool


@dataclasses.dataclass
class Relation:
    to_id: str
    type: RelationType


@dataclasses.dataclass
class CreateArticle(_BasePublishArticleInputDTO):
    relations: list[Relation]


@dataclasses.dataclass
class GetArticleInputDTO:
    article_id: str
    article_type: ArticleType


@dataclasses.dataclass
class ViewArticleRelation:
    to_id: str
    to_name: str
    type: RelationType


@dataclasses.dataclass
class GetArticleOutputDTO:
    id: str
    type: ArticleType
    author_id: int
    title: str
    text: str
    rating: int
    relations: list[ViewArticleRelation]
