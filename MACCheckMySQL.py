# -*- coding:utf-8 -*-
import time
from functools import reduce

import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import Timer
from MACNodeSQL import *
from MyEncoder import *
from include.const import *

# SQLCODE="mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8"
SQLCODE = "mysql+pymysql://tiger:test123456!@@127.0.0.1/test?charset=utf8"

# const pool0 = mysql.createPool({
#   connectionLimit: 50,
#   host: '127.0.0.1',
#   user: 'tiger',
#   password: 'test123456!@',
#   database: 'test',
#   multipleStatements: true //是否允许执行多条sql语句
# });

ti = Timer.Timer()

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
    indexOfsubNodeListIndex = []
    sortedMycodeListdict = []
    ListLen = 0
    savetime = 0

    def __init__(self):
        self.IsMinerAwardCached = []
        self.MinerAwardCachedValue = []

        self.IsTreeBalanceCached = []
        self.TreeBalanceCachedValue = []

        self.IsstaticIncomeTreeCached = []
        self.staticIncomeTreeCachedValue = []

        self.IsvipLevelCached = []
        self.vipLevelCachedValue = []

        self.savetime = time.strftime('%Y%m%d_%H%M%S')
        # self.savetime = time.time()
        # print(time.strftime('%y/%m/%d %H:%M:%S %A'))
        print('Load SQL Data from MySQL....')

    def initDB(self):
        self.engine = create_engine(SQLCODE)
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

    def list_dict_duplicate_removal(self, list_dict_data):
        run_function = lambda x, y: x if y in x else x + [y]
        return reduce(run_function, [[], ] + list_dict_data)

    def build_dict(self, seq, key):
        return dict((d[key], dict(d, index=i)) for (i, d) in enumerate(seq))

    def LoadSQLData(self):

        # self.nodeList = self.s.query(AssetLoadsqldatum).filter(text("ID < :value AND parentID = :pValue")).params(value=100, pValue=1)

        # self.nodeList = self.s.query(AssetLoadsqldatum).filter(text("ID < :value ")).params(value=1000).order_by(
        #     AssetLoadsqldatum.Balance.desc())

        # self.nodeList = self.s.query(AssetLoadsqldatum).filter(text("ID < :value ")).params(value=Nums.MaxRecords).order_by(AssetLoadsqldatum.Balance.desc())
        ## for test aim, we reshuffle it! desc() means order reverse
        ## self.NodeList = self.NodeList[::2]+self.NodeList[1::2] ## error! since query object is not a list
        ## load asset_fund

        # #UserList=s.query(User)
        # UserList=s.query(User).all()
        # UserListdict = [u.__dict__ for u in UserList]
        # print(UserListdict)
        # UserListdict1 = [u._asdict() for u in UserList]
        # print(UserListdict1)

        ## 首先获得用户列表

        # phone = Column(String(32), nullable=False, comment='phone number')
        # email = Column(String(32), comment='email address')
        # password = Column(String(64), comment='md5 of password')
        # code = Column(String(10), comment='invitation code')
        # mycode = Column(String(10), comment='my invitation code')
        # id = Column(INTEGER(11), primary_key=True)
        # paypassword = Column(String(64), comment='pay password')
        #

        # 字典反转的例子 {v: k for k, v in m.items()}

        UserList = self.s.query(User.phone, User.mycode, User.code).all()

        ## only useful column is selected
        # id = Column(INTEGER(8), primary_key=True)
        # fund = Column(Float(asdecimal=True), server_default=text("'0'"), comment='本金')
        # static = Column(Float(asdecimal=True), server_default=text("'0'"), comment='静态利息')
        # dynamic = Column(Float(asdecimal=True), server_default=text("'0'"), comment='动态利息')
        # status = Column(TINYINT(1), server_default=text("'0'"), comment='0、未激活 1、运行、2淘汰')
        # fundtype = Column(INTEGER(4), server_default=text("'0'"), comment='基金类型')
        # userid = Column(String(32), nullable=False, comment='用户id')
        # starttime = Column(BIGINT(20), nullable=False, comment='购买矿机时间')

        emptyFundItem = {"userid": "", "fund": 0, "static": 0, "dynamic": 0, "circle": 0, "recommend": 0,
                         "starttime": time.time()}
        FundList = self.s.query(AssetFund.userid, AssetFund.fund, AssetFund.static, AssetFund.dynamic, AssetFund.circle,
                                AssetFund.recommend,
                                AssetFund.starttime).all()

        BaseList = self.s.query(AssetBase).all()

        FundListdict1 = [u._asdict() for u in FundList]
        UserListdict1 = [u._asdict() for u in UserList]
        BaseListdict1 = [u._asdict() for u in BaseList]

        # FundListdict2 = sorted(FundListdict1, key=lambda k: k['userid'])  ## total 54
        # UserListdict2 = sorted(UserListdict1, key=lambda k: k['phone'])  ## total 135
        # BaseListdict2 = sorted(BaseListdict1, key=lambda k: k['phone'])  ## total 136

        self.sortedFundListdict = self.list_dict_duplicate_removal(FundListdict1)
        self.sortedUserListdict = self.list_dict_duplicate_removal(UserListdict1)
        self.sortedBaseListdict = self.list_dict_duplicate_removal(BaseListdict1)

        # 根据 userid/phone/phone建立字典，方便快速查找

        self.IndexOfFund = self.build_dict(self.sortedFundListdict, key="userid")
        self.IndexOfUser = self.build_dict(self.sortedUserListdict, key="phone")
        self.IndexOfBase = self.build_dict(self.sortedBaseListdict, key="phone")

        # 生成空列表：
        # emptyFundItem={v: k for k, v in m.items()}

        # 得到sortedMycodeListdict即可
        # self.sortedMycodeListdict = sorted(FundListdict1, key=lambda k: k['mycode'])  ## total 54
        # self.IndexOfUser=sorted(self.IndexOfUser,key=lambda k: k['phone'])
        # from operator import itemgetter
        # self.IndexOfUser1=sorted(self.IndexOfUser,key=itemgetter('phone'),reverse=False)
        # keys = self.IndexOfUser.keys()
        # keys.sort()
        # a=[self.IndexOfUser[key] for key in keys]
        # self.IndexOfUser1 = sorted(self.IndexOfUser, reverse=False)
        # self.IndexOfUser1 =[{k,self.IndexOfUser[k]} for k in sorted(self.IndexOfUser, reverse=False)]

        self.IndexOfUser1 = sorted(self.IndexOfUser, reverse=False)
        self.IndexOfUser2 = [{key: self.IndexOfUser[key]} for key in self.IndexOfUser1]
        self.IndexOfUser = dict((key, self.IndexOfUser[key]) for key in self.IndexOfUser1)

        for x in self.IndexOfUser:  # it convert to a list, list item is a dict, and contain index, x ='8613008104208'
            y = self.IndexOfFund.get(x, emptyFundItem)
            # dict combines, it equal
            # dictMerged1 = dict( dict1.items() + dict2.items() )
            # dictMerged2 = dict1.copy()
            # dictMerged2.update(dict2)
            z = dict(self.IndexOfUser[x], **y)  # 合并表格

            self.sortedMycodeListdict.append(z)

        # 根据 userid/phone/phone建立字典，方便快速查找
        self.indexOfMycode = self.build_dict(self.sortedMycodeListdict, key="mycode")
        # 考虑到层级关系，还需要建立mycode的字典，方便查找上下级关系，所以 mycode 是关键index
        self.ListLen = len(self.sortedMycodeListdict)

    def InitCacheList(self):
        CacheLen = self.ListLen

        self.IsMinerAwardCached = [False] * CacheLen
        self.MinerAwardCachedValue = [0] * CacheLen
        self.indexOfsubAwardict = [{} for _ in range(CacheLen)]

        self.IsFastMinerAwardCached = [False] * CacheLen
        self.FastMinerAwardCachedValue = [0] * CacheLen

        self.IsTreeBalanceCached = [False] * CacheLen
        self.TreeBalanceCachedValue = [0] * CacheLen

        self.IsNodeTreeListCached = [False] * CacheLen
        self.NodeTreeListCachedValue = [0] * CacheLen

        self.IsstaticIncomeTreeCached = [False] * CacheLen
        self.staticIncomeTreeCachedValue = [0] * CacheLen

        self.IsvipLevelCached = [False] * CacheLen
        self.vipLevelCachedValue = [0] * CacheLen

        self.IsNodeInfoCached = [False] * CacheLen
        self.NodeInfoCachedValue = [""] * CacheLen

    def LoadSQLData1(self):

        FundList = self.s.query(AssetLoadsqldatum).all()

        print(f"SQLAlchemy ORM query(): Total time for {Nums.MaxRecords} records {(time.time() - self.t0)}  secs")
        FundListdict1 = [u._asdict() for u in FundList]

        self.sortedMycodeListdict = sorted(FundListdict1, key=lambda k: k['mycode'])  ## total 54

        # 根据 userid/phone/phone建立字典，方便快速查找
        self.indexOfMycode = self.build_dict(self.sortedMycodeListdict, key="mycode")
        # 考虑到层级关系，还需要建立mycode的字典，方便查找上下级关系，所以 mycode 是关键index

        print(f"sorted: Total time for {Nums.MaxRecords} records {(time.time() - self.t0)}  secs")
        # print(f"SQLAlchemy ORM query(): Total time for {len(self.nodeList)} records {(time.time() - self.t0)}  secs")

    def build_dict(self, seq, key):
        return dict((d[key], dict(d, index=i)) for (i, d) in enumerate(seq))

    def saveData2excel(self):
        path = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(path, 'CheckData.xlsx')

        # nodedict = node.__dict__
        # df = pd.DataFrame(nodedict, pd.Index(range(1)))

        writer = pd.ExcelWriter(output_file)
        df = pd.DataFrame(self.sortedMycodeListdict)
        df['TotalAward'] = self.indexOfTotalAward
        df['vipLevel'] = self.indexOfvipLevel
        df['RecommendAward'] = self.indexOfRecommend1Award
        df['staticIncome'] = self.indexOfstaticIncome

        # df = df.append(node.__dict__, ignore_index=True)
        # # df = df.append(node.__dict__, pd.Index(range(1)))

        df.to_excel(writer, sheet_name="origin data")
        writer.close()

    def saveData(self):
        path = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(path, 'fullresult.xlsx')
        writer = pd.ExcelWriter(output_file)

        node = AssetCheckresultpython()
        # nodedict = node._asdict()
        # nodedict = node.__dict__
        # df = pd.DataFrame(nodedict, pd.Index(range(1)))

        # copy data from fund, and integrate userlist
        # FundNum = len(self.sortedMycodeListdict)
        # print(f"sorted: Total time for FundNum:{self.ListLen} records {(time.time() - self.t0)}  secs")
        i = 1
        for x in self.sortedMycodeListdict:
            node = AssetCheckresultpython()  # should in loop, otherwise it will overlap all record and only 1 in database
            node.fund = x.get('fund', 0)
            node.static = x.get('static', 0)
            node.dynamic = x.get('dynamic', 0)
            node.status = x.get('status', 0)
            node.fundtype = x.get('fundtype', 0)
            node.userid = x.get('userid', 0)
            node.starttime = x.get('starttime', 0)
            node.stoptime = x.get('stoptime', 0)
            node.lastdayinterest = x.get('lastdayinterest', 0)
            node.gas = x.get('gas', 0)
            node.attribute = x.get('attribute', 0)
            node.production = x.get('production', 0)
            node.updatetime = x.get('updatetime', 0)

            node.name = x.get('name', 0)
            node.phone = x.get('phone', 0)
            node.email = x.get('email', 0)
            node.password = x.get('password', 0)
            node.code = x.get('code', 0)
            node.mycode = x.get('mycode', 0)

            node.paypassword = x.get('paypassword', 0)
            node.status = x.get('status', 0)
            node.registertime = x.get('registertime', 0)
            node.countryCode = x.get('countryCode', 0)
            node.signtime = x.get('signtime', 0)

            node.ethaddress = x.get('ethaddress', 0)
            node.tokenbalance = x.get('tokenbalance', 0)
            node.usdtbalance = x.get('usdtbalance', 0)
            node.lockbalance = x.get('lockbalance', 0)
            node.tokenaddress = x.get('tokenaddress', 0)
            node.macbalance = x.get('macbalance', 0)
            node.circle = x.get('circle', 0) if x.get('circle', 0) else 0
            node.recommend = x.get('recommend', 0) if x.get('recommend', 0) else 0

            z = self.indexOfMycode.get(node.mycode)
            Index = z['index']
            node.mycodeID = Index
            # node.mycodeIDSubListIndex = ' '.join(str(i) for i in self.indexOfsubNodeListIndex[Index])
            # node.mycodeIDGrandSonListIndex = ','.join(str(i) for i in self.indexOfGrandSonNodeListIndex[Index])
            # node.mycodeIDsubNodevipLevelIndex = ','.join(str(i) for i in self.indexOfsubNodevipLevelIndex[Index])

            d = ' '.join(str(i) for i in self.indexOfsubNodeListIndex[Index])
            node.mycodeIDSubListIndex = d if len(d) < 1024 else d[0:1023]
            d = ','.join(str(i) for i in self.indexOfGrandSonNodeListIndex[Index])
            node.mycodeIDGrandSonListIndex = d if len(d) < 1024 else d[0:1023]
            d = ','.join(str(i) for i in self.indexOfsubNodevipLevelIndex[Index])
            node.mycodeIDsubNodevipLevelIndex = d if len(d) < 32 else d[0:32]

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

            d = self.getNodeTreeInfobyIndex(Index)
            d1 = d if len(d) < 4096 else d[0:4095]
            node.decription = d1

            i = i + 1
            self.s.add(node)
            if i % 1000 == 0:
                self.s.flush()

            # if i==1:
            # df = pd.DataFrame({'id': 1, 'name': 'Alice'}, pd.Index(range(1)))
            # df = df.append(node.__dict__, ignore_index=True) ## this ok
            # # df = df.append(node.__dict__, pd.Index(range(1)))
            with open(f'./oklist_{self.savetime}.txt', 'a') as w0, open(f'./errorlist_{self.savetime}.txt', 'a') as w1:
                if int(node.TotalAward) == int(node.static + node.dynamic):
                    w = w0
                    w.write(f"\n\n=====================  正确：")
                else:
                    w = w1
                    w.write(f"\n\n====================== 复杂：")
                w.write(
                    f"流水单号 {Index}：{node.phone} 投入资产:{int(node.fund)} 推荐码:{node.mycode} 上线:{node.code} ====================================")
                w.write(f"\n{time.asctime()}\n")
                w.write(
                    f"method1(yhw):静态:{node.static:5.1f} 矿圈:{node.circle if node.circle else 0} 推荐:{node.recommend:5.1f} 动态:{node.dynamic:5.1f}\n")
                w.write(
                    f"method2(lqh):静态:{node.staticIncome:5.1f} 矿圈:{node.MinerAward:5.1f} 推荐:{node.RecommendAward:5.1f} 动态:{node.DynamicAward:5.1f}新矿圈：{self.FastMinerAwardCachedValue[Index]:5.1f}\n")
                msg = f"理论最大矿圈收益:v1:{(node.staticIncomeTree - node.staticIncome) * 0.1}\tv2:{(node.staticIncomeTree - node.staticIncome) * 0.15}\tv3:{(node.staticIncomeTree - node.staticIncome) * 0.2}"
                w.write(msg)
                # desc = f"{i}\t{Node['phone']}\t{int(Node['fund'])}\tvip{self.indexOfvipLevel[i]}\tL{self.indexOfNodeLevel[i]}\t${self.indexOfvipTreeBalance[i]}\t${int(self.indexOfTreeBalance[i])}\t{Node['name']}\n"
                # w.write(f"\n总子节点数量\t累加和\t累加和1：子节点列表及详细信息\n")
                w.write(
                    f"\n内部序号\t注册名\tt本金\t\tV等级\t层级\tvip业绩\t总业绩\t矿圈1\tY矿圈\t总推荐\tY推荐\t动态\tY动态\t静态\tY静态\t二代推荐\t推荐码\t上级编码\n")
                w.write("\n详情如下:\n--------------------------------------------------------------\n")
                w.write(d)

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

        # df.to_excel(writer, sheet_name="origin data")
        # writer.close()

        # print(f"SQLAlchemy ORM add(): Total time for all records {(time.time() - self.t0)}  secs")

    def saveList(self, filename, List):

        wname = f"{filename}{self.savetime}.json"
        # x = json.dumps(List)
        # x =json.dumps(List,sort_keys=True, indent=2,separators=(',', ':'))
        x = json.dumps(List, sort_keys=False, indent=4, separators=(',', ':'), cls=MyEncoder, ensure_ascii=False)

        # y = json.loads(x)

        with open(wname, 'a') as w:
            w.write(x)
            # w.write(f"{List}")

    def getsubNodeListIndexbyIndex(self, Index):
        # subNodeListIndex = []
        # It contains more indice, so we must use index function, can't utilize dict function
        # subNodeIndex = self.indexOfparentID.index(ID)

        subNodeListIndex = [i for i, x in enumerate(self.sortedMycodeListdict) if
                            x['code'] == self.sortedMycodeListdict[Index]['mycode']]

        if Index in subNodeListIndex:
            subNodeListIndex.remove(Index)

        return subNodeListIndex

    def genIndexbysubNodeListIndex(self):
        ti.start("genIndexbysubNodeListIndex")
        self.indexOfsubNodeListIndex = []
        for x in range(self.ListLen):
            y = self.getsubNodeListIndexbyIndex(x)
            self.indexOfsubNodeListIndex.append(y)

        ti.stop("genIndexbysubNodeListIndex")

    def genIndexbyGrandSonNodeListIndex(self):
        ti.start("genIndexbyGrandSonNodeListIndex")
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

        # print(f"genIndexbyGrandSonNodeListIndex: Total time for all records {(time.time() - self.t0)}  secs")
        ti.stop("genIndexbyGrandSonNodeListIndex")

    def getNodeInfobyIndex(self, i):
        if self.IsNodeInfoCached[i]:
            return self.NodeInfoCachedValue[i]

        Node = self.sortedMycodeListdict[i]
        d = f"{i}"
        d = d + "\t" + f"{Node['phone']}"
        d = d + "\t" + f"{int(Node['fund'])}"
        d = d + "\t" + f"{self.indexOfvipLevel[i]}"
        d = d + "\t" + f"{self.indexOfNodeLevel[i]}"
        d = d + "\t" + f"{self.indexOfvipTreeBalance[i]}"
        d = d + "\t" + f"{int(self.indexOfTreeBalance[i])}"
        d = d + "\t" + f"{self.FastMinerAwardCachedValue[i]:4.1f}"
        circle = Node['circle'] if Node['circle'] else 0
        d = d + "\t" + f"{circle:4.1f}"
        d = d + "\t" + f"{self.indexOfRecommendAward[i]:4.1f}"
        recommend = Node['recommend'] if Node['recommend'] else 0
        d = d + "\t" + f"{recommend:4.1f}"
        d = d + "\t" + f"{self.indexOfDynamicAward[i]:4.1f}"
        d = d + "\t" + f"{Node['dynamic']:4.1f}"
        d = d + "\t" + f"{self.indexOfstaticIncome[i]:4.1f}"
        d = d + "\t" + f"{Node['static']:4.1f}"
        d = d + "\t" + f"{self.indexOfRecommend2Award[i]:4.1f}"
        d = d + "\t" + f"{Node['mycode']}"
        d = d + "\t" + f"{Node['code']}"
        d = d + "\n"

        return d

    def getNodeInfoJsonbyIndex(self, i):
        mycode = self.sortedMycodeListdict[i]['mycode']
        Node = {}
        Node['用户推荐码'] = mycode
        Node['VIP等级'] = self.indexOfvipLevel[i]
        Node['当前用户属于第几代'] = self.indexOfNodeLevel[i]
        Node['下属VIP计算的业绩'] = self.indexOfvipTreeBalance[i]
        Node['全部业绩'] = int(self.indexOfTreeBalance[i])
        Node['矿圈奖励情况'] = self.FastMinerAwardCachedValue[i]
        Node['推荐总奖励'] = self.indexOfRecommendAward[i]
        Node['总动态收益'] = self.indexOfDynamicAward[i]
        Node['静态收益'] = self.indexOfstaticIncome[i]
        Node['第一级推荐奖励'] = self.indexOfRecommend1Award[i]
        Node['第二级推荐奖励'] = self.indexOfRecommend2Award[i]
        Node['内部登记信息'] = self.sortedMycodeListdict[i]

        return Node

    def getNodeTreeInfoJsonbyIndex(self, i):
        subTreeList = self.getNodeTreeListbyIndex(i)
        # fundSum0 = sum(self.sortedMycodeListdict[i]['fund'] for i in subTreeList)
        fundSum = sum(self.indexOfusedBalance[x] for x in subTreeList)

        mycode = self.sortedMycodeListdict[i]['mycode']
        treeinfo = {}

        treeinfo['用户推荐码'] = mycode
        treeinfo['用户编号'] = i
        treeinfo['VIP等级'] = self.indexOfvipLevel[i]
        treeinfo['投入本金'] = self.sortedMycodeListdict[i]['fund']
        treeinfo['电话'] = self.sortedMycodeListdict[i]['phone']
        treeinfo['全部业绩'] = fundSum
        treeinfo['直属用户编号列表'] = self.indexOfsubNodeListIndex[i]
        treeinfo['全部下线编号'] = subTreeList
        treeinfo['矿圈奖子用户贡献列表'] = self.indexOfsubAwardict[i]
        treeinfo[f'详细信息'] = self.getNodeInfoJsonbyIndex(i)

        for x in subTreeList:
            # submycode = self.sortedMycodeListdict[x]['mycode']
            if x == i:
                continue
            else:
                treeinfo[f"下线{x}的信息"] = self.getNodeInfoJsonbyIndex(x)

        return treeinfo

    def genAllNodeTreeInfoJson(self):
        ti.start("genAllNodeTreeInfoJson")

        self.indexOfNodeTreeInfoJson = []
        # 创建空list的方法：
        # features = [[] for _ in range(6)]
        for x in range(self.ListLen):
            y = self.getNodeTreeInfoJsonbyIndex(x)
            self.indexOfNodeTreeInfoJson.append(y)

        self.saveList("nodeTreeInfo", self.indexOfNodeTreeInfoJson)
        ti.stop("genAllNodeTreeInfoJson")

    def getNodeTreeInfobyIndex(self, i):
        subTreeList = self.getNodeTreeListbyIndex(i)
        fundSum0 = sum(self.sortedMycodeListdict[i]['fund'] for i in subTreeList)
        fundSum1 = sum(self.indexOfusedBalance[i] for i in subTreeList)
        # sum([i for i in l if isinstance(i, int) or isinstance(i, float)])
        d = f"Info {i}:\n总业绩(含自身):{int(fundSum0)}\t{int(fundSum1)}\n下属贡献:{int(fundSum0 - self.sortedMycodeListdict[i]['fund'])}\n下属数量:{len(subTreeList)}\n下属编号:\t{subTreeList}\n\n"

        for x in subTreeList:
            info = self.getNodeInfobyIndex(x)
            d = d + info
        return d

    def getNodeTreeListbyIndex(self, i):
        if self.IsNodeTreeListCached[i]:
            return self.NodeTreeListCachedValue[i]

        x = self.indexOfsubNodeListIndex[i]
        TreeList = [i]
        if x:
            for y in x:
                z = self.getNodeTreeListbyIndex(y)
                TreeList.extend(z)

        self.NodeTreeListCachedValue[i] = TreeList
        self.IsNodeTreeListCached[i] = True

        return TreeList

    def genIndexbyNodeTreeList(self):
        self.indexOfNodeTreeList = []
        for x in range(self.ListLen):
            y = self.getNodeTreeListbyIndex(x)
            self.indexOfNodeTreeList.append(y)

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
        ti.start("genIndexbyNodeLevel")
        self.indexOfNodeLevel = []
        self.IDNodeLeveldict = {}
        for x in self.sortedMycodeListdict:
            y = x['mycode']
            level = self.getNodeLevelbyMycode(y)
            self.indexOfNodeLevel.append(level)
            self.IDNodeLeveldict[y] = level

        ti.stop("genIndexbyNodeLevel")

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

        debugInfo = []

        if subNodeIndex:
            for y in subNodeIndex:
                b = self.getTreeBalancebyIndex(y)
                subTreeBalance = subTreeBalance + b
                debugInfo.append(b)
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
        ti.start("genIndexbyTreeBalance")
        self.indexOfTreeBalance = []

        self.IDTreeBalancedict = {}
        for x in range(self.ListLen):
            # TreeBalance = self.getTreeBalancebyMycode(x)
            TreeBalance = self.getTreeBalancebyIndex(x)
            self.indexOfTreeBalance.append(TreeBalance)
            self.IDTreeBalancedict[self.sortedMycodeListdict[x]['mycode']] = TreeBalance

        self.saveList("IDTreeBalancedict", self.IDTreeBalancedict)
        ti.stop("genIndexbyTreeBalance")

    def genIndexbyvipTreeBalance(self):
        ti.start("genIndexbyvipTreeBalance")
        self.indexOfvipTreeBalance = []
        self.IDvipTreeBalancedict = {}
        self.indexOfvipTag = []

        for x in range(self.ListLen):
            vipBalance = self.getvipTreeBalancebyIndex(x)
            vipTag = 1 if vipBalance >= Nums.VipStdBalance else 0
            self.indexOfvipTreeBalance.append(vipBalance)
            self.IDvipTreeBalancedict[self.sortedMycodeListdict[x]['mycode']] = vipBalance
            self.indexOfvipTag.append(vipTag)

        # self.saveList("IDvipTreeBalancedict",self.IDvipTreeBalancedict)
        self.saveList("IDvipTreeBalancedict", self.IDvipTreeBalancedict)

        ti.stop("genIndexbyvipTreeBalance")

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

        vipLevel = self.indexOfvipTag[i]
        if (vipLevel == 0 or len(subNodeIndex) < 2):
            return vipLevel

        no1 = 0
        no2 = 0
        if (vipLevel > 0):
            for y in subNodeIndex:
                subvipLevel = self.getvipLevelbyIndex(y)
                subvipLevelList.append(subvipLevel)
                if (subvipLevel >= no1):
                    no2 = no1
                    no1 = subvipLevel
                elif (subvipLevel >= no2):
                    no2 = subvipLevel

            vipLevel = no2 + 1
            # subvipTop2 = heapq.nlargest(2, subvipLevelList)
            #
            # subvipLevel = min(subvipTop2)
            # if (subvipLevel == 0):
            #     vipLevel = vipbase
            # else:
            #     vipLevel = subvipLevel + 1
        else:
            vipLevel = 0

        self.vipLevelCachedValue[i] = vipLevel
        self.IsvipLevelCached[i] = True

        return vipLevel

    def genIndexbyvipLevel(self):
        self.indexOfvipLevel = []
        self.IDvipLeveldict = {}
        for x in range(self.ListLen):
            vipLevel = self.getvipLevelbyIndex(x)
            self.indexOfvipLevel.append(vipLevel)
            self.IDvipLeveldict[self.sortedMycodeListdict[x]['mycode']] = vipLevel

        self.saveList("IDvipLeveldict", self.IDvipLeveldict)

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
        self.IsstaticIncomeTreeCached[Index] = True
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
            raise Exception("Invalid level!", vipLevel)

        return minerCoeff

    def genIndexbystaticIncomeTree(self):
        self.indexOfstaticIncomeTree = []
        self.IDstaticIncomeTreedict = {}
        for x in range(self.ListLen):
            staticIncomeTree = self.getstaticIncomeTreebyIndex(x)
            self.indexOfstaticIncomeTree.append(staticIncomeTree)
            self.IDstaticIncomeTreedict[self.sortedMycodeListdict[x]['mycode']] = staticIncomeTree

    def genIndexbystaticIncomeTreevip(self):
        self.indexOfstaticIncomeTreevip = []
        for x in range(self.ListLen):
            staticIncomeTreevip = self.indexOfstaticIncomeTree[x] * self.getMinerCoeffbyvipLevel(
                self.indexOfvipLevel[x])
            self.indexOfstaticIncomeTreevip.append(staticIncomeTreevip)

    def genFastMinerAward(self):
        ti.start("genFastMinerAward")
        FullList = list(range(self.ListLen))

        while FullList:

            x = FullList.pop()
            # if not ok, should insert back with FullList.insert(0,x)
            vipLevel = self.indexOfvipLevel[x]
            minerCoeff = self.getMinerCoeffbyvipLevel(vipLevel)
            if self.indexOfvipLevel[x] == 0:
                self.IsFastMinerAwardCached[x] = True
                self.FastMinerAwardCachedValue[x] = 0

            else:
                FullNodeTreeList = self.indexOfNodeTreeList[x]
                NodeTreeList = FullNodeTreeList[1:]
                if NodeTreeList:
                    OK = True
                    for y in NodeTreeList:
                        if not self.IsFastMinerAwardCached[y]:
                            OK = False
                            FullList.insert(0, x)  # key for loop iterate
                            break

                    if (OK):
                        # all data is avalible

                        # firstLevel
                        subNodeIndex1 = self.indexOfsubNodeListIndex[x]
                        L1Revenue = 0
                        L2Revenue = 0
                        l2 = []
                        for y in subNodeIndex1:
                            subvipLevel = self.indexOfvipLevel[y]

                            if (vipLevel > subvipLevel):
                                revenue = self.indexOfstaticIncome[y] * minerCoeff - self.FastMinerAwardCachedValue[y]
                                l = self.indexOfsubNodeListIndex[y]
                                if l:
                                    l2.extend(l)
                            elif (vipLevel == subvipLevel):
                                revenue = self.indexOfstaticIncome[y] * minerCoeff + self.FastMinerAwardCachedValue[
                                    y] * 0.15
                            else:
                                revenue = self.indexOfstaticIncome[y] * minerCoeff

                            L1Revenue = L1Revenue + revenue

                        subNodeIndex2 = l2.copy()
                        while (subNodeIndex2):

                            y = subNodeIndex2[-1]
                            subNodeIndex2.pop()
                            subvipLevel = self.indexOfvipLevel[y]

                            if vipLevel > subvipLevel:
                                # caculate normal static revenue, every node is iterated!
                                # revenue = self.indexOfTreeBalance[y] * minerCoeff - self.getMinerAwardbyIndex(y)
                                # revenue = self.indexOfstaticIncome[y] * (minerCoeff-self.getMinerCoeffbyvipLevel(subvipLevel))
                                revenue = self.indexOfstaticIncome[y] * minerCoeff - self.FastMinerAwardCachedValue[y]

                                # if revenue < 0:
                                #     revenue = 0
                                #     raise Exception("error for calculate revenue")

                                l = self.indexOfsubNodeListIndex[y].copy()

                                if l:  # use to continue loop, add it subNodeIndex. DFS search
                                    subNodeIndex2.extend(l)

                            else:
                                revenue = self.indexOfstaticIncome[
                                              y] * minerCoeff  # if higher, don't think about the subnode

                            L2Revenue = L2Revenue + revenue

                        self.IsFastMinerAwardCached[x] = True
                        self.FastMinerAwardCachedValue[x] = L2Revenue + L1Revenue

                else:
                    self.IsFastMinerAwardCached[x] = True
                    self.FastMinerAwardCachedValue[x] = 0

        ti.stop("genFastMinerAward")

    def getMinerAwardbyIndex(self, Index):
        vipLevel = self.indexOfvipLevel[Index]
        if vipLevel == 0:
            return 0

        if self.IsMinerAwardCached[Index]:
            return self.MinerAwardCachedValue[Index]

        minerCoeff = self.getMinerCoeffbyvipLevel(vipLevel)
        grandsonNodeList = []
        MinerAward = 0

        subAwardict = {}  # [y.mycode] = revenue
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
                revenue = self.indexOfstaticIncome[y] * minerCoeff
                if vipLevel > subvipLevel:
                    # caculate normal static revenue,can't use indexOfstaticIncomeTreevip, since it should change by vip Level
                    # revenue = self.indexOfstaticIncomeTreevip[y]  - self.getMinerAwardbyIndex(y)
                    # also it should not be indexOfstaticIncomeTree, since the case V1-V0-v3. Only way we do is that caculate contribute v0 itself. then it's subnode
                    # 计算从子节点拿到的收益，并扣除该节点的矿圈收益。 仅计算该子节点，不能计算下属全部节点，因为下属如果有一个巨大的高级节点，实际是错误收益
                    # 典型例子 v1 - v0 - v3，此时计算V1收益，必然会是 v0.staticIncome* minercoeff，而不是 (V0+V3)*staticIncome* minercoeff -MinerAward(V0)-MinerAward(V3)
                    # 后者会出现负值
                    # 所以变为：仅计算本地节点
                    revenue -= self.getMinerAwardbyIndex(y)

                    # grandsonNodeList = self.indexOfsubNodeListIndex[y]
                    # should use copy method
                    vipgrandsonNodeList = self.indexOfsubNodeListIndex[y].copy()

                    # 添加子节点的子节点，即孙子节点到计算列表
                    if vipgrandsonNodeList:
                        grandsonNodeList.extend(vipgrandsonNodeList)

                elif vipLevel == subvipLevel:
                    revenue += self.getMinerAwardbyIndex(
                        y) * Nums.sameLevelRate
                else:
                    revenue = 0

                MinerAward += revenue

                mycodename = self.sortedMycodeListdict[y]['mycode']
                subAwardict[mycodename] = revenue

            subNodeIndex = grandsonNodeList.copy()

            while subNodeIndex:
                y = subNodeIndex[-1]
                subNodeIndex.pop()
                subvipLevel = self.indexOfvipLevel[y]

                revenue = self.indexOfstaticIncome[y] * minerCoeff
                if vipLevel > subvipLevel:
                    # caculate normal static revenue, every node is iterated!
                    # revenue = self.indexOfTreeBalance[y] * minerCoeff - self.getMinerAwardbyIndex(y)
                    # revenue = self.indexOfstaticIncome[y] * (minerCoeff-self.getMinerCoeffbyvipLevel(subvipLevel))
                    revenue -= self.getMinerAwardbyIndex(y)

                    # if revenue < 0:
                    #     revenue = 0
                    #     raise Exception("error for calculate revenue")

                    vipsub2NodeList = self.indexOfsubNodeListIndex[y].copy()

                    if vipsub2NodeList:  # use to continue loop, add it subNodeIndex. DFS search
                        subNodeIndex.extend(vipsub2NodeList)

                MinerAward += revenue
                mycodename = self.sortedMycodeListdict[y]['mycode']
                subAwardict[mycodename] = revenue

        else:
            MinerAward = 0
            raise Exception("error for calculat revenue since subnodelist is empty")

        self.MinerAwardCachedValue[Index] = MinerAward
        self.IsMinerAwardCached[Index] = True

        self.indexOfsubAwardict[Index] = subAwardict
        # with open(f'./debug{self.savetime}.txt', 'a') as w:
        #     w.write(f"\n{self.sortedMycodeListdict[Index]['mycode']}:\t{MinerAward}\n")
        #     # for key, value in subAwardict.items():
        #     #     w.write('{key}:\t{value}\n'.format(key=key, value=value))
        #     for i, k in enumerate(subAwardict):
        #         w.write(f'{i}:\t{k}\t{subAwardict[k]} \n')
        #     # w.write(f"{subAwardict}\n")
        return MinerAward

    def getRecommendAwardbyIndex(self, Index):
        subNodeIndex = self.indexOfsubNodeListIndex[Index]

        # validMinerList=[self.indexOfusedBalance[x] for x in subNodeIndex if self.indexOfusedBalance[x]>0]
        subNodeIndexValid = [x for x in subNodeIndex if self.indexOfusedBalance[x] > 0]

        r1 = 0
        r2 = 0
        RecommmendLevel = len(subNodeIndexValid)
        if RecommmendLevel == 0:
            r1 = 0
        elif (RecommmendLevel < 3):

            minerProductiveX = self.indexOfminerProductive[Index]
            BalanceX = self.indexOfusedBalance[Index]

            # subNodeList = self.getListHit(self.indexOfID, subNodeIndex)
            for y in subNodeIndexValid:
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

    def genIndexbyMinerAward(self):
        ti.start("genIndexbyMinerAward")

        self.indexOfMinerAward = []
        self.IDMinerAwarddict = {}
        for x in range(self.ListLen):
            MinerAward = self.getMinerAwardbyIndex(x)
            self.indexOfMinerAward.append(MinerAward)
            self.IDMinerAwarddict[self.sortedMycodeListdict[x]['mycode']] = MinerAward

        self.saveList("MinerAwarddict",self.IDMinerAwarddict)
        ti.stop("genIndexbyMinerAward")

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

    def genAllIndex(self):
        ti.start("total Index")
        self.InitCacheList()
        self.genIndexbysubNodeListIndex()
        self.genIndexbyGrandSonNodeListIndex()
        self.genIndexbyNodeLevel()
        self.genIndexbyNodeTreeList()
        self.genIndexbystaticIncome()

        self.genIndexbyTreeBalance()
        self.genIndexbyvipTreeBalance()
        self.genIndexbyvipLevel()
        self.genIndexbysubNodevipLevelIndex()

        self.genIndexbystaticIncomeTree()
        self.genIndexbystaticIncomeTreevip()
        self.genFastMinerAward()
        self.genIndexbyMinerAward()
        self.genIndexbyRecommendAward()
        self.genIndexbyTotalAward()
        self.genAllNodeTreeInfoJson()
        ti.stop("Total Index")


if __name__ == "__main__":
    t = CheckSQLData()
    print("start test ...")
    t.initDB()
    t.LoadSQLData()
    t.genAllIndex()
    t.saveData()
    t.saveData2excel()
    t.closDB()
