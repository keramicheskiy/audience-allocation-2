from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReactionTypeEmoji
from urllib3 import request

import services
from settings import *
import telebot
import os
import requests

from text_messages import *

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    token = services.get_token(user_id)
    if not token:
        bot.reply_to(message, basic_start_message)
        return
    response = requests.get(url=BACKEND_URL + "/authentication/verify-token", cookies={"Token": token})
    if response.status_code == 200:
        role = response.json()["role"]
        if role == "teacher":
            bot.reply_to(message, teacher_start_message)
            return
        elif role == "moderator":
            bot.reply_to(message, moderator_start_message)
            return
    bot.reply_to(message, f"Ошибка {response.status_code}")


@bot.message_handler(commands=['register'])
def register(message):
    bot.reply_to(message, 'Дароу')


@bot.message_handler(commands=['login'])
def send_welcome(message):
    bot.reply_to(message, 'Дароу')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Дароу')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Дароу')


@bot.message_handler()
def text_handler(message):
    pass


if __name__ == "__main__":
    print("Бот запущен...")
    services.create_table()
    # bot.add_edited_message_handler({
    #     'callback': handle_edited_message,
    # })
    bot.polling(none_stop=True)
