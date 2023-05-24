import logging
import os
from datetime import datetime
from logging import handlers
import time
import requests

import telebot
from telebot import types
from telebot.types import User
from dotenv import dotenv_values

from answer_service.answer_service import get_answer

config = dotenv_values("./bot/env/.env")
bot = telebot.TeleBot(config.get("TG_BOT_TOKEN"))


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет исследователь, я на связи. Задавай свой вопрос ...')


@bot.message_handler(commands=["info"])
def info(message):
    info_message_handle(message)


@bot.message_handler(commands=["question"])
def question(message):
    bot.send_message(message.chat.id, 'Задавате вопрос ...')


def info_message_handle(message):
    bot.send_message(message.chat.id, f'''👋 Здравствуйте {get_user_name(message.from_user)}!
Вас приветствует бот которому Вы можете задать вопрос на историческую тематику по материалам КФФД.''')

@bot.message_handler(content_types=['text'])
def find_answer(message):
    bot.send_message(message.chat.id, 'Спасибо за Ваш вопрос, начал искать ответ, пожалуйста, подождите ...')
    bot.send_message(message.chat.id, f'Вот что мне удалось найти:\n{get_answer(message.text)}')


def get_user_name(user: User) -> str:
    if user is None:
        return ''

    if user.last_name != '' or user.first_name != '':
        return f'{user.first_name} {user.last_name}'.strip()

    if user.username is not None:
        return user.username


def main():
    try:
        logging.info("Я запустился :)")

        bot.polling(none_stop=True, interval=0, timeout=60)
    except Exception as e:
        logging.error(f'Bot pooling exception - main function \n {e}')
        exit(1)


if __name__ == '__main__':
    main()