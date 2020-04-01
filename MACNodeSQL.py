# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Tab2(Base):
    __tablename__ = 'tab2'

    nid = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), server_default=text("'bigdot'"))
    email = Column(String(255))
