from aiogram import types, Dispatcher
from start.create_bot import bot, dispetcher, db

@dispetcher.message_handler(commands = ['send_message'])
async def send_message_all_user(message: types.Message):
    users = await db.get_all_user()
    for user in users:
        await bot.send_message(user[0], message.text[13:])

def register_client_handlers(dispetcher: Dispatcher):
    dispetcher.register_message_handler(send_message_all_user, commands = ['send_message'])
    