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
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0

# class PhotoControl(Setup):
#
#     def __init__(self, message):
#         super().__init__(message)
#
#     async def transform_message(self):
#         self.translate_dict = self.message.chat.id
#         self.message_tread = self.message.message_thread_id
#         del self.translate_dict[str(self.message_tread)]
#         logger.info(self.translate_dict)
#
#         for i in self.translate_dict.keys():
#             fp = io.BytesIO()
#             await self.message.photo[-1].download(fp)
#
#             await bot.send_photo(self.message.chat.id,
#                                  photo=fp,
#                                  caption=await self._translate(self.translate_dict[i], self.message.caption, msg=' and more'),
#                                  message_thread_id=i)
#


class SinglePhoto:
    def __init__(self, message):
        self.message = message
        self.translate_dict = [
            'RU',
            'EN',
            'FR'
        ]


    @property
    def determine_language(self):
        return self._language

    @determine_language.setter
    def determine_language(self, val):
        self._language = detect(f'{val}').upper()

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

    async def _translate(self, language, message, msg=''):
        logger.info(self.message.text)
        response = await translate(language, message)
        response = response['choices'][0]['text'].split('\n')

        translated_message = f'<b>{self.message.from_user.first_name}</b>\n'
        for i in response:
            translated_message += i

        # url = hlink(f'Original{msg} {self.determine_language[:2].upper()}', self.message.url)
        # translated_message += '\n' + url
        # logger.info(self.message.url)
        return translated_message


