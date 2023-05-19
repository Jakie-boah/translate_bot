
from translate import translate
from config import bot
from loguru import logger
from aiogram.utils.markdown import hlink
from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, BadRequest
from urllib.parse import urlparse, parse_qs
from .airtable import AirtableParser
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0


class SetUp:
    def __init__(self, message):
        self.message = message
        # self.translate_dict = {
        #     'RU': 'RUSSIAN',
        #     'EN': 'ENGLISH',
        #     'FR': 'FRENCH'
        # }


    @property
    def determine_language(self):
        return self._language

    @determine_language.setter
    def determine_language(self, val):
        self._language = detect(f'{val}').upper()

    @property
    def translate_dict(self) -> dict:
        return self._translate_dict

    @translate_dict.setter
    def translate_dict(self, val):
        self._translate_dict = AirtableParser(val).get_dict()

    async def _translate(self, language, message, msg=''):
        logger.info(self.message.reply_to_message.text)
        response = await translate(language, message)
        response = response['choices'][0]['text'].split('\n')

        translated_message = str()
        for i in response:
            translated_message += i
        translated_message += f'\n<b>{language}</b>'

        return translated_message

    def set_active_languages(self) -> bool:
        if self.determine_language in self.translate_dict:
            del self.translate_dict[self.determine_language]
            return True
        else:
            return False


class AcceptableLength(SetUp):
    def __init__(self, message):
        super().__init__(message)

    def active_language(self):
        self.translate_dict = self.message.chat.id
        self.determine_language = self.message.text
        return self.existed_language()

    def existed_language(self):
        if self.determine_language in self.translate_dict:
            return True
        else:
            return False
