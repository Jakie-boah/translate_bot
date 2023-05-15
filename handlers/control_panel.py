"""Handler for all messages - here we translate them and send to the topics"""

from translate import translate
from config import bot
from loguru import logger
from aiogram.utils.markdown import hlink
from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, BadRequest
from urllib.parse import urlparse, parse_qs
from .airtable import AirtableParser
from .common_class import SetUp


class MessageControl(SetUp):

    def __init__(self, message):
        super().__init__(message)

    async def send_message(self):
        self.determine_language = self.message.text
        logger.info(self.determine_language)
        if self.set_active_languages():
            for lang in self.translate_dict:
                await bot.send_message(self.message.chat.id,
                                       text=await self._translate(lang, self.message.text),
                                       reply_to_message_id=self.message.message_id
                                       )

    async def _translate(self, language, message, msg=''):
        logger.info(self.message.text)
        response = await translate(language, message)
        response = response['choices'][0]['text'].split('\n')

        translated_message = f'<b>{self.message.from_user.first_name}</b>\n'
        for i in response:
            translated_message += i

        # url = hlink(f'Original{msg} {self.determine_language[:2].upper()}', self.message.url)
        #         # translated_message += '\n' + url
        #         # logger.info(self.message.url)
        return translated_message

    def set_active_languages(self) -> bool:
        if self.determine_language in self.translate_dict:
            self.translate_dict.remove(self.determine_language)
            return True
        else:
            return False
