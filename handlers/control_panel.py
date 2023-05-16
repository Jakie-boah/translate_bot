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
        msg = ''

        if self.set_active_languages():
            m = ','.join(self.translate_dict)
            p = await bot.send_message(self.message.chat.id,
                                       text=f'Message will be translated in <b>{m}</b>',
                                       reply_to_message_id=self.message.message_id
                                       )

            for lang in self.translate_dict:
                res = await self._translate(lang, self.message.text)
                msg += res + '\n\n'
            await bot.delete_message(chat_id=p.chat.id, message_id=p.message_id)
            await bot.send_message(self.message.chat.id,
                                   text=msg,
                                   reply_to_message_id=self.message.message_id
                                   )

    async def _translate(self, language, message, msg=''):
        logger.info(self.message.text)
        response = await translate(language, message)
        response = response['choices'][0]['text'].split('\n')

        # translated_message = f'<b>{language}</b>\n'
        translated_message = ''
        for i in response:
            translated_message += i
        translated_message += f'\n<b>{language}</b>'
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
