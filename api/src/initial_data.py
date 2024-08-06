import logging

from src.db.init_db import init_db
from src.db.session import AsyncSessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    db = AsyncSessionLocal()

    await init_db(db)
    await db.close()


async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
