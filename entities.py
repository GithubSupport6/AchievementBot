from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table
from sqlalchemy import create_engine


Base = declarative_base()

UserAchievement = Table('user_achievement',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('achievement_id', Integer, ForeignKey('achievements.id'))
)

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    description = Column(String)
    users = relationship('User', secondary=UserAchievement, back_populates="achievements")

    def __init__(self,userid,name,description):
       self.userid = userid    
       self.name = name
       self.description = description 


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    achievements = relationship('Achievement', secondary=UserAchievement, back_populates="users")

def init_db():
    hostname = "localhost:5432"
    engine = create_engine('postgresql+psycopg2://postgres:admin@' + hostname + '/postgres', echo=True, future=True)
    Base.metadata.create_all(engine)
    return engine