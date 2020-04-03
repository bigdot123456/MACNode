from sqlalchemy import create_engine
from MACNodeSQL import *
from sqlalchemy.orm import sessionmaker
# 连接本地test数据库
engine = create_engine("mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8")
# 创建会话
session = sessionmaker(engine)
mySession = session()
# 查询结果集
result = mySession.query(Stdmacnode).all()
