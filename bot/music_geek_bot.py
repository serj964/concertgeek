import telebot
import time
from telebot import types
import logging
#import random
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

def menu_analyze_proc(message):
    text = "Выбери действие среди предложенных:"
    bot.send_message(message.chat.id, text=text, reply_markup=make_keyboard(menu_analyze))
    bot.register_next_step_handler(message, menu_analize_keyboard_handler)
    return

def change_service():
    return 1

def menu_manage_list_proc():
    return 1

def menu_send_concerts_proc():
    return 1

def menu_reset_proc():
    return 1

def menu_analyze_spotify_proc():
    return 1

def menu_analyze_vk_proc():
    return 1

def menu_startup_vk_proc(message):
    bot.send_message(message.chat.id, "Для работы сервиса необходимо, чтобы у тебя был открытый аккаунт и открытые аудио!")
    time.sleep(3)
    bot.send_message(message.chat.id, text = "Перейди, пожалуйста, по ссылке для авторизации: "+address+"?&tg_id="+str(message.from_user.id)+"&scope=vk")
    #bot.register_next_step_handler(message, get_vk_id)
    return 1

def menu_startup_spotify_proc(message):
    #bot.send_message(message.chat.id, "Для работы сервиса необходимо, чтобы у вас был открытый аккаунт и открытые аудио")
    #bot.send_message(message.chat.id, text = "Перейдите, пожалуйста, по ссылке для авторизации. "+address+"?&tg_id="+str(message.from_user.id)+"&scope=vk")
    #bot.register_next_step_handler(message, get_vk_id)
    bot.send_message(message.chat.id, text = "ХАЙп")
    return 1

def menu_startup_abort(message):
    bot.send_message(message.chat.id, text = "Тогда я просто побуду у тебя в телефоне)\nПиши, если вдруг надумаешь)")
    bot.register_next_step_handler(message, talk)
    return 1


change_service = {
    'btn_menu_analize_vk' : ('Vk', menu_startup_vk_proc),
    'btn_menu_analize_spotify' : ('Spotify', menu_startup_spotify_proc)
}

handle_menu = {
    'btn_menu_analize' : ('Выбрать другой сервис', change_service), 
    'btn_menu_manage_list' : ('Обновить музыкальные предпочтения', menu_manage_list_proc),
    #'btn_menu_send_concerts' : ('Прислать рекомендованные концерты', menu_send_concerts_proc),
    'btn_menu_reset' : ('Стереть данные', menu_reset_proc)
}

startup_menu = {
    'btn_menu_startup_vk' : ('Vk', menu_startup_vk_proc),
    'btn_menu_startup_spotify' : ('Spotify', menu_startup_spotify_proc),
    'btn_menu_startup_abort' : ('Выберу потом', menu_startup_abort)
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "Привет, я MusicGEEKbot. Приятно познакомиться)\nЯ помогу тебе не пропустить концерт или любое другое мероприятие любимых групп.\n\nДля работы нашего сервиса необходимо проанализировать твою медиатеку. Выбери подходящий вариант:"
    bot.send_message(message.from_user.id, text = text, reply_markup=make_keyboard(startup_menu))
    bot.register_next_step_handler(message, menu_startup_keyboard_handler)
    return


@bot.callback_query_handler(func=lambda call: True)
def menu_startup_keyboard_handler(call):
    try:
        btn = call.data
        print(btn)
        if startup_menu.get(btn) != None:
            print('ok')
            startup_menu[btn][1](call.message)
    except AttributeError:
        pass
        
    

@bot.message_handler(content_types = ["text", "sticker", "pinned_message", "photo", "audio"])
def talk(message):
    text = "Можем пообщаться\nА если хочешь перейти в меню, напиши мне /menu"
    #bot.send_message(message.from_user.id, text=text, reply_markup=make_keyboard(menu))
    #bot.register_next_step_handler(message, menu_keyboard_handler)
    return

'''
@bot.callback_query_handler(func=lambda call: True)
def menu_startup_keyboard_handler(call):
    btn = call.data
    print(btn)
    if startup_menu.get(btn) != None:
        print('ok')
        startup_menu[btn][1](call.message)'''


@bot.message_handler(commands=['menu'])
def handle_menu(message):
    text = "Выбери действие среди предложенных:"
    bot.send_message(message.from_user.id, text=text, reply_markup=make_keyboard(handle_menu))
    bot.register_next_step_handler(message, menu_keyboard_handler)
    return
     
'''
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
    #    menu[btn][1](call.message)'''

   
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
          



#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

bot.polling(none_stop=True)
