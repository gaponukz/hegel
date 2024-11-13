from src.application.dto import (
    CreateArticle,
    PublishArticleOutputDTO,
    PublishSynthesisArticleInputDTO,
    Relation,
)
from src.application.errors import ApplicationError
from src.application.persistent import UnitOfWork
from src.application.usecases import PublishSynthesisArticle
from src.domain.value_objects import RelationType


class PublishSynthesis(PublishSynthesisArticle):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def __call__(self, dto: PublishSynthesisArticleInputDTO) -> PublishArticleOutputDTO:
        if dto.thesis_id == dto.antithesis_id:
            raise ApplicationError("Can not create synthesis from one article")

        if not self._db.is_antithesis(dto.thesis_id, dto.antithesis_id):
            raise ApplicationError(
                f"To create synthesis article {dto.antithesis_id}"
                f" need to be antithesis to {dto.thesis_id}"
            )

        article_id = self._uow.repository.add_article(
            CreateArticle(
                author_id=dto.author_id,
                title=dto.title,
                text=dto.text,
                relations=[
                    Relation(to_id=dto.thesis_id, type=RelationType.SYNTHESIS),
                    Relation(to_id=dto.antithesis_id, type=RelationType.SYNTHESIS),
                ],
            )
        )

        return PublishArticleOutputDTO(id=article_id)
