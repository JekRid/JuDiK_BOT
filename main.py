from msilib.schema import MsiAssembly
import re
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
from button import Auth, Menu, CancelCreate #Next_step, Start, Menu, End, Next_ques
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

class CreateMeeting(StatesGroup):
    Name = State()
    Date = State()
    Time = State()
    Place = State()
    Worker = State()


# Вывод меню при команде /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет!\nВведите свой логин:")
    await Form.Login.set()


@dp.message_handler(state=Form.Login)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Login'] = message.text
    await message.answer('Введите пароль:')
    await Form.Password.set()


@dp.message_handler(state=Form.Password,)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Password'] = message.text

    Login = md.code(data['Login']).replace("`", "")
    Password = md.code(data['Password']).replace("`", "")

    await message.delete()

    con = connect_db()
    cur = con.cursor()
    cur.execute(
            f'''\
            SELECT name_worker, otch_worker FROM worker
            WHERE login = '{Login}' and password = '{Password}'
            '''
        )

    rows = cur.fetchall()
    if len(rows) == 1:
        await message.answer(f'Добро пожаловать, {rows[0][0]} {rows[0][1]}!', reply_markup=Menu())
    else:
        await message.answer(f'Неверный логин или пароль.', reply_markup=Auth())
        await state.finish()     
        

@dp.callback_query_handler(text="Create meeting", state='*')
async def Exit_Quiz(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите имя (назначение) собрания:', reply_markup=CancelCreate())
    await CreateMeeting.Name.set()

@dp.message_handler(state=CreateMeeting.Name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Name'] = message.text
    await message.answer('Введите дату собрания:', reply_markup=CancelCreate())
    await CreateMeeting.Date.set()

@dp.message_handler(state=CreateMeeting.Date)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Date'] = message.text
    await message.answer('Введите время собрания:', reply_markup=CancelCreate())
    await CreateMeeting.Time.set()

@dp.message_handler(state=CreateMeeting.Time)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Time'] = message.text
    await message.answer('Введите место собрания:', reply_markup=CancelCreate())
    await CreateMeeting.Place.set()

@dp.message_handler(state=CreateMeeting.Place)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Place'] = message.text
    await CreateMeeting.Time.set()    
    print(f'''
        {md.code(data['Name'])}\n
        {md.code(data['Date'])}\n
        {md.code(data['Time'])}\n
        {md.code(data['Place'])}\n
    ''')



@dp.callback_query_handler(text=["Auth", "Cancel"], state='*')
async def Exit_Quiz(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text("Введите свой логин:")
    await Form.Login.set()
    await callback.answer()  


@dp.callback_query_handler(text=["Cancel Create"], state='*')
async def Exit_Quiz(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.answer("Введите свой логин:")
    await Form.Login.set()
    await callback.answer()  

if __name__ == '__main__':
    executor.start_polling(dp)
