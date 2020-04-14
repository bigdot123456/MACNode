const mysql = require('./mysql');

// 白银矿机
// 算力：2000T
// 购买价格：300 USDT
// 矿机总产量：12,000 MAC价值约600 USDT
// 静态挖矿收益率约：1%/天

// 白银矿机每天的静态产量为：60MAC/天 

// 黄金矿机
// 算力：4800T
// 购买价格：1000 USDT
// 矿机总产量：44,000 MAC 价值约 2200 USDT
// 静态挖矿收益率约：1.1%/天

// 黄金矿机每天的静态产量为：220 MAC/天

// 白金矿机
// 算力：9800T
// 购买价格：2000 USDT
// 矿机总产量：100,000 MAC 价值约 5000 USDT
// 静态挖矿收益率约：1.2%/天

// 白金矿机每天的实际产量为：480 MAC/天

// 钻石矿机
// 算力：21800T
// 购买价格：4000 USDT
// 矿机总产量：240,000 MAC 价值约 12000 USDT
// 静态挖矿收益率约：1.3%/天

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

const vipquota = 3000; //vip 限额

//const vipStandard = 30000

const Services = {};

const SQLSelect = "SELECT user.mycode, user.code ,user.phone,IFNULL(asset_fund.fund,0) as rootfund,IFNULL(asset_fund.fundtype,0) as fundType,asset_fund.starttime FROM  user left join asset_fund on (asset_fund.userid=user.phone) "
//先计算所有 下线的vip等级 及日产量
//至上而下遍历，所有下级，v大于自己的，跳过所有子节点计算，v

//日产量*收益率 + 该节点平级计算 - 该节点下级矿圈收益 
//剔除vip平级或者高级下线
function dynamic1(community, vip) {
    let dynamic = {};
    dynamic.dailyproduction = 0; //日产量
    dynamic.dynamic = 0;
    // console.log(community);
    for (let i = 0; i < community.length; i++) {
        let item = community[i];
        if (vip <= item.vip) {
            dynamic.dailyproduction += item.mydaily;
            dynamic.dynamic += item.mydynamic;
            //跳过改线
            continue;
        } else if (vip > item.vip) {
            //统计日产量
            dynamic.dailyproduction += item.mydaily;
            dynamic.dynamic += item.mydynamic;
            let ret = dynamic1(item.community, vip)
            dynamic.dailyproduction += ret.dailyproduction;
            dynamic.dynamic += ret.dynamic;
        }
    }
    return dynamic;
}

//添加vip 平级奖励
function dynamic2(community, vip) {
    let dynamic = {};
    dynamic.sameaward = 0; //平级奖励
    for (let i = 0; i < community.length; i++) {
        let item = community[i];
        if (vip == item.vip) {
            //平级计算
            dynamic.sameaward += item.dailyproduction;
            continue;
        }
    }
    return dynamic;
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
    let fundinfo = await mysql.ROW(SQLStatement);

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
    console.log(SQLStatement)
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

        let SQLStatement1 = SQLSelect + " where " + multiusr + " ;"
        console.log(SQLStatement1)
        let usrInfoL2 = await mysql.ROW(SQLStatement1);
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
    let treeNodeInfoList={}

    let SQLStatement = SQLSelect + " where mycode= '" + mycode + "' ;"
    console.log(SQLStatement)
    let rootInfo = await mysql.ROW(SQLStatement);
    treeNodeInfoList.rootInfo = rootInfo
    treeNodeInfoList.rootfund = rootInfo[0].rootfund
    treeNodeInfoList.totalTreefund= treeNodeInfoList.rootfund

    SQLStatement = SQLSelect + " where code= '" + mycode + "' ;"
    console.log(SQLStatement)
    let usrInfoL1 = await mysql.ROW(SQLStatement);
    treeNodeInfoList.subNodeL1Info = usrInfoL1
    treeNodeInfoList.subNodeL1Num = usrInfoL1.length
    treeNodeInfoList.layFund = [treeNodeInfoList.rootfund]
    treeNodeInfoList.TreeInfo = [rootInfo]

    while (usrInfoL1 && usrInfoL1.length>0) {
        let multiusr = ""
        let subfund = 0
        for (let y of usrInfoL1) {
            multiusr += " code='" + y.mycode + "' or"
            subfund += y.rootfund
        }
        treeNodeInfoList.totalTreefund+=subfund
        treeNodeInfoList.layFund.push(subfund)
        treeNodeInfoList.layFund.push(usrInfoL1)


        multiusr = multiusr.slice(0, -3)
        let SQLStatement1 = SQLSelect + " where " + multiusr + " ;"
        console.log(SQLStatement1)
        usrInfoL1 = await mysql.ROW(SQLStatement1);
    }

    return treeNodeInfoList
}

