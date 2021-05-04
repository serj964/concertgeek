from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import BigInteger
import json
import datetime
import Db.db as db_classes
from Concerts.yandex_afisha_concerts import Concerts


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
con = db_classes.Concert(name = "Party", concert_datetime = datetime.datetime(2021, 5, 29), is_new=1)



# vasiaUser.preferences.append(sanyaMusician)
# #sanyaMusician.users_in_preference.append(vasiaUser)
# sanyaMusician.concerts.append(con)
# vasiaUser.concerts_to_notify.append(con)
# #con.musicians.append(sanyaMusician)

# session.add(vasiaUser)
# session.add(sanyaMusician)
# session.add(con)
# session.commit()

def update_concerts():
    new_concerts = Concerts()
    new_concerts.load_concerts()
    new_concerts = new_concerts.get_concerts()
    for concert in new_concerts:
        db_concert = session.query(db_classes.Concert).filter_by(url=concert['url']).first()
        if db_concert is None:
            new_concert = db_classes.Concert(name=concert['title'], 
                                            city_id=concert['city'], 
                                            price=concert['price'], 
                                            url=concert['url'], 
                                            source_id='yandex')
            session.add(new_concert)
    session.commit()


def add_user(tg_id=None, tg_username=None):
    if tg_id is None:
        raise Exception("No tg_id")
    new_user = db_classes.User(tg_id=tg_id, tg_username=tg_username)
    session.add(new_user)
    session.commit()

def user_update_info(tg_id=None, vk_id=None, spotify_id=None):
    if tg_id is None:
        raise Exception("No tg_id")
    user = session.query(db_classes.User).filter_by(tg_id=tg_id).first()
    if vk_id is not None:
        user.vk_id = vk_id
    if spotify_id is not None:
        user.spotify_id = spotify_id
    session.commit()

if __name__ == "__main__":
    update_concerts()