# MACNode
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

## second generate test vector
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