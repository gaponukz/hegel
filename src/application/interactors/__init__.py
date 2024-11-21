from src.application import dto
from src.application.errors import ApplicationError, ArticleNotFoundError
from src.application.persistent import UnitOfWork
from src.domain.value_objects import RelationType


async def get_article(
    uow: UnitOfWork, data: dto.GetArticleInputDTO
) -> dto.GetArticleOutputDTO:
    return await uow.repository.get_article_for_view(data)


async def publish_thesis(
    uow: UnitOfWork, article: dto.PublishThesisArticleInputDTO
) -> dto.PublishArticleOutputDTO:
    article_id = await uow.repository.add_article(
        dto.CreateArticle(
            author_id=article.author_id,
            title=article.title,
            text=article.text,
            relations=[],
        )
    )

    return dto.PublishArticleOutputDTO(id=article_id)


async def publish_antithesis(
    uow: UnitOfWork, article: dto.PublishAntithesisArticleInputDTO
) -> dto.PublishArticleOutputDTO:
    if not await uow.repository.is_article_exists(article.thesis_id):
        raise ArticleNotFoundError(article.thesis_id)

    article_id = await uow.repository.add_article(
        dto.CreateArticle(
            author_id=article.author_id,
            title=article.title,
            text=article.text,
            relations=[
                dto.Relation(to_id=article.thesis_id, type=RelationType.ANTITHESIS)
            ],
        )
    )

    return dto.PublishArticleOutputDTO(id=article_id)


async def publish_synthesis(
    uow: UnitOfWork, article: dto.PublishSynthesisArticleInputDTO
) -> dto.PublishArticleOutputDTO:
    if article.thesis_id == article.antithesis_id:
        raise ApplicationError("Can not create synthesis from one article")

    if not await uow.repository.is_antithesis(article.thesis_id, article.antithesis_id):
        raise ApplicationError(
            f"To create synthesis article {article.antithesis_id}"
            f" need to be antithesis to {article.thesis_id}"
        )

    article_id = await uow.repository.add_article(
        dto.CreateArticle(
            author_id=article.author_id,
            title=article.title,
            text=article.text,
            relations=[
                dto.Relation(
                    to_id=article.thesis_id, type=RelationType.THESIS_SYNTHESIS
                ),
                dto.Relation(
                    to_id=article.antithesis_id, type=RelationType.ANTITHESIS_SYNTHESIS
                ),
            ],
        )
    )

    return dto.PublishArticleOutputDTO(id=article_id)


async def rate_article(uow: UnitOfWork, data: dto.RateArticleInputDTO) -> None:
    async with uow:
        article = await uow.repository.get_article(data.article_id)
        article.rating += 1 if data.is_positive else -1

        await uow.repository.update_article(article)
