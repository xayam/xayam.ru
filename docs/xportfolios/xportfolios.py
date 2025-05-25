# coding: utf-8

from __init__ import *

import os.path
import re

import telebot
from telebot import types


bot = telebot.TeleBot(TELEGRAM_BOT_API_KEY)

def command_html():
    pass

def command_pdf():
    pass


def menu_execute(command, message):
    try:
        data_file = os.getcwd() + "/xportfolios/" + command[1:] + ".html"
        print(data_file)
        info = "В базе бота отсутствует информация по данной команде."
        if os.path.exists(data_file):
            with open(data_file, mode="r", encoding="UTF-8") as f:
                info = f.read()
    except KeyError:
        info = "Ошибка. Команда не корректна. Выберите правильную команду в меню."
    info += "\n\n/menu"
    bot.send_message(
        chat_id=message.chat.id,
        text=info,
        parse_mode="HTML",
    )

commands = {
    "/projects": { "handler": menu_execute, "name": "Проекты"},
    "/links": { "handler": menu_execute, "name": "Ссылки"},
    "/skills": { "handler": menu_execute, "name": "Навыки"},
    "/tools": { "handler": menu_execute, "name": "Инструменты"},
    "/education": { "handler": menu_execute, "name": "Образование"},
    "/experience": { "handler": menu_execute, "name": "Опыт работы"},
    "/interests": { "handler": menu_execute, "name": "Интересы"},
    "/disease": { "handler": menu_execute, "name": "Болезнь"},
    "/autobiography": { "handler": menu_execute, "name": "Автобиография"},
    "/status": { "handler": menu_execute, "name": "Статус"},
    "/html": { "handler": command_html, "name": "HTML"},
    "/pdf": { "handler": command_pdf, "name": "PDF"},
}

def menu_create() -> types.InlineKeyboardMarkup:
    btn_list = dict()
    for command in commands:
        btn_list[commands[command]["name"]] = command
    menu = []
    row = []
    for element in btn_list.items():
        btn = types.InlineKeyboardButton(
            text=element[0], callback_data=element[1],
        )
        row.append(btn)
        if len(row) == 2:
            menu.append(row)
            row = []
    return types.InlineKeyboardMarkup(menu)

@bot.message_handler(commands=["start", "menu"])
def start(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Выберите нужный пункт меню...",
        reply_markup=menu_create()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    commands[call.data]["handler"](command=call.data, message=call.message)


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print("ERROR 1000: " + str(type(e)) + " / " + e.__str__())
