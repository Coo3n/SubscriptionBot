from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyqiwip2p import QiwiP2P
from Constants import TG_TOKEN, QIWI_TOKEN
from database import DataBase

bot = Bot(token=TG_TOKEN)
storage = MemoryStorage()
dispetcher = Dispatcher(bot, storage=storage)
db = DataBase.DataBase()
qiwi = QiwiP2P(auth_key=QIWI_TOKEN)