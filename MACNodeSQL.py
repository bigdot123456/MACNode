# coding: utf-8
from sqlalchemy import Column, Float, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Dbtable(Base):
    __tablename__ = 'dbtable'

    nid = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), server_default=text("'bigdot'"))
    email = Column(String(255))


class Mymacnode(Base):
    __tablename__ = 'mymacnode'

    ID = Column(INTEGER(11), primary_key=True)
    Address = Column(String(32), nullable=False, server_default=text("'MAN.11111111111'"))
    Balance = Column(INTEGER(11), server_default=text("'0'"))
    parentID = Column(INTEGER(11))
    parentAddress = Column(String(32))
    name = Column(String(32), server_default=text("'MACMAN'"))
    tel = Column(String(11), server_default=text("'13800138000'"))
    email = Column(String(64))
    attendRound = Column(INTEGER(11))
    NodeLevel = Column(INTEGER(11))
    TreeBalance = Column(Float)
    vipTreeBalance = Column(Float)
    vipTag = Column(INTEGER(11))
    vipLevel = Column(INTEGER(11))
    usedBalance = Column(Float)
    minerProductive = Column(Float)
    staticIncome = Column(Float)
    staticIncomeTree = Column(Float)
    MinerAward = Column(Float)
    RecommendAward = Column(Float)
    TotalAward = Column(Float)
    withdrawStatus = Column(INTEGER(11))


class Mymacnoderesult(Base):
    __tablename__ = 'mymacnoderesult'

    ID = Column(INTEGER(11), primary_key=True)
    Address = Column(String(32), nullable=False, server_default=text("'MAN.11111111111'"))
    Balance = Column(INTEGER(11), server_default=text("'0'"))
    parentID = Column(INTEGER(11))
    parentAddress = Column(String(32))
    name = Column(String(32), server_default=text("'MACMAN'"))
    tel = Column(String(11), server_default=text("'13800138000'"))
    email = Column(String(64))
    attendRound = Column(INTEGER(11))
    NodeLevel = Column(INTEGER(11))
    TreeBalance = Column(Float)
    vipTreeBalance = Column(Float)
    vipTag = Column(INTEGER(11))
    vipLevel = Column(INTEGER(11))
    usedBalance = Column(Float)
    minerProductive = Column(Float)
    staticIncome = Column(Float)
    staticIncomeTree = Column(Float)
    MinerAward = Column(Float)
    RecommendAward = Column(Float)
    TotalAward = Column(Float)
    withdrawStatus = Column(INTEGER(11))


class SqlTest(Base):
    __tablename__ = 'sql_test'

    id = Column(INTEGER(11), primary_key=True)
    user_name = Column(String(32))
    user_password = Column(String(64))


class Student(Base):
    __tablename__ = 'student'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(100))
    age = Column(INTEGER(11))
    address = Column(String(100))
