from src.application.dto import (
    CreateArticle,
    PublishArticleOutputDTO,
    PublishThesisArticleInputDTO,
)
from src.application.persistent import UnitOfWork
from src.application.usecases import PublishThesisArticle


class PublishThesis(PublishThesisArticle):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def __call__(self, dto: PublishThesisArticleInputDTO) -> PublishArticleOutputDTO:
        article_id = self._uow.repository.add_article(
            CreateArticle(
                author_id=dto.author_id,
                title=dto.title,
                text=dto.text,
                relations=[],
            )
        )

        return PublishArticleOutputDTO(id=article_id)
