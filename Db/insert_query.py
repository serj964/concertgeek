from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import BigInteger
import json
import datetime
import Db.db as db_classes
from Concerts.yandex_afisha_concerts import Concerts
from bot.city_slovar import City_slovar


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


cons = [db_classes.Concert(name = str(i), concert_datetime = datetime.datetime(2021, 6, i), is_new=1) for i in range(1,30)]
#con = db_classes.Concert(name = "Party", concert_datetime = datetime.datetime(2021, 6, ), is_new=1)



vasiaUser.preferences.append(sanyaMusician)
sanyaMusician.users_in_preference.append(vasiaUser)
for con in cons:
    sanyaMusician.concerts.append(con)
    vasiaUser.concerts.append(con)


session.add(vasiaUser)
session.add(sanyaMusician)
for i in cons:
    session.add(i)
session.commit()

def update_concerts():
    cities = []
    city_dict = City_slovar().get_dict()
    for city_rus in city_dict:
        cities.append(city_dict[city_rus][0])
    for city in cities:
        new_concerts = Concerts()
        new_concerts.load_concerts(city=city)
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
            else:
                db_concert.price = concert['price']
                

    session.commit()


def add_user(tg_id=None, tg_username=None):
    if tg_id is None:
        raise Exception("No tg_id")
    new_user = db_classes.User(tg_id=tg_id, tg_username=tg_username)
    session.add(new_user)
    session.commit()

def update_user_info(tg_id=None, vk_id=None, spotify_id=None, preferences=None, city=None):
    assert tg_id is not None, "No tg_id"
    user = session.query(db_classes.User).filter_by(tg_id=tg_id).first()
    assert user is not None, f"No user in db with tg_id {tg_id}"
    if vk_id is not None:
        user.vk_id = vk_id
    if spotify_id is not None:
        user.spotify_id = spotify_id
    if city is not None:
        db_city = session.query(db_classes.City).filter_by(name=city).first()
        assert db_city is not None, f"No city in db with name {city}"
        user.cities = db_city
    if preferences is not None:
        for musician in preferences:
            db_musician = session.query(db_classes.Musician).filter_by(name=musician).first()
            if db_musician is None:
                db_musician = db_classes.Musician(name=musician)
                session.add(db)
            db_musician.users_in_preference.append(user)
    session.commit()




if __name__ == "__main__":
    pass