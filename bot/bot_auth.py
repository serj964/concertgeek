import telebot
from telebot import types
import logging
import random




TOKEN = '1682871069:AAHM5exgvsRaA5qmvZoU8SaCXr2Y_CeRSfM'

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    hash = message.text.split()[1]
    print(hash)
    bot.reply_to(message, f'Я MUSICGEEK бот авторизации. Вы успешно авторизовались!')

#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

bot.polling(none_stop=True)
