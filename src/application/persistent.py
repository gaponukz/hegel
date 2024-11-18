from __future__ import annotations

import typing

from src.application.dto import AllThesises, CreateArticle, GetArticleInputDTO


class DialecticalGraph(typing.Protocol):
    async def add_article(self, dto: CreateArticle) -> str: ...

    async def get_article(self, dto: GetArticleInputDTO) -> AllThesises: ...

    async def update_article(self, thesis: AllThesises) -> None: ...

    async def is_antithesis(self, thesis_id: str, antithesis_id: str) -> bool: ...


class UnitOfWork(typing.Protocol):
    async def __aenter__(self) -> UnitOfWork: ...

    async def __aexit__(self, *args): ...

    @property
    def repository(self) -> DialecticalGraph: ...
