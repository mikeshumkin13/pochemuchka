from fastapi import FastAPI
from app.routers import chat, children, telegram

app = FastAPI(title="Pochemuchka API", version="0.1.0")

app.include_router(children.router, prefix="/api/v1/children", tags=["children"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(telegram.router, prefix="/api/v1/telegram", tags=["telegram"])

@app.get("/health")
async def health():
    return {"status": "ok"}


