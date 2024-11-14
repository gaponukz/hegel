from src.application.dto import PublishThesisArticleInputDTO
from src.application.interactors.publish_thesis import PublishThesis


async def test_ok(uow):
    publish_thesis = PublishThesis(uow)

    out = await publish_thesis(
        PublishThesisArticleInputDTO(author_id=1, title="A", text="aaa")
    )

    assert out.id in uow.repository
