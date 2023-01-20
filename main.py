from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Token import TG_TOKEN
from DataBase import DataBase
import Keyboard as kb 


bot = Bot(token = TG_TOKEN)
storage = MemoryStorage()
dispetcher = Dispatcher(bot, storage = storage)
db = DataBase()


async def anti_flood(*args, **kwargs):
    ans = args[0]
    await ans.answer("Пожалуйста, не спамьте! Нажимайте спокойнее :)")
        

@dispetcher.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user_exists = await db.user_exists(message.from_user.id)
    if user_exists == False:
        await db.add_user(message.from_user.id)

    await message.reply("Добро пожаловать, данный Бот предоставляет услуги\nпо продаже подписок на канал!\nЧтобы преобрести подписку - нажмите на одну из предложенных кнопок! ", reply_markup = kb.main_menu)

if __name__ == '__main__':
    executor.start_polling(dispetcher, skip_updates = True)    