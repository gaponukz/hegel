import enum


class ArticleType(enum.StrEnum):
    THESIS = "THESIS"
    ANTITHESIS = "ANTITHESIS"
    SYNTHESIS = "SYNTHESIS"


class RelationType(enum.StrEnum):
    ANTITHESIS = "ANTITHESIS"
    THESIS_SYNTHESIS = "THESIS_SYNTHESIS"
    ANTITHESIS_SYNTHESIS = "ANTITHESIS_SYNTHESIS"

    @classmethod
    def is_synthesis(cls, _type) -> bool:
        return _type in [cls.THESIS_SYNTHESIS, cls.ANTITHESIS_SYNTHESIS]
