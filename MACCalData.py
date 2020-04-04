import heapq
import sys
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from MACNodeSQL import *
from const import *

sys.setrecursionlimit(1000000)

Nums = Constants(
    VipStdBalance=50000,
    moneyInput=[300, 1000, 2000, 4000],
    dayLimited=[0.01, 0.011, 0.013, 0.015],
    totalUSDT=[600, 2500, 6000, 14000],
    rateSon=0.5,
    rateGradnSon=0.2,
    withdrawlRate=0.7
)


# print(Nums.VipStdBalance)

# 连接本地test数据库
# engine = create_engine("mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8",echo=True)
# session = sessionmaker(engine)
# 查询结果集, 对象模式，需要取出具体数据
# result = s.query(Stdmacnode).all()

# ID = Column(INTEGER(11), primary_key=True)
# Address = Column(String(32), nullable=False, server_default=text("'MAN.11111111111'"))
# Balance = Column(INTEGER(11), server_default=text("'0'"))
# parentID = Column(INTEGER(11))
# parentAddress = Column(String(32))
# name = Column(String(32), server_default=text("'MACMAN'"))
# tel = Column(String(11), server_default=text("'13800138000'"))
# email = Column(String(64))
# attendRound = Column(INTEGER(11))
# subNodeNum = Column(INTEGER(11))
# level = Column(INTEGER(11))
# IDleft = Column(INTEGER(11))
# IDright = Column(INTEGER(11))
# vipTag = Column(INTEGER(11))
# untilNowIncome = Column(INTEGER(11))
# staticIncome = Column(INTEGER(11))
# subStaticIncome = Column(INTEGER(11))
# dynamicIncome = Column(INTEGER(11))
# withdrawStatus = Column(INTEGER(11))