async function getvipTag(mycode) {
    let vip = {}
    vip.subTreeBalanceList = []
    vip.subTreeBalanceInfoList=[]
    vip.totalTreefund=0

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

    if (vip.RootSubNodeInfoList.subNodeL1Num === 0) {
        vip.balancevip = 0
        vip.vipTag = 0
        vip.subTreeBalancesum = 0
    } else {
        let max = 0
        let sum = 0
        // for (let i = 0; i < vip.RootSubNodeInfoList.mycodeSubNodeListL1.length; i++) {
        for (let L1 of vip.mycodeSubNodeListL1) {

            let x=await getTreeBalanceInfowfs(L1)
            vip.subTreeBalanceInfoList.push(x)
            let y=x.totalTreefund
            vip.subTreeBalanceList.push(y)
            sum += y
            max = y > max ? y : max
        }
        vip.balancevip = (sum - max)
        vip.subTreeBalancesum = sum
        vip.vipTag = vip.balancevip >= vipquota ? 1 : 0
    }

    vip.totalTreefund=vip.subTreeBalancesum+vip.rootfund

    return vip
}

async function getvipLevel(mycode) {
    let vip = {}
    vip.vipLevel = 0
    vip.minerCoeff = 0
    vip.subvipLevel = []
    vip.subvipLevelCallResult = []

    vip.vipTagRoot = await getvipTag(mycode)

    vip.subTreeBalanceList       =vip.vipTagRoot.subTreeBalanceList
    vip.subTreeBalanceInfoList   =vip.vipTagRoot.subTreeBalanceInfoList
    vip.totalTreefund            =vip.vipTagRoot.totalTreefund

    vip.RootSubNodeInfoList      =vip.vipTagRoot.RootSubNodeInfoList
    vip.rootInfo                 =vip.vipTagRoot.rootInfo
    vip.subNodeL1Info            =vip.vipTagRoot.subNodeL1Info
    vip.mycodeSubNodeListL1      =vip.vipTagRoot.mycodeSubNodeListL1

    vip.subNodeL1Fund            =vip.vipTagRoot.subNodeL1Fund
    vip.subNodeL1Num             =vip.vipTagRoot.subNodeL1Num

    vip.recomend1                =vip.vipTagRoot.recomend1
    vip.recomend2                =vip.vipTagRoot.recomend2
    vip.recomend                 =vip.vipTagRoot.recomend
    vip.mycode                   =vip.vipTagRoot.mycode

    vip.rootInfo                 =vip.vipTagRoot.rootInfo
    vip.rootfund                 =vip.vipTagRoot.rootfund
    vip.rootmill                 =vip.vipTagRoot.rootmill
    vip.phone                    =vip.vipTagRoot.phone

    vip.balancevip               =vip.vipTagRoot.balancevip
    vip.vipTag                   =vip.vipTagRoot.vipTag
    vip.subTreeBalancesum        =vip.vipTagRoot.subTreeBalancesum

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

    vip.vipLevel               =     vip.RootvipLevel.vipLevel
    vip.minerCoeff             =     vip.RootvipLevel.minerCoeff
    vip.subvipLevel            =     vip.RootvipLevel.subvipLevel
    vip.subvipLevelCallResult  =     vip.RootvipLevel.subvipLevelCallResult

    vip.vipTagRoot             =     vip.RootvipLevel.vipTagRoot

    vip.subTreeBalanceList     =     vip.RootvipLevel.subTreeBalanceList
    vip.TreeBalanceInfo        =     vip.RootvipLevel.TreeBalanceInfo

    vip.RootSubNodeInfoList    =     vip.RootvipLevel.RootSubNodeInfoList
    vip.rootInfo               =     vip.RootvipLevel.rootInfo
    vip.subNodeL1Info          =     vip.RootvipLevel.subNodeL1Info
    vip.mycodeSubNodeListL1    =     vip.RootvipLevel.mycodeSubNodeListL1

    vip.subNodeL1Fund          =     vip.RootvipLevel.subNodeL1Fund
    vip.subNodeL1Num           =     vip.RootvipLevel.subNodeL1Num

    vip.recomend1              =     vip.RootvipLevel.recomend1
    vip.recomend2              =     vip.RootvipLevel.recomend2
    vip.recomend               =     vip.RootvipLevel.recomend
    vip.mycode                 =     vip.RootvipLevel.mycode

    vip.rootInfo               =     vip.RootvipLevel.rootInfo
    vip.rootfund               =     vip.RootvipLevel.rootfund
    vip.rootmill               =     vip.RootvipLevel.rootmill
    vip.phone                  =     vip.RootvipLevel.phone

    vip.balancevip             =     vip.RootvipLevel.balancevip
    vip.vipTag                 =     vip.RootvipLevel.vipTag
    vip.subTreeBalancesum      =     vip.RootvipLevel.subTreeBalancesum

    vip.AwardContribute = [] // 下属节点的贡献度

    let revenue = 0

    let minerCoeff = vip.minerCoeff
    let vipgrandsonNodeList = []
    let subAwardict = {}
    if (vip.vipLevel > 0) {
        if (vip.subvipLevel) {
            let subNodeIndex = vip.subNodeL1Info.slice(0)
            while (subNodeIndex) {
                // let y=subNodeIndex.slice(-1)
                let y = subNodeIndex.pop()
                revenue = minerCoeff * y.rootfund
                if (vip.vipLevel  >= y.vipLevel) {
                    let subFastMinerAward = await getFastMinerAward(y.mycode)
                    if (vip.vipLevel  > y.vipLevel) {
                        revenue -= subFastMinerAward.Award

                        if (subFastMinerAward.subNodeL1Info) {
                            vipgrandsonNodeList.push(subFastMinerAward.subNodeL1Info)
                        }

                    } else {
                        revenue += subFastMinerAward.Award * 0.15
                    }
                }
                vip.Award = vip.Award + revenue
                subAwardict[y.mycode] = revenue
            }
            subNodeIndex = vipgrandsonNodeList
            while (subNodeIndex) {
                // let y=subNodeIndex.slice(-1)
                let y = subNodeIndex.pop()
                revenue = minerCoeff * y.rootfund
                if (vipLevel >= y.vipLevel) {
                    let subFastMinerAward = await getFastMinerAward(y.mycode)
                    if (vipLevel > y.vipLevel) {
                        revenue -= subFastMinerAward.Award

                        if (subFastMinerAward.subvipLevelCallResult) {
                            subNodeIndex.push(subFastMinerAward.subvipLevelCallResult)
                        }

                    }
                }

                vip.Award = vip.Award + revenue
                subAwardict[y.mycode] = revenue
            }
        } else {
            vip.Award = 0
            console.log("error with vip level >0, but no subsidy")
        }

    }
    vip.AwardContribute = subAwardict
    return vip
}

