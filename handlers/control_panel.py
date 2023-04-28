"""Handler for all messages - here we translate them and send to the topics"""

from translate import translate
from config import bot
from loguru import logger
from aiogram.utils.markdown import hlink
from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, BadRequest
from urllib.parse import urlparse, parse_qs
from .airtable import AirtableParser
from .common_class import Setup


class ControlAdvanced(Setup):

    bot_id = 6122243229

    def __init__(self, message):
        super().__init__(message)

    async def translate_and_send_message(self):
        logger.info(self.message)
        self.translate_dict = self.message.chat.id
        self.message_tread = self.message.message_thread_id

        del self.translate_dict[str(self.message_tread)]
        logger.info(self.translate_dict)

        for i in self.translate_dict.keys():
            try:
                await bot.send_message(
                    self.message.chat.id, text=await self._translate(self.translate_dict[i], self.message.text),
                    message_thread_id=i, disable_web_page_preview=True,
                    parse_mode=types.ParseMode.HTML
                )
            except BadRequest:
                pass

    async def check_if_reply_on_tr_msg(self) -> bool:
        try:
            return self.bot_id == self.message['reply_to_message']['from']['id']
        except TypeError:
            return False

    async def reply_on_message(self):

        self.translate_dict = self.message.chat.id
        self.message_tread = self.message.message_thread_id

        language, message_id, topic_id = await self.url_parser()

        await bot.send_message(self.message.chat.id,
                               # text=self.message.text,
                               text=await self._translate(language, self.message.text),
                               reply_to_message_id=message_id, message_thread_id=topic_id,
                               disable_web_page_preview=True)

    async def url_parser(self):
        logger.info(self.message)
        try:
            url = self.message['reply_to_message']['entities'][1]['url']
            #url = self.message['reply_to_message']['entities'][0]['url']
        except IndexError:
            url = self.message['reply_to_message']['caption_entities'][1]['url']

        parsed_url = urlparse(url)
        message_id = parsed_url.path.split('/')[-1]

        if parsed_url.query:
            topic_id = int(parse_qs(parsed_url.query)['topic'][0])
            language = self.translate_dict[str(topic_id)]

        else:
            topic_id = None
            language = self.translate_dict[str(topic_id)]

        return language, message_id, topic_id

