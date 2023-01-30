import sys
sys.path.append('./')

from aiogram.utils import executor
from create_bot import dispetcher
from handlers import admin, client

if __name__ == '__main__':
    client.register_client_handlers(dispetcher)
    admin.register_client_handlers(dispetcher)
    executor.start_polling(dispetcher, skip_updates = True)
 