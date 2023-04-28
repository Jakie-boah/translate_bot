
from translate import translate
from config import bot
from loguru import logger
from aiogram.utils.markdown import hlink
from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, BadRequest
from urllib.parse import urlparse, parse_qs
from .airtable import AirtableParser


class Setup:
    def __init__(self, message):
        self.message = message

    @property
    def message_tread(self):
        return self._message_tread

    @message_tread.setter
    def message_tread(self, value):
        if str(value) in self.translate_dict.keys():
            self._message_tread = value
            self.original_lan = value
        else:
            self._message_tread = None
            self.original_lan = None

    @property
    def original_lan(self):
        return self._original_lan

    @original_lan.setter
    def original_lan(self, value):
        self._original_lan = self.translate_dict[str(value)]

    @property
    def translate_dict(self):
        return self._translate_dict

    @translate_dict.setter
    def translate_dict(self, value):
        self._translate_dict = AirtableParser(value).get_dict()

    async def _translate(self, language, message, msg=''):
        logger.info(self.message.text)
        response = await translate(language, message)
        logger.info(language)
        logger.info(response)
        response = response['choices'][0]['text'].split('\n')

        translated_message = f'<b>{self.message.from_user.first_name}</b>\n'
        for i in response:
            translated_message += i

        url = hlink(f'Original{msg} {self.original_lan[:2].upper()}', self.message.url)
        translated_message += '\n' + url
        return translated_message
