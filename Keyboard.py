from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

#Main menu
but_rate         = KeyboardButton("🗓 Тарифные планы")
but_subscribe    = KeyboardButton("🗃 Моя подписка")
but_info_account = KeyboardButton("👤 Мой аккаунт")
but_help_admins  = KeyboardButton("🤝 Поддержка")


#Buttons for choosing payment by date
but_rate_month      = InlineKeyboardButton(text = "🎯 МЕСЯЦ  🎯 | 30 ДНЕЙ | 150 RUB", callback_data = "rate_month")
but_rate_six_months = InlineKeyboardButton(text = "💘 ПОЛГОДА 💘 | 182 ДНЯ | 250 RUB", callback_data = "rate_six_months")
but_rate_year       = InlineKeyboardButton(text = "⚡ ЦЕЛЫЙ ГОД ⚡ | 365 ДНЕЙ | 500 RUB", callback_data = "rate_year")
but_rate_forever    = InlineKeyboardButton(text = "🔥 НАВСЕГДА 🔥 | ∞ ДНЕЙ | 800 RUB", callback_data = "rate_forever")


#Close payment
but_close_payment = InlineKeyboardButton(text = "❌ Отменить платеж ❌", callback_data = "close_payment")

#Check payment
but_check_payment = InlineKeyboardButton(text = "✅ Проверить оплату ✅", callback_data = "check_payment")

main_menu         = ReplyKeyboardMarkup(resize_keyboard = True).insert(but_rate).insert(but_subscribe).add(but_info_account).insert(but_help_admins)
choice_menu_rate  = InlineKeyboardMarkup(row_width = 1).add(but_rate_month, but_rate_six_months, but_rate_year, but_rate_forever)
payment_menu      = InlineKeyboardMarkup(row_width = 1).add(but_check_payment, but_close_payment)