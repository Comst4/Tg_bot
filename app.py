import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from dotenv import load_dotenv
from openai import OpenAI

# загрузка .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Я ChatGPT в Telegram 😈 Пиши что угодно")


@dp.message(F.text)
async def chat(message: Message):
    try:
        response = client.chat.completions.create(
            model="gpt-5.4",
            messages=[
                {"role": "user", "content": message.text}
            ]
        )

        reply = response.choices[0].message.content

        await message.answer(reply)

    except Exception as e:
        await message.answer(f"Ошибка: {e}")


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
