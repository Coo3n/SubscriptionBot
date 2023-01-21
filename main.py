from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
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
        

@dispetcher.message_handler(commands = ['start'])
@dispetcher.throttled(anti_flood, rate = 2)
async def process_start_command(message: types.Message):
    user_exists = await db.user_exists(message.from_user.id)
    if user_exists == False:
        await db.add_user(message.from_user.id)

    await message.reply("Добро пожаловать, данный Бот предоставляет услуги\nпо продаже подписок на канал!\nЧтобы преобрести подписку - нажмите на одну из предложенных кнопок! ", reply_markup = kb.main_menu)


@dispetcher.message_handler(Text(equals = "🤝 Поддержка"))
async def show_help_admin(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message_id)
    await message.answer("🤝 Поддержка\n📨 По всем интересующим вопросам — @coo3n")
        

@dispetcher.message_handler(Text(equals = "👤 Мой аккаунт"))
@dispetcher.throttled(anti_flood, rate = 1)
async def show_user_account(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message_id)
    cnt_money = await db.get_user_money(message.from_user.id)
    await message.answer("👤 Мой аккаунт\n— ID: " + str(message.from_user.id) + "\n— Текущий баланс: " + str(cnt_money[0][0]) + " руб")
    

@dispetcher.message_handler(Text(equals = "🗓 Тарифные планы"))
async def show_all_rates(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message_id)
    await message.answer("🗓 Тарифные планы \nВыбирай любой подходящий для себя тариф и производи оплату по 🥝QIWI!", reply_markup = kb.menu_сhoice_rate)


if __name__ == '__main__':
    executor.start_polling(dispetcher, skip_updates = True)