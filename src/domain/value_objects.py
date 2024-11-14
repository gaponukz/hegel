import enum


class ArticleType(enum.StrEnum):
    THESIS = "thesis"
    ANTITHESIS = "antithesis"
    SYNTHESIS = "synthesis"


class RelationType(enum.StrEnum):
    ANTITHESIS = "antithesis"
    THESIS_SYNTHESIS = "thesis_synthesis"
    ANTITHESIS_SYNTHESIS = "antithesis_synthesis"
