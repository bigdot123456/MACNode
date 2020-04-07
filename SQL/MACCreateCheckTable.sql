use fastroot;
CREATE TABLE `asset_base` (
  `phone` varchar(32) NOT NULL COMMENT 'account phone',
  `ethaddress` varchar(42) DEFAULT NULL COMMENT 'eth address',
  `tokenbalance` double NOT NULL DEFAULT '0' COMMENT 'token balance',
  `usdtbalance` double NOT NULL DEFAULT '0' COMMENT 'usdt 余额',
  `lockbalance` double DEFAULT '0',
  `tokenaddress` varchar(42) DEFAULT NULL,
  `macbalance` double DEFAULT '0',
  PRIMARY KEY (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `asset_fund` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `fund` double DEFAULT '0' COMMENT '本金',
  `static` double DEFAULT '0' COMMENT '静态利息',
  `dynamic` double DEFAULT '0' COMMENT '动态利息',
  `status` tinyint(1) DEFAULT '0' COMMENT '0、未激活 1、运行、2淘汰',
  `fundtype` int(4) DEFAULT '0' COMMENT '基金类型',
  `userid` varchar(32) NOT NULL COMMENT '用户id',
  `starttime` bigint(20) NOT NULL COMMENT '购买矿机时间',
  `stoptime` bigint(20) DEFAULT '0' COMMENT '退租矿机时间',
  `lastdayinterest` double DEFAULT '0',
  `gas` double DEFAULT '0',
  `attribute` varchar(1024) DEFAULT NULL COMMENT '矿机属性',
  `production` double(20,4) DEFAULT '0.0000',
  `updatetime` bigint(20) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=124 DEFAULT CHARSET=utf8;

CREATE TABLE `user` (
  `name` varchar(20) DEFAULT NULL COMMENT 'username ',
  `phone` varchar(32) NOT NULL COMMENT 'phone number',
  `email` varchar(32) DEFAULT NULL COMMENT 'email address',
  `password` varchar(64) DEFAULT NULL COMMENT 'md5 of password',
  `code` varchar(10) DEFAULT NULL COMMENT 'invitation code',
  `mycode` varchar(10) DEFAULT NULL COMMENT 'my invitation code',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `paypassword` varchar(64) DEFAULT NULL COMMENT 'pay password',
  `status` tinyint(4) DEFAULT NULL COMMENT 'account status',
  `registertime` bigint(20) DEFAULT NULL COMMENT 'register time',
  `countryCode` varchar(8) DEFAULT NULL,
  `signtime` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=200 DEFAULT CHARSET=utf8;
