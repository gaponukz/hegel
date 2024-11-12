import dataclasses


@dataclasses.dataclass
class _BaseArticle:
    id: int
    author_id: int
    title: str
    text: str
    rating: int


@dataclasses.dataclass
class ThesisArticle(_BaseArticle):
    pass


@dataclasses.dataclass
class AntithesisArticle(_BaseArticle):
    refer_to: int


@dataclasses.dataclass
class SynthesisArticle(_BaseArticle):
    thesis_id: int
    antithesis_id: int
