# coding: utf-8

from __init__ import *

import json
import os.path
import re

import telebot

bot = telebot.TeleBot(TELEGRAM_BOT_API_KEY)


# bot.send_message(
#             chat_id=message.chat.id,
#             text="<b>История очищена.</b> Начните диалог с Абсолярисом заново. Океан ждет...",
#             parse_mode="HTML",
#             reply_to_message_id=message.message_id,
#             allow_sending_without_reply=False,
#         )

def command_start(message, data):
    pass

def command_projects(message, data):
    pass

def command_links(message, data):
    pass

def command_skills(message, data):
    pass

def command_tools(message, data):
    pass

def command_education(message, data):
    pass

def command_experience(message, data):
    pass

def command_interests(message, data):
    pass

def command_disease(message, data):
    pass

def command_autobiography(message, data):
    pass

def command_status(message, data):
    pass

def command_html(message, data):
    pass

def command_pdf(message, data):
    pass

commands = {
    "/start": { "handler": command_start, "name": "Старт", "view": False, },
    "/projects": { "handler": command_projects, "name": "Проекты", "view": True, },
    "/links": { "handler": command_links, "name": "Ссылки", "view": True, },
    "/skills": { "handler": command_skills, "name": "Навыки", "view": True, },
    "/tools": { "handler": command_tools, "name": "Инструменты", "view": True, },
    "/education": { "handler": command_education, "name": "Образование", "view": True, },
    "/experience": { "handler": command_experience, "name": "Опыт работы", "view": True, },
    "/interests": { "handler": command_interests, "name": "Интересы", "view": True, },
    "/disease": { "handler": command_disease, "name": "Болезнь", "view": True, },
    "/autobiography": { "handler": command_autobiography, "name": "Автобиография", "view": True, },
    "/status": { "handler": command_status, "name": "Статус", "view": True, },
    "/html": { "handler": command_html, "name": "HTML", "view": True, },
    "/pdf": { "handler": command_pdf, "name": "PDF", "view": True, },
}

@bot.message_handler(content_types=['text'])
def process_commands(message):
    try:
        data_file = "xportfolio/" + message.text[1:] + ".html"
        if os.path.exists(data_file):
            with open(data_file, mode="r", encoding="UTF-8") as f:
                data = f.read()
            info = commands[message.text](message=message, data=data)
    except KeyError:
        info = "Ошибка. Команда не распознана. Выберите корректную команду в меню."
    bot.send_message(
        chat_id=message.chat.id,
        text=info,
        parse_mode="HTML",
        reply_to_message_id=message.message_id,
        allow_sending_without_reply=False,
    )


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print("ERROR 1000: " + str(type(e)) + " / " + e.__str__())
