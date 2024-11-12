from src.application import UseCase
from src.application.dto import (
    PublishAntithesisArticleInputDTO,
    PublishArticleOutputDTO,
    PublishSynthesisArticleInputDTO,
    PublishThesisArticleInputDTO,
    RateArticleInputDTO,
)


class PublishThesisArticle(
    UseCase[PublishThesisArticleInputDTO, PublishArticleOutputDTO]
):
    pass


class PublishAntithesisArticle(
    UseCase[PublishAntithesisArticleInputDTO, PublishArticleOutputDTO]
):
    pass


class PublishSynthesisArticle(
    UseCase[PublishSynthesisArticleInputDTO, PublishArticleOutputDTO]
):
    pass


class RateArticle(UseCase[RateArticleInputDTO, None]):
    pass
