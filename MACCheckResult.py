import heapq
import os
import time

import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from MACNodeSQL import *
from include.const import *

Nums = Constants(
    VipStdBalance=3000,
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
    indexOfsubNodeListIndex = []
    ListLen = 0

    def __init__(self):
        self.IsMinerAwardCached = []
        self.MinerAwardCachedValue = []

        self.IsTreeBalanceCached = []
        self.TreeBalanceCachedValue = []

        self.IsstaticIncomeTreeCached = []
        self.staticIncomeTreeCachedValue = []

        self.IsvipLevelCached = []
        self.vipLevelCachedValue =[]

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
        self.indexOfMycode = self.build_dict(self.sortedMycodeListdict, key="mycode")
        # 考虑到层级关系，还需要建立mycode的字典，方便查找上下级关系，所以 mycode 是关键index
        self.ListLen = len(self.sortedMycodeListdict)

        self.IsMinerAwardCached = [False] * self.ListLen
        self.MinerAwardCachedValue = [0] * self.ListLen

        self.IsTreeBalanceCached = [False] * self.ListLen
        self.TreeBalanceCachedValue = [0] * self.ListLen

        self.IsstaticIncomeTreeCached = [False] * self.ListLen
        self.staticIncomeTreeCachedValue = [0] * self.ListLen

        self.IsvipLevelCached = [False] * self.ListLen
        self.vipLevelCachedValue = [0] * self.ListLen

        print(f"sorted: Total time for {Nums.MaxRecords} records {(time.time() - self.t0)}  secs")
        # print(f"SQLAlchemy ORM query(): Total time for {len(self.nodeList)} records {(time.time() - self.t0)}  secs")

    def build_dict(self, seq, key):
        return dict((d[key], dict(d, index=i)) for (i, d) in enumerate(seq))

    def saveData2excel(self):
        path = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(path, 'CheckData.xlsx')

        writer = pd.ExcelWriter(output_file)
        df = pd.DataFrame(self.sortedMycodeListdict)
        df['TotalAward'] = self.indexOfTotalAward
        df['vipLevel'] = self.indexOfvipLevel
        df['RecommendAward'] = self.indexOfRecommend1Award
        df['staticIncome'] = self.indexOfstaticIncome

        df.to_excel(writer, sheet_name="origin data")
        writer.close()

    def saveData(self):
        path = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(path, 'fullresult.xlsx')
        writer = pd.ExcelWriter(output_file)

        node = AssetCheckresultpython()
        # nodedict = node._asdict()
        nodedict = node.__dict__
        df = pd.DataFrame(nodedict, pd.Index(range(1)))

        # copy data from fund, and integrate userlist
        # FundNum = len(self.sortedMycodeListdict)
        print(f"sorted: Total time for FundNum:{self.ListLen} records {(time.time() - self.t0)}  secs")
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

            z = self.indexOfMycode.get(node.mycode)
            Index = z['index']
            node.mycodeID = Index
            node.mycodeIDSubListIndex = ' '.join(str(i) for i in self.indexOfsubNodeListIndex[Index])
            node.mycodeIDGrandSonListIndex = ','.join(str(i) for i in self.indexOfGrandSonNodeListIndex[Index])
            node.mycodeIDsubNodevipLevelIndex = ','.join(str(i) for i in self.indexOfsubNodevipLevelIndex[Index])

            node.NodeLevel = self.indexOfNodeLevel[Index]
            node.TreeBalance = self.indexOfTreeBalance[Index]

            node.vipTreeBalance = self.indexOfvipTreeBalance[Index]
            node.vipTag = self.indexOfvipTag[Index]

            node.vipLevel = self.indexOfvipLevel[Index]
            node.usedBalance = self.indexOfusedBalance[Index]
            node.minerProductive = self.indexOfminerProductive[Index]
            node.staticIncome = self.indexOfstaticIncome[Index]

            node.staticIncomeTree = self.indexOfstaticIncomeTree[Index]
            node.MinerAward = self.indexOfMinerAward[Index]
            node.RecommendAward = self.indexOfRecommendAward[Index]
            node.Recommend1Award = self.indexOfRecommend1Award[Index]
            node.Recommend2Award = self.indexOfRecommend2Award[Index]
            node.DynamicAward = self.indexOfDynamicAward[Index]
            node.TotalAward = self.indexOfTotalAward[Index]

            d = self.getDescriptionByIndex(x, Index)
            if int(node.TotalAward) == int(node.static + node.dynamic):
                node.decription = f"OK:={d}"
            else:
                node.decription = f"ERR:={d}"

            # if i==1:
            # df = pd.DataFrame({'id': 1, 'name': 'Alice'}, pd.Index(range(1)))
            df = df.append(node.__dict__, ignore_index=True)
            # df = df.append(node.__dict__, pd.Index(range(1)))

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

        df.to_excel(writer, sheet_name="origin data")
        writer.close()

        print(f"SQLAlchemy ORM add(): Total time for all records {(time.time() - self.t0)}  secs")

    def getDescriptionByIndex(self, Node, Index):
        desc = ""f"ID{Index}:{Node['name']}:v{self.indexOfvipTreeBalance[Index]}:v{self.indexOfvipLevel[Index]}:\n"
        desc = desc + f"L1:"
        for i in self.indexOfsubNodeListIndex[Index]:
            desc = desc + (
                f"ID{i}:{self.sortedMycodeListdict[i]['phone']}{self.sortedMycodeListdict[i]['mycode']}:{int(self.sortedMycodeListdict[i]['fund'])}:t{int(self.indexOfTreeBalance[i])}:v{self.indexOfvipLevel[i]}\n")
        desc = desc + f"L2:"
        for i in self.indexOfGrandSonNodeListIndex[Index]:
            desc = desc + (
                f"ID{i}:{self.sortedMycodeListdict[i]['phone']}{self.sortedMycodeListdict[i]['mycode']}:{int(self.sortedMycodeListdict[i]['fund'])}:t{int(self.indexOfTreeBalance[i])}:v{self.indexOfvipLevel[i]}\n")
        desc = desc + f"@:{int(self.indexOfTreeBalance[Index])}:{int(self.indexOfstaticIncomeTreevip[Index])}:{self.indexOfRecommend1Award[Index]}:{self.indexOfRecommendAward[Index]}:{self.indexOfMinerAward[Index]}:{self.indexOfTotalAward[Index]}"

        return desc

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
        self.indexOfsubNodeListIndex = []
        for x in range(self.ListLen):
            y = self.getsubNodeListIndexbyNodeIndex(x)
            self.indexOfsubNodeListIndex.append(y)
        print(f"genIndexbysubNodeListIndex: Total time for all records {(time.time() - self.t0)}  secs")

    def genIndexbyGrandSonNodeListIndex(self):
        self.indexOfGrandSonNodeListIndex = []
        # 创建空list的方法：
        # features = [[] for _ in range(6)]
        for x in range(self.ListLen):
            y = self.indexOfsubNodeListIndex[x]
            u = []  # u is the grandson list
            if y:
                for z in y:
                    v = self.indexOfsubNodeListIndex[z]
                    u.extend(v)

            self.indexOfGrandSonNodeListIndex.append(u)

        print(f"genIndexbyGrandSonNodeListIndex: Total time for all records {(time.time() - self.t0)}  secs")

    def genIndexbysubNodevipLevelIndex(self):
        self.indexOfsubNodevipLevelIndex = []
        for x in range(self.ListLen):
            y = self.indexOfsubNodeListIndex[x]
            u = []  # u is the subnode vipLevel list
            if y:

                for z in y:
                    v = self.indexOfvipLevel[z]
                    u.append(v)

            self.indexOfsubNodevipLevelIndex.append(u)

        print(f"genIndexbysubNodevipLevelIndex: Total time for all records {(time.time() - self.t0)}  secs")

    def getsubNodeListbyNode(self, Node):

        subNodeList = []
        # It contains more indice, so we must use index function, can't utilize dict function
        # subNodeIndex = self.indexOfparentID.index(ID)

        subNodeListIndex = [i for i, x in enumerate(self.sortedMycodeListdict) if x['code'] == Node['mycode']]

        z = self.indexOfMycode.get(Node['mycode'])
        i = z['index']

        if i in subNodeListIndex:
            subNodeListIndex.remove(i)

        for x in subNodeListIndex:
            subNodeList.append(self.sortedMycodeListdict[x])

        return subNodeList

    def getNodeLevelbyMycode(self, Mycode):
        # prime key should start with 1
        DictMycode = self.indexOfMycode.get(Mycode)
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

        z = self.indexOfMycode.get(Mycode)
        i = z['index']

        if i in subNodeIndex:
            subNodeIndex.remove(i)

        if subNodeIndex:

            for x in subNodeIndex:
                y = self.indexOfMycode[x]
                TreeBalance = TreeBalance + self.getTreeBalancebyMycode(y)
        else:
            TreeBalance = 0

        return TreeBalance + z['fund']

    def getTreeBalancebyNode(self, Node):
        TreeBalance = 0
        # It contains more indice, so we must use index function, can't utilize dict function
        # subNodeIndex = self.indexOfparentID.index(ID)

        subNodeIndex = [i for i, x in enumerate(self.sortedMycodeListdict) if x['code'] == Node['mycode']]

        z = self.indexOfMycode.get(Node['mycode'])
        i = z['index']
        if i in subNodeIndex:
            subNodeIndex.remove(i)

        if subNodeIndex:
            for x in subNodeIndex:
                y = self.sortedMycodeListdict[x]
                TreeBalance = TreeBalance + self.getTreeBalancebyNode(y)
        else:
            TreeBalance = 0

        return TreeBalance + Node['fund']

    def getTreeBalancebyIndex(self, Index):

        if self.IsTreeBalanceCached[Index]:
            return self.TreeBalanceCachedValue[Index]

        subNodeIndex = self.indexOfsubNodeListIndex[Index]
        subTreeBalance = 0

        if subNodeIndex:
            for y in subNodeIndex:
                subTreeBalance = subTreeBalance + self.getTreeBalancebyIndex(y)
        else:
            try:
                subTreeBalance = 0
            except:
                print(
                    "should exec get static income function genIndexbystaticIncome() to get ub of indexOfusedBalance ")
                assert ("Failure")

        try:
            TreeBalance = self.indexOfusedBalance[Index] + subTreeBalance
            self.TreeBalanceCachedValue[Index] = TreeBalance
            self.IsTreeBalanceCached[Index] = True

        except:
            print("should exec get static income function genIndexbystaticIncome() to get ub of indexOfusedBalance ")
            assert ("Failure")

        return TreeBalance

    # def genIndexbyTreeBalanceOld(self):
    #     self.indexOfTreeBalance = []
    #
    #     self.IDTreeBalancedict = {}
    #     for x in self.sortedMycodeListdict:
    #         # TreeBalance = self.getTreeBalancebyMycode(x)
    #         TreeBalance = self.getTreeBalancebyNode(x)
    #         self.indexOfTreeBalance.append(TreeBalance)
    #         self.IDTreeBalancedict[x['mycode']] = TreeBalance
    #
    #     print(f"genIndexbyTreeBalance: Total time for all records {(time.time() - self.t0)}  secs")

    def genIndexbyTreeBalance(self):
        self.indexOfTreeBalance = []

        self.IDTreeBalancedict = {}
        for x in range(self.ListLen):
            # TreeBalance = self.getTreeBalancebyMycode(x)
            TreeBalance = self.getTreeBalancebyIndex(x)
            self.indexOfTreeBalance.append(TreeBalance)
            self.IDTreeBalancedict[self.sortedMycodeListdict[x]['mycode']] = TreeBalance

        print(f"genIndexbyTreeBalance: Total time for all records {(time.time() - self.t0)}  secs")

    def genIndexbyvipTreeBalance(self):
        self.indexOfvipTreeBalance = []
        self.IDvipTreeBalancedict = {}
        self.indexOfvipTag = []

        for x in range(self.ListLen):
            vipBalance = self.getvipTreeBalancebyIndex(x)
            vipTag = 1 if vipBalance >= Nums.VipStdBalance else 0
            self.indexOfvipTreeBalance.append(vipBalance)
            self.IDvipTreeBalancedict[self.sortedMycodeListdict[x]['mycode']] = vipBalance
            self.indexOfvipTag.append(vipTag)

        print(f"genIndexbyvipTreeBalance: Total time for all records {(time.time() - self.t0)}  secs")

    def getvipTreeBalancebyIndex(self, i):
        vipBalance = 0
        subvipBalanceList = []
        subNodeIndex = self.indexOfsubNodeListIndex[i]

        if subNodeIndex:
            for y in subNodeIndex:
                subBalance = self.indexOfTreeBalance[y]
                subvipBalanceList.append(subBalance)

            vipBalance = sum(subvipBalanceList) - max(subvipBalanceList)
        else:
            vipBalance = 0

        return vipBalance

    def getvipLevelbyIndex(self, i):
        if self.IsvipLevelCached[i]:
            return self.vipLevelCachedValue[i]

        subvipLevelList = []
        subNodeIndex = self.indexOfsubNodeListIndex[i]

        vipbase = self.indexOfvipTag[i]  # + 0  # use it to convert boolean to int

        if subNodeIndex:
            # subNodeList = self.getListHit(self.indexOfID, subNodeIndex)

            for y in subNodeIndex:
                subvipLevel = self.getvipLevelbyIndex(y)
                subvipLevelList.append(subvipLevel)

            subvipTop2 = heapq.nlargest(2, subvipLevelList)

            subvipLevel = min(subvipTop2)
            if (subvipLevel == 0):
                vipLevel = vipbase
            else:
                vipLevel = subvipLevel + 1
        else:
            vipLevel = 0

        self.vipLevelCachedValue[i] = vipLevel
        self.IsvipLevelCached[i]=True

        return vipLevel

    def genIndexbyvipLevel(self):
        self.indexOfvipLevel = []
        self.IDvipLeveldict = {}
        for x in range(self.ListLen):
            vipLevel = self.getvipLevelbyIndex(x)
            self.indexOfvipLevel.append(vipLevel)
            self.IDvipLeveldict[self.sortedMycodeListdict[x]['mycode']] = vipLevel
        print(f"genIndexbyvipLevel: Total time for all records {(time.time() - self.t0)}  secs")

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

    def getstaticIncomebyIndex(self, Index):
        balance, minerProductive, staticIncome = self.getstaticIncomebyBalance(self.sortedMycodeListdict[Index]['fund'])
        return balance, minerProductive, staticIncome

    def genIndexbystaticIncome(self):

        self.indexOfusedBalance = []
        self.indexOfminerProductive = []
        self.indexOfstaticIncome = []
        self.IDminerProductivedict = {}
        self.IDstaticIncomedict = {}
        for x in range(self.ListLen):
            usedBalance, minerProductive, staticIncome = self.getstaticIncomebyIndex(x)
            self.indexOfusedBalance.append(usedBalance)
            self.indexOfminerProductive.append(minerProductive)
            self.indexOfstaticIncome.append(staticIncome)
            self.IDminerProductivedict[self.sortedMycodeListdict[x]['mycode']] = minerProductive
            self.IDstaticIncomedict[self.sortedMycodeListdict[x]['mycode']] = staticIncome
        print(f"genIndexbystaticIncome: Total time for all records {(time.time() - self.t0)}  secs")

    def getstaticIncomeTreebyIndex(self, Index):

        if self.IsstaticIncomeTreeCached[Index]:
            return self.staticIncomeTreeCachedValue[Index]

        subNodeIndex = self.indexOfsubNodeListIndex[Index]
        staticIncome = self.indexOfstaticIncome[Index]
        substaticIncomeTree = 0
        if subNodeIndex:
            for y in subNodeIndex:
                substaticIncomeTree = substaticIncomeTree + self.getstaticIncomeTreebyIndex(y)

        staticIncomeTree = staticIncome + substaticIncomeTree

        self.staticIncomeTreeCachedValue[Index] = staticIncomeTree
        self.IsstaticIncomeTreeCached[Index]=True
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
        for x in range(self.ListLen):
            staticIncomeTree = self.getstaticIncomeTreebyIndex(x)
            self.indexOfstaticIncomeTree.append(staticIncomeTree)
            self.IDstaticIncomeTreedict[self.sortedMycodeListdict[x]['mycode']] = staticIncomeTree
        print(f"genIndexbystaticIncomeTree: Total time for all records {(time.time() - self.t0)}  secs")

    def genIndexbystaticIncomeTreevip(self):
        self.indexOfstaticIncomeTreevip = []
        for x in range(self.ListLen):
            staticIncomeTreevip = self.indexOfstaticIncomeTree[x] * self.getMinerCoeffbyvipLevel(
                self.indexOfvipLevel[x])
            self.indexOfstaticIncomeTreevip.append(staticIncomeTreevip)
        print(f"genIndexbystaticIncomeTreevip: Total time for all records {(time.time() - self.t0)}  secs")

    def getMinerAwardbyIndex(self, Index):

        vipLevel = self.indexOfvipLevel[Index]
        if vipLevel == 0:
            return 0

        if self.IsMinerAwardCached[Index]:
            return self.MinerAwardCachedValue[Index]

        minerCoeff = self.getMinerCoeffbyvipLevel(vipLevel)
        grandsonNodeList = []
        MinerAward = 0

        # list should use copy method
        # subNodeIndex = self.indexOfsubNodeListIndex[Index]
        subNodeIndex = self.indexOfsubNodeListIndex[Index].copy()
        # can use zip function and depth to optimize code size
        if subNodeIndex:
            # subNodeList = self.getListHit(self.indexOfID, subNodeIndex)
            while subNodeIndex:
                y = subNodeIndex[-1]
                subNodeIndex.pop()
                subvipLevel = self.indexOfvipLevel[y]

                if vipLevel > subvipLevel:
                    # caculate normal static revenue,can't use indexOfstaticIncomeTreevip, since it should change by vip Level
                    # revenue = self.indexOfstaticIncomeTreevip[y]  - self.getMinerAwardbyIndex(y)
                    # also it should not be indexOfstaticIncomeTree, since the case V1-V0-v3. Only way we do is that caculate contribute v0 itself. then it's subnode
                    # 计算从子节点拿到的收益，并扣除该节点的矿圈收益。 仅计算该子节点，不能计算下属全部节点，因为下属如果有一个巨大的高级节点，实际是错误收益
                    # 典型例子 v1 - v0 - v3，此时计算V1收益，必然会是 v0.staticIncome* minercoeff，而不是 (V0+V3)*staticIncome* minercoeff -MinerAward(V0)-MinerAward(V3)
                    # 后者会出现负值
                    # 所以变为：仅计算本地节点
                    revenue = self.indexOfstaticIncome[y] * minerCoeff -  self.getMinerAwardbyIndex(y)

                     # grandsonNodeList = self.indexOfsubNodeListIndex[y]
                    # should use copy method
                    vipgrandsonNodeList = self.indexOfsubNodeListIndex[y].copy()

                    # 添加子节点的子节点，即孙子节点到计算列表
                    if vipgrandsonNodeList:
                        grandsonNodeList.extend(vipgrandsonNodeList)

                elif vipLevel == subvipLevel:
                    revenue = self.getMinerAwardbyIndex(y) * Nums.sameLevelRate
                else:
                    revenue = 0

                MinerAward = MinerAward + revenue

            subNodeIndex = grandsonNodeList.copy()

            while subNodeIndex:
                y = subNodeIndex[-1]
                subNodeIndex.pop()
                subvipLevel = self.indexOfvipLevel[y]

                if vipLevel > subvipLevel:
                    # caculate normal static revenue, every node is iterated!
                    #revenue = self.indexOfTreeBalance[y] * minerCoeff - self.getMinerAwardbyIndex(y)
                    #revenue = self.indexOfstaticIncome[y] * (minerCoeff-self.getMinerCoeffbyvipLevel(subvipLevel))
                    revenue = self.indexOfstaticIncome[y] * minerCoeff - self.getMinerAwardbyIndex(y)

                    # if revenue < 0:
                    #     revenue = 0
                    #     raise Exception("error for calculate revenue")

                    vipsub2NodeList = self.indexOfsubNodeListIndex[y].copy()

                    if vipsub2NodeList:  # use to continue loop, add it subNodeIndex. DFS search
                        subNodeIndex.extend(vipsub2NodeList)

                elif vipLevel == subvipLevel:  # no add new node if same level
                    revenue = 0
                else:
                    revenue = 0  # if higher, don't think about the subnode

                MinerAward = MinerAward + revenue

        else:
            MinerAward = 0
            raise Exception("error for calculat revenue since subnodelist is empty")

        self.MinerAwardCachedValue[Index] = MinerAward
        self.IsMinerAwardCached[Index]=True

        return MinerAward

    def getRecommendAwardbyIndex(self, Index):

        subNodeIndex = self.indexOfsubNodeListIndex[Index]
        r1 = 0
        r2 = 0
        RecommmendLevel = len(subNodeIndex)
        if RecommmendLevel == 0:
            r1 = 0
        elif (RecommmendLevel < 3):

            minerProductiveX = self.indexOfminerProductive[Index]
            BalanceX = self.indexOfusedBalance[Index]

            # subNodeList = self.getListHit(self.indexOfID, subNodeIndex)
            for y in subNodeIndex:
                minerProductiveY = self.indexOfminerProductive[y]
                BalanceY = self.indexOfusedBalance[y]
                r1 = r1 + min(minerProductiveY, minerProductiveX) * min(BalanceY,
                                                                        BalanceX) * Nums.rateSon
        else:
            recommendAward = 0
            minerProductiveX = self.indexOfminerProductive[Index]
            BalanceX = self.indexOfusedBalance[Index]

            # subNodeList = self.getListHit(self.indexOfID, subNodeIndex)
            for y in subNodeIndex:
                minerProductiveY = self.indexOfminerProductive[y]
                BalanceY = self.indexOfusedBalance[y]
                r1 = r1 + min(minerProductiveY, minerProductiveX) * min(BalanceY,
                                                                        BalanceX) * Nums.rateSon

            subNodeIndex = self.indexOfGrandSonNodeListIndex[Index]
            for y in subNodeIndex:
                minerProductiveY = self.indexOfminerProductive[y]
                BalanceY = self.indexOfusedBalance[y]
                r2 = r2 + min(minerProductiveY, minerProductiveX) * min(BalanceY,
                                                                        BalanceX) * Nums.rateGrandSon

        return r1, r2, (r1 + r2)

    def getTotalAwardbyIndex(self, Index):

        DynamicAward = self.indexOfRecommendAward[Index] + self.indexOfMinerAward[Index]
        TotalAward = self.indexOfstaticIncome[Index] + DynamicAward
        return DynamicAward, TotalAward

    def genIndexbyTotalAward(self):
        self.indexOfTotalAward = []
        self.IDTotalAwarddict = {}
        self.indexOfDynamicAward = []
        self.IDDynamicAwarddict = {}
        for x in range(self.ListLen):
            DynamicAward, TotalAward = self.getTotalAwardbyIndex(x)
            self.indexOfTotalAward.append(TotalAward)
            self.IDTotalAwarddict[self.sortedMycodeListdict[x]['mycode']] = TotalAward
            self.indexOfDynamicAward.append(DynamicAward)
            self.IDDynamicAwarddict[self.sortedMycodeListdict[x]['mycode']] = DynamicAward
        print(f"genIndexbyTotalAward: Total time for all records {(time.time() - self.t0)}  secs")

    def genIndexbyMinerAward(self):
        self.indexOfMinerAward = []
        self.IDMinerAwarddict = {}
        for x in range(self.ListLen):
            MinerAward = self.getMinerAwardbyIndex(x)
            self.indexOfMinerAward.append(MinerAward)
            self.IDMinerAwarddict[self.sortedMycodeListdict[x]['mycode']] = MinerAward
        print(f"genIndexbyMinerAward: Total time for all records {(time.time() - self.t0)}  secs")

    def genIndexbyRecommendAward(self):
        self.indexOfRecommendAward = []
        self.indexOfRecommend1Award = []
        self.indexOfRecommend2Award = []
        self.IDRecommendAwarddict = {}
        for x in range(self.ListLen):
            r1, r2, r = self.getRecommendAwardbyIndex(x)
            self.indexOfRecommendAward.append(r)
            self.indexOfRecommend1Award.append(r1)
            self.indexOfRecommend2Award.append(r2)
            self.IDRecommendAwarddict[self.sortedMycodeListdict[x]['mycode']] = r
        print(f"genIndexbyRecommendAward: Total time for all records {(time.time() - self.t0)}  secs")

    def genAllIndex(self):
        self.genIndexbysubNodeListIndex()
        self.genIndexbyGrandSonNodeListIndex()
        self.genIndexbyNodeLevel()
        self.genIndexbystaticIncome()

        self.genIndexbyTreeBalance()
        self.genIndexbyvipTreeBalance()
        self.genIndexbyvipLevel()
        self.genIndexbysubNodevipLevelIndex()

        self.genIndexbystaticIncomeTree()
        self.genIndexbystaticIncomeTreevip()

        self.genIndexbyMinerAward()
        self.genIndexbyRecommendAward()
        self.genIndexbyTotalAward()


if __name__ == "__main__":
    t = CheckSQLData()
    print("start test ...")
    t.initDB()
    t.LoadSQLData()
    t.genAllIndex()
    t.saveData()
    t.saveData2excel()
    t.closDB()
