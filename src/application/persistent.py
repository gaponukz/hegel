from __future__ import annotations

import typing

from src.application.dto import AllThesises, CreateArticle


class DialecticalGraph(typing.Protocol):
    async def add_article(self, dto: CreateArticle) -> int: ...

    async def get_article(self, article_id: int) -> AllThesises: ...

    async def update_article(self, thesis: AllThesises) -> None: ...

    async def is_antithesis(self, thesis_id: int, antithesis_id: int) -> bool: ...


class UnitOfWork(typing.Protocol):
    async def __aenter__(self) -> UnitOfWork: ...

    async def __aexit__(self, *args): ...

    @property
    def repository(self) -> DialecticalGraph: ...
