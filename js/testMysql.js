const mysql = require('./mysql');

const SQLSelect = "SELECT user.mycode, user.code ,user.phone,IFNULL(asset_fund.fund,0) as rootfund,IFNULL(asset_fund.fundtype,0) as fundType,asset_fund.starttime FROM  user left join asset_fund on (asset_fund.userid=user.phone) "
// 白金矿机每天的实际产量为：1040MAC/天
//总产量
const mill1pro = 600;//600*0.01;//usdt,小型矿机
const mill2pro = 2500;//2200*0.011; //usdt，中型矿机
const mill3pro = 6000;//5000*0.012; //usdt，大型矿机
const mill4pro = 14000;//12000*0.013; //usdt，超级矿机
//矿机日产量
const mill1 = 300 * 0.01;//300*0.01;//usdt,小型矿机
const mill2 = 1000 * 0.011;//1000*0.011; //usdt，中型矿机
const mill3 = 2000 * 0.013;//2000*0.013; //usdt，大型矿机
const mill4 = 4000 * 0.015;//4000*0.015; //usdt，超级矿机

const vipquota = 30000; //vip 限额

let s=0
async function testMysql() {
    let fundinfo = await mysql.ROW("select * from asset_fund;");
    let i = 0
    if (fundinfo)
        i = fundinfo.length

    console.log(i, fundinfo[0])
    console.log("fs")
    return i
}

// start python function
async function getSingleNodeInfo(mycode) {

    let NodeInfo = {}
    // NodeInfo.fundinfo = []
    //let fundinfo = await mysql.ROW("select * from asset_fund where userid= '" + phone + "' ;");
    // valid sql as following:
    // select asset_fund.* ,user.mycode, user.code from asset_fund right join user on (asset_fund.userid=user.phone);
    //SELECT user.mycode, user.code ,user.phone,IFNULL(asset_fund.fund,0),
    // asset_fund.starttime FROM  user left join asset_fund on (asset_fund.userid=user.phone)
    // where mycode="OHU357136";

    // SELECT user.*,IFNULL(asset_fund.fund,0),asset_fund.starttime FROM  user left join asset_fund on (asset_fund.userid=user.phone);
    //"SELECT user.mycode, user.code ,user.phone,IFNULL(asset_fund.fund,0),asset_fund.starttime FROM  user left join asset_fund on (asset_fund.userid=user.phone);"
    // let fundinfo = await mysql.ROW("select asset_fund.*  ,user.mycode, user.code from asset_fund right join user on (asset_fund.userid=user.phone) where mycode= '" + mycode + "' ;");

    let SQLStatement = SQLSelect + " where mycode= '" + mycode + "' ;"
    console.log(SQLStatement)
    let fundinfo = []
    try {
        fundinfo = await mysql.ROW(SQLStatement);
    } catch (e) {
        console.log("SQL Error with" + SQLStatement)
        return {}
    }

    NodeInfo.fundinfo = fundinfo
    // NodeInfo.mymill = 0
    NodeInfo.mycode = fundinfo[0].mycode
    NodeInfo.phone = fundinfo[0].phone

    let mymill = 0
    let subfund = 0
    if (fundinfo && fundinfo.length > 0) {
        for (let j = 0; j < fundinfo.length; j++) {
            subfund += fundinfo[j].rootfund;
            if (fundinfo[j].fundType == 1) {
                mymill += mill1;
            } else if (fundinfo[j].fundType == 2) {
                mymill += mill2;
            } else if (fundinfo[j].fundType == 3) {
                mymill += mill3;
            } else if (fundinfo[j].fundType == 4) {
                mymill += mill4;
            }
        }
    }
    NodeInfo.rootmill = mymill
    NodeInfo.rootfund = subfund
    return NodeInfo
}

function sumFn() {
    var arg = arguments;
    var sum = 0;
    if (arg == '' || arg == ' ' || arg == null) {
        sum = 0;
    } else {
        for (var i = 0; i < arg.length; i++) {
            if (isNaN(arg[i]) || arg[i] == '' || arg[i] == ' ') {
                continue//sum = sum;
            } else {
                sum += arg[i];
            }
        }
    }
    return sum;
}

// moneyInput=[300, 1000, 2000, 4000],
//     dayLimited=[0.01, 0.011, 0.013, 0.015],

