import pytest

from src.application.dto import CreateArticle, RateArticleInputDTO
from src.application.interactors import rate_article


@pytest.mark.parametrize(
    "is_positive, rating",
    [
        (True, 1),
        (False, -1),
    ],
)
async def test_ok(uow, is_positive: bool, rating: int):
    thesis_id = await uow.repository.add_article(
        CreateArticle(author_id=0, title="B", text="bbb", relations=[])
    )

    await rate_article(
        uow, RateArticleInputDTO(article_id=thesis_id, is_positive=is_positive)
    )

    thesis = await uow.repository.get_article(thesis_id)
    assert thesis.rating == rating
    assert uow.executed_in_transaction
