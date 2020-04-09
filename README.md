# 在线真实环境检查
## 运行测试向量
```bash
python ./MACLoadSQLData.py
```
## 设置SQL
```sql
DROP TABLE IF EXISTS `asset_loadsqldata`;
CREATE TABLE `asset_loadsqldata`
(
    `id`              int(11)     NOT NULL AUTO_INCREMENT,
    `phone`           varchar(32) NOT NULL COMMENT 'phone number',
    `paypassword`     varchar(64)          DEFAULT NULL COMMENT 'pay password',
    `registertime`    bigint(20)           DEFAULT NULL COMMENT 'register time',
    `countryCode`     varchar(8)           DEFAULT NULL,
    `signtime`        bigint(20)           DEFAULT NULL,
    `ethaddress`      varchar(42)          DEFAULT NULL COMMENT 'eth address',
    `tokenbalance`    double      NOT NULL DEFAULT '0' COMMENT 'token balance',
    `usdtbalance`     double      NOT NULL DEFAULT '0' COMMENT 'usdt 余额',
    `lockbalance`     double               DEFAULT '0',
    `tokenaddress`    varchar(42)          DEFAULT NULL,
    `macbalance`      double               DEFAULT '0',
    `name`            varchar(20)          DEFAULT NULL COMMENT 'username ',
    `email`           varchar(32)          DEFAULT NULL COMMENT 'email address',
    `password`        varchar(64)          DEFAULT NULL COMMENT 'md5 of password',
    `code`            varchar(10)          DEFAULT NULL COMMENT 'invitation code',
    `mycode`          varchar(10)          DEFAULT NULL COMMENT 'my invitation code',

    `fund`            double               DEFAULT '0' COMMENT '本金',
    `static`          double               DEFAULT '0' COMMENT '静态利息',
    `dynamic`         double               DEFAULT '0' COMMENT '动态利息',
    `status`          tinyint(1)           DEFAULT '0' COMMENT '0、未激活 1、运行、2淘汰',
    `fundtype`        int(4)               DEFAULT '0' COMMENT '基金类型',
    `userid`          varchar(32) NOT NULL COMMENT '用户id',
    `starttime`       bigint(20)  NOT NULL COMMENT '购买矿机时间',
    `stoptime`        bigint(20)           DEFAULT '0' COMMENT '退租矿机时间',
    `lastdayinterest` double               DEFAULT '0',
    `gas`             double               DEFAULT '0',
    `attribute`       varchar(1024)        DEFAULT NULL COMMENT '矿机属性',
    `production`      double(20, 4)        DEFAULT '0.0000',
    `updatetime`      bigint(20)           DEFAULT '0',


    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;


DROP TABLE IF EXISTS `asset_checkresultPython`;
CREATE TABLE `asset_checkresultPython`
(
    `id`               int(11)     NOT NULL AUTO_INCREMENT,
    `phone`            varchar(32) NOT NULL COMMENT 'phone number',
    `paypassword`      varchar(64)          DEFAULT NULL COMMENT 'pay password',
    `registertime`     bigint(20)           DEFAULT NULL COMMENT 'register time',
    `countryCode`      varchar(8)           DEFAULT NULL,
    `signtime`         bigint(20)           DEFAULT NULL,
    `ethaddress`       varchar(42)          DEFAULT NULL COMMENT 'eth address',
    `tokenbalance`     double      NOT NULL DEFAULT '0' COMMENT 'token balance',
    `usdtbalance`      double      NOT NULL DEFAULT '0' COMMENT 'usdt 余额',
    `lockbalance`      double               DEFAULT '0',
    `tokenaddress`     varchar(42)          DEFAULT NULL,
    `macbalance`       double               DEFAULT '0',
    `name`             varchar(20)          DEFAULT NULL COMMENT 'username ',
    `email`            varchar(32)          DEFAULT NULL COMMENT 'email address',
    `password`         varchar(64)          DEFAULT NULL COMMENT 'md5 of password',
    `code`             varchar(10)          DEFAULT NULL COMMENT 'invitation code',
    `mycode`           varchar(10)          DEFAULT NULL COMMENT 'my invitation code',

    `fund`             double               DEFAULT '0' COMMENT '本金',
    `static`           double               DEFAULT '0' COMMENT '静态利息',
    `dynamic`          double               DEFAULT '0' COMMENT '动态利息',
    `status`           tinyint(1)           DEFAULT '0' COMMENT '0、未激活 1、运行、2淘汰',
    `fundtype`         int(4)               DEFAULT '0' COMMENT '基金类型',
    `userid`           varchar(32) NOT NULL COMMENT '用户id',
    `starttime`        bigint(20)  NOT NULL COMMENT '购买矿机时间',
    `stoptime`         bigint(20)           DEFAULT '0' COMMENT '退租矿机时间',
    `lastdayinterest`  double               DEFAULT '0',
    `gas`              double               DEFAULT '0',
    `attribute`        varchar(1024)        DEFAULT NULL COMMENT '矿机属性',
    `production`       double(20, 4)        DEFAULT '0.0000',
    `updatetime`       bigint(20)           DEFAULT '0',


    `vipTreeBalance`   float                DEFAULT '0' COMMENT 'vip计算的领主金额',
    `vipTag`           int                  DEFAULT '0' COMMENT 'vip标志',
    `vipLevel`         int                  DEFAULT '0' COMMENT 'vip等级',
    `usedBalance`      float                DEFAULT '0' COMMENT '用户用于真实计算的金额',
    `minerProductive`  float                DEFAULT '0' COMMENT '矿机系数',
    `staticIncome`     float,
    `staticIncomeTree` float,
    `MinerAward`       float,
    `RecommendAward`   float,
    `DynamicAward`     float,

    `TotalAward`       float,

    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- CREATE  TABLE IF NOT EXISTS asset_checkresultPython (LIKE asset_loadsqldata);

```
## 产生sqlalchemy辅助文件
```bash

sqlacodegen --outfile MACNodeSQL.py mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8
```
## 运行检查代码
```bash
python ./MACCheckResult.py

```
## 代码关键
```python
   def getMinerAwardbyIndex(self, Index):
        vipLevel = self.indexOfvipLevel[Index]
        if vipLevel == 0:
            return 0

        minerCoeff = self.getMinerCoeffbyvipLevel(vipLevel)

        subNodeIndex = self.indexOfsubNodeListIndex[Index]

        grandsonNodeList = []
        MinerAward = 0
        # can use zip function and depth to optimize code size
        if subNodeIndex:
            # subNodeList = self.getListHit(self.indexOfID, subNodeIndex)
            while subNodeIndex:
                y = subNodeIndex[-1]
                subNodeIndex.pop()
                subvipLevel = self.indexOfvipLevel[y]

                if vipLevel > subvipLevel:
                    # caculate normal static revenue
                    revenue = self.indexOfvipLevel[y] * minerCoeff - self.getMinerAwardbyIndex(y)
                    if revenue < 0:
                        revenue = 0

                    grandsonNodeList = self.indexOfsubNodeListIndex[y]

                    if grandsonNodeList:
                        grandsonNodeList.extend(grandsonNodeList)

                elif vipLevel == subvipLevel:
                    revenue = self.getMinerAwardbyIndex(y) * Nums.sameLevelRate
                else:
                    revenue = 0

                MinerAward = MinerAward + revenue

            subNodeList = grandsonNodeList
            while subNodeList:
                y = subNodeIndex[-1]
                subNodeIndex.pop()
                subvipLevel = self.indexOfvipLevel[y]

                if vipLevel > subvipLevel:
                    # caculate normal static revenue
                    revenue = self.indexOfvipLevel[y] * minerCoeff - self.getMinerAwardbyIndex(y)
                    if revenue < 0:
                        revenue = 0
                        raise Exception("error for calculate revenue")

                    grandsonNodeList = self.indexOfsubNodeListIndex[y]

                    if grandsonNodeList:
                        grandsonNodeList.extend(grandsonNodeList)

                elif vipLevel == subvipLevel:
                    revenue = 0
                else:
                    revenue = 0

                MinerAward = MinerAward + revenue

```
# MACNode测试检查
Use this program to verify database
```bash
git clone https://github.com/bigdot123456/MACNode
```
## 数据库登录方法
1. 打开数据库工具，例如 mysql workbench
* 创建表的过程
```sql
CREATE TABLE `MyMACNode` (
`ID`      int NOT NULL,
`Address` varchar(32) NOT NULL Default "MAN.11111111111s",
`Balance` int default 0,
`parentID` int,
`parentAddress` varchar(32) ,
`name` varchar(32) DEFAULT 'MACMAN',
`tel` varchar(11) DEFAULT '13800138000',
`email` varchar(64),

`attendRound` int,

`NodeLevel` int,
`TreeBalance` float,

`vipTreeBalance` float,
`vipTag` int,
`vipLevel` int,
`usedBalance` float,
`minerProductive` float,
`staticIncome` float,
`staticIncomeTree` float,
`MinerAward` float,
`RecommendAward` float,

`TotalAward` float,
                                                  
`withdrawStatus`  int , -- = None  # // 是否提现      
    
PRIMARY KEY (`ID`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE  TABLE IF NOT EXISTS MyMACNodeResult (LIKE MyMACNode);
select * from MyMACNode;
select * from MyMACNodeResult;

```
* 注意不要将ID设置为 autoincrement
2. 输入链接密码和Ip地址如下：
```bash
用户名/密码: "fastroot:test123456@"
IP: 111.229.168.108
数据库名称: fastroot
```
## first generate sql base
```bash
sqlacodegen --outfile MACNodeSQL.py mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8
```
然后在MACNodeSQL.py添加如下代码，用于支持dict功能
```python
@as_declarative()
class Base:
    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in sqlalchemy.inspection.inspect(self).mapper.column_attrs}

```
然后自动导入对应的sqlalchemy库和as_declarative，即可。

