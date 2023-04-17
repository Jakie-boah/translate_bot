from config import dp, bot
from aiogram.types import Message
from control_panel import Control
from loguru import logger
from config import bot


@dp.message_handler()
async def start(message: Message):
    # logger.info(message.url)
    control = Control(message.chat.id, message)
    logger.info(message.message_thread_id)
    # await bot.send_message(620755101, message.text)
    await control.set_languages_and_send_message()

