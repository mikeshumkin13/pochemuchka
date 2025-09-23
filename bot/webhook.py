import asyncio, os, httpx
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "PUT_TOKEN_HERE")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text)
async def on_text(msg: Message):
    child_id = 1
    async with httpx.AsyncClient(timeout=30) as cli:
        r = await cli.post(f"{API_URL}/chat/ask", json={"child_id": child_id, "message": msg.text})
        data = r.json()
    await msg.answer(data.get("reply", "Ой, что-то пошло не так"))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


