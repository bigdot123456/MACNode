# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER, primary_key=True, comment='用户ID')
    passport = Column(String(45), nullable=False, comment='账号')
    password = Column(String(45), nullable=False, comment='密码')
    nickname = Column(String(45), nullable=False, comment='昵称')
    create_time = Column(TIMESTAMP, nullable=False, comment='创建时间/注册时间')
