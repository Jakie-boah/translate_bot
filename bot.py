from config import dp, bot
from aiogram.types import Message, ContentType, Document, InputFile
from handlers.control_panel import ControlAdvanced
from loguru import logger
from filters.filter import user_is_admin
from update_airtable import update
import io
from photo_handler import handle_albums


@dp.message_handler()
async def start(message: Message):

    control = ControlAdvanced(message)
    logger.info(message)

    if await control.check_if_reply_on_tr_msg():

        """
        Message was sent from topic - everything alright.
        Now bot calls necessary function to translate and resend message to the remaining topics
        """

        await control.reply_on_message()

    else:
        logger.info(message)
        await control.translate_and_send_message()

