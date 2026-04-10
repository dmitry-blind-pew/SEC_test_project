from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
import uvicorn

from src.api.v1.router import api_v1_router
from src.core.domain_exc import SecTestException
from src.core.exc_handler import sectest_exception_handler


app = FastAPI()

app.add_exception_handler(SecTestException, sectest_exception_handler)
app.include_router(api_v1_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)