class macnode:
    engine = None
    s = None
    nodeList = []
    # tempNode=Stdmacnode() ## tempNode
    indexOfAddress = []
    indexOfBalance = []
    indexOfID = []
    IDindexDict = {}
    indexOfparentID = []
    IDparentIDdict = {}
    IDAddressdict = {}
    IDBalancedict = {}
    indexOfparentAddress = []
    indexOfNodeLevel = []
    IDNodeLeveldict = {}

    def __init__(self):

        print('init Node info')

    def initDB(self):
        self.engine = create_engine("mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8")
        # 创建会话
        session = sessionmaker(self.engine)
        self.s = session()

    def closDB(self):
        self.s.close()

    def LoadSQLData(self):
        t0 = time.time()
        # self.nodeList = self.s.query(Stdmacnode).filter(text("ID < :value AND parentID = :pValue")).params(value=100, pValue=1)

        # self.nodeList = self.s.query(Stdmacnode).filter(text("ID < :value ")).params(value=1000).order_by(
        #     Stdmacnode.Balance.desc())

        self.nodeList = self.s.query(Stdmacnode).filter(text("ID < :value ")).params(value=1000).order_by(
            Stdmacnode.Balance.desc())
        ## for test aim, we reshuffle it! desc() means order reverse
        ## self.NodeList = self.NodeList[::2]+self.NodeList[1::2] ## error! since query object is not a list
        print(f"SQLAlchemy ORM query(): Total time for 100 records {(time.time() - t0)}  secs")

        # self.nodeList = self.s.query(Stdmacnode).all()
        # print(f"SQLAlchemy ORM query(): Total time for {len(self.nodeList)} records {(time.time() - t0)}  secs")

    def print(self):
        for x in self.nodeList:
            print(f"ID:{x.ID}  Balance:{x.Balance} vip:{x.vipTag} income:{x.untilNowIncome}")

    def genIndexbyID(self):
        self.indexOfID = []
        self.IDindexDict = {}
        pos = 0
        for x in self.nodeList:
            self.indexOfID.append(x.ID)
            self.IDindexDict[x.ID] = pos
            pos = pos + 1

    def genIndexbyAddress(self):
        self.indexOfAddress = []
        for x in self.nodeList:
            self.indexOfAddress.append(x.Address)

    def genIndexbyBalance(self):
        self.indexOfBalance = []
        for x in self.nodeList:
            self.indexOfBalance.append(x.Balance)

    def genIDparentIDdict(self):
        self.IDparentIDdict = {}
        for x in self.nodeList:
            self.IDparentIDdict[x.ID] = x.parentID

    def genIDAddressdict(self):
        self.IDAddressdict = {}
        for x in self.nodeList:
            self.IDAddressdict[x.ID] = x.Address

    def genIDBalancedict(self):
        self.IDBalancedict = {}
        for x in self.nodeList:
            self.IDBalancedict[x.ID] = x.Balance

    def genIndexbyparentID(self):
        self.indexOfparentID = []
        for x in self.nodeList:
            self.indexOfparentID.append(x.parentID)

    def genIndexbyparentAddress(self):
        self.indexOfparentAddress = []
        for x in self.nodeList:
            debugX = self.IDAddressdict[x.parentID]
            self.indexOfparentAddress.append(debugX)

    def getNodeLevelbyID(self, ID):
        if ID == 0:
            return 0
        else:
            return 1 + self.getNodeLevelbyID(self.IDparentIDdict[ID])

    def genIndexbyNodeLevel(self):
        self.indexOfNodeLevel = []
        self.IDNodeLeveldict = {}
        for x in self.indexOfID:
            level = self.getNodeLevelbyID(x)
            self.indexOfNodeLevel.append(level)
            self.IDNodeLeveldict[x] = level

    def getsubNodeNumberbyID(self, ID):
        subNodeNumber = 0
        subNodeIndex = self.indexOfparentID.index(ID)
        if subNodeIndex is None:
            subNodeNumber = 0
        else:
            subNodeList = self.indexOfID[subNodeIndex]
            for x in subNodeList:
                subNodeNumber = subNodeNumber + self.getsubNodeNumberbyID(x.ID)

        return subNodeNumber

    def getNodebyID(self, ID):
        # IDPos=self.indexOfID.index(ID)
        # IDPos = self.IDindexDict[ID]
        IDPos = self.IDindexDict.get(ID)  ## can avoid exception.
        return self.nodeList[IDPos]

    def getMultiIndex(self, List, value):
        return [i for i, x in enumerate(List) if x == value]

    def getListHit(self, List, posList):
        # return [x for i,x in enumerate(List) if i in posList]
        return [List[x] for x in posList]

    def getTreeBalancebyID(self, ID):
        TreeBalance = 0
        # It contains more indice, so we must use index function, can't utilize dict function
        # subNodeIndex = self.indexOfparentID.index(ID)

        subNodeIndex = self.getMultiIndex(self.indexOfparentID, ID)
        x=self.IDindexDict[ID]
        if x in subNodeIndex:
            subNodeIndex.remove(x)

        if subNodeIndex:
            subNodeList = self.getListHit(self.indexOfID, subNodeIndex)
            for x in subNodeList:
                TreeBalance = TreeBalance + self.getTreeBalancebyID(x)
        else:
            TreeBalance = 0

        return TreeBalance + self.IDBalancedict.get(ID)

    def genIndexbyTreeBalance(self):
        self.indexbyTreeBalance = []

        self.IDTreeBalancedict = {}
        for x in self.indexOfID:
            TreeBalance = self.getTreeBalancebyID(x)
            self.indexbyTreeBalance.append(TreeBalance)
            self.IDTreeBalancedict[x] = TreeBalance

    def getvipTreeBalancebyID(self, ID):
        subvipBalanceList = []
        subNodeIndex = self.indexOfparentID.index(ID)
        if subNodeIndex:
            subNodeList = self.indexOfID[subNodeIndex]
            for x in subNodeList:
                subBalance = self.IDTreeBalancedict.get(x)
                subvipBalanceList.append(subBalance)

                vipBalance = sum(subvipBalanceList) - max(subvipBalanceList)
        else:
            vipBalance = 0

        return vipBalance

    def genIndexbyvipTreeBalance(self):
        self.indexOfvipTreeBalance = []
        self.IDvipTreeBalancedict = {}
        self.indexOfvipTag = []
        for x in self.indexOfID:
            vipBalance = self.getvipTreeBalancebyID(x)
            vipTag = vipBalance >= Nums.VipStdBalance
            self.indexOfvipTreeBalance.append(vipBalance)
            self.IDvipTreeBalancedict[x] = vipBalance
            self.indexOfvipTag.append(vipTag)

    def getvipLevelbyID(self, ID):
        subvipLevelList = []
        subNodeIndex =  self.getMultiIndex(self.indexOfparentID, ID)
        x = self.IDindexDict[ID]
        if x in subNodeIndex:
            subNodeIndex.remove(x)

        if subNodeIndex:
            subNodeList = self.getListHit(self.indexOfID, subNodeIndex)

            for x in subNodeList:
                subvipLevel = self.getvipLevelbyID(x)
                subvipLevelList.append(subvipLevel)

            subvipTop2 = heapq.nlargest(2, subvipLevelList)
            vipLevel = min(subvipTop2)

        else:
            vipLevel = 0

        return vipLevel

    def genIndexbyvipLevel(self):
        self.indexOfvipLevel = []
        self.IDvipLeveldict = {}
        for x in self.indexOfID:
            vipLevel = self.getvipLevelbyID(x)
            self.indexOfvipLevel.append(vipLevel)
            self.IDvipLeveldict[x] = vipLevel

    def getSubNodeIndexbyID(self, ID):
        subNodeIndex = self.indexOfparentID.index(ID)
        return subNodeIndex

    def getstaticIncomebyBalance(self, orginBalance):
        usedBalance = 0
        index = -1
        staticIncome = 0
        for x in Nums.moneyInput:
            if orginBalance < x:
                break
            else:
                index = index + 1

        if index == -1:
            usedBalance = 0
            staticIncome = 0
        else:
            usedBalance = Nums.moneyInput[index]
            staticIncome = usedBalance * Nums.dayLimited[index]

        return usedBalance, index, staticIncome

    def getstaticIncomebyID(self, ID):
        balance, minerLevel, staticIncome = self.getstaticIncomebyBalance(self.IDBalancedict.get(ID))
        return balance, minerLevel, staticIncome

    def genIndexbystaticIncome(self):

        self.indexOfusedBalance = []
        self.indexOfminerLevel = []
        self.indexOfstaticIncome = []
        self.IDminerLeveldict = {}
        self.IDstaticIncomedict = {}
        for x in self.indexOfID:
            usedBalance, minerLevel, staticIncome = self.getstaticIncomebyID(x)
            self.indexOfusedBalance.append(usedBalance)
            self.indexOfminerLevel.append(minerLevel)
            self.indexOfstaticIncome.append(staticIncome)
            self.IDminerLeveldict[x] = minerLevel
            self.IDstaticIncomedict[x] = staticIncome

    def genAllIndex(self):
        self.initDB()
        self.LoadSQLData()
        self.closDB()
        self.genIndexbyID()
        self.genIndexbyAddress()
        self.genIndexbyBalance()
        self.genIDparentIDdict()
        self.genIDAddressdict()
        self.genIDBalancedict()
        self.genIndexbyparentID()
        self.genIndexbyparentAddress()
        self.genIndexbyNodeLevel()
        self.genIndexbyTreeBalance()
        self.genIndexbyvipTreeBalance()
        self.genIndexbyvipLevel()
        self.genIndexbystaticIncome()
        print("Finish genAllIndex test")


if __name__ == "__main__":
    t = macnode()
    print("start test")
    t.genAllIndex()
