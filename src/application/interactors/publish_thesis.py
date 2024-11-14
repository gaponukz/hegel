from src.application.dto import (
    CreateArticle,
    PublishArticleOutputDTO,
    PublishThesisArticleInputDTO,
)
from src.application.persistent import UnitOfWork
from src.application.usecases import PublishThesisArticleUseCase


class PublishThesis(PublishThesisArticleUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(
        self, dto: PublishThesisArticleInputDTO
    ) -> PublishArticleOutputDTO:
        article_id = await self._uow.repository.add_article(
            CreateArticle(
                author_id=dto.author_id,
                title=dto.title,
                text=dto.text,
                relations=[],
            )
        )

        return PublishArticleOutputDTO(id=article_id)
