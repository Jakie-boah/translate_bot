
from aiogram.utils import executor
from bot import *

from handlers.album_handler import AlbumMiddleware

if __name__ == '__main__':
    dp.middleware.setup(AlbumMiddleware())

    logger.info("Бот запущен ветка new_version")
    # dp.start_polling(bot)
    executor.start_polling(dp)
