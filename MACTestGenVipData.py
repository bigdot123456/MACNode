import random
import time

import pymysql
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from MACNodeSQL import *

# 连接本地test数据库
# engine = create_engine("mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8",echo=True)
engine = create_engine("mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8")
# 创建会话
session = sessionmaker(engine)
s = session()
# 查询结果集, 对象模式，需要取出具体数据
# result = s.query(Mymacnode).all()

## Create root node，which is not used for calculate VIP
node = Mymacnode()
node.ID = 0
node.Address = f'MAN.8888888888'
node.Balance = 10000
node.parentID = 0
node.parentAddress = None
node.name = f"MACROOT"
node.tel = f'{13900139000}'
node.email = f"macroot123@gmail.com"

try:
    result = s.query(Mymacnode).filter(Mymacnode.ID == node.ID).all()
    if (result is None):
        s.add(node)
    else:
        # 不能整体替代，只能每个值替换
        # s.query(Mymacnode).filter(Mymacnode.ID == node.ID).update(node)
        s.query(Mymacnode).filter(Mymacnode.ID == node.ID).delete()
        s.add(node)

    s.commit()
    print(f'New Node {node}')
except pymysql.err.IntegrityError:
    s.rollback()
    print(f'Duplicate Node {node}')
except sqlalchemy.orm.exc.FlushError:
    s.rollback()
    print(f'FlushError Node {node}')
except Exception as result:
    s.rollback()
    print(f'Node take error {node} {result}!')

t0 = time.time()
start = 1
level = 1
stoplist = [10, 100, 500, 2000, 5000, 10000, 20000]
s.query(mymacnode).filter(mymacnode.ID <= stoplist[-1], mymacnode.ID >= start).delete()
s.commit()
print(f'delete {stoplist[-1]} ')
for stop in stoplist:
    # range(start, stop[, step])
    for i in range(start, stop):
        node = Mymacnode()
        node.ID = i #(stop - i) + start
        node.Address = f'MAN.{level}000{i}'
        node.Balance = random.randint(1, 7000)
        node.parentID = random.randint(0, start-1) ## we can change it to i for more strictly test case!
        #node.parentID = random.randint(0, node.ID-1) ## we can change it to i for more strictly test case!
        node.parentAddress = None
        node.name = f"mac{level}{i}"
        node.tel = f'{i * 10 + 1380013800}'
        node.email = None

        s.add(node)
        if i % 1000 == 0:
            s.flush()

    level = level + 1
    start = stop

## batch mode for speed
try:
    # result = s.query(Mymacnode).filter(Mymacnode.ID == node.ID).all()
    # if (result is None):
    #     s.add(node)
    # else:
    #     # 不能整体替代，只能每个值替换
    #     # s.query(Mymacnode).filter(Mymacnode.ID == node.ID).update(node)
    #     s.query(Mymacnode).filter(Mymacnode.ID == node.ID).delete()
    #     s.add(node)

    s.commit()
    print(f'New Node {node} {i}')
except pymysql.err.IntegrityError:
    s.rollback()
    print(f'Duplicate Node {node} {i}')
except sqlalchemy.orm.exc.FlushError:
    s.rollback()
    print(f'FlushError Node {node} {i}')
except Exception as result:
    s.rollback()
    print(f'Node take error {node} {i} {result}!')

print(f"SQLAlchemy ORM add(): Total time for {stoplist[-1]} records {(time.time() - t0)}  secs")

###
# update information


s.close()
