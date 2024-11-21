import pytest

from src.application.dto import CreateArticle, PublishAntithesisArticleInputDTO
from src.application.errors import ArticleNotFoundError
from src.application.interactors import publish_antithesis


async def test_thesis_not_exist(uow):
    thesis_id = "0"

    assert not await uow.repository.is_article_exists(thesis_id)

    with pytest.raises(ArticleNotFoundError):
        await publish_antithesis(
            uow,
            PublishAntithesisArticleInputDTO(
                author_id=1,
                title="A",
                text="aaa",
                thesis_id=thesis_id,
            ),
        )


async def test_ok(uow):
    thesis_id = await uow.repository.add_article(
        CreateArticle(author_id=0, title="B", text="bbb", relations=[])
    )

    article = PublishAntithesisArticleInputDTO(
        author_id=1,
        title="A",
        text="aaa",
        thesis_id=thesis_id,
    )

    out = await publish_antithesis(uow, article)
    thesis = await uow.repository.get_article(out.id)

    assert thesis.author_id == article.author_id
    assert thesis.title == article.title
    assert thesis.text == article.text
    assert thesis.thesis_id == thesis_id
    assert thesis.rating == 0
