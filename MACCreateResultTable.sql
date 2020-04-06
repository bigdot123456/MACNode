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