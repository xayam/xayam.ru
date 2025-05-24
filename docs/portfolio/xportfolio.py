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

def command_start(message):
    pass

def command_projects(message):
    pass

def command_links(message):
    pass

def command_skills(message):
    pass

def command_tools(message):
    pass

def command_education(message):
    pass

def command_experience(message):
    pass

def command_interests(message):
    pass

def command_disease(message):
    pass

def command_autobiography(message):
    pass

def command_status(message):
    pass

def command_html(message):
    pass

def command_pdf(message):
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
    commands[message.text](message)


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print("ERROR 1000: " + str(type(e)) + " / " + e.__str__())
