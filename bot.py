from config import dp
from aiogram.types import Message
from handlers.control_panel import Control
from loguru import logger
from filters.filter import user_is_admin


@dp.message_handler()
async def start(message: Message):

    control = Control(message)
    logger.info(message)

    """ Bot checks if user is replying on one of the translated messages"""
    if message.reply_to_message and control.check_if_reply_on_tr_msg():

        """
        Message was sent from topic - everything alright.
        Now bot calls necessary function to translate and resend message to the remaining topics
        """

        await control.reply_on_message()

    """ Bot is checking if message was sent from topic or general chat """
    if not message.is_topic_message:

        """
        Message wasn't sent from topic, so now bot is going to try to delete it,
        through this function bot checks if it has needed admin privilege and only after that deletion is committed
        """

        if not await user_is_admin(message):
            await control.delete_message()

    """ Bot takes message if it is from topic and translate it and than resend it to the rest of the topics """
    if message.is_topic_message and not control.check_if_reply_on_tr_msg():
        logger.info(message)
        await control.translate_and_send_message()
