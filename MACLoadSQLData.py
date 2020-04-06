import random
import time

import pymysql
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from MACNodeSQL import *

from const import *

Nums = Constants(
    VipStdBalance=30000,
    moneyInput=[300, 1000, 2000, 4000],
    dayLimited=[0.01, 0.011, 0.013, 0.015],
    totalUSDT=[600, 2500, 6000, 14000],
    vipCoef=[0.1, 0.15, 0.2, 0.25, 0.3],
    rateSon=0.5,
    rateGrandSon=0.2,
    withdrawlRate=0.7,
    sameLevelRate=0.15,
    RootID=1,
    MaxRecords=20000
)


class LoadSQLData():
    t0 = time.time()
    def __init__(self):

        print('Load SQL Data from MySQL....')

    def initDB(self):
        self.engine = create_engine("mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8")
        # 创建会话
        session = sessionmaker(self.engine)
        self.s = session()
        # 查询结果集, 对象模式，需要取出具体数据
        # result = s.query(AssetLoadsqldatum).all()
        self.engine.execute(f"delete from asset_loadsqldata where ID >1; ")
        print(f'delete All record in table')

    def closDB(self):
        self.s.close()

    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key)
                    for c in sqlalchemy.inspection.inspect(obj).mapper.column_attrs}

    def LoadSQLData(self):

        # self.nodeList = self.s.query(AssetLoadsqldatum).filter(text("ID < :value AND parentID = :pValue")).params(value=100, pValue=1)

        # self.nodeList = self.s.query(AssetLoadsqldatum).filter(text("ID < :value ")).params(value=1000).order_by(
        #     AssetLoadsqldatum.Balance.desc())

        #self.nodeList = self.s.query(AssetLoadsqldatum).filter(text("ID < :value ")).params(value=Nums.MaxRecords).order_by(AssetLoadsqldatum.Balance.desc())
        ## for test aim, we reshuffle it! desc() means order reverse
        ## self.NodeList = self.NodeList[::2]+self.NodeList[1::2] ## error! since query object is not a list
        ## load asset_fund

        # #UserList=s.query(User)
        # UserList=s.query(User).all()
        # UserListdict = [u.__dict__ for u in UserList]
        # print(UserListdict)
        # UserListdict1 = [u._asdict() for u in UserList]
        # print(UserListdict1)

        FundList = self.s.query(AssetFund).all()
        UserList = self.s.query(User).all()
        BaseList = self.s.query(AssetBase).all()
        print(f"SQLAlchemy ORM query(): Total time for {Nums.MaxRecords} records {(time.time() - self.t0)}  secs")
        FundListdict1 = [u._asdict() for u in FundList]
        UserListdict1 = [u._asdict() for u in UserList]
        BaseListdict1 = [u._asdict() for u in BaseList]

        self.sortedFundListdict = sorted(FundListdict1, key=lambda k: k['userid'])  ## total 54
        self.sortedUserListdict = sorted(UserListdict1, key=lambda k: k['phone'])  ## total 135
        self.sortedBaseListdict = sorted(BaseListdict1, key=lambda k: k['phone'])  ## total 136

        # 根据 userid/phone/phone建立字典，方便快速查找

        self.IndexOfFund = self.build_dict(self.sortedFundListdict, key="userid")
        self.IndexOfUser = self.build_dict(self.sortedUserListdict, key="phone")
        self.IndexOfBase = self.build_dict(self.sortedBaseListdict, key="phone")


        # self.nodeList = self.s.query(AssetLoadsqldatum).all()
        print(f"sorted: Total time for {Nums.MaxRecords} records {(time.time() - self.t0)}  secs")
        # print(f"SQLAlchemy ORM query(): Total time for {len(self.nodeList)} records {(time.time() - self.t0)}  secs")

    def build_dict(self,seq, key):
        return dict((d[key], dict(d, index=i)) for (i, d) in enumerate(seq))

    def saveData(self):

        # copy data from fund, and integrate userlist
        FundNum=len(self.sortedFundListdict)
        print(f"sorted: Total time for FundNum:{FundNum} records {(time.time() - self.t0)}  secs")
        i=1
        for x in self.sortedFundListdict:
            node = AssetLoadsqldatum() # should in loop, otherwise it will overlap all record and only 1 in database
            node.fund = x['fund']
            node.static = x['static']
            node.dynamic = x['dynamic']
            node.status = x['status']
            node.fundtype = x['fundtype']
            node.userid = x['userid']
            node.starttime = x['starttime']
            node.stoptime = x['stoptime']
            node.lastdayinterest = x['lastdayinterest']
            node.gas = x['gas']
            node.attribute = x['attribute']
            node.production = x['production']
            node.updatetime = x['updatetime']

            y=self.IndexOfUser.get(node.userid) ## it will contain a dict, y[-1] contains index in node.user.id

            node.name=y['name']
            node.phone=y['phone']
            node.email=y['email']
            node.password=y['password']
            node.code=y['code']
            node.mycode=y['mycode']

            node.paypassword=y['paypassword']
            node.status=y['status']
            node.registertime=y['registertime']
            node.countryCode=y['countryCode']
            node.signtime=y['signtime']

            z=self.IndexOfBase.get(node.userid)

            node.ethaddress = z['ethaddress']
            node.tokenbalance = z['tokenbalance']
            node.usdtbalance = z['usdtbalance']
            node.lockbalance = z['lockbalance']
            node.tokenaddress = z['tokenaddress']
            node.macbalance = z['macbalance']

            i=i+1
            self.s.add(node)
            if i % 1000 == 0:
                self.s.flush()

        ## batch mode for speed
        try:
            # result = s.query(AssetLoadsqldatum).filter(AssetLoadsqldatum.ID == node.ID).all()
            # if (result is None):
            #     s.add(node)
            # else:
            #     # 不能整体替代，只能每个值替换
            #     # s.query(AssetLoadsqldatum).filter(AssetLoadsqldatum.ID == node.ID).update(node)
            #     s.query(AssetLoadsqldatum).filter(AssetLoadsqldatum.ID == node.ID).delete()
            #     s.add(node)

            self.s.commit()
            print(f'New Node  {i}')
        except pymysql.err.IntegrityError:
            self.s.rollback()
            print(f'Duplicate Node  {i}')
        except sqlalchemy.orm.exc.FlushError:
            self.s.rollback()
            print(f'FlushError Node  {i}')
        except Exception as result:
            self.s.rollback()
            print(f'Node take error {i} {result}!')

        print(f"SQLAlchemy ORM add(): Total time for all records {(time.time() - self.t0)}  secs")

if __name__ == "__main__":
    t = LoadSQLData()
    print("start test ...")
    t.initDB()
    t.LoadSQLData()
    t.closDB()
    t.saveData()


