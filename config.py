
from aiogram import Bot, Dispatcher
import asyncio
import os
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')
openai_api_key = os.getenv('openai_api_key')
loop = asyncio.new_event_loop()
bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())