//获取动态收益

async function getMyDynamic(mycode, fund, la) {
    let community = {};

    //直推收益，一比一燃烧
    let fundvalue = fund;

    //日产量
    community.dailyproduction = 0;
    //总投入
    community.totalfund = 0;
    //最大下线金额
    community.biggestline = 0;
    //我的矿圈动态收益
    community.mydynamic = 0;
    //所有下线矿圈动态收益
    community.totaldynamic = 0;

    //直推一级静态收益
    community.child1 = 0;
    //直推二级静态收益
    community.child2 = 0;

    //直退下级等级数量
    community.vip1 = 0;
    community.vip2 = 0;
    community.vip3 = 0;
    community.vip4 = 0;
    community.vip5 = 0;
    community.vip = 0;

    community.vip11 = 0;
    community.vip22 = 0;
    community.vip33 = 0;
    community.vip44 = 0;
    community.vip55 = 0;

    community.totalchild = 0;
    community.validchild = 0;
    community.community = []
    community.community2 = []

    let laa = la + 1;
    //每日静态产量
    let mymill = 0;
    //获取下级
    let layer = await mysql.ROW("select * from user where code ='" + mycode + "';");
    if (layer && layer.length > 0) {
        // 下级收益
        for (let i = 0; i < layer.length; i++) {

            let myfundtemp = 0;
            let ret = await getMyDynamic(layer[i].mycode, fundvalue, laa);
            community.dailyproduction += ret.dailyproduction;
            community.totalfund += ret.totalfund;
            community.community2.push.apply(community.community2, ret.community2);
            community.vip55 += ret.vip55;
            community.vip44 += ret.vip44;
            community.vip33 += ret.vip33;
            community.vip22 += ret.vip22;
            community.vip11 += ret.vip11;
            community.totalchild += ret.totalchild;

            community.totalchild++;
            // community.totaldynamic += ret.totaldynamic;
            community.child1 += ret.child1;
            community.child2 += ret.child2;

            if (ret.vip4 + ret.vip5 >= 2) {
                community.vip5++;
                community.vip55++;
                community.vip = 5;
            } else if (ret.vip3 + ret.vip4 + ret.vip5 >= 2) {
                community.vip4++;
                community.vip44++;
                community.vip = 4;
            } else if (ret.vip2 + ret.vip3 + ret.vip4 + ret.vip5 >= 2) {
                community.vip3++;
                community.vip33++;
                community.vip = 3;
            } else if (ret.vip1 + ret.vip2 + ret.vip3 + ret.vip4 + ret.vip5 >= 2) {
                community.vip2++;
                community.vip22++;
                community.vip = 2;
            } else if (ret.totalfund - ret.biggestline > vipquota) {
                community.vip1++;
                community.vip11++;
                community.vip = 1;
            } else {
                community.vip = 0;
            }

            // community.mill4 += ret.mill4;
            let fundinfo = await mysql.ROW("select * from asset_fund where userid= '" + layer[i].phone + "' ;");
            if (fundinfo && fundinfo.length > 0) {
                for (let j = 0; j < fundinfo.length; j++) {
                    community.totalfund += fundinfo[j].fund;
                    ret.totalfund += fundinfo[j].fund;
                    myfundtemp += fundinfo[j].fund;
                    if (fundinfo[j].fundtype == 1) {
                        mymill += mill1;
                    } else if (fundinfo[j].fundtype == 2) {
                        mymill += mill2;
                    } else if (fundinfo[j].fundtype == 3) {
                        mymill += mill3;
                    } else if (fundinfo[j].fundtype == 4) {
                        mymill += mill4;
                    }
                }
                community.dailyproduction += mymill;
                community.validchild++;
            }
            //抛除最多一条线
            if (ret.totalfund > community.biggestline)
                community.biggestline = ret.totalfund;

            if (community.vip == 1) {
                let myret = dynamic1(ret.community, community.vip);
                let sameaward = dynamic2(ret, community.vip);
                community.mydynamic = (myret.dailyproduction + sameaward.sameaward * 0.15) * 0.1 - myret.dynamic;
                if (community.mydynamic < 0) {
                    community.mydynamic = 0;
                }
            } else if (community.vip == 2) {
                // community.mydynamic = ret.dailyproduction * 0.15 -  ret.totaldynamic;
                let myret = dynamic1(ret.community, community.vip);
                let sameaward = dynamic2(ret.community, community.vip);

                community.mydynamic = (myret.dailyproduction + sameaward.sameaward * 0.15) * 0.15 - myret.dynamic;
                if (community.mydynamic < 0) {
                    community.mydynamic = 0;
                }
            } else if (community.vip == 3) {
                let myret = dynamic1(ret.community, community.vip);
                let sameaward = dynamic2(ret.community, community.vip);

                community.mydynamic = (myret.dailyproduction + sameaward.sameaward * 0.15) * 0.2 - myret.dynamic;
                if (community.mydynamic < 0) {
                    community.mydynamic = 0;
                }
            } else if (community.vip == 4) {
                let myret = dynamic1(ret.community, community.vip);
                let sameaward = dynamic2(ret.community, community.vip);

                community.mydynamic = (myret.dailyproduction + sameaward.sameaward * 0.15) * 0.25 - myret.dynamic;
                if (community.mydynamic < 0) {
                    community.mydynamic = 0;
                }
            } else if (community.vip == 5) {
                let myret = dynamic1(ret.community, community.vip);
                let sameaward = dynamic2(ret.community, community.vip);
                community.mydynamic = (myret.dailyproduction + sameaward.sameaward * 0.15) * 0.3 - myret.dynamic;
                if (community.mydynamic < 0) {
                    community.mydynamic = 0;
                }
            } else {
                community.mydynamic = 0;
            }
            community.totaldynamic += community.mydynamic;
            community.community.push({
                vip: community.vip,
                childfund: ret.totalfund,
                dailyproduction: ret.dailyproduction,
                mydynamic: community.mydynamic,
                mydaily: mymill,
                myfund: myfundtemp,
                phone: layer[i].phone,
                community: ret.community
            });

            community.community2.push({
                vip: community.vip,
                myfund: myfundtemp,
                phone: layer[i].phone,
            })

            //推广奖励 1：1 燃烧
            if (laa == 1) {
                if (mymill > fundvalue)
                    community.child1 += fundvalue * 0.5;
                else
                    community.child1 += mymill * 0.5
            } else if (laa == 2) {
                if (mymill > fundvalue)
                    community.child2 += fundvalue * 0.2;
                else
                    community.child2 += mymill * 0.2;
            }
        }

    }

    return community;
}

