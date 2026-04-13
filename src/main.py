from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

import logging
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api.v1.router import api_v1_router
from src.core.domain_exc import SecTestException
from src.core.exc_handler import sectest_exception_handler
from src.core.redis_connector import redis_connector


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения: начинаем инициализацию...")
    try:
        await redis_connector.connect()
        FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
        await redis_connector.ping()
        logger.info("Приложение успешно запущено.")
        yield
    finally:
        logger.info("Остановка приложения: закрываем подключение к Redis")
        await redis_connector.disconnect()
        logger.info("Остановка приложения: Redis отключен")
        logger.info("Приложение остановлено.")


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(SecTestException, sectest_exception_handler)
app.include_router(api_v1_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
