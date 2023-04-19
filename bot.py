from config import dp, bot
from aiogram.types import Message
from control_panel import Control
from loguru import logger


@dp.message_handler()
async def start(message: Message):

    control = Control(message)

    if message.reply_to_message and control.check_if_reply_on_tr_msg():
        await control.reply_on_message()

    if not message.is_topic_message:
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)

        if not member.is_chat_admin():
            await control.delete_message()

    if message.is_topic_message and not control.check_if_reply_on_tr_msg():
        logger.info(message)
        await control.translate_and_send_message()

    # """Bot checks if user is replying on one of the translated messages"""
    # if not message.reply_to_message:
    #     """ Bot is checking if message was sent from topic or general chat """
    #
    #     if message.is_topic_message:
    #         """
    #         Message was sent from topic - everything alright.
    #         Now bot calls necessary function to translate and resend message to the remaining topics
    #         """
    #
    #         await control.translate_and_send_message()
    #
    #     else:
    #         """
    #         Message wasn't sent from topic, so now bot is going to try to delete it,
    #         through this function bot checks if it has needed admin privilege and only after that deletion is committed
    #         """
    #
    #         await control.delete_message()
    #
    # else:
    #     """If it is indeed, bot resend reply directly to the user and in specific topic"""
    #
    #     await control.reply_on_message()


        # logger.info(message)








