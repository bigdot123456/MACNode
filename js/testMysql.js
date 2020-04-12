const mysql = require('./mysql');
async function testMysql(){
    let fundinfo = await mysql.ROW("select * from asset_fund;");
    let i=fundinfo.length
    console.log(i,fundinfo[0])
    console.log("fs")
}

testMysql()
console.log("finish!")
console.log("finish2!")