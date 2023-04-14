from config import dp, bot
from aiogram.types import Message
from control_panel import Control
from loguru import logger


@dp.message_handler()
async def start(message: Message):
    logger.info(message.url)
    control = Control(message.chat.id, message)
    await control.set_languages_and_send_message()



# -970406949 - русский
# -826578431 - англ
# -807639216 - арабский