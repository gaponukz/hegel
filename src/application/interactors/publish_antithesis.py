from src.application.dto import (
    CreateArticle,
    PublishAntithesisArticleInputDTO,
    PublishArticleOutputDTO,
    Relation,
)
from src.application.errors import ArticleNotFoundError
from src.application.persistent import UnitOfWork
from src.application.usecases import PublishAntithesisArticleUseCase
from src.domain.value_objects import RelationType


class PublishAntithesis(PublishAntithesisArticleUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(
        self, dto: PublishAntithesisArticleInputDTO
    ) -> PublishArticleOutputDTO:
        if not await self._uow.repository.is_article_exists(dto.thesis_id):
            raise ArticleNotFoundError(dto.thesis_id)

        article_id = await self._uow.repository.add_article(
            CreateArticle(
                author_id=dto.author_id,
                title=dto.title,
                text=dto.text,
                relations=[Relation(to_id=dto.thesis_id, type=RelationType.ANTITHESIS)],
            )
        )

        return PublishArticleOutputDTO(id=article_id)
