# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(32))
    password = Column(String(64))


class Bigdot(Base):
    __tablename__ = 'bigdot'

    nid = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), server_default=text("'bigdot'"))
    email = Column(String(255))


class Dbtable(Base):
    __tablename__ = 'dbtable'

    nid = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), server_default=text("'bigdot'"))
    email = Column(String(255))


class Fast(Base):
    __tablename__ = 'fast'

    nid = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), server_default=text("'bigdot'"))
    email = Column(String(255))


class SqlTest(Base):
    __tablename__ = 'sql_test'

    id = Column(INTEGER(11), primary_key=True)
    user_name = Column(String(32))
    user_password = Column(String(64))


class Stdmacnode(Base):
    __tablename__ = 'stdmacnode'

    ID = Column(INTEGER(11), primary_key=True)
    Address = Column(String(32), nullable=False, server_default=text("'MAN.11111111111'"))
    Balance = Column(INTEGER(11), server_default=text("'0'"))
    parentID = Column(INTEGER(11))
    parentAddress = Column(String(32))
    name = Column(String(32), server_default=text("'MACMAN'"))
    tel = Column(String(11), server_default=text("'13800138000'"))
    email = Column(String(64))
    attendRound = Column(INTEGER(11))
    subNodeNum = Column(INTEGER(11))
    level = Column(INTEGER(11))
    IDleft = Column(INTEGER(11))
    IDright = Column(INTEGER(11))
    vipTag = Column(INTEGER(11))
    untilNowIncome = Column(INTEGER(11))
    staticIncome = Column(INTEGER(11))
    subStaticIncome = Column(INTEGER(11))
    dynamicIncome = Column(INTEGER(11))
    withdrawStatus = Column(INTEGER(11))


class Student(Base):
    __tablename__ = 'student'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(100))
    age = Column(INTEGER(11))
    address = Column(String(100))


class Tab2(Base):
    __tablename__ = 'tab2'

    nid = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), server_default=text("'bigdot'"))
    email = Column(String(255))
