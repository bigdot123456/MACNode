CREATE TABLE `MyMACNode` (
`ID`      int NOT NULL auto_increment, 
`Address` varchar(32) NOT NULL Default "MAN.11111111111",
`Balance` int default 0,
`parentID` int,
`parentAddress` varchar(32) ,
`name` varchar(32) DEFAULT 'MACMAN',
`tel` varchar(11) DEFAULT '13800138000',
`email` varchar(64),

`attendRound` int,

`NodeLevel` int,
`TreeBalance` int,

`vipTreeBalance` int,
`vipTag` int,
`vipLevel` int,
`usedBalance` int,
`minerProductive` int,
`staticIncome` int,
`staticIncomeTree` int,
`MinerAward` int,
`RecommendAward` int,

`TotalAward` int,
                                                  
`withdrawStatus`  int , -- = None  # // 是否提现      
    
PRIMARY KEY (`ID`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE  TABLE IF NOT EXISTS MyMACNodeResult (LIKE MyMACNode);
select * from MyMACNodeResult;
