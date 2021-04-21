import telebot
import time
from telebot import types
import logging
from pymongo import MongoClient
from Music_analyzer.vk_music_analyzer import Vk_music_analyzer
from Music_analyzer.spotify_music_analyzer import Spotify_music_analyzer
from Concerts.yandex_afisha_concerts import Concerts
from bot.city_slovar import City_slovar
import json


class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)


CONFIG_FILE = './bot/config.json'

with open(CONFIG_FILE) as conf:
    config = json.load(conf)

bot_config = config['bot_config']
oauth_config = config["oauth_config"]
server_config = config["server_config"]
db_config = config["db_config"]

client = MongoClient(db_config['address'], db_config['port'])
db = client[db_config['name']]
vk_collection = db[db_config['collections']['vk_collection']]
spotify_collection = db[db_config['collections']['spotify_collection']]

vk_oauth_config = oauth_config['vk_oauth_config']
spotify_oauth_config = oauth_config['spotify_oauth_config']




TOKEN = bot_config['token']
bot = telebot.TeleBot(TOKEN)

vk_oauth_url = vk_oauth_config['redirect_url_base']+vk_oauth_config['oauth_startpoint']
spotify_oauth_url = spotify_oauth_config['redirect_url_base']+spotify_oauth_config['oauth_startpoint']

#TEXT = "(если ты еще не отправлял мне свой плейлист - напиши /start, если хочешь перейти в основное меню - напиши /menu)"
TEXT = "(если ты еще не отправлял мне свой плейлист - напиши /start)"

def get_vk_id_from_db(tg_id):
    res = vk_collection.find_one({'_id' : tg_id})
    if res != None:
        vk_collection.delete_one({'_id' : tg_id})
    return res


def get_spotify_id_from_db(tg_id):
    res = spotify_collection.find_one({'_id' : tg_id})
    if res != None:
        spotify_collection.delete_one({'_id' : tg_id})
    return res


def get_info_from_db(mode, tg_id):
    for i in range(24):
        if mode == 0:
            res = get_vk_id_from_db(str(tg_id))
            if res != None:
                return res
        elif mode == 1:
            res = get_spotify_id_from_db(str(tg_id))
            if res != None:
                return res
        time.sleep(5)


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

'''
def menu_reset_proc(message):
    bot.send_message(message.chat.id, text = "хайп")'''


def menu_analyze_spotify_proc():
    url = spotify_oauth_url+"?&tg_id="+str(message.chat.id)
    bot.send_message(message.chat.id, text = "Перейди, пожалуйста, по ссылке для авторизации: "+url)
    db_object = get_info_from_db(1, message.chat.id)
    print(message.chat.id, "successful authorization")
    token = db_object['spotify_access_token']
    get_info_from_spotify(message, token)


def menu_analyze_vk_proc():
    url = spotify_oauth_url+"?&tg_id="+str(message.chat.id)
    text1 = "Обязательно проверь, что у тебя открытый аккаунт и открытые аудио!\n\n"
    text2 = "После этого перейди, пожалуйста, по ссылке для авторизации: "
    bot.send_message(message.chat.id, text = text1 + text2 + url)
    db_object = get_info_from_db(0, message.chat.id)
    print(message.chat.id, db_object)
    vk_id = db_object['vk_id']
    get_info_from_vk(message, vk_id)


def menu_change_service_proc(message):
    txt = "хайп"
    bot.send_message(message.chat.id, text = txt, reply_markup=make_keyboard(menu_change_service))


def menu_startup_vk_proc(message):
    url = vk_oauth_url+"?&tg_id="+str(message.chat.id)
    text1 = "Обязательно проверь, что у тебя открытый аккаунт и открытые аудио!\n\n"
    text2 = "После этого перейди, пожалуйста, по ссылке для авторизации: "
    bot.send_message(message.chat.id, text = text1 + text2 + url)
    db_object = get_info_from_db(0, message.chat.id)
    print(message.chat.id, db_object)
    vk_id = db_object['vk_id']
    get_info_from_vk(message, vk_id)

    
def menu_startup_spotify_proc(message):
    url = spotify_oauth_url+"?&tg_id="+str(message.chat.id)
    bot.send_message(message.chat.id, text = "Перейди, пожалуйста, по ссылке для авторизации: "+url)
    db_object = get_info_from_db(1, message.chat.id)
    print(message.chat.id, "successful authorization")
    token = db_object['spotify_access_token']
    get_info_from_spotify(message, token)


def menu_startup_abort_proc(message):
    text1 = "Тогда я просто побуду у тебя в телефоне)\n\n"
    bot.send_message(message.chat.id, text = text1+TEXT)
    

