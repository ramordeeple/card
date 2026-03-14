from fastapi import FastAPI, status
from starlette.responses import JSONResponse

from src.api.routes import auth, transactions, cards, admin

app = FastAPI()
app.include_router(auth.router)
app.include_router(transactions.router)
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