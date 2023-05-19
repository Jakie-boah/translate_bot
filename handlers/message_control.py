"""Handler for all messages - here we translate them and send to the topics"""

from loguru import logger
from .setup import SetUp


class MessageControl(SetUp):

    def __init__(self, message):
        super().__init__(message)

    async def make_message(self):
        self.translate_dict = self.message.chat.id
        self.determine_language = self.message.reply_to_message.text
        logger.info(self.determine_language)

        if self.set_active_languages():
            msg = str()
            m = ','.join(self.translate_dict.values())
            await self.message.edit_text(
                text=f'Message will be translated in <b>{m}</b>',
            )

            for lang in self.translate_dict.values():
                logger.info(lang)
                res = await self._translate(lang, self.message.reply_to_message.text)
                msg += res + '\n\n'

            return msg
