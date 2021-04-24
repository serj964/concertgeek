import sqlalchemy
import telebot
import time
import datetime
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import BigInteger


import Db.db as db_classes


#connect with db
CONFIG_FILE = './bot/config.json'

with open(CONFIG_FILE) as conf:
    config = json.load(conf)

bot_config = config['bot_config']
db_config = config["db_config"]



engine = create_engine(db_config['sqlite_address'])

TOKEN = bot_config['token']
bot = telebot.TeleBot(TOKEN)
TIMETICK = 60


bot = telebot.TeleBot(TOKEN)
Session = sessionmaker(bind=engine)
session = Session()

def GetListOfConcerts:
    date = datetime.datetime.now().date()
    return session.query(db_classes.Concert).filter_by(datetime.datetime(db_classes.Concert.concert_datetime).date() == date)

def GetListOfUsersForConcert(concert_id):
    query = session.query(db_classes.User, db_classes.Concert)
    query = query.join(db_classes.Preferences, db_classes.Preferences.user_id = db_classes.User.id)
    query = query.join(db_classes.Musician, db_classes.Musician.id = db_classes.Preferences.musician_id)
    query = query.join(db_classes.Conmus, db_classes.Conmus.musician_id = db_classes.Musician.id)
    query = query.join(db_classes.Concert, db_classes.Conmus.concert_id = db_classes.Concert.id)
    query = query.filter_by(db_classes.Concert.id == concert_id)
    return query.all()

def Notify():
    #check db and if there are some events, it will notify user
    #db will contain information about how often should the service notify user
    #user would be notified in advance if the number of tickets is low
    concerts = GetListOfConcerts()
    print(concerts)
    for concert in concerts:
        print(concert)

    

    #bot.send_message(373959637, "hey")

##while True:
Notify()
#    time.sleep(TIMETICK)