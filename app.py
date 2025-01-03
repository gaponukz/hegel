import typing
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from neo4j import AsyncGraphDatabase
from pydantic import BaseModel

from config import config
from src.application import dto
from src.application import interactors as services
from src.application.persistent import UnitOfWork
from src.domain.value_objects import ArticleType
from src.infrastructure.controllers.middleware import (
    ErrorHandlingMiddleware,
    TokenAuthMiddleware,
)
from src.infrastructure.logger import log_interactor
from src.infrastructure.repository import Neo4jThesisUnitOfWork


class InteractorsFactory:
    def __init__(self):
        self.get_article = log_interactor(services.get_article)
        self.publish_thesis = log_interactor(services.publish_thesis)
        self.publish_antithesis = log_interactor(services.publish_antithesis)
        self.publish_synthesis = log_interactor(services.publish_synthesis)
        self.rate_article = log_interactor(services.rate_article)


interactors = InteractorsFactory()
driver = AsyncGraphDatabase.driver(
    config.neo4j_uri, auth=(config.neo4j_user, config.neo4j_password)
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await driver.close()


app = FastAPI(lifespan=lifespan)
if config.token is not None:
    app.add_middleware(TokenAuthMiddleware, token=config.token)
app.add_middleware(ErrorHandlingMiddleware)


async def get_uow():
    async with driver.session(database=config.neo4j_database) as session:
        yield Neo4jThesisUnitOfWork(session)


@app.get("/view/{article_type}/{article_id}", response_model=dto.GetArticleOutputDTO)
async def view_article(
    article_type: str, article_id: str, uow: UnitOfWork = Depends(get_uow)
):
    if article_type.upper() not in ArticleType:
        raise HTTPException(status_code=400, detail="Incorrect article type")

    return await interactors.get_article(
        uow,
        dto.GetArticleInputDTO(
            article_id=article_id,
            article_type=ArticleType[article_type.upper()],
        ),
    )


@app.post("/publish", response_model=dto.PublishArticleOutputDTO)
async def publish_article(
    data: typing.Union[
        dto.PublishThesisArticleInputDTO,
        dto.PublishAntithesisArticleInputDTO,
        dto.PublishSynthesisArticleInputDTO,
    ],
    uow: UnitOfWork = Depends(get_uow),
):
    D = typing.TypeVar("D")

    def get_interactor(
        data: typing.Type[D],
    ) -> typing.Callable[
        [UnitOfWork, D], typing.Awaitable[dto.PublishArticleOutputDTO]
    ]:
        # fmt: off
        return {
            dto.PublishThesisArticleInputDTO: interactors.publish_thesis,
            dto.PublishAntithesisArticleInputDTO: interactors.publish_antithesis,
            dto.PublishSynthesisArticleInputDTO: interactors.publish_synthesis,
        }[data]  # type: ignore
        # fmt: on

    publish = get_interactor(type(data))

    return await publish(uow, data)


class RataArticleModel(BaseModel):
    is_positive: bool


@app.post("/rate/{article_id}")
async def rate_article(
    article_id: str, data: RataArticleModel, uow: UnitOfWork = Depends(get_uow)
):
    await interactors.rate_article(
        uow,
        dto.RateArticleInputDTO(article_id=article_id, is_positive=data.is_positive),
    )
