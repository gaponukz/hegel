import enum


class ArticleTypeMeta(enum.EnumMeta):
    def __contains__(self, member):
        if isinstance(member, str):
            return member in self._value2member_map_

        return super().__contains__(member)


class ArticleType(enum.StrEnum, metaclass=ArticleTypeMeta):
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
