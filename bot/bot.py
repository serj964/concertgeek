import telebot
from telebot import types
import logging



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


grant_type = "client_credentials"
client_id = "7562746"
redirect_url = "http://localhost:8000"
v = "5.130"
basic_url = "https://oauth.vk.com/authorize"
url = basic_url+"?client_id="+client_id+"&v="+v+"&redirect_uri="+redirect_url+"&grant_type="+grant_type

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes_vk_analyze":
        bot.send_message(call.from_user.id, text = url)
        print("YES\n")
        
    




#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

bot.polling(none_stop=True)