function getRecommendValue(a, b) {
    let x = a > b ? b : a
    let y = 0
    if (x < 300) {
        y = 0
    } else if (x < 1000) {
        y = x * 0.010
    } else if (x < 2000) {
        y = x * 0.011
    } else if (x < 4000) {
        y = x * 0.013
    } else {
        y = x * 0.015
    }
    return y
}

async function getSubNodeInfoList(mycode) {
    let SubNodeInfoList = {}
    SubNodeInfoList.rootInfo = []
    SubNodeInfoList.subNodeL1Info = []
    SubNodeInfoList.mycodeSubNodeListL1 = []

    SubNodeInfoList.subNodeL1Fund = 0
    SubNodeInfoList.subNodeL1Num = 0

    SubNodeInfoList.recomend1 = 0
    SubNodeInfoList.recomend2 = 0 // if error, we replace it with eval(r2.join("+")); or use sumfun
    SubNodeInfoList.recomend = 0
    SubNodeInfoList.mycode = mycode

    // if (typeof usrInfo=="null" || usrInfo.length == 0 ){
    //     staticIncomeTree=0
    //     staticIncomeTreevip=0
    // }
    SubNodeInfoList.rootInfo = await getSingleNodeInfo(mycode)
    SubNodeInfoList.rootfund = SubNodeInfoList.rootInfo.rootfund
    SubNodeInfoList.rootmill = SubNodeInfoList.rootInfo.rootmill
    SubNodeInfoList.phone = SubNodeInfoList.rootInfo.phone

    // let usrInfoL1 = await mysql.ROW("select * from user where code ='" + mycode + "';");
    let SQLStatement = SQLSelect + " where code= '" + mycode + "' ;"
    console.log(s++ , " "+SQLStatement)
    let usrInfoL1 = await mysql.ROW(SQLStatement);
    SubNodeInfoList.subNodeL1Info = usrInfoL1
    SubNodeInfoList.subNodeL1Num = usrInfoL1.length

    let validsubNodeL1Num = 0
    let r1 = 0
    let r2 = 0

    for (let x of usrInfoL1) {
        SubNodeInfoList.mycodeSubNodeListL1.push(x.mycode)
        if (x.rootfund) {
            r1 += getRecommendValue(SubNodeInfoList.rootfund, x.rootfund)
            SubNodeInfoList.subNodeL1Fund += (x.rootfund)
            validsubNodeL1Num++
        }
    }
    if (validsubNodeL1Num >= 3) {
        let multiusr = ""
        for (let y of usrInfoL1) {
            multiusr += " code='" + y.mycode + "' or"
        }
        multiusr = multiusr.slice(0, -3)

        let SQLStatement = SQLSelect + " where " + multiusr + " ;"
        console.log(s++ , " "+SQLStatement)
        let usrInfoL2 = await mysql.ROW(SQLStatement);
        for (let z of usrInfoL2) {
            r2 += getRecommendValue(SubNodeInfoList.rootfund, z.rootfund)
            SubNodeInfoList.subNodeL1Fund += (z.rootfund)
        }
    }

    SubNodeInfoList.recomend1 = r1 * 0.5
    SubNodeInfoList.recomend2 = r2 * 0.2 // if error, we replace it with eval(r2.join("+")); or use sumfun
    SubNodeInfoList.recomend = SubNodeInfoList.recomend1 + SubNodeInfoList.recomend2

    return SubNodeInfoList
}

async function getTreeBalanceInfo(mycode) {
    let root = await getSubNodeInfoList(mycode)
    if (root.subNodeL1Num === 0)
        // return root.rootInfo.fund
        return root.rootfund

    let balance = root.rootfund
    for (let i of root.mycodeSubNodeListL1) {
        let x = await getTreeBalanceInfo(i)
        balance += x
    }
    return balance
}

