CREATE TABLE `stdMACNode` (
`ID` int NOT NULL auto_increment, 
`Address` varchar(32) NOT NULL Default "MAN.11111111111",
`Balance` int default 0,
`parentID` int,
`parentAddress` varchar(32) ,
`name` varchar(32) DEFAULT 'MACMAN',
`tel` varchar(11) DEFAULT '13800138000',
`email` varchar(64),
`attendRound` int,
`subNodeNum`      int , -- = 0  # 默认没有小弟                 
`level`           int , -- = 1  # 默认是第一级加入                
`IDleft`          int , -- = 1  # 加入的左值                   
`IDright`         int , -- = 2  # 加入的右值                   
`vipTag`          int , -- = None  # // 是否vip, 每日更新      
                                                  
`untilNowIncome`  int , -- = None  # // 已累计入账的收益          
`staticIncome`    int , -- = None  # // 静态收益              
`subStaticIncome` int , -- = None  # // 下级贡献的收益           
`dynamicIncome`   int , -- = None  # // 动态收益              
                                                  
`withdrawStatus`  int , -- = None  # // 是否提现      
    
PRIMARY KEY (`ID`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;