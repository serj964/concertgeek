import telebot
import time
from telebot import types
import logging
import random
#from Music_analyzer.vk_music_analyzer import vk_music_analyzer
#from Concerts.yandex_afisha_concerts import Concerts

TOKEN = '1787836132:AAE6ZA6psgjHfEM5nSP9Ti5ya2AWwuIKJl8'

bot = telebot.TeleBot(TOKEN)

address = "127.0.0.1:8000/auth"

def make_keyboard(d):
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    for i in d.keys():
        buttons.append(types.InlineKeyboardButton(text=d[i][0], callback_data=i))
    keyboard.add(*buttons)
    return keyboard

def menu_analize_proc(message):
    text = "Выбери действие среди предложенных:"
    bot.send_message(message.chat.id, text=text, reply_markup=make_keyboard(menu_analize))
    bot.register_next_step_handler(message, menu_analize_keyboard_handler)
    return

def menu_manage_list_proc():
    return 1

def menu_send_concerts_proc():
    return 1

def menu_reset_proc():
    return 1

def menu_analize_spotify_proc():
    return 1

def menu_analize_vk_proc():
    return 1


menu_analize = {
    'btn_menu_analize_vk' : ('Проанализировать медиатеку Vk', menu_analize_vk_proc),
    'btn_menu_analize_spotify' : ('Проанализировать медиатеку Spotify', menu_analize_spotify_proc)
}

menu = {
    'btn_menu_analize' : ('Проанализировать медиатеку', menu_analize_proc), 
    'btn_menu_manage_list' : ('Конфигурировать список любимых исполнителей', menu_manage_list_proc),
    'btn_menu_send_concerts' : ('Прислать рекомендованные концерты', menu_send_concerts_proc),
    'btn_menu_reset' : ('Стереть данные', menu_reset_proc)
}




@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Я MUSICGEEK бот. Приятно познакомиться. Я помогу тебе не пропустить концерт или любое другое мероприятие любимой группы. Напиши любое сообщение боту в любое время и он тебе пришлет варианты взаимодействия.')


@bot.message_handler(content_types = ["text", "sticker", "pinned_message", "photo", "audio"])
def handle_menu(message):
    text = "Выбери действие среди предложенных:"
    bot.send_message(message.from_user.id, text=text, reply_markup=make_keyboard(menu))
    bot.register_next_step_handler(message, menu_keyboard_handler)
    return


@bot.message_handler(content_types = ['text'])
def callback_worker(message):
    if message.text == '/yes':
        bot.send_message(message.from_user.id, text = "Перейдите, пожалуйста, по ссылке для авторизации. "+address+"?&tg_id="+str(message.from_user.id))
        #bot.register_next_step_handler(message, get_vk_id)
        
@bot.callback_query_handler(func=lambda call: True)
def menu_keyboard_handler(call):
    btn = call.data
    print(btn)
    if menu.get(btn) != None:
        print('ok')
        menu[btn][1](call.message)

@bot.callback_query_handler(func=lambda call: True)
def menu_analize_keyboard_handler(call):
    btn = call.data
    print(btn)
    #if menu.get(btn) != None:
    #    print('ok')
    #    menu[btn][1](call.message)

"""        
def get_vk_id(message):
    vk_id = message.text
    print(message.from_user.id, vk_id) #add this pair to db
    bot.send_message(message.from_user.id, text = "Подожди, пока я подберу для тебя концерты)")
    vk = vk_music_analyzer()
    artists = vk.get_favourite_artists(vk_id)
    #print(answer)
    #bot.send_message(message.from_user.id, answer)
    con = Concerts()
    con.load_concerts()
    bot.send_message(message.from_user.id, text = "Вот, что мне удалось найти)")
    for i in range(len(artists)):
        concert = con.find_concerts(artists[i])
        if concert != []:
            txt = "Концерт группы {title}\nОн пройдет {date}\nВот ссылка на мероприятие {url}".format(title = concert[0]['title'], date = concert[0]['date'], url = concert[0]['url'])
            bot.send_message(message.from_user.id, text=txt)
            time.sleep(10)
            
    bot.send_message(message.from_user.id, text = "Наслаждайся)")
        
        
"""    




#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

bot.polling(none_stop=True)
