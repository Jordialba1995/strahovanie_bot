from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


from text import *


def row_keyboard(items: list[str]):
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], input_field_placeholder='/start', resize_keyboard=True)


def services_kb():
    row1 = [KeyboardButton(text=list_services[0]), KeyboardButton(text=list_services[1])]
    row2 = [KeyboardButton(text=list_services[2]), KeyboardButton(text=list_services[3])]
    row3 = [KeyboardButton(text=list_services[4]), KeyboardButton(text=list_services[5])]
    row4 = [KeyboardButton(text=list_services[6]), KeyboardButton(text=list_services[7])]
    row5 = [KeyboardButton(text='Вернуться')]
    return ReplyKeyboardMarkup(keyboard=[row1, row2, row3, row4, row5], resize_keyboard=True)
