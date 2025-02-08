from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user_info'
    user_id = Column(String, primary_key=True)
    nickname = Column(String, nullable=False)
    full_name = Column(String, nullable=False, default='')

    def __repr__(self):
        return f"<User(user_id={self.user_id}, nickname={self.nickname})>"

class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, autoincrement=True, primary_key=True)
    group_name = Column(String, unique=True, nullable=False)
    thread_id = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Group(group_name={self.group_name}, thread_id={self.thread_id})>"