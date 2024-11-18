import dataclasses


@dataclasses.dataclass
class ThesisArticle:
    id: str
    author_id: int
    title: str
    text: str
    rating: int


@dataclasses.dataclass
class AntithesisArticle(ThesisArticle):
    refer_to: str


@dataclasses.dataclass
class SynthesisArticle(ThesisArticle):
    thesis_id: str
    antithesis_id: str
