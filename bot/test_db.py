from sqlalchemy import Column, Integer, String, create_engine, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import BigInteger, SmallInteger, Float, DateTime, Text
import time
import datetime

engine = create_engine('sqlite:///Db/test.db', echo=True)

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


class Interaction(base):
    __tablename__ = 'interactions'
    id = Column(SmallInteger, primary_key = True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return "<Interaction('%d','%s')>" % (self.id, self.name)

Session = sessionmaker(bind=engine)
session = Session()
usr = session.query(User).first()
print(usr)
#vasiaUser = User(1234, "Vasiliy Pypkin", 1234, 1234, datetime.datetime.now(), 1)
#print(vasiaUser)
#session.add(vasiaUser)
#session.commit()