async function getTreeBalanceInfowfs(mycode) {
    let treeNodeInfoList = {}

    let SQLStatement = SQLSelect + " where mycode= '" + mycode + "' ;"
    console.log(s++ , " "+SQLStatement)
    let rootInfo = await mysql.ROW(SQLStatement);
    treeNodeInfoList.rootInfo = rootInfo
    treeNodeInfoList.rootfund = rootInfo[0].rootfund
    treeNodeInfoList.totalTreefund = treeNodeInfoList.rootfund

    SQLStatement = SQLSelect + " where code= '" + mycode + "' ;"
    console.log(s++ , " "+SQLStatement)
    let usrInfoL1 = await mysql.ROW(SQLStatement);
    treeNodeInfoList.subNodeL1Info = usrInfoL1
    treeNodeInfoList.subNodeL1Num = usrInfoL1.length
    treeNodeInfoList.layFund = [treeNodeInfoList.rootfund]
    treeNodeInfoList.TreeInfo = [rootInfo]

    while (usrInfoL1 && usrInfoL1.length > 0) {
        let multiusr = ""
        let subfund = 0
        for (let y of usrInfoL1) {
            multiusr += " code='" + y.mycode + "' or"
            subfund += y.rootfund
        }
        treeNodeInfoList.totalTreefund += subfund
        treeNodeInfoList.layFund.push(subfund)
        treeNodeInfoList.layFund.push(usrInfoL1)


        multiusr = multiusr.slice(0, -3)
        let SQLStatement1 = SQLSelect + " where " + multiusr + " ;"
        console.log(s++ , " "+SQLStatement)
        usrInfoL1 = await mysql.ROW(SQLStatement1);
    }

    return treeNodeInfoList
}

async function getvipTag(mycode) {
    let vip = {}
    vip.subTreeBalanceList = []
    vip.subTreeBalanceInfoList = []
    vip.totalTreefund = 0

    vip.RootSubNodeInfoList = await getSubNodeInfoList(mycode)
    vip.rootInfo = vip.RootSubNodeInfoList.rootInfo
    vip.subNodeL1Info = vip.RootSubNodeInfoList.subNodeL1Info
    vip.mycodeSubNodeListL1 = vip.RootSubNodeInfoList.mycodeSubNodeListL1

    vip.subNodeL1Fund = vip.RootSubNodeInfoList.subNodeL1Fund
    vip.subNodeL1Num = vip.RootSubNodeInfoList.subNodeL1Num

    vip.recomend1 = vip.RootSubNodeInfoList.recomend1
    vip.recomend2 = vip.RootSubNodeInfoList.recomend2
    vip.recomend = vip.RootSubNodeInfoList.recomend
    vip.mycode = vip.RootSubNodeInfoList.mycode

    vip.rootInfo = vip.RootSubNodeInfoList.rootInfo
    vip.rootfund = vip.RootSubNodeInfoList.rootfund
    vip.rootmill = vip.RootSubNodeInfoList.rootmill
    vip.phone = vip.RootSubNodeInfoList.phone
    vip.subTreeBalancesum = 0

    if (vip.RootSubNodeInfoList.subNodeL1Num === 0) {
        vip.balancevip = 0
        vip.vipTag = 0
        vip.subTreeBalancesum = 0
    } else {
        let max = 0
        let sum = 0
        // for (let i = 0; i < vip.RootSubNodeInfoList.mycodeSubNodeListL1.length; i++) {
        for (let L1 of vip.mycodeSubNodeListL1) {

            let x = await getTreeBalanceInfowfs(L1)
            vip.subTreeBalanceInfoList.push(x)
            let y = x.totalTreefund
            vip.subTreeBalanceList.push(y)
            sum += y
            max = y > max ? y : max
        }
        vip.balancevip = (sum - max)
        vip.subTreeBalancesum = sum
        vip.vipTag = vip.balancevip >= vipquota ? 1 : 0
    }

    vip.totalTreefund = vip.subTreeBalancesum + vip.rootfund

    return vip
}

