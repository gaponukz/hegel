from src.application import UseCase
from src.application.dto import (
    GetArticleOutputDTO,
    PublishAntithesisArticleInputDTO,
    PublishArticleOutputDTO,
    PublishSynthesisArticleInputDTO,
    PublishThesisArticleInputDTO,
    RateArticleInputDTO,
)


class PublishThesisArticleUseCase(
    UseCase[PublishThesisArticleInputDTO, PublishArticleOutputDTO]
):
    pass


class PublishAntithesisArticleUseCase(
    UseCase[PublishAntithesisArticleInputDTO, PublishArticleOutputDTO]
):
    pass


class PublishSynthesisArticleUseCase(
    UseCase[PublishSynthesisArticleInputDTO, PublishArticleOutputDTO]
):
    pass


class RateArticleUseCase(UseCase[RateArticleInputDTO, None]):
    pass


class GetArticleUseCase(UseCase[int, GetArticleOutputDTO]):
    pass
