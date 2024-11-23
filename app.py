import contextlib
import typing

from fastapi import FastAPI, HTTPException, Request
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


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncGraphDatabase.driver(
        config.neo4j_uri, auth=(config.neo4j_user, config.neo4j_password)
    ) as driver:
        async with driver.session(database="neo4j") as session:
            app.uow = Neo4jThesisUnitOfWork(session)  # type: ignore
            yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(TokenAuthMiddleware, token=config.token)
app.add_middleware(ErrorHandlingMiddleware)


@app.get("/view/{article_type}/{article_id}", response_model=dto.GetArticleOutputDTO)
async def view_article(request: Request, article_type: str, article_id: str):
    if article_type.upper() not in ArticleType:
        raise HTTPException(status_code=400, detail="Incorrect article type")

    return await interactors.get_article(
        request.app.uow,
        dto.GetArticleInputDTO(
            article_id=article_id,
            article_type=ArticleType[article_type.upper()],
        ),
    )


@app.post("/publish", response_model=dto.PublishArticleOutputDTO)
async def publish_article(
    request: Request,
    data: typing.Union[
        dto.PublishThesisArticleInputDTO,
        dto.PublishAntithesisArticleInputDTO,
        dto.PublishSynthesisArticleInputDTO,
    ],
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

    return await publish(request.app.uow, data)


class RataArticleModel(BaseModel):
    is_positive: bool


@app.post("/rate/{article_id}")
async def rate_article(request: Request, article_id: str, data: RataArticleModel):
    await interactors.rate_article(
        request.app.uow,
        dto.RateArticleInputDTO(article_id=article_id, is_positive=data.is_positive),
    )
