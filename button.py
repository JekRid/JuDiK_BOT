from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

def Start():
    buttons = [
        [
            types.InlineKeyboardButton(text="Меню", callback_data="menu"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def Auth():
    buttons = [
        [
            types.InlineKeyboardButton(text="Попробовать снова", callback_data="Auth"),
        ],

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def CancelCreate():
    buttons = [
        [
            types.InlineKeyboardButton(text="Прервать сессию", callback_data="Cancel Create"),
        ],

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def Menu():
    buttons = [
        [
            types.InlineKeyboardButton(text="Назначить собрание", callback_data="Create meeting"),
        ],
        [
            types.InlineKeyboardButton(text="Предстоящие события", callback_data="Future meeting"),
        ],
        [
            types.InlineKeyboardButton(text="Выход", callback_data="Cancel"),
        ],

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def Continue():
    buttons = [
        [
            types.InlineKeyboardButton(text="Завершить", callback_data="Continue"),
        ],


    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

'''
def Menu():
    buttons = [
        [
            types.InlineKeyboardButton(text="Пройти опрос", callback_data="go_quiz"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard




def Next_step():
    buttons = [
        [
            types.InlineKeyboardButton(text="Пройти опрос", callback_data="Next"),
        ],
        [
            types.InlineKeyboardButton(text="Вернуться", callback_data="Close"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def Next_ques():
    buttons = [
        [
            types.InlineKeyboardButton(text="Следующий вопрос", callback_data="Next"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def End():
    buttons = [
        [
            types.InlineKeyboardButton(text="Завершить опрос", callback_data="end"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard







    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, one_time_keyboard=True)
    '''