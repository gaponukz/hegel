from __future__ import annotations

import typing

from src.application.dto import (
    AllThesises,
    CreateArticle,
    GetArticleInputDTO,
    GetArticleOutputDTO,
)


class DialecticalGraph(typing.Protocol):
    async def add_article(self, dto: CreateArticle) -> str: ...

    async def get_article(self, article_id: str) -> AllThesises: ...

    async def get_article_for_view(
        self, dto: GetArticleInputDTO
    ) -> GetArticleOutputDTO: ...

    async def update_article(self, thesis: AllThesises) -> None: ...

    async def is_antithesis(self, thesis_id: str, antithesis_id: str) -> bool: ...


class UnitOfWork(typing.Protocol):
    async def __aenter__(self) -> UnitOfWork: ...

    async def __aexit__(self, *args): ...

    @property
    def repository(self) -> DialecticalGraph: ...
