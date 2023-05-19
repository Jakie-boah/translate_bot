from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def message_keyboard():
    message_keyboard_ = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text='Translate', callback_data='translate_message')
    message_keyboard_.add(button)
    return message_keyboard_


def media_keyboard():
    media_keyboard_ = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text='Translate', callback_data='translate_media')
    media_keyboard_.add(button)
    return media_keyboard_
