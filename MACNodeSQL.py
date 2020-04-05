# coding: utf-8
from sqlalchemy import Column, String, text
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
    TreeBalance = Column(INTEGER(11))
    vipTreeBalance = Column(INTEGER(11))
    vipTag = Column(INTEGER(11))
    vipLevel = Column(INTEGER(11))
    usedBalance = Column(INTEGER(11))
    minerProductive = Column(INTEGER(11))
    staticIncome = Column(INTEGER(11))
    staticIncomeTree = Column(INTEGER(11))
    MinerAward = Column(INTEGER(11))
    RecommendAward = Column(INTEGER(11))
    TotalAward = Column(INTEGER(11))
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
    TreeBalance = Column(INTEGER(11))
    vipTreeBalance = Column(INTEGER(11))
    vipTag = Column(INTEGER(11))
    vipLevel = Column(INTEGER(11))
    usedBalance = Column(INTEGER(11))
    minerProductive = Column(INTEGER(11))
    staticIncome = Column(INTEGER(11))
    staticIncomeTree = Column(INTEGER(11))
    MinerAward = Column(INTEGER(11))
    RecommendAward = Column(INTEGER(11))
    TotalAward = Column(INTEGER(11))
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
