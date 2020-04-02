CREATE TABLE `stdMACNode` (
`ID` int NOT NULL auto_increment, 
`Address` varchar(255) NOT NULL Default "MAN.11111111111",
`Balance` int default 0,
`parentID` int,
`name` varchar(255) DEFAULT 'MACMAN',
`tel` varchar(11) DEFAULT '13800138000',
`email` varchar(255),
PRIMARY KEY (`nid`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;