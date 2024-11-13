from __future__ import annotations

import typing

from src.application.dto import AllThesises, CreateArticle


class DialecticalGraph(typing.Protocol):
    def add_article(self, dto: CreateArticle) -> int: ...

    def get_article(self, article_id: int) -> AllThesises: ...

    def update_article(self, thesis: AllThesises) -> None: ...

    def is_antithesis(self, thesis_id: int, antithesis_id: int) -> bool: ...


class UnitOfWork(typing.Protocol):
    def __enter__(self) -> UnitOfWork: ...

    def __exit__(self, *args): ...

    @property
    def repository(self) -> DialecticalGraph: ...