## 单独检查的过程
### second generate test vector
```bash
python ./MACTestGenVipData.py
```

## check database
```bash
python ./MACCalData.py

```
```python
# 在文件MACTestGenVipData.py中修改，也可以数据库直接修改
for stop in stoplist: 
    # range(start, stop[, step])
    for i in range(start, stop):
        node = Mymacnode() # 数据库表名称
        node.ID = i #(stop - i) + start
        node.Address = f'MAN.{level}000{i}'
        node.Balance = random.randint(1, 7000)  ## 修改此处，选择数据如何生成
        node.parentID = random.randint(1, start-1) ## 修改父亲节点，we can change it to i for more strictly test case!
        #node.parentID = random.randint(1, node.ID-1) ## we can change it to i for more strictly test case!
        node.parentAddress = None
        node.name = f"mac{level}{i}"
        node.tel = f'{i * 10 + 1380013800}'
        node.email = None

        s.add(node)
        if i % 1000 == 0:
            s.flush()

    level = level + 1
    start = stop

```

## open mysql to see table `mymacnoderesult`
```sql
select * from mymacnode;
select * from mymacnoderesult;
```

## 如何采集数据
### 通过 SQL简表，获得各自的表单内容

```python

 node.name                 = x['name             ']
 node.phone                = x['phone            ']
 node.email                = x['email            ']
 node.password             = x['password         ']
 node.code                 = x['code             ']
 node.mycode               = x['mycode           ']
 node.id                   = x['id               ']
 node.paypassword          = x['paypassword      ']
 node.status               = x['status           ']
 node.registertime         = x['registertime     ']
 node.countryCode          = x['countryCode      ']
 node.signtime             = x['signtime         ']
                                                        
                                                        
 node.id                   = y['id               ']
 node.fund                 = y['fund             ']
 node.static               = y['static           ']
 node.dynamic              = y['dynamic          ']
 node.status               = y['status           ']
 node.fundtype             = y['fundtype         ']
 node.userid               = y['userid           ']
 node.starttime            = y['starttime        ']
 node.stoptime             = y['stoptime         ']
 node.lastdayinterest      = y['lastdayinterest  ']
 node.gas                  = y['gas              ']
 node.attribute            = y['attribute        ']
 node.production           = y['production       ']
 node.updatetime           = y['updatetime       ']
 
           
 node.phone                = z['phone            ']
 node.ethaddress           = z['ethaddress       ']
 node.tokenbalance         = z['tokenbalance     ']
 node.usdtbalance          = z['usdtbalance      ']
 node.lockbalance          = z['lockbalance      ']
 node.tokenaddress         = z['tokenaddress     ']
 node.macbalance           = z['macbalance       ']
```
通过正则表达式，替换空格
```regexp
 [ ]*\'
```
然后加入异常处理，例如数据不存在，最终结果如下：
```bash

```