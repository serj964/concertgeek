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
TEXT = "(если ты еще не отправлял мне свой плейлист - напиши /start, если хочешь перейти в основное меню - напиши /menu)"

def make_keyboard(d):
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    for i in d.keys():
        buttons.append(types.InlineKeyboardButton(text=d[i][0], callback_data=i))
    keyboard.add(*buttons)
    return keyboard

'''
def menu_analyze_proc(message):
    text = "Выбери действие среди предложенных:"
    bot.send_message(message.chat.id, text=text, reply_markup=make_keyboard(menu_analyze))
    bot.register_next_step_handler(message, menu_analize_keyboard_handler)
    return'''


def change_service():
    return 1


def menu_manage_list_proc(message):
    bot.send_message(message.chat.id, text = "хайп")

'''
def menu_send_concerts_proc():
    return 1'''


def menu_reset_proc(message):
    bot.send_message(message.chat.id, text = "хайп")


def menu_analyze_spotify_proc():
    bot.send_message(message.from_user.id, text = "хайп")


def menu_analyze_vk_proc():
    bot.send_message(message.from_user.id, text = "хайп")


def menu_change_service_proc(message):
    txt = "хайп"
    bot.send_message(message.from_user.id, text = txt, reply_markup=make_keyboard(menu_change_service))


def menu_startup_vk_proc(message):
    bot.send_message(message.chat.id, "Для работы сервиса необходимо, чтобы у тебя был открытый аккаунт и открытые аудио!")
    time.sleep(3)
    bot.send_message(message.chat.id, text = "Перейди, пожалуйста, по ссылке для авторизации: "+address+"?&tg_id="+str(message.from_user.id)+"&scope=vk")
    #bot.register_next_step_handler(message, get_vk_id)
    

def menu_startup_spotify_proc(message):
    #bot.send_message(message.chat.id, "Для работы сервиса необходимо, чтобы у вас был открытый аккаунт и открытые аудио")
    #bot.send_message(message.chat.id, text = "Перейдите, пожалуйста, по ссылке для авторизации. "+address+"?&tg_id="+str(message.from_user.id)+"&scope=vk")
    #bot.register_next_step_handler(message, get_vk_id)
    bot.send_message(message.chat.id, text = "ХАЙп")
    

def menu_abort_proc(message):
    text1 = "Тогда я просто побуду у тебя в телефоне)\n\n"
    bot.send_message(message.chat.id, text = text1+TEXT)

def menu_startup_abort_proc(message):
    text1 = "Тогда я просто побуду у тебя в телефоне)\n\n"
    bot.send_message(message.chat.id, text = text1+TEXT)
    #bot.register_next_step_handler(message, talk)
    

menu_change_service = {
    'btn_menu_analize_vk' : ('Vk', menu_analyze_vk_proc),
    'btn_menu_analize_spotify' : ('Spotify', menu_analyze_spotify_proc)
}


menu = {
    'btn_menu_change_service' : ('Другой сервис', menu_change_service_proc), 
    'btn_menu_manage_list' : ('Обновить музыку', menu_manage_list_proc),
    #'btn_menu_send_concerts' : ('Прислать рекомендованные концерты', menu_send_concerts_proc),
    'btn_menu_reset' : ('Стереть', menu_reset_proc),
    'btn_menu_abort' : ('Выберу потом', menu_abort_proc)
}


menu_startup = {
    'btn_menu_startup_vk' : ('Vk', menu_startup_vk_proc),
    'btn_menu_startup_spotify' : ('Spotify', menu_startup_spotify_proc),
    'btn_menu_startup_abort' : ('Выберу потом', menu_startup_abort_proc)
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    text1 = "Привет, я MusicGEEKbot. Приятно познакомиться)\nЯ помогу тебе не пропустить концерт или любое другое мероприятие любимых исполнителей.\n\n"
    text2 = "Для работы нашего сервиса необходимо проанализировать твою медиатеку, поэтому выбери подходящий вариант\n\n"
    #text3 = если хочешь перейти в основное меню - напиши /menu
    bot.send_message(message.from_user.id, text = text1+text2, reply_markup=make_keyboard(menu_startup))
    #bot.register_next_step_handler(message, menu_startup_keyboard_handler)


@bot.message_handler(commands=['menu'])
def handle_menu(message):
    text1 = "Это основное меню!\n\n"
    text2 = "Если у тебя появился новый стриминговый сервис и ты хочешь, чтобы я его проанализировал, нажми ДРУГОЙ СЕРВИС\n\n"
    text3 = "Если твои вкусы изменились, ты добавил много нового и хочешь, чтобы я это учел, нажми ОБНОВИТЬ МУЗЫКУ\n\n"
    text4 = "Если хочешь, чтобы твои данные были стерты, нажми СТЕРЕТЬ\n\n"
    text5 = "(если ты еще не отправлял мне свой плейлист, напиши /start)"
    bot.send_message(message.from_user.id, text=text1+text2+text3+text4+text5, reply_markup=make_keyboard(menu))
    #bot.register_next_step_handler(message, menu_keyboard_handler)


@bot.message_handler(content_types = ["text", "sticker", "pinned_message", "photo", "audio"])
def talk(message):
    text1 = "Мы могли бы пообщаться, но, к сожалению, пока что я умею отвечать только привет)\n"
    text2 = "Однако скоро мой создатель научит меня еще чему-нибудь)\n\n"
    bot.send_message(message.from_user.id, text=text1+text2+TEXT)
    #bot.register_next_step_handler(message, menu_keyboard_handler)

        
@bot.callback_query_handler(func=lambda call: type(call) == types.CallbackQuery and call.data in menu.keys())
def menu_keyboard_handler(call):
    btn = call.data
    print(btn)
    if menu.get(btn) != None:
        print('ok')
        menu[btn][1](call.message)


@bot.callback_query_handler(func=lambda call: type(call) == types.CallbackQuery and call.data in menu_startup.keys())
def menu_startup_keyboard_handler(call):
    #print((lambda call: type(call) == types.CallbackQuery and call.data in menu_startup.keys())(call))
    btn = call.data
    print(btn)
    if menu_startup.get(btn) != None:
        print('ok')
        menu_startup[btn][1](call.message)

     
@bot.callback_query_handler(func=lambda call: type(call) == types.CallbackQuery and call.data in menu_change_service.keys())
def menu_change_service_keyboard_handler(call):
    btn = call.data
    print(btn)
    if menu_change_service.get(btn) != None:
        print('ok')
        menu_change_service[btn][1](call.message)

   
def get_vk_id(message):
    vk_id = message.text
    print(message.from_user.id, vk_id) #add this pair to db
    vk = vk_music_analyzer()
    bot.send_message(message.from_user.id, text = "Подожди, пока я подберу для тебя концерты)")
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
