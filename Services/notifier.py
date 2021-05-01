import sqlalchemy
import telebot
import time
import datetime
from datetime import timedelta
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
TIMETICK = 60*60*24

def CompareDates(first, second, delta):
    pass

def DeleteExpiredConcerts(now):
    concerts = session.query(db_classes.Concert).filter(db_classes.Concert.concert_datetime < now)
    for concert in concerts:
        concert.musicians = []
        session.delete(concert)
    session.commit()

def GetListOfConcerts(now):
    #getting concerts which dates are 28 days after now
    query = session.query(db_classes.Concert).filter(db_classes.Concert.concert_datetime <= now+datetime.timedelta(days=28))
    return query.all()

def GetListOfUsersForConcert(concert_id, days_before_concert):
    query = session.query(db_classes.User, db_classes.Musician, db_classes.Concert).filter(db_classes.Concert.id == concert_id)
    return query.all()

def GetListOfNewConcerts(now):
    query

def PostNewConcerts(now):
    new_concerts = GetListOfNewConcerts(now)
    for concert in new_concerts:
        users_for_concert_responce = GetListOfUsersForConcert(concert_id)
        for user in users_for_concert_responce:
            tg_id = user[0].tg_id
            concert_name = user[1].name
            print("tg_id = {}, concert name = {}".format(tg_id, concert_name))
            #bot.send_message(tg_id, concert_name)

def Notify(now):
    concerts = GetListOfConcerts(now)
    for concert in concerts:
        days_before_concert = (concert.concert_datetime-now).days
        print(days_before_concert)
        res = GetListOfUsersForConcert(concert.id, days_before_concert)
        print(res)
        for obj in res:
            tg_id = obj[0].tg_id
            concert_name = obj[1].name
            print("tg_id = {}, concert name = {}".format(tg_id, concert_name))
            #bot.send_message(tg_id, concert_name)

    
##while True:

now = datetime.datetime.now()
DeleteExpiredConcerts(now)
Notify(now)
#    time.sleep(TIMETICK)