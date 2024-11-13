import dataclasses


@dataclasses.dataclass
class ThesisArticle:
    id: int
    author_id: int
    title: str
    text: str
    rating: int


@dataclasses.dataclass
class AntithesisArticle(ThesisArticle):
    refer_to: int


@dataclasses.dataclass
class SynthesisArticle(ThesisArticle):
    thesis_id: int
    antithesis_id: int
