import datetime
import heapq
import sys
import time

import pymysql
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from MACNodeSQL import *
from const import *

sys.setrecursionlimit(10000)

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


# print(Nums.VipStdBalance)

# 连接本地test数据库
# engine = create_engine("mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8",echo=True)
# session = sessionmaker(engine)
# 查询结果集, 对象模式，需要取出具体数据
# result = s.query(Mymacnode).all()

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

    indexOfID = []
    indexOfAddress = []
    indexOfBalance = []
    indexOfparentID = []
    indexOfparentAddress = []
    indexOfNodeLevel = []
    indexOfTreeBalance = []

    indexOfvipTreeBalance = []
    indexOfvipTag = []
    indexOfvipLevel = []
    indexOfusedBalance = []
    indexOfminerProductive = []
    indexOfstaticIncome = []
    indexOfstaticIncomeTree = []
    indexOfMinerAward = []
    indexOfRecommendAward = []

    indexOfTotalAward = []

    IDindexDict = {}
    IDparentIDdict = {}
    IDAddressdict = {}
    IDBalancedict = {}
    IDNodeLeveldict = {}
    IDTreeBalancedict = {}
    IDvipTreeBalancedict = {}
    IDvipLeveldict = {}
    IDminerProductivedict = {}
    IDstaticIncomedict = {}
    IDstaticIncomeTreedict = {}
    IDMinerAwarddict = {}
    IDRecommendAwarddict = {}
    IDTotalAwarddict = {}

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
        # self.nodeList = self.s.query(Mymacnode).filter(text("ID < :value AND parentID = :pValue")).params(value=100, pValue=1)

        # self.nodeList = self.s.query(Mymacnode).filter(text("ID < :value ")).params(value=1000).order_by(
        #     Mymacnode.Balance.desc())

        self.nodeList = self.s.query(Mymacnode).filter(text("ID < :value ")).params(value=Nums.MaxRecords).order_by(
            Mymacnode.Balance.desc())
        ## for test aim, we reshuffle it! desc() means order reverse
        ## self.NodeList = self.NodeList[::2]+self.NodeList[1::2] ## error! since query object is not a list
        print(f"SQLAlchemy ORM query(): Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")

        # self.nodeList = self.s.query(Mymacnode).all()
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
            try:
                debugX = self.IDAddressdict[x.parentID]
            except:
                print(f"{x.parentID} is not exists")
                debugX=Nums.RootID

            self.indexOfparentAddress.append(debugX)

    def getNodeLevelbyID(self, ID):
        # prime key should start with 1
        if ID == Nums.RootID:
            return 0
        else:
            #parentID=self.IDparentIDdict[ID]
            parentID = self.IDparentIDdict.get(ID)

            if(parentID==ID or parentID is None):
                print(f"Find new Node with {ID}")
                return 0
            else:
                return 1 + self.getNodeLevelbyID(parentID)

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
        # IDPos = self.IDindexDict.get(ID)
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
        x = self.IDindexDict.get(ID)
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
        self.indexOfTreeBalance = []

        self.IDTreeBalancedict = {}
        for x in self.indexOfID:
            TreeBalance = self.getTreeBalancebyID(x)
            self.indexOfTreeBalance.append(TreeBalance)
            self.IDTreeBalancedict[x] = TreeBalance

    def getvipTreeBalancebyID(self, ID):
        vipBalance = 0
        subvipBalanceList = []
        subNodeIndex = self.getMultiIndex(self.indexOfparentID, ID)
        x = self.IDindexDict.get(ID)

        if x in subNodeIndex:
            subNodeIndex.remove(x)

        if subNodeIndex:
            subNodeList = self.getListHit(self.indexOfID, subNodeIndex)

            for y in subNodeList:
                subBalance = self.IDTreeBalancedict.get(y)
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
        subNodeIndex = self.getMultiIndex(self.indexOfparentID, ID)
        x = self.IDindexDict.get(ID)
        vipbase = self.indexOfvipTag[x] + 0

        if x in subNodeIndex:
            subNodeIndex.remove(x)

        if subNodeIndex:
            subNodeList = self.getListHit(self.indexOfID, subNodeIndex)

            for y in subNodeList:
                subvipLevel = self.getvipLevelbyID(y)
                subvipLevelList.append(subvipLevel)

            subvipTop2 = heapq.nlargest(2, subvipLevelList)
            subvipLevel = min(subvipTop2)
            vipLevel = max(subvipLevel, vipbase)
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
        # usedBalance = 0
        # staticIncome = 0
        # minerProductive=0
        index = -1
        for x in Nums.moneyInput:
            if orginBalance < x:
                break
            else:
                index = index + 1

        if index == -1:
            usedBalance = 0
            staticIncome = 0
            minerProductive = 0
        else:
            usedBalance = Nums.moneyInput[index]
            minerProductive = Nums.dayLimited[index]
            staticIncome = usedBalance * minerProductive

        return usedBalance, minerProductive, staticIncome

    def getstaticIncomebyID(self, ID):
        balance, minerProductive, staticIncome = self.getstaticIncomebyBalance(self.IDBalancedict.get(ID))
        return balance, minerProductive, staticIncome

    def genIndexbystaticIncome(self):

        self.indexOfusedBalance = []
        self.indexOfminerProductive = []
        self.indexOfstaticIncome = []
        self.IDminerProductivedict = {}
        self.IDstaticIncomedict = {}
        for x in self.indexOfID:
            usedBalance, minerProductive, staticIncome = self.getstaticIncomebyID(x)
            self.indexOfusedBalance.append(usedBalance)
            self.indexOfminerProductive.append(minerProductive)
            self.indexOfstaticIncome.append(staticIncome)
            self.IDminerProductivedict[x] = minerProductive
            self.IDstaticIncomedict[x] = staticIncome

    def getstaticIncomeTreebyID(self, ID):
        subNodeIndex = self.getMultiIndex(self.indexOfparentID, ID)
        staticIncomeTree = 0
        x = self.IDindexDict.get(ID)

        if x in subNodeIndex:
            subNodeIndex.remove(x)

        if subNodeIndex:
            subNodeList = self.getListHit(self.indexOfID, subNodeIndex)

            for y in subNodeList:
                staticIncomeTree = staticIncomeTree + self.getstaticIncomeTreebyID(y)
        else:

            # staticIncomeTree=self.IDstaticIncomedict[ID]
            staticIncomeTree = self.indexOfstaticIncome[x]

        return staticIncomeTree

    def getMinerCoeffbyvipLevel(self, vipLevel):
        if (vipLevel == 0):
            minerCoeff = 0
        elif (vipLevel == 1):
            minerCoeff = 0.1
        elif (vipLevel == 2):
            minerCoeff = 0.15
        elif (vipLevel == 3):
            minerCoeff = 0.2
        elif (vipLevel == 4):
            minerCoeff = 0.25
        elif (vipLevel == 5):
            minerCoeff = 0.3
        else:
            minerCoeff = 0
            raise Exception("Invalid level!", minerCoeff)

        return minerCoeff

    def genIndexbystaticIncomeTree(self):
        self.indexOfstaticIncomeTree = []
        self.IDstaticIncomeTreedict = {}
        for x in self.indexOfID:
            staticIncomeTree = self.getstaticIncomeTreebyID(x)
            staticIncomeTreeSum = staticIncomeTree * self.getMinerCoeffbyvipLevel(self.IDvipLeveldict[x])
            self.indexOfstaticIncomeTree.append(staticIncomeTreeSum)
            self.IDstaticIncomeTreedict[x] = staticIncomeTreeSum

    def getMinerAwardbyID(self, ID):
        vipLevel = self.IDvipLeveldict[ID]
        if vipLevel == 0:
            return 0

        minerCoeff = self.getMinerCoeffbyvipLevel(vipLevel)

        subNodeIndex = self.getMultiIndex(self.indexOfparentID, ID)
        x = self.IDindexDict.get(ID)
        if x in subNodeIndex:
            subNodeIndex.remove(x)

        subNodeList = []
        grandsonNodeList = []
        MinerAward = 0
        # can use zip function and depth to optimize code size
        if subNodeIndex:
            subNodeList = self.getListHit(self.indexOfID, subNodeIndex)
            while subNodeList:
                y = subNodeList[-1]
                subNodeList.pop()
                subvipLevel = self.IDvipLeveldict[y]

                if vipLevel > subvipLevel:
                    # caculate normal static revenue
                    revenue = self.IDBalancedict[y] * minerCoeff - self.getMinerAwardbyID(y)
                    if revenue < 0:
                        revenue = 0

                    grandsonNodeList = self.getMultiIndex(self.indexOfparentID, y)
                    Indexy = self.IDindexDict[y]
                    if Indexy in grandsonNodeList:
                        grandsonNodeList.remove(Indexy)
                    if grandsonNodeList:
                        grandsonNodeList.extend(grandsonNodeList)

                elif vipLevel == subvipLevel:
                    revenue = self.getMinerAwardbyID(y) * Nums.sameLevelRate
                else:
                    revenue = 0

                MinerAward = MinerAward + revenue

            subNodeList = grandsonNodeList
            while subNodeList:
                y = subNodeList[-1]
                subNodeList.pop()
                subvipLevel = self.IDvipLeveldict[y]

                if vipLevel > subvipLevel:
                    # caculate normal static revenue
                    # revenue = self.IDBalancedict[y] * minerCoeff - self.getMinerAwardbyID(y)
                    revenue = self.IDstaticIncomedict[y] * minerCoeff - self.getMinerAwardbyID(y)

                    if revenue < 0:
                        revenue = 0
                        raise Exception("error for calculat revenue")

                    grandsonNodeList = self.getMultiIndex(self.indexOfparentID, y)
                    Indexy = self.IDindexDict[y]
                    if Indexy in grandsonNodeList:
                        grandsonNodeList.remove(Indexy)
                    if grandsonNodeList:
                        subNodeList.extend(grandsonNodeList)

                elif vipLevel == subvipLevel:
                    revenue = 0
                else:
                    revenue = 0

                MinerAward = MinerAward + revenue

        else:
            MinerAward = 0
            raise Exception("error for calculat revenue since subnodelist is empty")

        return MinerAward

    def getTotalAwardbyID(self, ID):

        x = self.IDindexDict.get(ID)
        TotalAward = self.indexOfRecommendAward[x] + self.indexOfstaticIncome[x] + self.indexOfMinerAward[x]
        return TotalAward

    def genIndexbyTotalAward(self):
        self.indexOfTotalAward = []
        self.IDTotalAwarddict = {}
        for x in self.indexOfID:
            TotalAward = self.getTotalAwardbyID(x)
            self.indexOfTotalAward.append(TotalAward)
            self.IDTotalAwarddict[x] = TotalAward

    def genIndexbyMinerAward(self):
        self.indexOfMinerAward = []
        self.IDMinerAwarddict = {}
        for x in self.indexOfID:
            MinerAward = self.getMinerAwardbyID(x)
            self.indexOfMinerAward.append(MinerAward)
            self.IDMinerAwarddict[x] = MinerAward

    def genIndexbyRecommendAward(self):
        self.indexOfRecommendAward = []
        self.IDRecommendAwarddict = {}
        for x in self.indexOfID:
            RecommendAward = self.getRecommendAwardbyID(x)
            self.indexOfRecommendAward.append(RecommendAward)
            self.IDRecommendAwarddict[x] = RecommendAward

    def getRecommendAwardbyID(self, ID):

        subNodeIndex = self.getMultiIndex(self.indexOfparentID, ID)
        x = self.IDindexDict.get(ID)
        if x in subNodeIndex:
            subNodeIndex.remove(x)

        RecommmendLevel = len(subNodeIndex)
        if RecommmendLevel == 0:
            return 0
        elif (RecommmendLevel < 3):
            recommendAward = 0
            minerProductiveX = self.indexOfminerProductive[x]
            BalanceX = self.indexOfusedBalance[x]

            # subNodeList = self.getListHit(self.indexOfID, subNodeIndex)
            for y in subNodeIndex:
                minerProductiveY = self.indexOfminerProductive[y]
                BalanceY = self.indexOfusedBalance[y]
                recommendAward = recommendAward + min(minerProductiveY, minerProductiveX) * min(BalanceY,
                                                                                                BalanceX) * Nums.rateSon
        else:
            recommendAward = 0
            minerProductiveX = self.indexOfminerProductive[x]
            BalanceX = self.indexOfusedBalance[x]

            grandsonNodeIndex = []

            # subNodeList = self.getListHit(self.indexOfID, subNodeIndex)
            for y in subNodeIndex:
                minerProductiveY = self.indexOfminerProductive[y]
                BalanceY = self.indexOfusedBalance[y]
                recommendAward = recommendAward + min(minerProductiveY, minerProductiveX) * min(BalanceY,
                                                                                                BalanceX) * Nums.rateSon

                subNodeIndexY = self.getMultiIndex(self.indexOfparentID, self.IDindexDict.get(y))
                if y in subNodeIndexY:
                    subNodeIndexY.remove(y)

                if subNodeIndexY:
                    grandsonNodeIndex.extend(subNodeIndexY)

            subNodeIndex = grandsonNodeIndex
            for y in subNodeIndex:
                minerProductiveY = self.indexOfminerProductive[y]
                BalanceY = self.indexOfusedBalance[y]
                recommendAward = recommendAward + min(minerProductiveY, minerProductiveX) * min(BalanceY,
                                                                                                BalanceX) * Nums.rateGrandSon

        return recommendAward

    def genAllIndex(self):
        t0=time.time()
        self.initDB()
        self.LoadSQLData()
        self.closDB()
        self.genIndexbyID()
        self.genIndexbyAddress()
        self.genIndexbyBalance()
        print(f"genIndexbyBalance: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIDparentIDdict()
        print(f"genIDparentIDdict: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIDAddressdict()
        print(f"genIDAddressdict: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIDBalancedict()
        print(f"genIDBalancedict: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIndexbyparentID()
        print(f"genIndexbyparentID: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIndexbyparentAddress()
        print(f"genIndexbyparentAddress: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIndexbyNodeLevel()
        print(f"genIndexbyNodeLevel: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIndexbyTreeBalance()
        print(f"genIndexbyTreeBalance: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIndexbyvipTreeBalance()
        print(f"genIndexbyvipTreeBalance: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIndexbyvipLevel()
        print(f"genIndexbyvipLevel: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIndexbystaticIncome()
        print(f"genIndexbystaticIncome: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIndexbystaticIncomeTree()
        print(f"genIndexbystaticIncomeTree: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIndexbyRecommendAward()
        print(f"genIndexbyRecommendAward: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIndexbyMinerAward()
        print(f"genIndexbyMinerAward: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        self.genIndexbyTotalAward()
        print(f"genIndexbyTotalAward: Total time for {Nums.MaxRecords} records {(time.time() - t0)}  secs")
        print("Finish genAllIndex test")

    def newdateTable(self):
        self.initDB()
        dboldName = "Mymacnode"
        today = datetime.datetime.now()
        tabNow = today.strftime("%Y%m%d")
        dbnewName = f"{dboldName}{tabNow}"
        self.engine.execute(f"CREATE  TABLE IF NOT EXISTS {dbnewName} (LIKE {dboldName} ); ")

        self.closDB()

    def saveDataToDB(self):
        t0 = time.time()
        print(f'delete last result with  Mymacnoderesult')

        self.s.query(Mymacnoderesult).filter(Mymacnoderesult.ID < 2000).delete()
        # s.query(Mymacnode).filter(Mymacnode.ID < stop, Mymacnode.ID >= start).delete()
        # self.s.commit()
        print(f'delete Mymacnoderesult finished! ')
        i = 0
        for i in range(len(self.indexOfID)):
            node = Mymacnoderesult()

            node.ID = self.indexOfID[i]
            node.Address = self.indexOfAddress[i]
            node.Balance = self.indexOfBalance[i]
            node.parentID = self.indexOfparentID[i]
            node.parentAddress = self.indexOfparentAddress[i]
            node.NodeLevel = self.indexOfNodeLevel[i]
            node.TreeBalance = self.indexOfTreeBalance[i]

            node.vipTreeBalance = self.indexOfvipTreeBalance[i]
            node.vipTag = self.indexOfvipTag[i]

            node.vipLevel = self.indexOfvipLevel[i]
            node.usedBalance = self.indexOfusedBalance[i]
            node.minerProductive = self.indexOfminerProductive[i]
            node.staticIncome = self.indexOfstaticIncome[i]

            node.staticIncomeTree = self.indexOfstaticIncomeTree[i]
            node.MinerAward = self.indexOfMinerAward[i]
            node.RecommendAward = self.indexOfRecommendAward[i]
            node.TotalAward = self.indexOfTotalAward[i]

            node.name = f"MAN.{self.indexOfAddress[i]}"
            node.tel = f'{i * 10 + 1380013800}'
            node.email = None

            self.s.add(node)
            if i % 1000 == 0:
                self.s.flush()

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

        print(f"SQLAlchemy ORM add(): Total time for all records {(time.time() - t0)}  secs")


if __name__ == "__main__":
    t = macnode()
    print("start test")
    t.genAllIndex()
    t.saveDataToDB()
