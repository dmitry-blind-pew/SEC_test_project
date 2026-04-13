import pytest
from sqlalchemy import text

from src.core.db import async_session_maker_null_pool, engine_null_pool
from src.models import BaseORM
from src.models import activities, buildings, companies, companies_activities, company_phones  # noqa: F401
from src.seed.seed_data import seed_data


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine_null_pool.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)
    await seed_data(session_factory=async_session_maker_null_pool)
