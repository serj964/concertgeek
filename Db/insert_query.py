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

# vasiaUser = session.query(db_classes.User).filter_by(tg_id=123).first()
vasiaUser = db_classes.User(tg_id = 124, tg_username = "ahah", vk_id = 123, spotify_id = 123)
sanyaMusician = db_classes.Musician(name = "Sanya")
con = db_classes.Concert(name = "Party", concert_datetime = datetime.datetime(2021, 4, 16), is_new=1)



vasiaUser.preferences.append(sanyaMusician)
#sanyaMusician.users_in_preference.append(vasiaUser)
sanyaMusician.concerts.append(con)
vasiaUser.concerts_to_notify.append(con)
#con.musicians.append(sanyaMusician)

session.add(vasiaUser)
session.add(sanyaMusician)
session.add(con)
session.commit()

print(session.query(db_classes.User).all())