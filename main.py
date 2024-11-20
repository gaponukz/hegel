import asyncio

from neo4j import AsyncGraphDatabase

from src.infrastructure.repository import Neo4jThesisUnitOfWork


async def main():
    driver = AsyncGraphDatabase.driver(
        "neo4j://localhost:7687", auth=("neo4j", "password")
    )
    session = driver.session()
    uow = Neo4jThesisUnitOfWork(session)

    print(await uow.repository.get_article("d8b69a95-dedb-4d50-9a06-fb6ae52d9d96"))
    print(await uow.repository.get_article("6bedd47f-0632-4e60-978e-431d3513ae6e"))
    print(await uow.repository.get_article("360de613-8d08-4870-98fd-e73fa702b68f"))

    await session.close()
    await driver.close()


if __name__ == "__main__":
    asyncio.run(main())
