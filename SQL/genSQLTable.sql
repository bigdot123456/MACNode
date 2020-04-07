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
