import telebot
from telebot import types
import logging
import random




TOKEN = '1634504684:AAEk4wzUCsI_ZNdohfYZGy2jakWFFkfdeTs'

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Я MUSICGEEK бот. Приятно познакомиться. Я помогу тебе не пропустить концерт или любое другое мероприятие любимой группы.')

@bot.message_handler(content_types = ["text", "sticker", "pinned_message", "photo", "audio"])
def handle_message(message):
    txt = "Желаешь ли ты, чтобы наш бот проанализировал твою медиатеку ВК?"
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_vk_analyze'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    bot.send_message(message.from_user.id, text = txt, reply_markup = keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes_vk_analyze":
        url = "http://localhost:8000/auth?tg_id="+str(call.from_user.id)
        bot.send_message(call.from_user.id, text = url)
        print("YES\n")
        
    




#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

bot.polling(none_stop=True)
