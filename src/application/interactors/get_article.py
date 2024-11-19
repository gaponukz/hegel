from src.application.dto import GetArticleInputDTO, GetArticleOutputDTO
from src.application.persistent import UnitOfWork
from src.application.usecases import GetArticleUseCase


class GetArticle(GetArticleUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, dto: GetArticleInputDTO) -> GetArticleOutputDTO:
        return await self._uow.repository.get_article_for_view(dto)
