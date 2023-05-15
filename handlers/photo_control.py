"""Handler for messages which contain photos - here we translate caption's and send to the topics"""

from translate import translate
from config import bot
from loguru import logger
from aiogram.utils.markdown import hlink
from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, BadRequest
from urllib.parse import urlparse, parse_qs
from .airtable import AirtableParser
import io
from .common_class import SetUp


class PhotoControl(SetUp):
    def __init__(self, message):
        super().__init__(message)

    async def transform_message(self):
        self.determine_language = self.message.caption
        logger.info(self.determine_language)
        self.translate_dict.remove(self.determine_language)

        for lang in self.translate_dict:
            fp = io.BytesIO()
            await self.message.photo[-1].download(fp)

            await bot.send_photo(self.message.chat.id,
                                 photo=fp,
                                 caption=await self._translate(lang, self.message.caption, msg=' and more'),
                                 reply_to_message_id=self.message.message_id)
