from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from datetime import datetime, timedelta
from start.create_bot import bot, dispetcher, db, qiwi
import keyboards.client_kb as kb
import Constants as const 

async def anti_flood(*args, **kwargs):
    ans = args[0]
    await ans.answer("Не перенапрегай свою руку, друг мой 🙂")


#Проверка на подписку канала
async def check_sub_channel(user_id):
    chat_member = await bot.get_chat_member(chat_id = const.TELEGRAM_PUBLIC_CHAT_ID, user_id = user_id)
    return chat_member['status'] != 'left'


#Создание приватной ссылки на канал
async def create_link_to_group():
    expire_date = datetime.now() + timedelta(days = 1)
    link = await bot.create_chat_invite_link(const.TELEGRAM_PRIVATE_CHAT_ID, expire_date.timestamp, 1)
    return link.invite_link 


#Отправка текста тарифа на канал 
async def send_payment_invoice(user_id, price, rate, bill_url):
    await bot.send_message(user_id, 
                    f'⏳ Счет на оплату ⏳\n\n'

                    f'Информация:\n'
                    f'— Итоговая цена: {price} RUB\n'
                    f'— Период: {rate}\n'
                    f'— Тип платежа: Одноразовый\n\n'
                    f'После успешной оплаты вам станет доступен:\n'
                    f'— Канал «🔥Архив Хентай🔥»\n\n'
                    
                    f'Ссылка на оплату по QIWI 🥝:\n{bill_url}', reply_markup = kb.payment_menu)

    
@dispetcher.callback_query_handler(text = "check_sub_to_channel")
@dispetcher.throttled(anti_flood, rate = 1)
async def is_sub_to_channel(query: types.CallbackQuery):
    await query.answer("👉 ПОДПИСАЛСЯ 👈")
    
    if await check_sub_channel(query.from_user.id) == False:
        await bot.send_message(query.from_user.id, "❗ Для использования бота, Вам необходимо подписаться на основной канал ❗", reply_markup = kb.sub_check_menu)
    else:
        await bot.send_message(query.from_user.id, 
            '🏆 Конничива, любитель искусства! 🏆\n\n'
            'Я нашел уникальный способ, как тебе попасть в удивительный мир самых глубоких фантазий, без помощи школьного автобуса 🚌\n\n'
            'Предлагаю тебе попробовать воспользоваться моим безграничным предложением, у меня есть ВСЁ, что пожелаешь! 🥰\n\n'
            '🔥 Быстрей залетай к нам на канал 🔥', reply_markup = kb.main_menu)
        

@dispetcher.message_handler(commands = ['start'])
@dispetcher.throttled(anti_flood, rate = 1)
async def process_start_command(message: types.Message):
    if await check_sub_channel(message.from_user.id) == False:
        await message.reply("❗ Для использования бота, Вам необходимо подписаться на основной канал ❗", reply_markup = kb.sub_check_menu)
        return

    if await db.user_exists(message.from_user.id) == False:
        await db.add_user(message.from_user.id)

    await message.reply('🏆 Конничива, любитель искусства! 🏆\n\n'
                        'Я нашел уникальный способ, как тебе попасть в удивительный мир самых глубоких фантазий, без помощи школьного автобуса 🚌\n\n'
                        'Предлагаю тебе попробовать воспользоваться моим безграничным предложением, у меня есть ВСЁ, что пожелаешь! 🥰\n\n'
                        '🔥 Быстрей залетай к нам на канал 🔥' , reply_markup = kb.main_menu)
    

@dispetcher.message_handler(Text(equals = "🤝 Поддержка"))
@dispetcher.throttled(anti_flood, rate = 1)
async def show_help_admin(message: types.Message):
    if await check_sub_channel(message.from_user.id) == False:
        await message.reply("Для использования бота, Вам необходимо подписаться на основной канал!", reply_markup = kb.sub_check_menu)
        return

    await bot.delete_message(message.from_user.id, message.message_id)
    await message.answer("🤝 Поддержка\n📨 По всем интересующим вопросам — @coo3n")
        

