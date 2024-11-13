import dataclasses
import typing

from typing_extensions import TypeAlias

from src.domain.entities import AntithesisArticle, SynthesisArticle, ThesisArticle
from src.domain.value_objects import RelationType

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
    refer_to: int


@dataclasses.dataclass
class PublishSynthesisArticleInputDTO(_BasePublishArticleInputDTO):
    thesis_id: int
    antithesis_id: int


@dataclasses.dataclass
class PublishArticleOutputDTO:
    id: int


@dataclasses.dataclass
class RateArticleInputDTO:
    article_id: int
    is_positive: bool


@dataclasses.dataclass
class Relation:
    to_id: int
    type: RelationType


@dataclasses.dataclass
class CreateArticle(_BasePublishArticleInputDTO):
    relations: list[Relation]


@dataclasses.dataclass
class ViewArticleRelation:
    to_id: int
    to_name: str
    type: RelationType


@dataclasses.dataclass
class GetArticleOutputDTO:
    id: int
    author_id: int
    title: str
    text: str
    relations: list[ViewArticleRelation]