Services.calculateEarnings = async function () {

    let timestamp = new Date().getTime();
    console.log(timestamp)
    let timestamp1 = timestamp - (timestamp + 8 * 3600 * 1000) % 86400000
    console.log(timestamp1);

    // 可以设置及一个账户或者全部账户
    // let users = await mysql.EXECUTE("select * from user");
    let users = await mysql.EXECUTE("select * from user where phone='8615923582339'");
    if (users && users.length > 0) {
        for (let i = 0; i < users.length; i++) {
            console.log('n', i, "user:", users[i].phone);
            let myfund = await mysql.ROW("select * from asset_fund where userid='" + users[i].phone + "' and status=1;")
            console.log('fund:', myfund.length)
            if (myfund && myfund.length > 0) {
                let timestamp2 = (Math.floor((myfund[0].starttime) / (1000 * 60 * 60 * 24)) + 1) * 1000 * 60 * 60 * 24 - 8 * 60 * 60 * 1000;
                //收益从激活的第二天开始计算
                if ((timestamp - timestamp2) < 24 * 60 * 60 * 1000) {
                    console.log("start time:", myfund[0].starttime)
                    console.log('收益从激活的第二天开始计算！')
                    continue;
                }
                //今日算过收益的跳过
                if (myfund[0].updatetime > timestamp1) {
                    console.log('今日已计算过收益，明天再算！！')
                    // continue;
                }
                let mytotalfund = 0;
                let mymill = 0;
                //计算我的静态收益
                for (let j = 0; j < myfund.length; j++) {
                    if (myfund[j].fundtype == 1) {
                        mymill += mill1;
                    } else if (myfund[j].fundtype == 2) {
                        mymill += mill2;
                    } else if (myfund[j].fundtype == 3) {
                        mymill += mill3;
                    } else if (myfund[j].fundtype == 4) {
                        mymill += mill4;
                    }
                    mytotalfund += myfund[j].fund;
                }
                console.log('mymill:' + mymill);
                console.log("mytotalfund" + mytotalfund);
                // 获取动态收益
                let community = await getMyDynamic(users[i].mycode, mymill, 0);
                //
                // community.totalfund = community.totalfund;
                console.log('totalfund', community.totalfund)
                // 矿圈奖励
                if (community.vip4 + community.vip5 >= 2) {
                    community.vip = 5;
                    community.rate = 0.3
                } else if (community.vip3 + community.vip4 + community.vip5 >= 2) {
                    community.rate = 0.25;
                    community.vip = 4;
                } else if (community.vip2 + community.vip3 + community.vip4 + community.vip5 >= 2) {
                    community.rate = 0.20;
                    community.vip = 3;
                } else if (community.vip1 + community.vip2 + community.vip3 + community.vip4 + community.vip5 >= 2) {
                    community.rate = 0.15
                    community.vip = 2;
                } else if (community.totalfund - community.biggestline > vipquota) {
                    community.vip = 1;
                    community.rate = 0.1;
                } else {
                    community.vip = 0;
                    community.rate = 0;
                }
                community.mydynamic = 0
                if (community.vip != 0) {
                    let myret = dynamic1(community.community, community.vip);
                    let sameaward = dynamic2(community.community, community.vip);
                    community.mydynamic = (myret.dailyproduction + sameaward.sameaward * 0.15) * community.rate - myret.dynamic;
                    if (community.mydynamic < 0) {
                        community.mydynamic = 0;
                    }
                }
                let win = await getFastMinerAward(users[i].mycode)
                console.log(win.mycode, win.rootfund, win.vipLevel, win.Award, win.recomend, win.mill)

                console.log(community.community2)
                // let tt = 0;
                // for(let jj =0;jj<community.community2.length;jj++){
                //   tt += community.community2[jj].myfund;
                // }
                console.log('dailyproduction:', community.dailyproduction)
                console.log('totaldynamic:', community.totaldynamic)
                console.log('&&&&&&&&&&&&&&&&vip', community.vip)
                console.log("矿圈奖励：", community.mydynamic)
                console.log("child1 dynamic：", community.child1)
                console.log("child2 dynamic：", community.child2)
                console.log("validchild:", community.validchild);
                //动态收益 = 矿圈奖励+推广奖励
                let circleaward = community.mydynamic;
                let recommendaward = 0;
                //推广奖励 直推一个人 并且买矿机  可以拿1代的50%  直推三个人  并且买矿机  可以拿二代的20%
                if (community.validchild >= 1) {
                    recommendaward += community.child1;
                }
                if (community.validchild >= 3) {
                    recommendaward += community.child2;
                }
                console.log("推荐奖励：", recommendaward);
                let mydynamic = community.mydynamic + recommendaward;
                console.log('mydynamic:', mydynamic)
                mydynamic = mydynamic / myfund.length;
                let mystatic = 0;

                //更新收益
                for (let j = 0; j < myfund.length; j++) {
                    console.log('update interest');
                    let production = 0;
                    if (myfund[j].fundtype == 1) {
                        mystatic = mill1;
                        production = mill1pro;
                    } else if (myfund[j].fundtype == 2) {
                        mystatic = mill2;
                        production = mill2pro;
                    } else if (myfund[j].fundtype == 3) {
                        mystatic = mill3;
                        production = mill3pro;
                    } else if (myfund[j].fundtype == 4) {
                        mystatic = mill4;
                        production = mill4pro;
                    }
                    myfund[j].dynamic = mydynamic;
                    myfund[j].static = mystatic;

                    myfund[j].production += mydynamic + mystatic;
                    //三倍出局

                    if ((myfund[j].dynamic + myfund[j].static) >= production)
                        myfund[j].status = 2;
                    else
                        myfund[j].status = 1;


                    await mysql.ROW("update asset_fund set static=" + myfund[j].static +
                        ",recommend=" + recommendaward + ",circle=" + circleaward +
                        ",dynamic=" + myfund[j].dynamic + ",production =" + myfund[j].production +
                        ",status=" + myfund[j].status + ",updatetime=" + timestamp + " where id='" + myfund[j].id + "';")

                    // 更新收益订单
                    let type = 1; //静态收益
                    let insertsql = "INSERT INTO bill_interest (userid,timestamp,value,type) VALUES ('"
                    insertsql = insertsql + users[i].phone + "'," + timestamp + "," + mystatic + "," + type + ");"
                    if (mystatic != 0) {
                        await mysql.ROW(insertsql)
                    }
                    // 动态收益
                    if (mydynamic != 0) {
                        type = 2;
                        insertsql = "INSERT INTO bill_interest (userid,timestamp,value,type) VALUES ('"
                        insertsql = insertsql + users[i].phone + "'," + timestamp + "," + mydynamic + "," + type + ");"
                        await mysql.ROW(insertsql);
                    }
                    //更新资产
                    let assetbase = await mysql.ROW("select * from asset_base where phone='" + users[i].phone + "';")
                    if (assetbase && assetbase.length > 0) {
                        assetbase[0].usdtbalance += mydynamic + mystatic;
                        await mysql.ROW("update asset_base set usdtbalance=" + assetbase[0].usdtbalance + " where phone='" + users[i].phone + "';")

                        // //更新收益转入订单
                        // let ordernum = 'in' + timestamp + common.genCode(0);
                        // sql = "INSERT INTO bill_coin (ordernum,coin,type,timestamp,userid,usdt,status) VALUES ('";
                        // sql = sql + ordernum + "'," +1+","+ 7 + "," + timestamp + ",'" + users[i].phone  + "'," + (mydynamic + mystatic) + "," + 2 + ");";
                        // await mysql.ROW(sql);
                    }
                }
            }
        }
    }
}


async function start() {
    // Service.scanInCharge();
    await Services.calculateEarnings();
    console.log('end')

    // setInterval(() => {
    //   console.log("start calculateEarn")
    //   Services.calculateEarnings();
    // }, 1*60*60 * 1000);
};

start();
console.log('start calculate Earning ...')
