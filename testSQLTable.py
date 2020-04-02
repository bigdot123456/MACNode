#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/10 20:58
# @Author  : Feng Xiaoqing
# @File    : demo1.py
# @Function: -----------

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8")
# engine = create_engine('mysql+pymysql://fxq:123456@192.168.100.101/sqlalchemy')

DBsession = sessionmaker(bind=engine)
session = DBsession()

Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer)
    address = Column(String(100))

student1 = Student(id=1001, name='ling', age=25, address="beijing")
student2 = Student(id=1002, name='molin', age=18, address="jiangxi")
student3 = Student(id=1003, name='karl', age=16, address="suzhou")


class User(Base):  # 继承生成的orm基类
    __tablename__ = "sql_test"  # 表名
    id = Column(Integer, primary_key=True)  # 设置主键
    user_name = Column(String(32))
    user_password = Column(String(64))


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(64))


Base.metadata.create_all(engine)  # 创建表结构
# 父类Base调用所有继承他的子类来创建表结构

session.add_all([student1, student2, student3])
session.commit()
session.close()