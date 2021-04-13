import telebot
import time
from telebot import types
from Music_analyzer.vk_music_analyzer import vk_music_analyzer
from Concerts.yandex_afisha_concerts import Concerts



TOKEN = '1634504684:AAEk4wzUCsI_ZNdohfYZGy2jakWFFkfdeTs'

bot = telebot.TeleBot(TOKEN)

address = "127.0.0.1:8000/auth"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Я MUSICGEEK бот. Приятно познакомиться. Я помогу тебе не пропустить концерт или любое другое мероприятие любимой группы.')

@bot.message_handler(content_types = ["text", "sticker", "pinned_message", "photo", "audio"])
def handle_message(message):
    txt = "Желаешь ли ты, чтобы наш бот проанализировал твою медиатеку ВК?/yes, /no.\nНе забудь, что твои аудиозаписи ВК должны быть открыты)"
    a = 5
    bot.send_message(message.from_user.id, text = txt)
    bot.register_next_step_handler(message, callback_worker)
    
@bot.message_handler(content_types = ['text'])
def callback_worker(message):
    if message.text == '/yes':
        bot.send_message(message.from_user.id, text = "Введи, пожалуйста, свой id вк")
        try:
            bot.register_next_step_handler(message, get_vk_id)
        except:
            bot.send_message(message.from_user.id, text = "Я сломался(\nСейчас мой создатель меня перезапустит, и давай попробуем сначала")
        
        
def get_vk_id(message):
    vk_id = message.text
    print(message.from_user.id, vk_id) #add this pair to db
    bot.send_message(message.from_user.id, text = "Подожди, я подберу для тебя концерты)")
    vk = vk_music_analyzer()
    artists = vk.get_favourite_artists(vk_id)
    con = Concerts()
    con.load_concerts(number_of_days=160)
    bot.send_message(message.from_user.id, text = "Вот, что мне удалось найти)")
    for i in range(len(artists)):
        concert = con.find_concerts(artists[i])
        if concert != []:
            try:
                txt = "Концерт группы {title}\nОн пройдет {date} в {place}\nСтоимость билетов начинается от {price} рублей\nВот ссылка на мероприятие {url}".format(price = concert[0]['price'],
                                      place = concert[0]['place'],
                                      title = concert[0]['title'],
                                      date = concert[0]['date'],
                                      url = concert[0]['url'])
                bot.send_message(message.from_user.id, text=txt)
            except KeyError:
                txt = "Концерт группы {title}\nОн пройдет {date} в {place}\nВот ссылка на мероприятие {url}".format(place = concert[0]['place'],
                                      title = concert[0]['title'],
                                      date = concert[0]['date'],
                                      url = concert[0]['url'])
                bot.send_message(message.from_user.id, text=txt)
            time.sleep(10)
    bot.send_message(message.from_user.id, text = "Наслаждайся)")
    print("done")
        
        
    

#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

bot.polling(none_stop=True)
