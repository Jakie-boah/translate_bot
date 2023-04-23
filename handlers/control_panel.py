from translate import translate
from config import bot
from loguru import logger
from aiogram.utils.markdown import hlink
from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, BadRequest
from urllib.parse import urlparse, parse_qs
from .airtable import AirtableParser


class Control:
    """
    Control panel for all bot actions.
    As input parameter takes only message in its row view
    """
    bot_id = 6122243229

    def __init__(self, message):
        self.message = message
        self.chat_id = message.chat.id
        self._url = message.url
        self.translate_dict = self.chat_id

    @property
    def translate_dict(self):
        return self._translate_dict

    @translate_dict.setter
    def translate_dict(self, value):
        self._translate_dict = AirtableParser(value).get_dict()

    async def translate_and_send_message(self):

        original_lan = self.translate_dict[self.message.message_thread_id]
        del self.translate_dict[self.message.message_thread_id]

        for i in self.translate_dict.keys():
            try:
                await bot.send_message(
                    self.chat_id, text=self._translate(self.translate_dict[i], original_lan),
                    message_thread_id=i, disable_web_page_preview=True,
                    parse_mode=types.ParseMode.HTML
                )
            except BadRequest:
                pass

    def _translate(self, language, original_lan):
        response = translate(language, self.message.text)['choices'][0]['text'].split('\n')

        translated_message = f'<b>{self.message.from_user.first_name}</b>\n'
        for i in response:
            translated_message += i

        url = hlink(f'Original {original_lan[:2].upper()}', self._url)
        translated_message += '\n' + url
        logger.info(translated_message)
        return translated_message

    async def delete_message(self):

        try:
            await bot.delete_message(self.chat_id, self.message.message_id)
            await bot.send_message(self.message.chat.id,
                                   text='Message cannot be sent in general chat\n'
                                        'Please, choose your language chat below')

        except MessageCantBeDeleted:
            logger.error('Бот не может удалять сообщения. Возможно у него нет админовской привилегии на это')

    def check_if_reply_on_tr_msg(self) -> bool:
        return self.bot_id == self.message['reply_to_message']['from']['id']

    async def reply_on_message(self):

        if self.check_if_reply_on_tr_msg():
            language, original_lan, message_id, topic_id = self.url_parser()

            await bot.send_message(self.message.chat.id,
                                   text=f"{self._translate(language, original_lan)}",
                                   reply_to_message_id=message_id, message_thread_id=topic_id,
                                   disable_web_page_preview=True)

    async def url_parser(self):
        try:
            url = self.message['reply_to_message']['entities'][1]['url']
        except IndexError:
            url = self.message['reply_to_message']['entities'][0]['url']

        m_id_topic = url.split('/')[-1]
        message_id = int(m_id_topic.split('?')[0])
        parsed_url = urlparse(url)
        topic_id = int(parse_qs(parsed_url.query)['topic'][0])
        language = self.translate_dict[topic_id]
        original_lan = self.translate_dict[self.message.message_thread_id]
        return language, original_lan, message_id, topic_id

