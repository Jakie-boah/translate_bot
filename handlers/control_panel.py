from translate import translate
from config import bot
from loguru import logger
from aiogram.utils.markdown import hlink
from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted
from urllib.parse import urlparse, parse_qs


class Control:
    """
    Control panel for all bot actions.
    As input parameter takes only message in its row view
    """
    bot_id = 6122243229
    friends_bots = [6211497478, 5713353769, 6196996810, 5704316497]

    def __init__(self, message):
        self.message = message
        self.chat_id = message.chat.id
        self._url = message.url

    @property
    def chat_id(self):
        return self._chat_id

    @chat_id.setter
    def chat_id(self, value):
        self._chat_id = value

    async def translate_and_send_message(self):

        translate_dict = {
            6617: 'RU',
            6016: 'EN',
            6017: 'AR'
        }
        # translate_dict = {
        #     2: 'Russian',
        #     19: 'English',
        #     12: 'Arabic'
        # }
        original_lan = translate_dict[self.message.message_thread_id]
        del translate_dict[self.message.message_thread_id]

        for i in translate_dict.keys():
            await bot.send_message(
                self.chat_id, text=self._translate(translate_dict[i], original_lan),
                message_thread_id=i, disable_web_page_preview=True,
                parse_mode=types.ParseMode.HTML
            )

    def _translate(self, language, original_lan):
        response = translate(language, self.message.text)['choices'][0]['text'].split('\n')
        logger.info(response)

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

    def check_if_reply_on_tr_msg(self):
        return Control.bot_id == self.message['reply_to_message']['from']['id']

    async def reply_on_message(self):
        if self.check_if_reply_on_tr_msg():
            # refactoring on parsing 100000000000000%
            try:
                url = self.message['reply_to_message']['entities'][1]['url']
            except IndexError:
                url = self.message['reply_to_message']['entities'][0]['url']
            translate_dict = {
                6617: 'Russian',
                6016: 'English',
                6017: 'Arabic'
            }
            m_id_topic = url.split('/')[-1]
            message_id = int(m_id_topic.split('?')[0])
            parsed_url = urlparse(url)
            topic_id = int(parse_qs(parsed_url.query)['topic'][0])
            language = translate_dict[topic_id]
            original_lan = translate_dict[self.message.message_thread_id]

            await bot.send_message(self.message.chat.id,
                                   text=f"{self._translate(language, original_lan)}",
                                   reply_to_message_id=message_id, message_thread_id=topic_id,
                                   disable_web_page_preview=True)

    async def control_proper_lan(self):
        translate_dict = {
            6617: 'Russian',
            6016: 'English',
            6017: 'Arabic'
        }
        lang = translate_dict[self.message.message_thread_id]
        response = translate(lang, self.message.text)['choices'][0]['text'].split('\n')
        translated_message = ''
        for i in response:
            translated_message += i

        await bot.delete_message(self.chat_id, self.message.message_id)
        await bot.send_message(self.message.chat.id,
                               text=translated_message,
                               message_thread_id=self.message.message_thread_id)














