# coding: utf-8

import json
import os.path
import re

import telebot
import model

from __init__ import *


bot = telebot.TeleBot(TELEGRAM_BOT_API_KEY)
m = model.Model()
limit = 22
replies_folder = os.getcwd() + "/absolaris"
if not os.path.exists(replies_folder):
    os.mkdir(replies_folder)

def escape_markdown(text):
    replace_chars = '_*[]()~`>#+-=|{}.!'
    for char in replace_chars:
        text = text.replace(char, '\\' + char)
    return text

def simple_format(text):
    jobs = [
        (r"\<think\>.*?\<\/think\>", r""),
        (r"\<think\>", r""),
        (r"\<\/think\>", r""),
        (r"\<", r"&lt;"),
        (r"\>", r"&gt;"),
        (r"\*\*(.*?)\*\*", r"<b>\1</b>"),
        (r"\*(.*?)\*", r"<i>\1</i>"),
    ]
    for task in jobs:
        pattern, replacement = task
        text = re.sub(pattern, replacement, text, flags=re.DOTALL)
    return text

def build_conversation_chain(message, limit=500):
    chain = []
    current = message
    count = 0
    while current.reply_to_message is not None:
        chain.append(current.reply_to_message)
        current = current.reply_to_message
        count += 1
        if count >= limit:
            break
    chain.reverse()
    return chain

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    answer = ""
    try:
        print("Input message | " + message.text)
        replies_file = replies_folder + "/" + str(message.from_user.id) + ".json"
        replies = []
        if (message.text == "/start") or (message.text == "/clear"):
            if os.path.exists(replies_file):
                os.remove(replies_file)
            bot.send_message(
                chat_id=message.chat.id,
                text="<b>История очищена.</b> Начните диалог с Абсолярисом заново. Океан ждет...",
                parse_mode="HTML",
                reply_to_message_id=message.message_id,
                allow_sending_without_reply=False,
            )
            return
        if os.path.exists(replies_file):
            with open(replies_file, mode="r", encoding="UTF-8") as f:
                replies = json.load(f)
        messages = replies + [
            {"role": "user", "content": message.text}
        ]
        print("Messages | " + str(messages))
        print("Processing... | Генерирую ответ")
        answer = m.prompt(messages)
        replies.append(
            {"role": "user", "content": message.text}
        )
        replies.append({"role": "assistant", "content": answer})
        if len(replies) > limit:
            replies = replies[2:]
        with open(replies_file, mode="w", encoding="UTF-8") as f:
            json.dump(replies, f, ensure_ascii=False, indent=4)

        answer = simple_format(answer)
    except Exception as e:
        error = "ERROR 1101 | " + str(type(e)) + " / " + e.__str__()
        print(error)
        bot.send_message(
            chat_id=message.chat.id,
            text=error,
            reply_to_message_id=message.message_id,
            allow_sending_without_reply=False,
        )
    bot.send_message(
        chat_id=message.chat.id,
        text=answer,
        parse_mode="HTML",
        reply_to_message_id=message.message_id,
        allow_sending_without_reply=False,
    )
    print("Answer | Ответ отослан пользователю " + str(message.from_user.id))

if __name__ == '__main__':
    try:
        bot.polling()
    except telebot.apihelper.ApiTelegramException as e1:
        print("ERROR 1001 | " + str(type(e1)) + " / " + e1.__str__())
    except Exception as e2:
        print("ERROR 1002 | " + str(type(e2)) + " / " + e2.__str__())