@dispetcher.message_handler(Text(equals = "👤 Мой аккаунт"))
@dispetcher.throttled(anti_flood, rate = 1)
async def show_user_account(message: types.Message):
    if await check_sub_channel(message.from_user.id) == False:
        await message.reply("❗ Для использования бота, Вам необходимо подписаться на основной канал ❗", reply_markup = kb.sub_check_menu)
        return

    await bot.delete_message(message.from_user.id, message.message_id)
    
    result = await db.get_tarif_user(message.from_user.id)
    channel = "🔥 Архив Хентая 🔥"
    tarif = "" 

    match result[0][0]:
        case 0: 
            await message.answer("👤 Мой аккаунт\n— ID: " + str(message.from_user.id) + "\n— Подписка: ❗️ОТСУТСТВУЕТ❗️") 
            return
        case 1:
            tarif = "🎯 МЕСЯЦ  🎯"
        case 2:
            tarif = "💘 ПОЛГОДА 💘"
        case 3:
            tarif = "⚡ ЦЕЛЫЙ ГОД ⚡"
        case 4:
            tarif = "🔥 НАВСЕГДА 🔥"
    
    await message.answer("👤 Мой аккаунт\n— ID: " + str(message.from_user.id) + "\n— Подписка: " + channel + "\n— Текущий тариф: " + tarif)
    

@dispetcher.message_handler(Text(equals = "🗓 Тарифные планы"))
@dispetcher.throttled(anti_flood, rate = 1)
async def show_all_rates(message: types.Message):
    if await check_sub_channel(message.from_user.id) == False:
        await message.reply("❗ Для использования бота, Вам необходимо подписаться на основной канал ❗", reply_markup = kb.sub_check_menu)
        return

    await bot.delete_message(message.from_user.id, message.message_id)
    await message.answer("🗓 Тарифные планы \n\n🥝 Выбирай любой подходящий для себя тариф и производи оплату по QIWI! 🥝", reply_markup = kb.choice_menu_rate)


@dispetcher.callback_query_handler(text = "rate_month")
@dispetcher.throttled(anti_flood, rate = 2)
async def top_up_balance_month(query: types.CallbackQuery):
    if await check_sub_channel(query.from_user.id) == False:
        await query.answer("❗ Для использования бота, Вам необходимо подписаться на основной канал ❗", reply_markup = kb.sub_check_menu)
        return

    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.answer("Тариф 🎯 МЕСЯЦ  🎯")
    
    if await db.exist_bill_сheck(query.from_user.id) == True:
        await bot.send_message(query.from_user.id, "⚠️ Предыдущий чек недействителен! ⚠️")
        await db.delete_check(query.from_user.id)

    bill = qiwi.bill(amount = 149, lifetime = 5, comment = "Время оплаты - 5 минут!")
    
    await db.add_check(query.from_user.id, bill.bill_id[21:], const.RATE_MONTH)
    await send_payment_invoice(query.from_user.id, 149, "🎯 МЕСЯЦ  🎯", bill.pay_url)
   
    
@dispetcher.callback_query_handler(text = "rate_six_months")
@dispetcher.throttled(anti_flood, rate = 2)
async def top_up_balance_six_month(query: types.CallbackQuery):
    if await check_sub_channel(query.from_user.id) == False:
        await query.answer("❗ Для использования бота, Вам необходимо подписаться на основной канал ❗", reply_markup = kb.sub_check_menu)
        return

    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.answer("Тариф 💘 ПОЛГОДА 💘")

    if await db.exist_bill_сheck(query.from_user.id) == True:
        await bot.send_message(query.from_user.id, "⚠️ Предыдущий чек недействителен! ⚠️")
        await db.delete_check(query.from_user.id)

    bill = qiwi.bill(amount = 249, lifetime = 5, comment = "Время оплаты - 5 минут!")
    
    await db.add_check(query.from_user.id, bill.bill_id[21:], const.RATE_SIX_MONTHS)
    await send_payment_invoice(query.from_user.id, 249, "💘 ПОЛГОДА 💘", bill.pay_url)


@dispetcher.callback_query_handler(text = "rate_year")
@dispetcher.throttled(anti_flood, rate = 2)
async def top_up_balance_year(query: types.CallbackQuery):
    if await check_sub_channel(query.from_user.id) == False:
        await query.answer("❗ Для использования бота, Вам необходимо подписаться на основной канал ❗", reply_markup = kb.sub_check_menu)
        return

    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.answer("Тариф ⚡ ЦЕЛЫЙ ГОД ⚡")

    if await db.exist_bill_сheck(query.from_user.id) == True:
        await bot.send_message(query.from_user.id, "⚠️ Предыдущий чек недействителен! ⚠️")
        await db.delete_check(query.from_user.id)

    bill = qiwi.bill(amount = 499, lifetime = 5, comment = "Время оплаты - 5 минут!")
    
    await db.add_check(query.from_user.id, bill.bill_id[21:], const.RATE_YEAR)
    await send_payment_invoice(query.from_user.id, 499, "⚡ ЦЕЛЫЙ ГОД ⚡", bill.pay_url)


