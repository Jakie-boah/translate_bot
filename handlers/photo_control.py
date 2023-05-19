"""Handler for messages which contain photos - here we translate caption's and send to the topics"""

from loguru import logger
from .setup import SetUp


class PhotoControl(SetUp):
    def __init__(self, message):
        super().__init__(message)

    async def transform_message(self):
        self.translate_dict = self.message.chat.id
        self.determine_language = self.message.reply_to_message.caption
        logger.info(self.determine_language)
        if self.set_active_languages():
            m = ','.join(self.translate_dict.values())
            await self.message.edit_text(
                text=f'Message will be translated in <b>{m}</b>',
            )
            msg = str()

            for lang in self.translate_dict:
                res = await self._translate(lang, self.message.reply_to_message.caption, msg=' and more')
                msg += res + '\n\n'

            return msg

