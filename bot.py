import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def fact_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🧠 Get Another Fact",
                    callback_data="another_fact"
                )
            ]
        ]
    )


async def get_fact():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("text", "I couldn't find a fact right now.")

    return "I couldn't find a fact right now."


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "👋 Welcome to Random Fact Bot!\n\n"
        "🧠 Send /fact to get a random fact.\n"
        "📚 Learn something new every time!"
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "📚 How to use this bot:\n\n"
        "/fact — Get a random fact\n"
        "/help — Show this help message"
    )


@dp.message(Command("fact"))
async def fact_command(message: Message):
    fact = await get_fact()

    await message.answer(
        f"🧠 <b>Did You Know?</b>\n\n{fact}",
        parse_mode="HTML",
        reply_markup=fact_keyboard()
    )


@dp.callback_query(lambda callback: callback.data == "another_fact")
async def another_fact(callback):
    fact = await get_fact()

    await callback.message.edit_text(
        f"🧠 <b>Did You Know?</b>\n\n{fact}",
        parse_mode="HTML",
        reply_markup=fact_keyboard()
    )

    await callback.answer()


async def main():
    print("🤖 Random Fact Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
