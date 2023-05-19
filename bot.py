from config import dp
from aiogram.types import Message, CallbackQuery, ContentType
from handlers.message_control import MessageControl
from handlers.setup import AcceptableLength
from handlers.photo_control import PhotoControl
from loguru import logger
from handlers.inlinekeyboard import message_keyboard, media_keyboard


@dp.message_handler()
async def start(message: Message):

    msg = AcceptableLength(message)
    if msg.active_language():
        await message.reply(text="You can translate this message",
                            reply_markup=message_keyboard())


@dp.message_handler(content_types=[ContentType.PHOTO, ])
async def handle_albums(message: Message):

    await message.reply(text="You can translate this message",
                        reply_markup=media_keyboard())


@dp.callback_query_handler(text='translate_message')
@dp.callback_query_handler(text='translate_media')
async def translate(query: CallbackQuery):
    answer_data = query.data

    if answer_data == 'translate_message':
        control = MessageControl(query.message)
        msg = await control.make_message()
        await query.message.edit_text(msg)

    if answer_data == 'translate_media':
        control = PhotoControl(query.message)
        msg = await control.transform_message()
        await query.message.edit_text(msg)
