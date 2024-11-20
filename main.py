import asyncio

from neo4j import AsyncGraphDatabase

from src.infrastructure.repository import Neo4jThesisUnitOfWork


async def main():
    driver = AsyncGraphDatabase.driver(
        "neo4j://localhost:7687", auth=("neo4j", "password")
    )
    session = driver.session()
    uow = Neo4jThesisUnitOfWork(session)

    thesis_id = "47f32608-72f0-4ccb-8eb2-dcb1c675886e"
    antithesis_id = "ae8c20ea-f987-4d10-9aea-ba6d53fba33c"

    print(await uow.repository.is_antithesis(thesis_id, antithesis_id))

    await session.close()
    await driver.close()


if __name__ == "__main__":
    asyncio.run(main())
