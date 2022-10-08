import logging
import os

import aiogram.utils.markdown as md
import psycopg2
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.types.message import ContentType

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.environ.get("API_TOKEN")

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

DB_HOST = os.environ.get("POSTGRES_HOST")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
connection = psycopg2.connect(f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}")
connection.autocommit = True
db_cursor = connection.cursor()


class Form(StatesGroup):
    sticker = State()
    alias = State()


@dp.message_handler(commands="start")
async def handle_start(message: types.Message):
    await Form.sticker.set()
    await message.answer("Send a sticker you want to name")


@dp.message_handler(state=Form.sticker, content_types=ContentType.STICKER)
async def handle_sticker(message: types.Message, state: FSMContext):
    await Form.next()
    async with state.proxy() as state_data:
        state_data["sticker_id"] = message.sticker.file_id
    await message.answer("Send an alias for the sticker")


@dp.message_handler(state=Form.alias, content_types=ContentType.TEXT)
async def handle_alias(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as state_data:
        sticker_id = state_data.get("sticker_id")
        db_cursor.execute(f"""
            INSERT INTO aliases (chat_id, sticker_id, alias) values ({message.chat.id}, '{sticker_id}', '{name}')
        """)
    await state.finish()
    await message.reply(f"The sticker was named, you can now use it with the following command: :{name}:")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
