import time

import pymysql
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


class CheckSQLData():
    t0 = time.time()
    indexOfsubNodeListIndex=[]

    def __init__(self):

        print('Load SQL Data from MySQL....')

    def initDB(self):
        self.engine = create_engine("mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8")
        # 创建会话
        session = sessionmaker(self.engine)
        self.s = session()
        # 查询结果集, 对象模式，需要取出具体数据
        # result = s.query(AssetLoadsqldatum).all()
        self.engine.execute(f"delete from asset_checkresultpython where ID >0; ")
        # print(f'delete All record in table')

    def closDB(self):
        self.s.close()

    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key)
                for c in sqlalchemy.inspection.inspect(obj).mapper.column_attrs}

    def LoadSQLData(self):

        FundList = self.s.query(AssetLoadsqldatum).all()

        print(f"SQLAlchemy ORM query(): Total time for {Nums.MaxRecords} records {(time.time() - self.t0)}  secs")
        FundListdict1 = [u._asdict() for u in FundList]

        self.sortedMycodeListdict = sorted(FundListdict1, key=lambda k: k['mycode'])  ## total 54

        # 根据 userid/phone/phone建立字典，方便快速查找
        self.IndexOfMycode = self.build_dict(self.sortedMycodeListdict, key="mycode")
        # 考虑到层级关系，还需要建立mycode的字典，方便查找上下级关系，所以 mycode 是关键index

        print(f"sorted: Total time for {Nums.MaxRecords} records {(time.time() - self.t0)}  secs")
        # print(f"SQLAlchemy ORM query(): Total time for {len(self.nodeList)} records {(time.time() - self.t0)}  secs")

    def build_dict(self, seq, key):
        return dict((d[key], dict(d, index=i)) for (i, d) in enumerate(seq))

    def saveData(self):

        # copy data from fund, and integrate userlist
        FundNum = len(self.sortedMycodeListdict)
        print(f"sorted: Total time for FundNum:{FundNum} records {(time.time() - self.t0)}  secs")
        i = 1
        for x in self.sortedMycodeListdict:
            node = AssetCheckresultpython()  # should in loop, otherwise it will overlap all record and only 1 in database
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

            node.name = x['name']
            node.phone = x['phone']
            node.email = x['email']
            node.password = x['password']
            node.code = x['code']
            node.mycode = x['mycode']

            node.paypassword = x['paypassword']
            node.status = x['status']
            node.registertime = x['registertime']
            node.countryCode = x['countryCode']
            node.signtime = x['signtime']

            node.ethaddress = x['ethaddress']
            node.tokenbalance = x['tokenbalance']
            node.usdtbalance = x['usdtbalance']
            node.lockbalance = x['lockbalance']
            node.tokenaddress = x['tokenaddress']
            node.macbalance = x['macbalance']

            i = i + 1
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

    def getsubNodeListIndexbyNodeIndex(self, NodeIndex):

        # subNodeListIndex = []
        # It contains more indice, so we must use index function, can't utilize dict function
        # subNodeIndex = self.indexOfparentID.index(ID)

        subNodeListIndex = [i for i, x in enumerate(self.sortedMycodeListdict) if
                            x['code'] == self.sortedMycodeListdict[NodeIndex]['mycode']]

        if NodeIndex in subNodeListIndex:
            subNodeListIndex.remove(NodeIndex)

        return subNodeListIndex

    def genIndexbysubNodeListIndex(self):
        self.indexOfsubNodeListIndex=[]
        for x in range(len(self.sortedMycodeListdict)):
            y=self.getsubNodeListIndexbyNodeIndex(x)
            self.indexOfsubNodeListIndex.append(y)
        print(f"genIndexbysubNodeListIndex: Total time for all records {(time.time() - self.t0)}  secs")

    def getsubNodeListbyNode(self, Node):

        subNodeList = []
        # It contains more indice, so we must use index function, can't utilize dict function
        # subNodeIndex = self.indexOfparentID.index(ID)

        subNodeListIndex = [i for i, x in enumerate(self.sortedMycodeListdict) if x['code'] == Node['mycode']]

        z = self.IndexOfMycode.get(Node['mycode'])
        i= z['index']

        if i in subNodeListIndex:
            subNodeListIndex.remove(i)

        for x in subNodeListIndex:
            subNodeList.append(self.sortedMycodeListdict[x])

        return subNodeList

    def getNodeLevelbyMycode(self, Mycode):
        # prime key should start with 1
        DictMycode = self.IndexOfMycode.get(Mycode)
        if DictMycode:
            parentID = DictMycode.get('code')

            if not parentID:
                return 0

            if (parentID == Mycode):
                print(f"Find Root Node with {Mycode}")
                return 0
            else:
                return 1 + self.getNodeLevelbyMycode(parentID)
        else:
            return 0

    def genIndexbyNodeLevel(self):
        self.indexOfNodeLevel = []
        self.IDNodeLeveldict = {}
        for x in self.sortedMycodeListdict:
            y = x['mycode']
            level = self.getNodeLevelbyMycode(y)
            self.indexOfNodeLevel.append(level)
            self.IDNodeLeveldict[y] = level

        print(f"genIndexbyNodeLevel: Total time for all records {(time.time() - self.t0)}  secs")

    def getMultiIndex(self, List, value):
        return [i for i, x in enumerate(List) if x == value]


    def getDictMultiIndex(self, List, key, value):
        return [i for i, x in enumerate(List) if x[key] == value]


    def getListHit(self, List, posList):
        # return [x for i,x in enumerate(List) if i in posList]
        return [List[x] for x in posList]


    def getTreeBalancebyMycode(self, Mycode):
        TreeBalance = 0
        # It contains more indice, so we must use index function, can't utilize dict function
        # subNodeIndex = self.indexOfparentID.index(ID)

        subNodeIndex = self.getDictMultiIndex(self.sortedMycodeListdict, 'code', Mycode)

        z = self.IndexOfMycode.get(Mycode)
        i= z['index']

        if i in subNodeIndex:
            subNodeIndex.remove(i)

        if subNodeIndex:

            for x in subNodeIndex:
                y = self.IndexOfMycode[x]
                TreeBalance = TreeBalance + self.getTreeBalancebyMycode(y)
        else:
            TreeBalance = 0

        return TreeBalance + z['fund']


    def getTreeBalancebyNode(self, Node):
        TreeBalance = 0
        # It contains more indice, so we must use index function, can't utilize dict function
        # subNodeIndex = self.indexOfparentID.index(ID)

        subNodeIndex = [i for i, x in enumerate(self.sortedMycodeListdict) if x['code'] == Node['mycode']]

        z = self.IndexOfMycode.get(Node['mycode'])
        i= z['index']
        if i in subNodeIndex:
            subNodeIndex.remove(i)

        if subNodeIndex:
            for x in subNodeIndex:
                y = self.sortedMycodeListdict[x]
                TreeBalance = TreeBalance + self.getTreeBalancebyNode(y)
        else:
            TreeBalance = 0

        return TreeBalance + Node['fund']


    def genIndexbyTreeBalance(self):
        self.indexOfTreeBalance = []

        self.IDTreeBalancedict = {}
        for x in self.sortedMycodeListdict:
            # TreeBalance = self.getTreeBalancebyMycode(x)
            TreeBalance = self.getTreeBalancebyNode(x)
            self.indexOfTreeBalance.append(TreeBalance)
            self.IDTreeBalancedict[x['mycode']] = TreeBalance

        print(f"genIndexbyTreeBalance: Total time for all records {(time.time() - self.t0)}  secs")


if __name__ == "__main__":
    t = CheckSQLData()
    print("start test ...")
    t.initDB()
    t.LoadSQLData()
    t.closDB()
    t.genIndexbysubNodeListIndex()
    print(t.indexOfsubNodeListIndex)
    t.genIndexbyNodeLevel()
    t.genIndexbyTreeBalance()
    # t.saveData()
