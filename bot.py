import asyncio
import os
from aiogram import Bot, Dispatcher, F 
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

import os
API_TOKEN = os.getenv("API_TOKEN")
CHANNEL_ID_1 = -10019145952198
CHANNEL_ID_2 = -1001703186768
ADMIN_ID = 1388312519
USERS_FILE = "users.txt"

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📲 Перейти на канал", url="https://t.me/+Ix3uck7QcoUzZTUy")],
        [InlineKeyboardButton(text="✅ Я підписався", callback_data="check_sub")]
    ])
    await message.answer(
        f"Привіт, {message.from_user.first_name}!\n\n"
        "Щоб отримати чек-лист, спочатку підпишись на канал, а потім натисни кнопку нижче.",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "check_sub")
async def check_sub(callback: CallbackQuery):
    user_id = callback.from_user.id
    try:
        member1 = await bot.get_chat_member(CHANNEL_ID_1, user_id)
        member2 = await bot.get_chat_member(CHANNEL_ID_2, user_id)

        if member1.status in ["member", "administrator", "creator"] and \
           member2.status in ["member", "administrator", "creator"]:
            await bot.send_document(chat_id=user_id, document=FSInputFile("checklist200.pdf"))
        else:
            await callback.message.answer("❗ Підпишись на обидва канали, будь ласка.")
    except Exception as e:
        await callback.message.answer("⚠️ Помилка при перевірці підписки.")

@dp.message(F.text.startswith("/send"))
async def broadcast(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    text = message.text[5:].strip()
    try:
        with open(USERS_FILE, "r") as f:
            users = f.read().splitlines()

        for uid in users:
            try:
                await bot.send_message(uid, text)
            except:
                continue

        await message.answer("✅ Повідомлення надіслано.")
    except:
        await message.answer("⚠️ Помилка розсилки.")

@dp.message()
async def save_user(message: Message):
    user_id = str(message.from_user.id)

    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()

    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()

    if user_id not in users:
        with open(USERS_FILE, "a") as f:
            f.write(user_id + "\n")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
