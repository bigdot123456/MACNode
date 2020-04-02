from sqlalchemy import create_engine
from MACNodeSQL import Tab2
from sqlalchemy.orm import sessionmaker
# 连接本地test数据库
engine = create_engine("mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8")
# 创建会话
session = sessionmaker(engine)
mySession = session()
# 查询结果集
result = mySession.query(Tab2).all()
print(result[0])
result = mySession.query(Tab2).first()
print(result.name) #打印对象属性
result = mySession.query(Tab2).filter_by(nid=1).first()
print(result.nid)
result = mySession.query(Tab2).filter(Tab2.nid==3).first()
print(result.nid)
# 分页查询 0,2
result = mySession.query(Tab2).filter(Tab2.nid>1).limit(2).offset(0).all()
print(result)
# 自定义过滤条件
result = mySession.query(Tab2).get(3)
print(result.name)
# 新增
news = Tab2(name="Fast Go")
mySession.add(news)
mySession.commit()
#修改
mySession.query(Tab2).filter(Tab2.nid==3).update({"name":"fastroot"})
mySession.commit()