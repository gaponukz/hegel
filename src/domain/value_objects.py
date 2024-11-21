import enum


class ArticleType(enum.StrEnum):
    THESIS = "THESIS"
    ANTITHESIS = "ANTITHESIS"
    SYNTHESIS = "SYNTHESIS"

    def __contains__(self, key):
        if isinstance(key, str):
            return key in self._member_map_

        return super().__contains__(key)


class RelationType(enum.StrEnum):
    ANTITHESIS = "ANTITHESIS"
    THESIS_SYNTHESIS = "THESIS_SYNTHESIS"
    ANTITHESIS_SYNTHESIS = "ANTITHESIS_SYNTHESIS"

    @classmethod
    def is_synthesis(cls, _type) -> bool:
        return _type in [cls.THESIS_SYNTHESIS, cls.ANTITHESIS_SYNTHESIS]
