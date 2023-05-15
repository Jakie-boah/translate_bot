from config import dp, bot
from aiogram.types import Message, ContentType, Document, InputFile
from handlers.control_panel import SingleControl
from loguru import logger
from filters.filter import user_is_admin
from update_airtable import update
import io
from photo_handler import handle_albums
# from langdetect import detect


@dp.message_handler()
async def start(message: Message):
    logger.info(message)

    control = SingleControl(message)
    await control.send_message()
