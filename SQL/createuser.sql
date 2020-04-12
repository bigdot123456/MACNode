use test;

CREATE USER 'dog'@'localhost' IDENTIFIED BY '1234567bb';
-- CREATE USER 'dog1'@'192.168.1.101_' IDENTIFIED BY '123456bb';
-- CREATE USER 'dog2'@'%' IDENTIFIED BY '123456bb';
-- CREATE USER 'dog3'@'%' IDENTIFIED BY '';
-- CREATE USER 'dog4'@'%';

GRANT SELECT, INSERT ON test.user TO 'dog'@'%';
GRANT ALL ON *.* TO 'dog'@'%';
GRANT ALL ON maindataplus.* TO 'dog'@'%';
