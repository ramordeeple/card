from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from starlette.responses import JSONResponse

from src.api.routes import auth, cards, admin
from src.core.setup_admin import create_admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_admin()
    yield
app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(cards.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Cards API"}

async def value_error_handler(exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': str(exc)},
    )