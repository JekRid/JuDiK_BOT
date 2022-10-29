from msilib.schema import MsiAssembly
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import Config as config
from button import Start #Next_step, Start, Menu, End, Next_ques
import psycopg2
import ast


# Подключение к postgres
def connect_db():
    try:
        con = psycopg2.connect(
        database=config.database, 
        user=config.user, 
        password=config.password, 
        host=config.host, 
        port=config.port
        )
        print("Database opened successfully")
        return con
    except psycopg2.OperationalError:
        print("Database opened error")
        exit()

# Инициализация бота и подключение storage
bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Форма для записи ввода пользователя
class Form(StatesGroup):
    Login = State()
    Password = State() 


# Вывод меню при команде /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет!\nВведи свой логин:")
    await Form.Login.set()

@dp.message_handler(state=Form.Login)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Login'] = message.text
    await message.reply('Введите пароль:')
    await Form.Password.set()


@dp.message_handler(state=Form.Password)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Password'] = message.text

    Login = md.code(data['Login']).replace("`", "")
    Password = md.code(data['Password']).replace("`", "")
    await Form.Password.set()

    if Login == "Admin" and Password == "Max":
        print("Test")
    else:
        await message.reply(f'Ты не пройдешь!')



if __name__ == '__main__':
    executor.start_polling(dp)