async function getvipLevel(mycode) {
    let vip = {}
    vip.vipLevel = 0
    vip.minerCoeff = 0
    vip.subvipLevel = []
    vip.subvipLevelCallResult = []

    vip.vipTagRoot = await getvipTag(mycode)

    vip.subTreeBalanceList = vip.vipTagRoot.subTreeBalanceList
    vip.subTreeBalanceInfoList = vip.vipTagRoot.subTreeBalanceInfoList
    vip.totalTreefund = vip.vipTagRoot.totalTreefund

    vip.RootSubNodeInfoList = vip.vipTagRoot.RootSubNodeInfoList
    vip.rootInfo = vip.vipTagRoot.rootInfo
    vip.subNodeL1Info = vip.vipTagRoot.subNodeL1Info
    vip.mycodeSubNodeListL1 = vip.vipTagRoot.mycodeSubNodeListL1

    vip.subNodeL1Fund = vip.vipTagRoot.subNodeL1Fund
    vip.subNodeL1Num = vip.vipTagRoot.subNodeL1Num

    vip.recomend1 = vip.vipTagRoot.recomend1
    vip.recomend2 = vip.vipTagRoot.recomend2
    vip.recomend = vip.vipTagRoot.recomend
    vip.mycode = vip.vipTagRoot.mycode

    vip.rootInfo = vip.vipTagRoot.rootInfo
    vip.rootfund = vip.vipTagRoot.rootfund
    vip.rootmill = vip.vipTagRoot.rootmill
    vip.phone = vip.vipTagRoot.phone

    vip.balancevip = vip.vipTagRoot.balancevip
    vip.vipTag = vip.vipTagRoot.vipTag
    vip.subTreeBalancesum = vip.vipTagRoot.subTreeBalancesum

    if (vip.vipTag === 1) {
        let no1 = 0
        let no2 = 0

        // for (let x of vip.vipTagRoot.RootSubNodeInfoList.mycodeSubNodeListL1){
        for (let x of vip.mycodeSubNodeListL1) {
            let L1 = await getvipLevel(x)
            let y = L1.vipLevel
            if (y >= no1) {
                no2 = no1
                no1 = y
            } else if (y >= no2) {
                no2 = y
            }
            vip.subvipLevelCallResult.push(L1)
            vip.subvipLevel.push(y)
        }

        vip.vipLevel = no2 === 0 ? 1 : (no2 + 1)
    }
    if (vip.vipLevel === 0) vip.minerCoeff = 0
    else if (vip.vipLevel === 1) vip.minerCoeff = 0.1
    else if (vip.vipLevel === 2) vip.minerCoeff = 0.15
    else if (vip.vipLevel === 3) vip.minerCoeff = 0.20
    else if (vip.vipLevel === 4) vip.minerCoeff = 0.25
    else if (vip.vipLevel === 5) vip.minerCoeff = 0.30
    else if (vip.vipLevel === 6) vip.minerCoeff = 0.35
    else if (vip.vipLevel === 7) vip.minerCoeff = 0.40
    else console.log("error in vip level")

    return vip
}

// vip.Award = 0
// vip.mycode = mycode
//
// vip.vipLevelCallResult = await getvipLevel(mycode)
//
// vip.RootSubNodeInfoList=vip.vipLevelCallResult.RootSubNodeInfoList
// vip.rootfund = vip.vipLevelCallResult.rootfund
// vip.rootInfo = vip.vipLevelCallResult.rootInfo
// vip.rootmill = vip.vipLevelCallResult.rootmill
// vip.mycode = vip.vipLevelCallResult.mycode
// vip.recomend=vip.vipLevelCallResult.recomend
// vip.recomend1=vip.vipLevelCallResult.recomend1
// vip.recomend2=vip.vipLevelCallResult.recomend2
// vip.mycodeSubNodeListL1=vip.vipLevelCallResult.mycodeSubNodeListL1
//
// vip.minerCoeff=vip.vipLevelCallResult.minerCoeff
//
// vip.level = vip.vipLevelCallResult.vipLevel
// vip.subvipLevel = vip.vipLevelCallResult.subvipLevel
// vip.subvipLevelCallResult = vip.vipLevelCallResult.subvipLevelCallResult
//
// vip.subNodeL1Info=vip.RootSubNodeInfoList.subNodeL1Info
// vip.AwardContribute=[]

