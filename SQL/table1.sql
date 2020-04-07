select version(),current_date();
show databases;
create database fastroot1 DEFAULT CHARSET utf8 COLLATE utf8_general_ci; #创建数据库:
use fastroot;
SHOW TABLES;
CREATE TABLE `dbtable` (
`nid` int(11) NOT NULL auto_increment,
`name` varchar(255) DEFAULT 'bigdot',
`email` varchar(255),
PRIMARY KEY (`nid`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert into dbtable values(1,'hello','big@qq.com');
insert into dbtable values(3,'2helloss','ssbig@qq.com');
insert into dbtable(name,email) values("fff","start1@qq.com");
select * from dbtable;
show tables;
update dbtable set email = "start2@qq.com" where nid = 1; #需要通过主键选择
alter table dbtable add column single char(1);

DESCRIBE dbtable;

# delete from tab2 where nid=2;

SELECT * FROM dbtable WHERE name = "f" AND email = "qq.com";
SELECT * FROM dbtable