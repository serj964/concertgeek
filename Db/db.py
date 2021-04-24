from sqlalchemy import Column, Integer, String, create_engine, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import BigInteger, SmallInteger, Float, DateTime, Text
import time

base = declarative_base()






class User(base):
    __tablename__ = 'users'
    tg_id = Column(BigInteger, primary_key=True)
    tg_nickname = Column(String)
    vk_id = Column(BigInteger)
    spotify_id = Column(BigInteger)
    inter_datetime = Column(DateTime)
    inter_type = Column(SmallInteger, ForeignKey('interactions.id'))
    
    def __init__(self, tg_id, tg_nickname, vk_id, spotify_id, inter_datetime, inter_type):
        self.tg_id = tg_id
        self.tg_nickname = tg_nickname
        self.vk_id = vk_id
        self.spotify_id = spotify_id
        self.inter_datetime = inter_datetime
        self.inter_type = inter_type
    def __repr__(self):
        return "<User('%d','%s', '%d', '%d')>" % (self.tg_id, self.tg_nickname, self.vk_id, self.spotify_id)

class City(base):
    __tablename__ = 'cities'
    id = Column(BigInteger, primary_key = True)
    name = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

    def __repr__(self):
        return "<City('%d','%s', '%f', '%f')>" % (self.id, self.name, self.latitude, self.longitude)


class Interaction(base):
    __tablename__ = 'interactions'
    type_id = Column(BigInteger, ForeignKey("interaction_type.type_id"))
    user_id = Column(BigInteger, ForeignKey("users.tg_id"))
    musician_id = Column(BigInteger, ForeignKey("musicians.id"))
    inter_datetime = Column(DateTime)


    def __repr__(self):
        return "<Interaction('%d','%s')>" % (self.id, self.name)



class Interaction_type(base):
    __tablename__ = "interaction_type"
    type_id = Column(BigInteger, primary_key=True)
    type_name = Column(String)

class Musician(base):
    __tablename__ = 'musicians'
    id = Column(BigInteger, primary_key = True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return "<Musician('%d','%s')>" % (self.id, self.name)

class Place(base):
    __tablename__ = 'places'
    id = Column(BigInteger, primary_key = True)
    name = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

    def __repr__(self):
        return "<Place('%d','%s', '%f', '%f')>" % (self.id, self.name, self.latitude, self.longitude)

class Concert(base):
    __tablename__ = 'concerts'
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    place_id = Column(BigInteger, ForeignKey("places.id"), nullable=False)
    city_id = Column(SmallInteger, ForeignKey("cities.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    price = Column(SmallInteger)
    comment = Column(Text)
    source_id = Column(BigInteger, ForeignKey("sources.id"))

    def __repr__(self):
        return "<Concert('%d', '%s', '%s', '%d', '%s')>" % (self.id, self.name, str(self.datetime), self.price. self.comment)


class Source(base):
    __tablename__ = "sources"
    id = Column(BigInteger, primary_key=True)
    name = Column(String)


ConcertMusicianTable = Table('concert_musician_link', base.metadata,
    Column('concert_id', BigInteger, ForeignKey('concerts.id')),
    Column('musician_id', BigInteger, ForeignKey('musicians.id'))
)


not_to_inform = Table('not_to_inform', base.metadata,
    Column('tg_id', BigInteger, ForeignKey('users.tg_id')),
    Column('musician_id', BigInteger, ForeignKey('musicians.musician_id'))
)

preferences = Table('preferences', base.metadata,
    Column('tg_id', BigInteger, ForeignKey('users.tg_id')),
    Column('musician_id', BigInteger, ForeignKey('musicians.musician_id'))
)


if __name__ == "__main__":
    import json
    CONFIG_FILE = './bot/config.json'

    with open(CONFIG_FILE) as conf:
        config = json.load(conf)
    db_config = config["db_config"]
    sqlite_address = db_config['sqlite_address']
    print(sqlite_address)
    engine = create_engine(sqlite_address, echo = True)
    base.metadata.create_all(engine)
