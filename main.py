import logging
import os

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.types.message import ContentType
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


class Form(StatesGroup):
    sticker = State()
    alias = State()


@dp.message_handler(commands='start')
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
        state_data["sticker_alias"] = name
        logging.warning(state_data.get("sticker_id"))
        logging.warning(state_data.get("sticker_alias"))
    await state.finish()
    await message.reply(f"The sticker was named, you can now use it with the following command: :{name}:")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
