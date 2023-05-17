from config import dp, bot
from aiogram.types import Message, CallbackQuery, Document, InputFile
from handlers.message_control import MessageControl
from loguru import logger
from filters.filter import user_is_admin
from update_airtable import update
import io
from photo_handler import handle_albums
# from langdetect import detect


@dp.message_handler()
async def start(message: Message):
    logger.info(message)

    control = MessageControl(message)
    await control.send_message()
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#
#
# urlkb = InlineKeyboardMarkup(row_width=1)
# urlButton = InlineKeyboardButton(text='tra', callback_data='tran')
# urlkb.add(urlButton)
#
#
# @dp.message_handler()
# async def start(message: Message):
#
#     await message.answer(message.text, reply_markup=urlkb)
#
#
# @dp.callback_query_handler(text='tran')
# async def translate(query: CallbackQuery):
#     answer_data = query.data
#
#     if answer_data == 'tran':
#         await query.message.delete()
#         await query.message.answer(f'переведу это сообщение {query.message.text}',)

