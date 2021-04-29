from sqlalchemy import Column, Integer, String, create_engine, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import Float, DateTime, Text
#import time

base = declarative_base()






class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    tg_username = Column(String)
    vk_id = Column(Integer)
    spotify_id = Column(Integer)
    last_date = Column(DateTime)
    preferences = relationship('Musician', secondary='preferences')
    not_to_inform = relationship('Musician', secondary='not_to_inform')
    
    '''def __repr__(self):
        return "<User('%d', '%d','%s', '%d', '%d')>" % (self.id, self.tg_id, self.tg_username, self.vk_id, self.spotify_id)'''

class City(base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    '''def __repr__(self):
        return "<City('%d','%s')>" % (self.id, self.name)'''


class Interaction(base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey("interaction_type.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    concert_id = Column(Integer, ForeignKey("concerts.id"))
    inter_datetime = Column(DateTime)


    '''def __repr__(self):
        return "<Interaction('%d','%s')>" % (self.id, self.name)'''



class Interaction_type(base):
    __tablename__ = "interaction_type"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Musician(base):
    __tablename__ = 'musicians'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    conmus = relationship('Concert', secondary='conmus')
    users_in_preference = relationship('User', secondary='preferences')
    users_not_to_inform = relationship('User', secondary='not_to_inform')
    '''def __repr__(self):
        return "<Musician('%d','%s')>" % (self.id, self.name)'''

class Place(base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key = True)
    name = Column(String)

    '''def __repr__(self):
        return "<Place('%d','%s')>" % (self.id, self.name)'''

class Concert(base):
    __tablename__ = 'concerts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    place_id = Column(Integer, ForeignKey("places.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))
    concert_datetime = Column(DateTime)
    price = Column(String)
    url = Column(String)
    comment = Column(Text)
    source_id = Column(Integer, ForeignKey("sources.id"))
    conmus = relationship('Musician', secondary='conmus')

    '''def __repr__(self):
        return "<Concert('%d', '%s', '%s', '%s', '%s', '%s')>" % (self.id, self.name, str(self.datetime), self.price, self.url, self.comment)'''


class Source(base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Conmus(base):
    __tablename__ = "conmus"
    concert_id = Column(Integer, ForeignKey('concerts.id'), primary_key=True)
    musician_id = Column(Integer, ForeignKey('musicians.id'), primary_key=True)


class Not_to_inform(base):
    __tablename__ = "not_to_inform"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    musician_id = Column(Integer, ForeignKey('musicians.id'), primary_key=True)


class Preference(base):
    __tablename__ = "preferences"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    musician_id = Column(Integer, ForeignKey('musicians.id', primary_key=True))


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
