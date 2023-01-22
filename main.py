from datetime import datetime, timedelta
from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Token import TG_TOKEN, QIWI_TOKEN
from DataBase import DataBase
from pyqiwip2p import QiwiP2P
import Keyboard as kb 
import random


bot = Bot(token = TG_TOKEN)
storage = MemoryStorage()
dispetcher = Dispatcher(bot, storage = storage)
db = DataBase()
qiwi = QiwiP2P(auth_key = QIWI_TOKEN)

TELEGRAM_CHAT_ID = -1001635609543
RATE_MONTH      = 1
RATE_SIX_MONTHS = 2
RATE_YEAR       = 3
RATE_FOREVER    = 4

async def anti_flood(*args, **kwargs):
    ans = args[0]
    await ans.answer("Пожалуйста, не спамьте! Нажимайте спокойнее :)")
        

@dispetcher.message_handler(commands = ['start'])
@dispetcher.throttled(anti_flood, rate = 1)
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
    cnt_money = await db.get_tarif_user(message.from_user.id)
    await message.answer("👤 Мой аккаунт\n— ID: " + str(message.from_user.id) + "\n— Текущий баланс: " + str(cnt_money[0][0]) + " руб")
    

@dispetcher.message_handler(Text(equals = "🗓 Тарифные планы"))
async def show_all_rates(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message_id)
    await message.answer("🗓 Тарифные планы \nВыбирай любой подходящий для себя тариф и производи оплату по 🥝QIWI!", reply_markup = kb.choice_menu_rate)


@dispetcher.callback_query_handler(text = "rate_month")
async def top_up_balance_month(query: types.CallbackQuery):
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.answer("Тариф 🎯 МЕСЯЦ  🎯")
    
    if await db.exist_bill_сheck(query.from_user.id) == True:
        await bot.send_message(query.from_user.id, "⚠️ Предыдущий чек недействителен! ⚠️")
        await db.delete_check(query.from_user.id)

    bill = qiwi.bill(amount = 150, lifetime = 5, comment = "Время оплаты - 5 минут!")
    
    await db.add_check(query.from_user.id, RATE_MONTH)
    await bot.send_message(query.from_user.id, 
                    '⏳ Счет на оплату ⏳\n\n'
                    'Информация:\n'
                    '— Итоговая цена: 150 RUB\n'
                    '— Период: 🎯 МЕСЯЦ 🎯\n'
                    '— Тип платежа: Одноразовый\n\n'
                    'После успешной оплаты вам станет доступен:\n'
                    '— Канал «🔥Архив Хентай🔥»\n\n'
                    
                    f'Ссылка на оплату по QIWI 🥝:\n{bill.pay_url}', reply_markup = kb.payment_menu)
   
        


@dispetcher.callback_query_handler(text = "rate_six_months")
async def top_up_balance_six_month(query: types.CallbackQuery):
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.answer("Тариф 💘 ПОЛГОДА 💘")

    if await db.exist_bill_сheck(query.from_user.id) == True:
        await bot.send_message(query.from_user.id, "⚠️ Предыдущий чек недействителен! ⚠️")
        await db.delete_check(query.from_user.id)

    bill = qiwi.bill(amount = 250, lifetime = 5, comment = "Время оплаты - 5 минут!")
    
    await db.add_check(query.from_user.id, RATE_SIX_MONTHS)
    await bot.send_message(query.from_user.id, 
                    '⏳ Счет на оплату ⏳\n\n'
                    'Информация:\n'
                    '— Итоговая цена: 250 RUB\n'
                    '— Период: 💘 ПОЛГОДА 💘\n'
                    '— Тип платежа: Одноразовый\n\n'
                    'После успешной оплаты вам станет доступен:\n'
                    '— Канал «🔥Архив Хентай🔥»\n\n'
                    
                    f'Ссылка на оплату по QIWI 🥝:\n{bill.pay_url}', reply_markup = kb.payment_menu)


@dispetcher.callback_query_handler(text = "rate_year")
async def top_up_balance_year(query: types.CallbackQuery):
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.answer("Тариф ⚡ ЦЕЛЫЙ ГОД ⚡")

    if await db.exist_bill_сheck(query.from_user.id) == True:
        await bot.send_message(query.from_user.id, "⚠️ Предыдущий чек недействителен! ⚠️")
        await db.delete_check(query.from_user.id)

    bill = qiwi.bill(amount = 500, lifetime = 5, comment = "Время оплаты - 5 минут!")
    
    await db.add_check(query.from_user.id, RATE_YEAR)
    await bot.send_message(query.from_user.id, 
                    '⏳ Счет на оплату ⏳\n\n'
                    'Информация:\n'
                    '— Итоговая цена: 500 RUB\n'
                    '— Период: ⚡ ЦЕЛЫЙ ГОД ⚡\n'
                    '— Тип платежа: Одноразовый\n\n'
                    'После успешной оплаты вам станет доступен:\n'
                    '— Канал «🔥Архив Хентай🔥»\n\n'
                    
                    f'Ссылка на оплату по QIWI 🥝:\n{bill.pay_url}', reply_markup = kb.payment_menu)

@dispetcher.callback_query_handler(text = "rate_forever")
async def top_up_balance_forever(query: types.CallbackQuery):
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.answer("Тариф 🔥 НАВСЕГДА 🔥")

    if await db.exist_bill_сheck(query.from_user.id) == True:
        await bot.send_message(query.from_user.id, "⚠️ Предыдущий чек недействителен! ⚠️")
        await db.delete_check(query.from_user.id)

    bill = qiwi.bill(amount = 800, lifetime = 5, comment = "Время оплаты - 5 минут!")
    
    await db.add_check(query.from_user.id, RATE_FOREVER)
    await bot.send_message(query.from_user.id, 
                    '⏳ Счет на оплату ⏳\n\n'
                    'Информация:\n'
                    '— Итоговая цена: 800 RUB\n'
                    '— Период: 🔥 НАВСЕГДА 🔥\n'
                    '— Тип платежа: Одноразовый\n\n'
                    'После успешной оплаты вам станет доступен:\n'
                    '— Канал «🔥Архив Хентай🔥»\n\n'
                    
                    f'Ссылка на оплату по QIWI 🥝:\n{bill.pay_url}', reply_markup = kb.payment_menu)
    

@dispetcher.callback_query_handler(text = "close_payment")
async def close_payment_check(query: types.CallbackQuery):
    await query.answer("❌ Отменить платеж ❌")
    
    if await db.exist_bill_сheck(query.from_user.id) == True:
        await db.delete_check(query.from_user.id)
    
    await bot.delete_message(query.from_user.id, query.message.message_id)

@dispetcher.callback_query_handler(text = "check_payment")
async def check_payment(query: types.CallbackQuery):
    await query.answer("✅ Проверить оплату ✅")
    
    if await db.exist_bill_сheck(query.from_user.id) == False:
        await bot.delete_message(query.from_user.id, query.message.message_id)
        await bot.send_message(query.from_user.id, "🚩 Данной оплаты не существует!\nПопробуйте заново! 🚩") 
    else: 
        pass



@dispetcher.message_handler(Text(equals = "link"))
async def create_link_to_group(message: types.Message):
    expire_date = datetime.now() + timedelta(days = 1)
    link = await bot.create_chat_invite_link(TELEGRAM_CHAT_ID, expire_date.timestamp, 1)

    print(link.invite_link) 

if __name__ == '__main__':
    executor.start_polling(dispetcher, skip_updates = True)