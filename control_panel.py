from test import translate
from config import bot
from loguru import logger


class Control:
    def __init__(self, chat_id, message):
        self.chat_id = chat_id
        self.message = message
        self._url = message.url

    @property
    def chat_id(self):
        return self._chat_id

    @chat_id.setter
    def chat_id(self, value):
        self._chat_id = value

    async def set_languages_and_send_message(self):

        translate_dict = {
            #1: 'Russian',
            6016: 'English',
            6017: 'Arabic'
        }

        del translate_dict[self.message.message_thread_id]

        for i in translate_dict.keys():
            await bot.send_message(self.chat_id, text=self._translate(translate_dict[i]), message_thread_id=i)


    def _translate(self, language):
        response = translate(language, self.message.text)['choices'][0]['text'].split('\n')
        logger.info(response)

        response.pop(0)
        translated_message = ''
        for i in response:
            translated_message += i
        translated_message += '\n\n' + self._url
        return translated_message
