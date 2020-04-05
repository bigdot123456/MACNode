from asyncio.log import logger

import pymysql
import sqlalchemy
from sqlalchemy import create_engine
from MACNodeSQL import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

import random

# 连接本地test数据库
#engine = create_engine("mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8",echo=True)
engine = create_engine("mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8")
# 创建会话
session = sessionmaker(engine)
s = session()
# 查询结果集, 对象模式，需要取出具体数据
#result = s.query(Mymacnode).all()

nodelist = s.query(Mymacnode).filter(text("ID < :value AND parentID = :pValue")).params(value=100,pValue=1)
#nodelist = s.query(Mymacnode).filter(text("ID < :value")).params(value=10)
print(nodelist)
for row in nodelist:
    print(row.ID, row.Address,row.parentID)

try:
    with engine.connect() as conn:

        query = text("SELECT * FROM Mymacnode WHERE "
                             "ID < 100 AND "
                             "parentID = 1 "
                             "ORDER BY ID ASC")
        rs = conn.execute(query)


        r = rs.first()

        if r is not None:
            print("ok")
        else:
            print("error")
except Exception as ex:
    logger.error(
        "Error querying for next queued task: %s" % str(ex),
        exc_info=True)

for i in range(10):
    pnode=s.query(Mymacnode).filter(Mymacnode.ID==i).first()
    pid=pnode.ID
    pAddress=pnode.Address
    node = s.query(Mymacnode).filter(Mymacnode.ID%10==i,Mymacnode.ID>10).update({Mymacnode.parentID:f"{pid}", Mymacnode.parentAddress:f"{pAddress}"})
    #node = s.query(Mymacnode).filter(Mymacnode.ID==2).update({Mymacnode.parentID:"1"})
    #node = s.query(Mymacnode).filter(Mymacnode.ID<=10, Mymacnode.ID >2).update({Mymacnode.parentID:"1"})
    # 此处的node表示更新的行数

    try:
        s.commit()
        print(f'New Node {node}')
    except pymysql.err.IntegrityError:
        s.rollback()
        print(f'Duplicate Node {node}')
    except sqlalchemy.orm.exc.FlushError:
        s.rollback()
        print(f'FlushError Node {node}')



for i in range(10):
    pnode=s.query(Mymacnode).filter(Mymacnode.ID==0).first()
    pid=pnode.ID
    pAddress=pnode.Address
    node = s.query(Mymacnode).filter(Mymacnode.ID==i).update({Mymacnode.parentID:f"{pid}", Mymacnode.parentAddress:f"{pAddress}"})
    #node = s.query(Mymacnode).filter(Mymacnode.ID==2).update({Mymacnode.parentID:"1"})
    #node = s.query(Mymacnode).filter(Mymacnode.ID<=10, Mymacnode.ID >2).update({Mymacnode.parentID:"1"})
    # 此处的node表示更新的行数

    try:
        s.commit()
        print(f'New Node {node}')
    except pymysql.err.IntegrityError:
        s.rollback()
        print(f'Duplicate Node {node}')
    except sqlalchemy.orm.exc.FlushError:
        s.rollback()
        print(f'FlushError Node {node}')


# node = Mymacnode(ID=23,name="Fastxx G1o")
# s.add(node)
# s.commit()
# node = Mymacnode(ID=25,name="Fastxx G1o")
# s.add(node)
# s.commit()
nodelist = s.query(Mymacnode).all()
for row in nodelist:
    print(row.ID, row.Address)
print('query again!')
print(nodelist)
nodelist1 = s.query(Mymacnode).filter(Mymacnode.ID>99).all()
for row in nodelist1:
    print(row.ID, row.Address)

for i in range(100):
    node = Mymacnode()
    node.ID = i + 100
    node.Address = f'MAN.11111111111{i * 9}'
    node.Balance = 3000 + 100 * random.randint(1, 200)
    node.parentID = 0
    node.parentAddress = None
    node.name = f"mac{i}"
    node.tel = f'{i + 1380013800}'
    node.email = None

    s.add(node)
    try:
        s.commit()
        print(f'New Node {node}')
    except pymysql.err.IntegrityError:
        s.rollback()
        print(f'Duplicate Node {node}')
    except sqlalchemy.orm.exc.FlushError:
        s.rollback()
        print(f'FlushError Node {node}')

nodelist = s.query(Mymacnode).all()
for row in nodelist:
    print(row.ID, row.Address)


# lucy = Mymacnode(name='lucy', fullname='lucy.F', password='asdf')
# s.add(lucy)
# s.commit()

# users = [Mymacnode(name='maven', fullname='maven.sms', password='1234'),
#          Mymacnode(name='fang', fullname='zhang fang', password='lkjhsd')]
# s.add_all(users)
# s.commit()

s.close()
