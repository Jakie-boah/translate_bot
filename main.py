
from aiogram import executor
from loguru import logger
from config import dp
from bot import *

if __name__ == '__main__':
    logger.info("Бот запущен")
    executor.start_polling(dp)
