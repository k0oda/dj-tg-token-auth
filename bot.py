from pathlib import Path

import aiohttp
import environ
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

env = environ.Env(
)
BASE_DIR = Path(__file__).resolve().parent
env.read_env(BASE_DIR / "dj_tg_auth/.env")

TOKEN = env("TELEGRAM_BOT_TOKEN")
DJANGO_HOST = env("DJANGO_HOST")
DJANGO_TELEGRAM_LOGIN_ENDPOINT = env("DJANGO_TELEGRAM_LOGIN_ENDPOINT")

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def start_handler(message: Message) -> None:
    args = message.text.split()
    if len(args) > 1:
        token = args[1]
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{DJANGO_HOST}{DJANGO_TELEGRAM_LOGIN_ENDPOINT}",
                json={
                    "telegram_id": message.from_user.id,
                    "telegram_username": message.from_user.username,
                    "token": token,
                },
            ) as response:
                if response.status == 200:
                    await message.answer("Ваш аккаунт был успешно привязан к Telegram")
                else:
                    await message.answer(f"Не удалось вас авторизовать. Код ошибки: {response.status}")
    else:
        await message.answer("Требуется токен. Проверьте ссылку")


if __name__ == "__main__":
    import asyncio

    async def main() -> None:
        await dp.start_polling(bot)
    asyncio.run(main())
