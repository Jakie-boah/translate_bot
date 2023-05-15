from typing import List
from config import dp
from aiogram import types
from handlers.photo_control import SinglePhoto
from config import bot


@dp.message_handler(content_types=[types.ContentType.PHOTO, ])
async def handle_albums(message: types.Message):
    """This handler will receive a complete album of any type."""
    control = SinglePhoto(message)
    await control.transform_message()

