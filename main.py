from asyncio.windows_events import NULL
from calendar import month
from tkinter.tix import Select
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
from button import Auth, Menu, CancelCreate, Continue
import psycopg2
from datetime import date, datetime, timedelta
import asyncio
from time import sleep

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
    MassWork = State()
    Worker = State()

    Time = State()
    Place = State()



# Вывод меню при команде /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет!\nВведите свой логин:")
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
        Login = data['Login']
        Password = data['Password']
        id = message.from_user.id

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

        con = connect_db()
        cur = con.cursor()
        cur.execute(
            f'''\
            UPDATE worker SET id_tg = '{id}' WHERE worker.login = '{Login}' AND worker.password = '{Password}';
            '''
        )

        con.commit()
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
    await message.answer('Введите место собрания:', reply_markup=CancelCreate())
    await CreateMeeting.Place.set()

@dp.message_handler(state=CreateMeeting.Place)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Place'] = message.text
    await message.answer('Введите ФИО сотрудника:', reply_markup=CancelCreate())
    await CreateMeeting.Worker.set()

@dp.message_handler(state=CreateMeeting.Worker)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Worker'] = message.text
    people = data['Worker'].replace(".","%").split(" ")
    #print(people)
    con = connect_db()
    cur = con.cursor()
    cur.execute(
            f'''\
            SELECT id_worker, fam_worker, name_worker, otch_worker FROM worker
            WHERE fam_worker like '{people[0]}' and
            name_worker like '{people[1]}' and
            otch_worker like '{people[2]}'; 
            '''
        )
    rows = cur.fetchall()
    

    builder = InlineKeyboardMarkup()
    for i in range(len(rows)):
        button = InlineKeyboardButton(f'{rows[i][1]} {rows[i][2]} {rows[i][3]}', callback_data=f'ID {rows[i][0]}')
        builder.add(button) 
    
    mass = []
    
    try:
        t = md.code(data["MassWork"]).replace("\\", "").replace("`", "").replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        t = t.split(',')
        for i in t:
            con = connect_db()
            cur = con.cursor()
            cur.execute(
                f'''\
                SELECT id_worker, fam_worker, name_worker, otch_worker FROM worker
                WHERE id_worker = {i};
                '''
            )
            rows = cur.fetchall()
            mass.append("\n"+rows[0][1]+" "+rows[0][2]+" "+rows[0][3])
            
        await message.answer(
            f'Выбранные пользователи: {"".join(i for i in mass)}',
            reply_markup=builder,
        )
    except KeyError:
        await message.answer(
        f'Выберите пользователя:',
        reply_markup=builder,
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('ID') , state='*')
async def Start_Quiz(c,  state: FSMContext):
    async with state.proxy() as test:
        try:
            test["MassWork"].append(c.data.replace("ID ", ""))
            print(test["MassWork"])
        except KeyError:
            test["MassWork"] = []
            test["MassWork"].append(c.data.replace("ID ", ""))
            print(test["MassWork"])

    mass = []
    
    try:
        for i in test["MassWork"]:
            con = connect_db()
            cur = con.cursor()
            cur.execute(
                f'''\
                SELECT id_worker, fam_worker, name_worker, otch_worker FROM worker
                WHERE id_worker = {i};
                '''
            )
            rows = cur.fetchall()
            mass.append("\n"+rows[0][1]+" "+rows[0][2]+" "+rows[0][3])
            
        await bot.send_message(c.message.chat.id, 
            f'На данный момент выбранные сотрудники: {"".join(i for i in mass)}\n\nВведите ФИО сотрудника или завершите процесс выбора.',
            reply_markup=Continue(),
        )
    except KeyError:
        await bot.send_message(c.message.chat.id,
        f'Выберите пользователя:',
        reply_markup=Continue(),
    )
    await CreateMeeting.Worker.set()


