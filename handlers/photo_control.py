"""Handler for messages which contain photos - here we translate caption's and send to the topics"""

from config import bot
from loguru import logger
import io
from .setup import SetUp


class PhotoControl(SetUp):
    def __init__(self, message):
        super().__init__(message)

    async def transform_message(self):
        self.translate_dict = self.message.chat.id
        self.determine_language = self.message.caption
        logger.info(self.determine_language)
        self.translate_dict.remove(self.determine_language)
        if self.set_active_languages():
            m = ','.join(self.translate_dict)
            p = await bot.send_message(self.message.chat.id,
                                       text=f'Message will be translated in <b>{m}</b>',
                                       reply_to_message_id=self.message.message_id,
                                       )
            msg = str

            fp = io.BytesIO()
            await self.message.photo[-1].download(fp)

            for lang in self.translate_dict:
                res = await self._translate(lang, self.message.caption, msg=' and more')
                msg += res + '\n\n'

            await bot.delete_message(chat_id=p.chat.id, message_id=p.message_id)
            await bot.send_photo(self.message.chat.id,
                                 photo=fp,
                                 caption=msg,
                                 reply_to_message_id=self.message.message_id)