async function getFastMinerAward(mycode) {
    let vip = {}
    vip.Award = 0 //矿圈奖励

    vip.RootvipLevel = await getvipLevel(mycode) // 得到VIP等级的结果信息

    vip.vipLevel = vip.RootvipLevel.vipLevel
    vip.minerCoeff = vip.RootvipLevel.minerCoeff
    vip.subvipLevel = vip.RootvipLevel.subvipLevel
    vip.subvipLevelCallResult = vip.RootvipLevel.subvipLevelCallResult

    vip.vipTagRoot = vip.RootvipLevel.vipTagRoot

    vip.subTreeBalanceList = vip.RootvipLevel.subTreeBalanceList
    vip.totalTreefund=vip.RootvipLevel.totalTreefund

    vip.RootSubNodeInfoList = vip.RootvipLevel.RootSubNodeInfoList
    vip.subNodeL1Info = vip.RootvipLevel.subNodeL1Info
    vip.mycodeSubNodeListL1 = vip.RootvipLevel.mycodeSubNodeListL1

    vip.subNodeL1Fund = vip.RootvipLevel.subNodeL1Fund
    vip.subNodeL1Num = vip.RootvipLevel.subNodeL1Num

    vip.recomend1 = vip.RootvipLevel.recomend1
    vip.recomend2 = vip.RootvipLevel.recomend2
    vip.recomend = vip.RootvipLevel.recomend
    vip.mycode = vip.RootvipLevel.mycode

    vip.rootInfo = vip.RootvipLevel.rootInfo
    vip.rootfund = vip.RootvipLevel.rootfund
    vip.rootmill = vip.RootvipLevel.rootmill
    vip.phone = vip.RootvipLevel.phone

    vip.balancevip = vip.RootvipLevel.balancevip
    vip.vipTag = vip.RootvipLevel.vipTag
    vip.subTreeBalancesum = vip.RootvipLevel.subTreeBalancesum

    vip.AwardContribute = [] // 下属节点的贡献度

    console.log(s++,"start monitor:" + vip.mycode)

    let revenue = 0

    let minerCoeff = vip.minerCoeff
    let GrandSonvipLevelCallResultList = []
    let subAwardict = {}
    if (vip.vipLevel > 0) {

        let subvipLevelCallResultList = vip.subvipLevelCallResult.slice(0)
        while (subvipLevelCallResultList && subvipLevelCallResultList.length > 0) {
            // let y=subNodeIndex.slice(-1)
            let y = subvipLevelCallResultList.pop()
            console.log(s++,"start inner monitor:" + y.mycode)
            let z = await getFastMinerAward(y.mycode)
            revenue = minerCoeff * z.rootmill
            if (vip.vipLevel >= z.vipLevel) {
                if (vip.vipLevel > z.vipLevel) {
                    revenue -= z.Award

                    if (z.subvipLevelCallResult && z.subvipLevelCallResult.length > 0) {
                        GrandSonvipLevelCallResultList.push.apply(GrandSonvipLevelCallResultList,z.subvipLevelCallResult)
                    }

                } else {
                    revenue += z.Award * 0.15
                }
            }

            vip.Award = vip.Award + revenue
            subAwardict[y.mycode] = revenue
        }
        subvipLevelCallResultList = GrandSonvipLevelCallResultList
        while (subvipLevelCallResultList && subvipLevelCallResultList.length > 0) {
            // let y=subNodeIndex.slice(-1)
            let y = subvipLevelCallResultList.pop()
            let z = await getFastMinerAward(y.mycode)
            revenue = minerCoeff * z.rootmill

            if (vip.vipLevel >= z.vipLevel) {
                if (vip.vipLevel > z.vipLevel) {
                    revenue -= z.Award

                    if (z.subvipLevelCallResult && z.subvipLevelCallResult.length > 0) {
                        subvipLevelCallResultList.push.apply(subvipLevelCallResultList,z.subvipLevelCallResult)
                    }

                }
            }

            vip.Award = vip.Award + revenue
            subAwardict[y.mycode] = revenue
        }
    } else {
        vip.Award = 0
        console.log(vip.mycode+" is not a vip & no Award with fund is:"+vip.rootfund
            +" balancevip: "+vip.balancevip
            +" subTreeBalancesum: "+vip.subTreeBalancesum
            +" totalTreefund: "+vip.totalTreefund
        )
    }

    vip.AwardContribute = subAwardict
    console.log(s++ , "vip result is \t ",vip.mycode,"\n",vip.AwardContribute,"\n")
    console.log(s++ , "Finish vip caculate ",vip.rootmill,vip.recomend,vip.Award)
    return vip

}

let mycode0 = "HCC246660"

let a = testMysql()
let b = getFastMinerAward(mycode0)
console.log("finish!")
//process.exit()