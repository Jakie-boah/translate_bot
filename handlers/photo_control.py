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
from .common_class import Setup


class PhotoControl(Setup):

    def __init__(self, message):
        super().__init__(message)

    async def transform_message(self):
        self.translate_dict = self.message.chat.id
        self.message_tread = self.message.message_thread_id
        del self.translate_dict[str(self.message_tread)]
        logger.info(self.translate_dict)

        for i in self.translate_dict.keys():
            fp = io.BytesIO()
            await self.message.photo[-1].download(fp)

            await bot.send_photo(self.message.chat.id,
                                 photo=fp,
                                 caption=await self._translate(self.translate_dict[i], self.message.caption, msg=' and more'),
                                 message_thread_id=i)
            