@dispetcher.callback_query_handler(text = "rate_forever")
@dispetcher.throttled(anti_flood, rate = 2)
async def top_up_balance_forever(query: types.CallbackQuery):
    if await check_sub_channel(query.from_user.id) == False:
        await query.answer("❗ Для использования бота, Вам необходимо подписаться на основной канал ❗", reply_markup = kb.sub_check_menu)
        return
        
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.answer("Тариф 🔥 НАВСЕГДА 🔥")

    if await db.exist_bill_сheck(query.from_user.id) == True:
        await bot.send_message(query.from_user.id, "⚠️ Предыдущий чек недействителен! ⚠️")
        await db.delete_check(query.from_user.id)

    bill = qiwi.bill(amount = 799, lifetime = 5, comment = "Время оплаты - 5 минут!")
    
    await db.add_check(query.from_user.id, bill.bill_id[21:], const.RATE_FOREVER)
    await send_payment_invoice(query.from_user.id, 799, "🔥 НАВСЕГДА 🔥", bill.pay_url)
    

@dispetcher.callback_query_handler(text = "close_payment")
async def close_payment_check(query: types.CallbackQuery):
    await query.answer("❌ Отменить платеж ❌")
    
    if await db.exist_bill_сheck(query.from_user.id) == True:
        await db.delete_check(query.from_user.id)
    
    await bot.delete_message(query.from_user.id, query.message.message_id)

 
@dispetcher.callback_query_handler(text = "check_payment")
@dispetcher.throttled(anti_flood, rate = 2)
async def check_payment(query: types.CallbackQuery):
    await query.answer("✅ Проверить оплату ✅")
    
    if await db.exist_bill_сheck(query.from_user.id) == False:
        await bot.delete_message(query.from_user.id, query.message.message_id)
        await bot.send_message(query.from_user.id, "🚩 Данной оплаты не существует! 🚩") 
        return 
    
    info_for_check = await db.get_info_for_check(query.from_user.id)               
        
    if len(info_for_check) != 0:
        status_bill_check = str(qiwi.check(bill_id = "WhiteApfel-PyQiwiP2P-" + str(info_for_check[0][2])).status)
        
        match status_bill_check:
            case "WAITING":
                await bot.send_message(query.from_user.id, "🕒 Этот счёт находиться в стадии ожидании оплаты 🕒")
                return
            case "PAID":
                await db.set_rate_to_user(query.from_user.id, info_for_check[0][3])
                link_group = await create_link_to_group()
                await bot.send_message(query.from_user.id, "🎉 Вы успешно оплатили счет! 🎉\nСсылка на приватный канал:\n" + str(link_group))
            case "EXPIRED":
                await bot.send_message(query.from_user.id, "⌛ Время жизни счёта истекло, попробуйте начать оплату заново! ⌛")
            case _:
                await bot.send_message(query.from_user.id, "🛠️ Счёт по техническим причинам отклонён, попробуйте заново! 🛠️")        

        await db.delete_check(query.from_user.id)     
    else: 
        await bot.send_message(query.from_user.id, "🚩 Данной оплаты не существует!\nПопробуйте заново! 🚩") 


def register_client_handlers(dispetcher: Dispatcher):
    dispetcher.register_callback_query_handler(is_sub_to_channel, text = "check_sub_to_channel")
    dispetcher.register_message_handler(process_start_command, commands = ['start'])
    dispetcher.register_message_handler(show_help_admin, Text(equals = "🤝 Поддержка"))
    dispetcher.register_message_handler(show_user_account, Text(equals = "👤 Мой аккаунт"))
    dispetcher.register_message_handler(show_all_rates, Text(equals = "🗓 Тарифные планы"))
    dispetcher.register_callback_query_handler(top_up_balance_month, text = "rate_month")
    dispetcher.register_callback_query_handler(top_up_balance_six_month, text = "rate_six_months")
    dispetcher.register_callback_query_handler(top_up_balance_year, text = "rate_year")
    dispetcher.register_callback_query_handler(top_up_balance_forever, text = "rate_forever")
    dispetcher.register_callback_query_handler(close_payment_check, text = "close_payment")
    dispetcher.register_callback_query_handler(check_payment, text = "check_payment")