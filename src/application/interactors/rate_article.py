from src.application.dto import RateArticleInputDTO
from src.application.persistent import UnitOfWork
from src.application.usecases import RateArticleUseCase


class RateArticle(RateArticleUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, dto: RateArticleInputDTO) -> None:
        async with self._uow as uow:
            article = await uow.repository.get_article(dto.article_id)
            article.rating += 1 if dto.is_positive else -1

            await uow.repository.update_article(article)
