from src.application.dto import PublishThesisArticleInputDTO
from src.application.interactors import publish_thesis


async def test_ok(uow):
    article = PublishThesisArticleInputDTO(author_id=1, title="A", text="aaa")

    out = await publish_thesis(uow, article)
    thesis = await uow.repository.get_article(out.id)

    assert thesis.author_id == article.author_id
    assert thesis.title == article.title
    assert thesis.text == article.text
    assert thesis.rating == 0
