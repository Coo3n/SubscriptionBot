from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

#Main menu
but_rate         = KeyboardButton("🗓 Тарифные планы")
but_subscribe    = KeyboardButton("🗃 Моя подписка")
but_info_account = KeyboardButton("👤 Мой аккаунт")
but_help_admins  = KeyboardButton("🤝 Поддержка")

#Return to main_menu
but_exit_to_MainMenu = InlineKeyboardButton(text = "⬅Главное меню", callback_data ="return_to_Mainmenu")

main_menu = ReplyKeyboardMarkup(resize_keyboard=True).insert(but_rate).insert(but_subscribe).add(but_info_account).insert(but_help_admins)