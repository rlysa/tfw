from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


buttons = [
    [KeyboardButton(text='Стажеры'), KeyboardButton(text='Группы')],
    [KeyboardButton(text='Задачи'), KeyboardButton(text='Профиль')]
]
admin_keyboard = ReplyKeyboardMarkup(keyboard=buttons,
                                     resize_keyboard=True,
                                     one_time_keyboard=True)

tasks_buttons = [
    [KeyboardButton(text='Создать задачу'), KeyboardButton(text='Посмотреть задачи')],
    # [KeyboardButton(text='Изменить задачу'), KeyboardButton(text='Удалить задачу')],
    [KeyboardButton(text='Меню команд')]
]
tasks_keyboard = ReplyKeyboardMarkup(keyboard=tasks_buttons,
                                     resize_keyboard=True,
                                     one_time_keyboard=True)

group_buttons = [
    [KeyboardButton(text='Создать группу'), KeyboardButton(text='Посмотреть группы')],
    # [KeyboardButton(text='Изменить группу'), KeyboardButton(text='Удалить группу')],
    [KeyboardButton(text='Меню команд')]
]
group_keyboard = ReplyKeyboardMarkup(keyboard=group_buttons,
                                     resize_keyboard=True,
                                     one_time_keyboard=True)

interns_buttons = [
    [KeyboardButton(text='Посмотреть список'), KeyboardButton(text='Поиск по скиллам')],
    [KeyboardButton(text='Отправить сообщение стажеру')],
    # [KeyboardButton(text='Изменить группу'), KeyboardButton(text='Удалить группу')],
    [KeyboardButton(text='Меню команд')]]
interns_keyboard = ReplyKeyboardMarkup(keyboard=interns_buttons,
                                     resize_keyboard=True,
                                     one_time_keyboard=True)