menu_change_service = {
    'btn_menu_analize_vk' : ('Vk', menu_analyze_vk_proc),
    'btn_menu_analize_spotify' : ('Spotify', menu_analyze_spotify_proc)
}


menu = {
    #'btn_menu_change_service' : ('Другой сервис', menu_change_service_proc), 
    'btn_menu_manage_list' : ('Обновить плейлист', menu_manage_list_proc),
    #'btn_menu_send_concerts' : ('Прислать рекомендованные концерты', menu_send_concerts_proc),
    #'btn_menu_reset' : ('Стереть', menu_reset_proc)
    #'btn_menu_abort' : ('Выберу потом', menu_abort_proc)
}


menu_startup = {
    'btn_menu_startup_vk' : ('Vk', menu_startup_vk_proc),
    'btn_menu_startup_spotify' : ('Spotify', menu_startup_spotify_proc),
    'btn_menu_startup_abort' : ('Выберу потом', menu_startup_abort_proc)
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    #text1 = "Привет, я MusicGEEKbot. Приятно познакомиться)\nЯ помогу тебе не пропустить концерт или любое другое мероприятие любимых исполнителей.\n\n"
    text2 = "Мне необходимо проанализировать твою медиатеку, поэтому выбери подходящий вариант:"
    #text3 = если хочешь перейти в основное меню - напиши /menu
    print(message.chat.id, message.from_user.username)
    bot.send_message(message.chat.id, text = text2, reply_markup=make_keyboard(menu_startup))
    #bot.register_next_step_handler(message, menu_startup_keyboard_handler)

'''
@bot.message_handler(commands=['menu'])
def handle_menu(message):
    text1 = "Это основное меню!\n\n"
    #text2 = "Если у тебя появился новый стриминговый сервис и ты хочешь, чтобы я его проанализировал, нажми ДРУГОЙ СЕРВИС\n\n"
    text3 = "Если твои вкусы изменились, ты добавил много нового и хочешь, чтобы я это учел, нажми ОБНОВИТЬ ПЛЕЙЛИСТ\n\n"
    #text4 = "Если хочешь, чтобы твои данные были стерты, нажми СТЕРЕТЬ\n\n"
    text5 = "(если ты еще не отправлял мне свой плейлист, напиши /start)"
    bot.send_message(message.chat.id, text=text1+text2+text3+text5, reply_markup=make_keyboard(menu))
    #bot.register_next_step_handler(message, menu_keyboard_handler)'''


@bot.message_handler(content_types = ["text", "sticker", "pinned_message", "photo", "audio"])
def talk(message):
    text1 = "Мы могли бы пообщаться, но, к сожалению, пока что я умею отвечать только привет)\n"
    text2 = "Однако скоро мой создатель научит меня еще чему-нибудь)\n\n"
    bot.send_message(message.chat.id, text=text1+text2+TEXT)
    #bot.register_next_step_handler(message, menu_keyboard_handler)


@bot.message_handler(content_types=["location", "text"])
def location_handler(message, artists = None):
    if artists is None:
        bot.send_message(message.chat.id, text = "ага, хайп")
    else:
        try:
            lat = message.location.latitude
            long = message.location.longitude
            nearest_city = get_nearest_city_by_location(lat, long)
            nearest_city_rus = list(nearest_city.keys())[0]
            print(message.chat.id, "city " + nearest_city[nearest_city_rus])
            text1 = "Твой город - "
            text2 = "\n\nОсталось подождать совсем чуть-чуть, я подбираю для тебя концерты)"
            bot.send_message(message.chat.id, text = text1 + nearest_city_rus + text2)
            show_concerts(message, artists, nearest_city[nearest_city_rus])
        except AttributeError:
            try:
                city = get_city_by_name(message.text)
                print(message.chat.id, "city " + city)
                bot.send_message(message.chat.id, text = "Осталось подождать совсем чуть-чуть, я подбираю для тебя концерты)")
                show_concerts(message, artists, city)
            except ValueError:
                text1 = "Возможно твоего города еще нет в нашей базе, либо ты написал его неправильно(\n\n"
                text2 = "Попробуй еще раз с команды /start"
                print(message.chat.id, 'wrong city name or no city in our base')
                bot.send_message(message.chat.id, text = text1 + text2)
                
             
@bot.callback_query_handler(func=lambda call: type(call) == types.CallbackQuery and call.data in menu.keys())
def menu_keyboard_handler(call):
    btn = call.data
    print(call.from_user.id, btn)
    if menu.get(btn) != None:
        menu[btn][1](call.message)


@bot.callback_query_handler(func=lambda call: type(call) == types.CallbackQuery and call.data in menu_startup.keys())
def menu_startup_keyboard_handler(call):
    #print((lambda call: type(call) == types.CallbackQuery and call.data in menu_startup.keys())(call))
    btn = call.data
    print(call.from_user.id, btn)
    if menu_startup.get(btn) != None:
        menu_startup[btn][1](call.message)

     
@bot.callback_query_handler(func=lambda call: type(call) == types.CallbackQuery and call.data in menu_change_service.keys())
def menu_change_service_keyboard_handler(call):
    btn = call.data
    print(call.from_user.id, btn)
    if menu_change_service.get(btn) != None:
        menu_change_service[btn][1](call.message)


#по координатам возвращает ближайший город
def get_nearest_city_by_location(user_lat, user_long):
    coordinates = City_slovar()
    return coordinates.nearest_city_by_location(user_lat, user_long) 


#по названию возвращает город
def get_city_by_name(city):
    name = City_slovar()
    return name.city_by_name(city)


def get_info_from_vk(message, vk_id): 
    try:    
        vk = Vk_music_analyzer()
        text1 = "Подожди немного, пока я анализирую твой плейлист...\n\n"
        text2 = "Обычно это занимает 4-6 минут."
        bot.send_message(message.chat.id, text = text1 + text2)
        artists = vk.get_favourite_artists(vk_id)
        if artists == []:
            bot.send_message(message.chat.id, text = "Ох, кажется, у тебя нет песен в VK...")
            print(message.chat.id, 'no songs in vk')
        else:
            text1 = "Поделись, пожалуйста, своей геопозицией, чтобы я показал концерты в интересующем тебя городе!\n\n"
            text2 = "Ты можешь отправить как точку на карте, так и название города (например \'Москва\' или \'Санкт-Петербург\')"
            msg = bot.send_message(message.chat.id, text = text1 + text2)
            bot.register_next_step_handler(message, lambda msg: location_handler(msg, artists))
            print(message.chat.id, "send to identify location")
    except Exception as e:
        if str(e) == 'You don\'t have permissions to browse {}\'s albums'.format(vk_id):
            text1 = "Мне кажется, что у тебя все-таки закрытый аккаунт или закрытые аудио(\n\n"
            text2 = "Проверь это еще раз, пожалуйста!"
            bot.send_message(message.chat.id, text = text1 + text2)
            print(message.chat.id, "closed account")
        else:
            bot.send_message(message.chat.id, text = "Что-то тут не так! хм-хм")
            print(message.chat.id, "something happen")
   
    
def get_info_from_spotify(message, token):
    sp = Spotify_music_analyzer()
    bot.send_message(message.chat.id, text = "Подожди немного, пока я анализирую твой плейлист...")
    artists = sp.get_favourite_artists(token)
    if artists == []:
        bot.send_message(message.chat.id, text = "Ох, кажется, у тебя нет песен в spotify...")
        print(message.chat.id, 'no songs in spotify')
    else:
        text1 = "Поделись, пожалуйста, своей геопозицией, чтобы я показал концерты в интересующем тебя городе!\n\n"
        text2 = "Ты можешь отправить как точку на карте, так и название города (например \'Москва\' или \'Санкт-Петербург\')"
        msg = bot.send_message(message.chat.id, text = text1+text2)
        bot.register_next_step_handler(message, lambda msg: location_handler(msg, artists))
        print(message.chat.id, "send to identify location")    
      
    
def show_concerts(message, artists, nearest_city):
    con = Concerts()
    con.load_concerts(city = nearest_city, number_of_days=120)
    bot.send_message(message.chat.id, text = "Вот всё, что мне удалось найти:")
    concert_counter = 0
    for i in range(len(artists)):
        concert = con.find_concerts(artists[i])
        if concert != []:
            try:
                txt = "Концерт группы [{title}]({url})\nОн пройдет {date} в {place}\nСтоимость билетов начинается от {price} рублей".format(price = concert[0]['price'],
                                      place = concert[0]['place'],
                                      title = concert[0]['title'],
                                      date = concert[0]['date'],
                                      url = concert[0]['url'])
                bot.send_message(message.chat.id, text=txt, parse_mode='markdown')
                concert_counter += 1
            except KeyError:
                txt = "Концерт группы [{title}]({url})\nОн пройдет {date} в {place}".format(place = concert[0]['place'],
                                      title = concert[0]['title'],
                                      date = concert[0]['date'],
                                      url = concert[0]['url'])
                bot.send_message(message.chat.id, text=txt, parse_mode='markdown')
                concert_counter += 1
            time.sleep(8)
    print(message.chat.id, "{0} concerts were sent".format(concert_counter))
    if concert_counter != 0:
        bot.send_message(message.chat.id, text = "Наслаждайся)")
    else:
        time.sleep(5)
        bot.send_message(message.chat.id, text = "Ох, кажется, что в выбранном тобой городе нет концертов, которые могли бы тебе понравиться(")

#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)
bot.polling(none_stop=True)
