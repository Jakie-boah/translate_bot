from config import dp, bot
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from handlers.airtable import AirtableParser


@dp.message_handler(Command(['update'], prefixes='/'))
async def update(message: Message):
    await AirtableParser().update_table()
    await bot.send_message(message.chat.id, text='Данные успешно обновлены')
