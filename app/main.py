from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app import models  # noqa: F401
from app.database import engine
from app.routes.itens import router as itens_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Catálogo de Futebol API", lifespan=lifespan)
app.include_router(itens_router)
