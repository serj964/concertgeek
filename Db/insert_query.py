from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import BigInteger
import json
import datetime

import Db.db as db_classes



CONFIG_FILE = './bot/config.json'

with open(CONFIG_FILE) as conf:
    config = json.load(conf)

db_config = config["db_config"]



engine = create_engine(db_config['sqlite_address'])

Session = sessionmaker(bind=engine)
session = Session()

vasiaUser = db_classes.User(tg_id = 123, tg_username = "ahah", vk_id = 123, spotify_id = 123)
session.add(vasiaUser)

sanyaMusician = db_classes.Musician(name = "Sanya")
session.add(sanyaMusician)

pref = db_classes.Preference(user_id = 1, musician_id = 1)
session.add(pref)

con = db_classes.Concert(name = "Party", concert_datetime = datetime.datetime.now())
session.add(con)

conmus = db_classes.Conmus(concert_id = 1, musician_id = 1)
session.add(conmus)

session.commit()