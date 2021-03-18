import telebot
from telebot import types
import logging
import random
from Music_analyzer.vk_music_analyzer import vk_music_analyzer



TOKEN = '1634504684:AAEk4wzUCsI_ZNdohfYZGy2jakWFFkfdeTs'

bot = telebot.TeleBot(TOKEN)

address = "127.0.0.1:8000/auth"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Я MUSICGEEK бот. Приятно познакомиться. Я помогу тебе не пропустить концерт или любое другое мероприятие любимой группы.')

@bot.message_handler(content_types = ["text", "sticker", "pinned_message", "photo", "audio"])
def handle_message(message):
    txt = "Желаешь ли ты, чтобы наш бот проанализировал твою медиатеку ВК?/yes, /no"
    bot.send_message(message.from_user.id, text = txt)
    bot.register_next_step_handler(message, callback_worker)
    
@bot.message_handler(content_types = ['text'])
def callback_worker(message):
    if message.text == '/yes':
        bot.send_message(message.from_user.id, text = "Введите, пожалуйста, Ваш id вк")
        bot.register_next_step_handler(message, get_vk_id)
        
def get_vk_id(message):
    vk_id = message.text
    print(message.from_user.id, vk_id) #add this pair to db
    vk = vk_music_analyzer()
    answer = vk.get_favourite_artists(vk_id)
    




#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

bot.polling(none_stop=True)