# Задаем продолжительность собрания
@dp.callback_query_handler(text="Continue", state='*')
async def Exit_Quiz(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите предполагаемую продолжительность собрания в формате HH:MM', reply_markup=CancelCreate())
    await CreateMeeting.Time.set()


def probraz(h, m, prod):
    t1 = ((h*60)+m)-8*60
    t2 = (((h*60)+m)-8*60) + prod
    mass = []
    for i in range(t1,t2+1):
        mass.append(i)
    return mass


@dp.message_handler(state=CreateMeeting.Time)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Time'] = message.text
        mass = data['MassWork']
        name = data['Name']
        place = data['Place']
        
        Login = data['Login']
        Password = data['Password']

    data = data['Time'].split(":")
    minutes = int(data[0])*60+int(data[1])
    print(minutes)
    print(name)

    d = -1
    stop = 0
    while stop != 1:
        print(d)
        d += 1
        date_now =  datetime.now().date()
        date_step = (datetime.now()+timedelta(days=d)).date()
 

        mass_min = [i for i in range(601)]

        for i in mass:
            con = connect_db()
            cur = con.cursor()
            cur.execute(
                f'''\
                SELECT time_event, duration_event FROM schedule
                INNER JOIN event
                ON schedule.id_event = event.id_event
                WHERE event.date_event = '{date_step}' and schedule.id_worker = {i}
                '''
            )
            rows = cur.fetchall()

            if len(rows) == 0:
                hour = 0
                min = 0
                prod = 0
            else:
                for j in rows:
                    hour = int(j[0].strftime("%H"))
                    min = int(j[0].strftime("%M"))
                    prod = int(j[1])
                    mass_min = list( set(mass_min) - set(probraz(hour, min, prod)))
                    print(hour, min, prod)
            mass_min = list( set(mass_min) - set(probraz(hour, min, prod)))
            

        t = 1
        start = mass_min[0]
        end = -1
        for i in range(1, len(mass_min)):
            if mass_min[i-1] == mass_min[i]-1:
                t+=1
                end = mass_min[i]
            else:
                print(t)
                t = 1
                start = mass_min[i]
                end = 0
            if minutes+16 == t and date_step == date_now:
                startH = 8 + start//60
                startM = 0 + (start+15)%60
                endH = 8 + end//60
                endM = 0 + end%60
            
                stop = 1
                break

            elif minutes+1 == t:
                startH = 8 + start//60
                startM = 0 + start%60
                endH = 8 + end//60
                endM = 0 + end%60

                stop = 1
                break


    con = connect_db()
    cur = con.cursor()
    cur.execute(
             f'''\
             SELECT MAX(id_event) FROM event
             '''
     )
    rows = cur.fetchall()
    print(rows[0][0])
    print(f'{name}')
    print(f'{date_step}')
    print(f'{startH}:{startM}')
    print(f'{minutes}')
    con = connect_db()
    cur = con.cursor()
    cur.execute(
        f'''\
        insert into event values
        ({rows[0][0]+1}, '{name}', '{date_step}', '{startH}:{startM}', {minutes},  '{place}');
        '''
    )    
    con.commit()

    for i in mass:
        cur.execute(
            f'''\
            insert into schedule values
            ({rows[0][0]+1}, {int(i)});
            '''
        )    
        con.commit()
    time_start = datetime.now().strptime(f'{startH}:{startM}', "%H:%M").time()
    time_end = datetime.now().strptime(f'{endH}:{endM}', "%H:%M").time()
    year = int(date_step.strftime("%Y"))
    month = int(date_step.strftime("%m"))
    day = int(date_step.strftime("%d"))
    

    await state.finish()

    async with state.proxy() as data:
        data['Login'] = Login
        data['Password'] = Password

    await message.answer(f'Встреча "{name}" успешна добавлена {day}.{month}.{year} с {time_start} по {time_end}.\nМесто встречи: {place}', reply_markup=Menu())



@dp.callback_query_handler(text=["Auth", "Cancel"], state='*')
async def Exit_Quiz(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text("Введите свой логин:")
    await Form.Login.set()
    await callback.answer()  



@dp.callback_query_handler(text="Future meeting", state='*')
async def Raspisanie(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
       Login =  data['Login']
       Password =  data['Password'] 

    for i in range(3):
        date_step = (datetime.now()+timedelta(days=i)).date()
        con = connect_db()
        cur = con.cursor()
        cur.execute(
                f'''\
                SELECT
                event.event_name,
                event.time_event,
                event.duration_event,
                event.place_event
                FROM worker
                INNER JOIN schedule
                ON schedule.id_worker = worker.id_worker
                INNER JOIN event
                ON schedule.id_event = event.id_event
                WHERE worker.login = '{Login}' and worker.password = '{Password}' and event.date_event = '{date_step}'
                '''
        )
        rows = cur.fetchall()
        print(rows)
        year = int(date_step.strftime("%Y"))
        month = int(date_step.strftime("%m"))
        day = int(date_step.strftime("%d"))
        t = f'{day}.{month}.{year}' + "\n\n"
        tmp = f''
        for j in rows:
            tmp += f'Собрание "{str(j[0])}" с {str(j[1])} продолжительностью {str(j[2])} минут.\nМесто встречи: {str(j[3])}\n\n'
        await callback.message.answer(f'{t}{tmp}')
    await callback.message.answer(f'Меню', reply_markup=Menu())   
        #await callback.message.answer(f"{t}{tabulate(mass, headers=['Имя', 'Начало', 'Продолжительность', 'Место проведения'])}")

@dp.callback_query_handler(text=["Cancel Create"], state='*')
async def Exit_Quiz(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.answer("Введите свой логин:")
    await Form.Login.set()
    await callback.answer()  



async def is_enabled():
    print('запускаю цикл')
    while True:
        con = connect_db()
        cur = con.cursor()
        date = (datetime.now()+timedelta(minutes=15)).date()
        time = ((datetime.now()+timedelta(minutes=15)).time()).strftime("%H, %M")
        print(date)
        print(time[0:2])
        print(time[4:6])
        cur.execute(
                f'''\
                SELECT
                worker.id_tg,
                event.event_name,
                event.place_event,
                worker.name_worker,
                worker.otch_worker
                FROM worker
                INNER JOIN schedule
                ON schedule.id_worker = worker.id_worker
                INNER JOIN event
                ON schedule.id_event = event.id_event
                WHERE event.date_event = '{date}' and event.time_event = '{time[0:2]}:{time[4:6]}'
                '''
        )
        rows = cur.fetchall()
        print(rows)
        for user_id in rows:
            await bot.send_message(chat_id=user_id[0], text=f'{user_id[3]} {user_id[4]}, через 15 минут у вас состоится собрание "{user_id[1]}"\nМесто проведения: {user_id[2]}\nПожалуйста, не опаздывайте')
            print('отправил')
        print('жду')
        await asyncio.sleep(60)

async def on_startup(x):
  asyncio.create_task(is_enabled())

if __name__ == '__main__':
    executor.start_polling(dp ,skip_updates=True, on_startup=on_startup)
