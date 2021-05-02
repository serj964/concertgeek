from sqlalchemy import Column, Integer, String, create_engine, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import Float, DateTime, Text
#import time

base = declarative_base()






preference_table = Table('preferences', base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('musician_id', Integer, ForeignKey('musicians.id')),
    Column('pisition', Integer)
)

not_to_inform_table = Table('not_to_inform', base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('musician_id', Integer, ForeignKey('musicians.id'))
)

user_city_table = Table('usecit', base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('city_id', Integer, ForeignKey('cities.id'))
)

conmus_table = Table('conmus', base.metadata, 
    Column('concert_id', Integer, ForeignKey('concerts.id')),
    Column('musician_id', Integer, ForeignKey('musicians.id'))
)

usecon_table = Table('usecon', base.metadata,
    Column('concert_id', Integer, ForeignKey('concerts.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('status', Integer, ForeignKey('status_type.id')),
    Column('date', DateTime)
)


class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    tg_username = Column(String)
    vk_id = Column(Integer)
    spotify_id = Column(Integer)
    last_date = Column(DateTime)

    cities = relationship('City', secondary=user_city_table)
    concerts = relationship('Concert', secondary=usecon_table)
    preferences = relationship('Musician', secondary=preference_table)
    not_to_inform = relationship('Musician', secondary=not_to_inform_table)
    
    def __repr__(self):
        return f"User {self.tg_id}"

class Status(base):
    __tablename__ = 'status_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class City(base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    users_in_city = relationship('User', secondary=user_city_table)
    '''def __repr__(self):
        return "<City('%d','%s')>" % (self.id, self.name)'''

class Interaction(base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey("interaction_type.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
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
    concerts = relationship('Concert', secondary=conmus_table)
    users_in_preference = relationship('User', secondary=preference_table)
    users_not_to_inform = relationship('User', secondary=not_to_inform_table)
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
    is_new = Column(Integer)

    users = relationship('User', secondary=usecon_table)
    musicians = relationship('Musician', secondary=conmus_table)

    '''def __repr__(self):
        return "<Concert('%d', '%s', '%s', '%s', '%s', '%s')>" % (self.id, self.name, str(self.datetime), self.price, self.url, self.comment)'''


class Source(base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    name = Column(String)




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
