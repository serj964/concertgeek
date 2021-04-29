import sqlalchemy
import telebot
import time
import datetime
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import BigInteger
import json


import Db.db as db_classes


#connect with db
CONFIG_FILE = './bot/config.json'

with open(CONFIG_FILE) as conf:
    config = json.load(conf)

#bot_config = config['bot_config']
db_config = config["db_config"]



engine = create_engine(db_config['sqlite_address'])
Session = sessionmaker(bind=engine)
session = Session()

#TOKEN = bot_config['token']
#bot = telebot.TeleBot(TOKEN)
TIMETICK = 60

def CompareDates(first, second, delta):
    pass

def DeleteExpiredConcerts(now):
    concerts = session.query(db_classes.Concert).filter(db_classes.Concert.concert_datetime < now)
    for concert in concerts:
        concert.musicians = []
        session.delete(concert)
    session.commit()

def GetListOfConcerts(now):
    return session.query(db_classes.Concert).filter(db_classes.Concert.concert_datetime <= now+datetime.timedelta(days=28))

def GetListOfUsersForConcert(concert_id):
    query = session.query(db_classes.User, db_classes.Musician, db_classes.Concert).filter(db_classes.Concert.concert_datetime != datetime.datetime.now()+datetime.timedelta(days=1))
    return query.all()

def Notify(now):
    #check db and if there are some events, it will notify user
    #db will contain information about how often should the service notify user
    #user would be notified in advance if the number of tickets is low
    concerts = GetListOfConcerts(now)
    for concert in concerts:
        print(concert.concert_datetime.day)
        res = GetListOfUsersForConcert(concert.id)
        print(res)
        for obj in res:
            tg_id = obj[0].tg_id
            concert_name = obj[1].name
            print("tg_id = {}, concert name = {}".format(tg_id, concert_name))
            #bot.send_message(tg_id, concert_name)

    

    #bot.send_message(373959637, "hey")

##while True:

now = datetime.datetime.now()
#DeleteExpiredConcerts(now)
Notify(now)
#    time.sleep(TIMETICK)