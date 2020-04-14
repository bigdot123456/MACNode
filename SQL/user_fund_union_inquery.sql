SELECT user.mycode, user.code ,user.phone,IFNULL(asset_fund.fund,0),asset_fund.starttime FROM  user left join asset_fund on (asset_fund.userid=user.phone);
SELECT user.mycode, user.code ,user.phone,IFNULL(asset_fund.fund,0),IFNULL(asset_fund.fundtype,0),asset_fund.starttime FROM  user left join asset_fund on (asset_fund.userid=user.phone);

SELECT user.mycode, user.code ,user.phone,IFNULL(asset_fund.fund,0),
asset_fund.starttime FROM  user left join asset_fund on (asset_fund.userid=user.phone)
where mycode="OHU357136";

SELECT user.*,IFNULL(asset_fund.fund,0),asset_fund.starttime FROM  user left join asset_fund on (asset_fund.userid=user.phone);

SELECT user.*,IFNULL(asset_fund.fund,0),asset_fund.starttime 
FROM  user left join asset_fund on (asset_fund.userid=user.phone) 
where user.code = "FXV059138";

-- "select * from asset_fund where userid= '" + phone + "' ;"
select asset_fund.* ,user.mycode, user.code from asset_fund right join user on (asset_fund.userid=user.phone);
