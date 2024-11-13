from src.application.dto import GetArticleOutputDTO, ViewArticleRelation
from src.application.persistent import UnitOfWork
from src.application.usecases import GetArticleUseCase
from src.domain.entities import AntithesisArticle, SynthesisArticle, ThesisArticle
from src.domain.value_objects import RelationType


class PublishAntithesis(GetArticleUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def __call__(self, article_id: int) -> GetArticleOutputDTO:
        article = self._uow.repository.get_article(article_id)
        output = GetArticleOutputDTO(
            id=article.id,
            author_id=article.author_id,
            title=article.title,
            text=article.text,
            relations=[],
        )

        if type(article) == ThesisArticle:
            return output

        if type(article) == AntithesisArticle:
            base = self._uow.repository.get_article(article.refer_to)
            output.relations.append(
                ViewArticleRelation(
                    to_id=base.id,
                    to_name=base.title,
                    type=RelationType.ANTITHESIS,
                )
            )

        elif type(article) == SynthesisArticle:
            thesis = self._uow.repository.get_article(article.thesis_id)
            antithesis = self._uow.repository.get_article(article.antithesis_id)

            for base in [thesis, antithesis]:
                output.relations.append(
                    ViewArticleRelation(
                        to_id=base.id,
                        to_name=base.title,
                        type=RelationType.SYNTHESIS,
                    )
                )

        return output
