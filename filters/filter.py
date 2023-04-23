from config import bot


async def user_is_admin(message) -> bool:
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.is_chat_admin()


