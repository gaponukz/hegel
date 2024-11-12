import dataclasses
import typing


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
    type: typing.Literal["positive", "negative"]
