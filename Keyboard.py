from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

#Main menu
but_rate         = KeyboardButton("🗓 Тарифные планы")
but_subscribe    = KeyboardButton("🗃 Моя подписка")
but_info_account = KeyboardButton("👤 Мой аккаунт")
but_help_admins  = KeyboardButton("🤝 Поддержка")


#Buttons for choosing payment by date
but_rate_month      = InlineKeyboardButton(text = "🎯 МЕСЯЦ  🎯 | 30 ДНЕЙ | 100 RUB", callback_data = "rate_month")
but_rate_six_months = InlineKeyboardButton(text = "💘 ПОЛГОДА 💘 | 182 ДНЯ | 250 RUB", callback_data = "rate_six_months")
but_rate_year       = InlineKeyboardButton(text = "⚡ ЦЕЛЫЙ ГОД ⚡ | 365 ДНЕЙ | 500 RUB", callback_data = "rate_year")
but_rate_forever    = InlineKeyboardButton(text = "🔥 НАВСЕГДА 🔥 | ∞ ДНЕЙ | 800 RUB", callback_data = "rate_forever")


#Return to main_menu
but_exit_to_MainMenu = InlineKeyboardButton(text = "⬅Главное меню", callback_data = "return_to_main_menu")

main_menu = ReplyKeyboardMarkup(resize_keyboard = True).insert(but_rate).insert(but_subscribe).add(but_info_account).insert(but_help_admins)
menu_сhoice_rate  = InlineKeyboardMarkup(row_width = 1).add(but_rate_month, but_rate_six_months, but_rate_year, but_rate_forever)
