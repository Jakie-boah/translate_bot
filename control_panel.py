from test import translate
from config import bot


class Control:
    def __init__(self, chat_id, message):
        self.chat_id = chat_id
        self.message = message.text
        self._url = message.url

    @property
    def chat_id(self):
        return self._chat_id

    @chat_id.setter
    def chat_id(self, value):
        self._chat_id = value

    async def set_languages_and_send_message(self):

        if self.chat_id == -970406949:
            self.language_1 = 'English'
            self.language_2 = 'Arabic'
            await bot.send_message(-826578431, self._translate()[0])
            await bot.send_message(-807639216, self._translate()[1])

        elif self.chat_id == -826578431:
            self.language_1 = 'Russian'
            self.language_2 = 'Arabic'
            await bot.send_message(-970406949, self._translate()[0])
            await bot.send_message(-807639216, self._translate()[1])

        elif self.chat_id == -807639216:
            self.language_1 = 'Russian'
            self.language_2 = 'English'
            await bot.send_message(-970406949, self._translate()[0])
            await bot.send_message(-826578431, self._translate()[1])

    def _translate(self):
        response = translate(self.language_1, self.language_2, self.message)['choices'][0]['text'].split('\n')

        response.pop(0)
        translated_messages = []
        for i in response:
            i = i[3:] + '\n' + self._url
            translated_messages.append(i)
        return translated_messages

