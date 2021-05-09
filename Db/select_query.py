from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import BigInteger

engine = create_engine('sqlite:///test.db', echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    tg_id = Column(BigInteger, primary_key=True)
    tg_nickname = Column(String)
    vk_id = Column(BigInteger)
    spotify_id = Column(BigInteger)
    
    def __init__(self, tg_id, tg_nickname, vk_id, spotify_id):
        self.tg_id = tg_id
        self.tg_nickname = tg_nickname
        self.vk_id = vk_id
        self.spotify_id = spotify_id
    def __repr__(self):
        return "<User('%d','%s', '%d', '%d')>" % (self.tg_id, self.tg_nickname, self.vk_id, self.spotify_id)


Session = sessionmaker(bind=engine)
session = Session()

res = session.query(User)
print(res.first())