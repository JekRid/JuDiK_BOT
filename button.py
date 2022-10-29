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