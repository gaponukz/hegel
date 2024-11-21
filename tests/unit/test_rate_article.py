import pytest

from src.application.dto import CreateArticle, RateArticleInputDTO
from src.application.interactors.rate_article import RateArticle


@pytest.mark.parametrize(
    "is_positive, rating",
    [
        (True, 1),
        (False, -1),
    ],
)
async def test_ok(uow, is_positive: bool, rating: int):
    rate_thesis = RateArticle(uow)
    thesis_id = await uow.repository.add_article(
        CreateArticle(author_id=0, title="B", text="bbb", relations=[])
    )

    await rate_thesis(
        RateArticleInputDTO(article_id=thesis_id, is_positive=is_positive)
    )

    thesis = await uow.repository.get_article(thesis_id)
    assert thesis.rating == rating
    assert uow.executed_in_transaction
