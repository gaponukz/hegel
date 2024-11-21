import pytest

from src.application.dto import CreateArticle, PublishSynthesisArticleInputDTO, Relation
from src.application.errors import ApplicationError
from src.application.interactors import publish_synthesis
from src.domain.value_objects import RelationType


async def test_thesis_is_antithesis(uow):
    with pytest.raises(ApplicationError):
        await publish_synthesis(
            uow,
            PublishSynthesisArticleInputDTO(
                author_id=1,
                title="A",
                text="aaa",
                thesis_id="0",
                antithesis_id="0",
            ),
        )


async def test_have_not_antithesis_relations(uow):
    thesis_id1 = await uow.repository.add_article(
        CreateArticle(author_id=0, title="B", text="bbb", relations=[])
    )

    thesis_id2 = await uow.repository.add_article(
        CreateArticle(author_id=0, title="B", text="bbb", relations=[])
    )

    article = PublishSynthesisArticleInputDTO(
        author_id=1,
        title="A",
        text="aaa",
        thesis_id=thesis_id1,
        antithesis_id=thesis_id2,
    )

    with pytest.raises(ApplicationError):
        await publish_synthesis(uow, article)


async def test_ok(uow):
    thesis_id = await uow.repository.add_article(
        CreateArticle(author_id=0, title="B", text="bbb", relations=[])
    )

    antithesis_id = await uow.repository.add_article(
        CreateArticle(
            author_id=0,
            title="B",
            text="bbb",
            relations=[Relation(to_id=thesis_id, type=RelationType.ANTITHESIS)],
        )
    )

    article = PublishSynthesisArticleInputDTO(
        author_id=1,
        title="A",
        text="aaa",
        thesis_id=thesis_id,
        antithesis_id=antithesis_id,
    )

    out = await publish_synthesis(uow, article)
    thesis = await uow.repository.get_article(out.id)

    assert thesis.author_id == article.author_id
    assert thesis.title == article.title
    assert thesis.text == article.text
    assert thesis.thesis_id == thesis_id
    assert thesis.antithesis_id == antithesis_id
    assert thesis.rating == 0
