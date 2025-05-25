# coding: utf-8

from __init__ import *

import os.path
import re

import telebot
from telebot import types


bot = telebot.TeleBot(TELEGRAM_BOT_API_KEY)


def command_start(command="/start", message=None):
    pass

def command_html(command="/html", message=None):
    pass

def command_pdf(command="/pdf", message=None):
    pass


def menu_execute(command, message):
    try:
        data_file = os.getcwd() + "/" + command.text[1:] + ".html"
        print(data_file)
        info = "В базе бота отсутствует информация по данной команде."
        if os.path.exists(data_file):
            with open(data_file, mode="r", encoding="UTF-8") as f:
                info = f.read()
    except KeyError:
        info = "Ошибка. Команда не корректна. Выберите правильную команду в меню."
    bot.send_message(
        chat_id=message.chat.id,
        text=info,
        parse_mode="HTML",
        reply_to_message_id=message.message_id,
        allow_sending_without_reply=False,
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

def menu_create(message) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    btn_list = dict()
    for command in commands:
        btn_list[commands[command]["name"]] = \
            lambda: commands[command]["handler"](command, message)
    for element in btn_list.items():
        btn = types.InlineKeyboardButton(text=element[0], callback_data=element[1])
        markup.add(btn)
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Добро пожаловать.",
        reply_markup=menu_create(message)
    )


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print("ERROR 1000: " + str(type(e)) + " / " + e.__str__())
