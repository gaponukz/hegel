from src.application.dto import GetArticleOutputDTO, ViewArticleRelation
from src.application.persistent import UnitOfWork
from src.application.usecases import GetArticleUseCase
from src.domain.entities import AntithesisArticle, SynthesisArticle, ThesisArticle
from src.domain.value_objects import ArticleType, RelationType


class PublishAntithesis(GetArticleUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, article_id: int) -> GetArticleOutputDTO:
        article = await self._uow.repository.get_article(article_id)
        output = GetArticleOutputDTO(
            id=article.id,
            type=ArticleType.THESIS,
            author_id=article.author_id,
            title=article.title,
            text=article.text,
            relations=[],
        )

        if type(article) == ThesisArticle:
            return output

        if type(article) == AntithesisArticle:
            output.type = ArticleType.ANTITHESIS
            base = await self._uow.repository.get_article(article.refer_to)
            output.relations.append(
                ViewArticleRelation(
                    to_id=base.id,
                    to_name=base.title,
                    type=RelationType.ANTITHESIS,
                )
            )

        elif type(article) == SynthesisArticle:
            output.type = ArticleType.SYNTHESIS
            thesis = await self._uow.repository.get_article(article.thesis_id)
            antithesis = await self._uow.repository.get_article(article.antithesis_id)

            output.relations.append(
                ViewArticleRelation(
                    to_id=thesis.id,
                    to_name=thesis.title,
                    type=RelationType.THESIS_SYNTHESIS,
                )
            )

            output.relations.append(
                ViewArticleRelation(
                    to_id=antithesis.id,
                    to_name=antithesis.title,
                    type=RelationType.ANTITHESIS_SYNTHESIS,
                )
            )

        return output
