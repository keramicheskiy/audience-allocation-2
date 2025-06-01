from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReactionTypeEmoji, InlineKeyboardMarkup, \
    InlineKeyboardButton
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
    markup = InlineKeyboardMarkup()
    url = "https://krmch.ru/"
    markup.add(InlineKeyboardButton("Открыть мини-приложение", url=url))

    bot.send_message(
        message.chat.id,
        "Нажмите на кнопку ниже, чтобы открыть мини-приложение.",
        reply_markup=markup
    )


if __name__ == "__main__":
    print("Бот запущен...")
    services.create_table()

    bot.polling(none_stop=True)
