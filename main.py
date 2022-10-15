import logging
import os
import re

import psycopg2
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType

from constants import STICKER_ID_FIELD, MESSAGE_SEND_ALIAS, MESSAGE_SEND_STICKER, \
    MESSAGE_ALIAS_HAS_ASTERISK, MESSAGE_ALIAS_TOO_LONG, MESSAGE_SUCCESS, ALIAS_REGEX
from query import SELECT_ALIASES_FOR_CHAT_QUERY, SELECT_STICKER_QUERY, \
    INSERT_ALIAS_QUERY

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.environ.get("API_TOKEN")
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

connection = psycopg2.connect(
    f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"
)
connection.autocommit = True
db_cursor = connection.cursor()


class Form(StatesGroup):
    sticker = State()
    alias = State()


@dp.message_handler(commands="sticker")
async def handle_sticker_command(message: types.Message):
    await Form.sticker.set()
    await message.answer(MESSAGE_SEND_STICKER)


@dp.message_handler(commands="aliases")
async def handle_aliases_command(message: types.Message):
    db_cursor.execute(SELECT_ALIASES_FOR_CHAT_QUERY, (message.chat.id,))
    alias_rows = db_cursor.fetchall()
    aliases = [alias_row[0] for alias_row in alias_rows]
    available_aliases = ", ".join(aliases)
    await message.answer(f"Available aliases: {available_aliases}")


@dp.message_handler(state=Form.sticker, content_types=ContentType.STICKER)
async def handle_sticker(message: types.Message, state: FSMContext):
    await Form.next()
    async with state.proxy() as state_data:
        state_data[STICKER_ID_FIELD] = message.sticker.file_id
    await message.answer(MESSAGE_SEND_ALIAS)


@dp.message_handler(state=Form.alias, content_types=ContentType.TEXT)
async def handle_alias(message: types.Message, state: FSMContext):
    if "*" in message.text:
        await message.reply(MESSAGE_ALIAS_HAS_ASTERISK)
        return
    if len(message.text) > 20:
        await message.reply(MESSAGE_ALIAS_TOO_LONG)
    sticker_alias = f"*{message.text}*"
    async with state.proxy() as state_data:
        sticker_id = state_data.get(STICKER_ID_FIELD)
        db_cursor.execute(INSERT_ALIAS_QUERY,
                          (message.chat.id, sticker_id, sticker_alias))
    await state.finish()
    await message.reply(f"""{MESSAGE_SUCCESS}{sticker_alias}""")


@dp.message_handler(content_types=ContentType.TEXT)
async def handle_message(message: types.Message):
    aliases = re.findall(ALIAS_REGEX, message.text)
    for sticker_alias in aliases:
        db_cursor.execute(SELECT_STICKER_QUERY,
                          (sticker_alias, message.chat.id))
        (sticker_id,) = db_cursor.fetchone()
        if sticker_id:
            await message.answer_sticker(sticker_id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
