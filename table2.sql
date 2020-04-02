select * from bigdot;
select * from tab2;
desc bigdot;
show create table bigdot;
create table fast like bigdot;
show full fields from bigdot; 

SELECT * FROM COLUMNS 
WHERE table_name = 'bigdot'; -- 不正确指令
SHOW TABLE STATUS LIKE '%bigdot%'; 


