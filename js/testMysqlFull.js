const mysql = require('./mysql');
// var sprintf = require('sprintf-js').sprintf,
//     vsprintf = require('sprintf-js').vsprintf

let fs = require("fs");
const SQLSelect = "SELECT user.mycode, user.code ,user.phone,IFNULL(asset_fund.fund,0) as myfund,IFNULL(asset_fund.fundtype,0) as fundType,IFNULL(user.status,0) as status,asset_fund.starttime FROM  user left join asset_fund on (asset_fund.userid=user.phone) "

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
const TopFund = 4000 // goodman

let s = 0

// async function testMysql() {
//     let fundinfo = await mysql.ROW("select * from asset_fund;");
//     let i = 0
//     if (fundinfo)
//         i = fundinfo.length
//
//     console.log(i, fundinfo[0])
//     console.log(s++, "finsh initial test")
//     return i
// }


let allNodeInfo = []
let ListLen = 0

async function getSqLFullResult() {
    allNodeInfo = await mysql.ROW(SQLSelect)
    ListLen = allNodeInfo.length
    // 对phone字段进行排序
    allNodeInfo.sort(function (a0, a1) {
        return a0.phone.localeCompare(a1.phone) // must offer correct key
        //    can't use a0-a1 for non digital
    })
    console.log(s++, "Get full Result with ", ListLen)
    return allNodeInfo
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

function writeFile(filename, strbuf) {
    if (strbuf && strbuf.length > 0) {
        console.log("写入文件：", filename);
        // 同步读取
        // var data = fs.writeFileSync('write1.txt', '我是被写入的内容1！');
        // var writeData1 = fs.readFileSync('write1.txt', 'utf-8');
        // console.log("同步读取写入的内容1: " + writeData1.toString());
        // 异步读取
        fs.writeFile(filename, strbuf, function (err) {
            if (err) {
                console.log("写入数据错误" + err);
                return console.error(err);
            }
        });
    } else {
        console("No content with file write!")
    }
}

function saveList(filename, List) {
    let strJSON = JSON.stringify(List, null, '\t');
    let txt0 = strJSON
    // let dim = strJSON.match('},')
    // if (dim !== null) {
    //     txt0 = strJSON.replace(/},/g, '},\n')
    // } else {
    //     txt0 = strJSON.replace(/,/g, ',\n')
    // }

    let myDate = new Date()
    let extDate = myDate.toISOString().replace(/:/g, '')

    let jsonfilename = filename + extDate + ".json"
    let xlsfilename = filename + extDate + ".xlsx"
    let xls1filename = filename + extDate + "mac.xlsx"
    let csvfilename = filename + extDate + ".csv"
    // writeFile(jsonfilename, txt0)
    JSONToExcelConvertorMAC(strJSON, xls1filename)
    // JSONToExcelConvertor(strJSON, xlsfilename)
    // JSONArrayToCSVConventor(strJSON, csvfilename)
}

function JSONToCSVConventor(data, csvfilename, key = null) {
    const Json2csvParser = require('json2csv').Parser;
    // let fs = require('fs');
    const json = JSON.parse(data)
    let fields = ['car', 'price', 'color']
    if (key == null) {
        fields = Object.keys(json)
    } else {
        fields = key
    }

    const json2csvParser = new Json2csvParser({fields})
    const csv = json2csvParser.parse(data)
    fs.writeFile(csvfilename, csv, function (err) {
        if (err) {
            return console.log(err)
        }
        console.log("File " + csvfilename + " was saved!")
    })

}

function JSONArrayToCSVConventor(data, csvfilename, key = null) {
    const Json2csvParser = require('json2csv').Parser;
    // let fs = require('fs');
    const json = JSON.parse(data)

    let fields = []
    if (key == null) {
        let firstData = Object.keys(json)[0]
        fields = Object.keys(json[firstData])
    } else {
        fields = key
    }
    let json2csvParser = new Json2csvParser({fields})
    for (let i in json) {
        let csv = json2csvParser.parse(json[i])
        fs.appendFile(csvfilename, csv, function (err) {
            if (err) {
                return console.log(err)
            }
        })
    }
}

function JSONToExcelConvertor(data, xlsfilename, key = null) {
    let Excel = require('exceljs')
    const json = JSON.parse(data);
    let workbook = new Excel.stream.xlsx.WorkbookWriter({
        filename: xlsfilename
    });
    let worksheet = workbook.addWorksheet('总体账目');

    let fields = []
    if (key == null) {
        let firstData = Object.keys(json)[0]
        fields = Object.keys(json[firstData])
    } else {
        fields = key
    }

    let itemlist = []
    let item = {}
    for (let i in fields) {
        // worksheet.columns[i].header = fields[i]
        // worksheet.columns[i].key = fields[i]
        item.header = fields[i]
        item.key = fields[i]
        let copy = JSON.parse(JSON.stringify(item));
        itemlist[i] = copy
    }
    worksheet.columns = itemlist
    // worksheet.columns = [
    //     {header: '账号', key: '账号'},
    //     {header: '手机', key: '手机'},
    //     {header: '投入本金', key: '投入本金'},
    //     {header: '静态奖励', key: '静态奖励'},
    //     {header: '推荐奖励', key: '推荐奖励'},
    //     {header: '动态奖励', key: '动态奖励'},
    //     {header: 'VIP等级', key: 'VIP等级'},
    //     {header: '特殊身份', key: '特殊身份'},
    // ];
    let temp = {}
    for (let i in json) {
        let info = json[i]
        for (let j in fields) {
            let x = info[fields[j]]
            if (typeof x === "object") {
                temp[fields[j]] = JSON.stringify(info[fields[j]])
            } else {
                temp[fields[j]] = info[fields[j]]
            }

        }
        worksheet.addRow(temp).commit();
    }
    workbook.commit();
    // let xls = json2xls(jsonArray);
    // fs.writeFileSync(xlsfilename, xls, 'binary');
}

function JSONToExcelConvertorMAC(data, xlsfilename) {
    let Excel = require('exceljs')
    const json = JSON.parse(data);
    let workbook = new Excel.stream.xlsx.WorkbookWriter({
        filename: xlsfilename
    });
    let worksheet = workbook.addWorksheet('总体账目');

    worksheet.columns = [
        {header: '账号', key: 'mycode'},
        {header: '手机', key: 'phone'},
        {header: '投入本金', key: 'myfund'},
        {header: '静态奖励', key: 'staticIncome'},
        {header: '推荐奖励', key: 'RecommendAward'},
        {header: '动态奖励', key: 'MinerAward'},
        {header: 'VIP等级', key: 'vipLevel'},
        {header: '特殊身份', key: 'status'},
    ];

    for (let i in json) {
        let info = json[i]
        let temp = {
            'mycode': info.allNodeInfo.mycode,
            'phone': info.allNodeInfo.phone,
            'myfund': info.allNodeInfo.myfund,
            'staticIncome': info.staticIncome,
            'RecommendAward': info.RecommendAward,
            'MinerAward': info.MinerAward,
            'vipLevel': info.vipLevel.vipLevel,
            'status': info.allNodeInfo.status
        }
        //jsonArray.push(temp);
        worksheet.addRow(temp).commit();
    }
    workbook.commit();
    // let xls = json2xls(jsonArray);
    // fs.writeFileSync(xlsfilename, xls, 'binary');
}

// moneyInput=[300, 1000, 2000, 4000],
//     dayLimited=[0.01, 0.011, 0.013, 0.015],

function getRecommendValue(a, b) {
    let x = a > b ? b : a
    let y = 0

    if (x >= 4000) {
        y = x * 0.015
    } else if (x >= 2000) {
        y = x * 0.013
    } else if (x >= 1000) {
        y = x * 0.011
    } else if (x >= 300) {
        y = x * 0.010
    }

    return y
}

function getmill(x) {
    let y = 0

    if (x >= 4000) {
        y = 60
    } else if (x >= 2000) {
        y = 26
    } else if (x >= 1000) {
        y = 11
    } else if (x >= 300) {
        y = 3
    }

    return y
}

var Timer = {
    data: {},
    start: function (key) {
        Timer.data[key] = new Date();
    },
    stop: function (key) {
        var time = Timer.data[key];
        if (time) {
            Timer.data[key] = new Date() - time;
            console.log(s++, key + " time usage: " + Timer.getTime(key) + " ms");
        }
    },
    getTime: function (key) {
        return Timer.data[key];
    }
};

// // test
// Timer.start("div");
// for(var i=0;i<count;i++){
//     document.createElement("div");
// }
// Timer.stop("div");
// console.log("the time is:"+Timer.getTime());

let indexOfsubNodeListIndex = []
let sortedMycodeListdict = {}
let indexOfstaticIncome = []
let IDstaticIncomedict = {}

function genIndexofmycode() {
    if (allNodeInfo && ListLen == 0) {
        console.log(s++, "\nError! not initialize the database info")
    }
    Timer.start("genIndexofmycode");
    //for (let i in allNodeInfo) {
    for (let i = 0; i < ListLen; i++) {
        let x = allNodeInfo[i].mycode
        let y = getmill(allNodeInfo[i].myfund)
        sortedMycodeListdict[x] = i
        indexOfstaticIncome[i] = y
        IDstaticIncomedict[x] = y
    }

    // for (let i in allNodeInfo) {
    for (let i = 0; i < ListLen; i++) {
        let y = allNodeInfo[i].mycode
        let subNodeIndex = []
        // for(let j in allNodeInfo){
        for (let j = 0; j < ListLen; j++) {
            if (allNodeInfo[j].code === y) {
                subNodeIndex.push(j)
            }
        }
        indexOfsubNodeListIndex.push(subNodeIndex)
    }
    Timer.stop("genIndexofmycode");
    return indexOfsubNodeListIndex
}

let IsNodeTreeListCached = []
let NodeTreeListCachedValue = []

function getNodeTreeListbyIndex(i) {
    if (IsNodeTreeListCached[i]) {
        return NodeTreeListCachedValue[i]
    }
    let TreeList = []
    TreeList.push(i)

    let x = indexOfsubNodeListIndex[i]
    if (x && x.length > 0) {
        for (let y of x) {
            let subTreeList = getNodeTreeListbyIndex(y)
            // TreeList.push.apply(TreeList,subTreeList)
            TreeList = [...TreeList, ...subTreeList]
        }
    }
    NodeTreeListCachedValue[i] = TreeList
    IsNodeTreeListCached[i] = 1
    return TreeList
}

function getNodeTreeListbyIndex(i) {
    if (IsNodeTreeListCached[i]) {
        return NodeTreeListCachedValue[i]
    }
    let TreeList = []
    TreeList.push(i)

    let x = indexOfsubNodeListIndex[i]
    if (x && x.length > 0) {
        for (let y of x) {
            let subTreeList = getNodeTreeListbyIndex(y)
            // TreeList.push.apply(TreeList,subTreeList)
            TreeList = [...TreeList, ...subTreeList]
        }
    }
    NodeTreeListCachedValue[i] = TreeList
    IsNodeTreeListCached[i] = 1
    return TreeList
}

let indexOfNodeTreeList = []

function genIndexofTreeList() {
    IsNodeTreeListCached = (new Array(ListLen)).fill(0)
    NodeTreeListCachedValue = (new Array(ListLen)).fill(0)

    for (let i = 0; i < ListLen; i++) {
        indexOfNodeTreeList[i] = getNodeTreeListbyIndex(i)
    }

    return indexOfNodeTreeList
}

let indexOfTreeBalance = []
let IDTreeBalancedict = {}

function genIndexbyTreeBalance() {
    Timer.start("genIndexbyTreeBalance")
    for (let i = 0; i < ListLen; i++) {
        let TreeBalance = 0
        for (j = 0; j < indexOfNodeTreeList[i].length; j++) {
            TreeBalance += allNodeInfo[indexOfNodeTreeList[i][j]].myfund
        }
        indexOfTreeBalance[i] = TreeBalance
        let x = allNodeInfo[i].mycode
        IDTreeBalancedict[x] = TreeBalance
    }

    // saveList("TreeBalance", IDTreeBalancedict)
    Timer.stop("genIndexbyTreeBalance")
    return indexOfTreeBalance
}

let indexOfRecommendAward = []
let IDRecommendAwarddict = {}

function getRecommendbyIndex(i, status = 0) {
    let validsubNodeL1Num = 0
    let r1 = 0
    let r2 = 0
    // let myfund = allNodeInfo[i].myfund
    let myfund = status ? TopFund : allNodeInfo[i].myfund
    let grandSonNodeListIndex = []
    // for (let j = 0; j < indexOfsubNodeListIndex[i].length; j++) {
    //     let submyfund = allNodeInfo[indexOfsubNodeListIndex[i][j]].myfund
    for (let j of indexOfsubNodeListIndex[i]) {
        let submyfund = allNodeInfo[j].myfund

        if (submyfund > 0) {
            r1 += getRecommendValue(submyfund, myfund)

            validsubNodeL1Num++
        }
        //grandSonNodeListIndex.push.apply(grandSonNodeListIndex,indexOfsubNodeListIndex[j])
        grandSonNodeListIndex = [...grandSonNodeListIndex, ...indexOfsubNodeListIndex[j]]
        // reference:
        // let subTreeList = getNodeTreeListbyIndex(y)
        // // TreeList.push.apply(TreeList,subTreeList)
        // TreeList = [...TreeList, ...subTreeList]
    }
    if (validsubNodeL1Num >= 3) {
        for (let k of grandSonNodeListIndex) {
            let submyfund = allNodeInfo[k].myfund

            if (submyfund > 0) {
                r2 += getRecommendValue(submyfund, myfund)
            }
        }
    }
    let R = {}
    R.recomend1 = r1 * 0.5
    R.recomend2 = r2 * 0.2 // if error, we replace it with eval(r2.join("+")); or use sumfun
    R.recomend = R.recomend1 + R.recomend2

    return R
}

function genIndexbyRecommend() {
    Timer.start("genIndexbyRecommend")
    // let totalRecommendAward=0
    let R = {}, R0 = {}, R1 = {}
    for (let i = 0; i < ListLen; i++) {
        let st = allNodeInfo[i].status
        if (st) {
            R0 = getRecommendbyIndex(i, 1)
            R1 = getRecommendbyIndex(i, 0)
            R = R0
            R.recommendDefault = R1.recomend
        } else {
            R0 = getRecommendbyIndex(i, 0)
            R = R0
            R.recommendDefault = R0.recomend
        }

        // totalRecommendAward+=R.recomend
        indexOfRecommendAward[i] = R
        let x = allNodeInfo[i].mycode
        IDRecommendAwarddict[x] = R
    }

    // saveList("Recommend", IDRecommendAwarddict)
    // console.log("Total Recommend Award is: "+totalRecommendAward)
    Timer.stop("genIndexbyRecommend")
    return indexOfRecommendAward
}

let indexOfvipTreeBalance = []
let indexOfvipTag = []
let IDvipTreeBalancedict = {}

function genIndexbyvipTag() {
    Timer.start("genIndexbyvipTag")
    // let indexOfvipTag=[0]
    for (let i = 0; i < ListLen; i++) {
        let vipTreeBalance = 0

        let max = 0
        let sum = 0

        // vip tree doesn't contain itself
        for (j = 0; j < indexOfsubNodeListIndex[i].length; j++) {
            let x = indexOfsubNodeListIndex[i][j]
            let y = indexOfTreeBalance[x]
            sum += y
            max = y > max ? y : max
        }
        z = sum - max
        if (z >= vipquota) {
            indexOfvipTag[i] = 1
        } else {
            indexOfvipTag[i] = 0
        }
        indexOfvipTreeBalance[i] = z
        let x = allNodeInfo[i].mycode
        IDvipTreeBalancedict[x] = z
    }

    // saveList("vipTreeBalance", IDvipTreeBalancedict)
    Timer.stop("genIndexbyvipTag")
    return indexOfvipTreeBalance
}

let IsvipLevelCached = []
let vipLevelCachedValue = []

function getvipLevelbyIndex(i) {
    if (IsvipLevelCached[i]) {
        return vipLevelCachedValue[i]
    }

    let vip = {}

    let vipLevel = indexOfvipTag[i]
    let minerCoeff = 0
    if (vipLevel > 0) {

        let no1 = 0
        let no2 = 0

        for (let j of indexOfsubNodeListIndex[i]) {

            let x = getvipLevelbyIndex(j)
            let y = x.vipLevel
            if (y >= no1) {
                no2 = no1
                no1 = y
            } else if (y >= no2) {
                no2 = y
            }
        }

        // vipLevel = no2 === 0 ? 1 : (no2 + 1)
        vipLevel = no2 + 1
        if (vipLevel === 1) minerCoeff = 0.1
        else if (vipLevel === 2) minerCoeff = 0.15
        else if (vipLevel === 3) minerCoeff = 0.20
        else if (vipLevel === 4) minerCoeff = 0.25
        else if (vipLevel === 5) minerCoeff = 0.30
        else if (vipLevel === 6) minerCoeff = 0.35
        else if (vipLevel === 7) minerCoeff = 0.40
        else {
            minerCoeff = 0
            console.log("error in vip level")
        }
    }

    vip.minerCoeff = minerCoeff
    vip.vipLevel = vipLevel
    IsvipLevelCached[i] = 1
    vipLevelCachedValue[i] = vip

    return vip
}

let indexOfvipLevel = []
let IDvipLevel = {}

// for all iterate function, we should use cache and clear it firstly
function genIndexbyvipLevel() {
    Timer.start("genIndexbyvipLevel")
    IsvipLevelCached = (new Array(ListLen)).fill(0)
    vipLevelCachedValue = (new Array(ListLen)).fill(0)

    for (let i = 0; i < ListLen; i++) {
        z = getvipLevelbyIndex(i)

        indexOfvipLevel[i] = z
        let x = allNodeInfo[i].mycode
        IDvipLevel[x] = z
    }

    // saveList("vipLevel", indexOfvipLevel)
    Timer.stop("genIndexbyvipLevel")
    return indexOfvipTreeBalance
}

let IsMinerAwardCached = []
let MinerAwardCachedValue = []

function getMinerAwardbyIndex(i) {
    if (IsMinerAwardCached[i])
        return MinerAwardCachedValue[i]

    let vip = {}
    vip.vipLevel = indexOfvipLevel[i].vipLevel
    vip.Award = 0

    let revenue = 0
    let minerCoeff = indexOfvipLevel[i].minerCoeff
    let GrandSonNodeList = []
    let subAwardict = {}

    if (vip.vipLevel > 0) {

        let subNodeList = indexOfsubNodeListIndex[i].slice(0)
        while (subNodeList && subNodeList.length > 0) {
            // let y=subNodeIndex.slice(-1)
            let y = subNodeList.pop()

            let z = getMinerAwardbyIndex(y)
            revenue = minerCoeff * getmill(allNodeInfo[y].myfund)
            if (vip.vipLevel >= indexOfvipLevel[y].vipLevel) {
                if (vip.vipLevel > indexOfvipLevel[y].vipLevel) {
                    revenue -= z.Award

                    if (indexOfsubNodeListIndex[y] && indexOfsubNodeListIndex[y].length > 0) {
                        GrandSonNodeList.push.apply(GrandSonNodeList, indexOfsubNodeListIndex[y])
                    }

                } else {
                    revenue += z.Award * 0.15
                }
            }

            vip.Award = vip.Award + revenue
            subAwardict[allNodeInfo[y].mycode] = revenue
        }
        subNodeList = GrandSonNodeList
        while (subNodeList && subNodeList.length > 0) {
            // let y=subNodeIndex.slice(-1)
            let y = subNodeList.pop()

            let z = getMinerAwardbyIndex(y)
            revenue = minerCoeff * getmill(allNodeInfo[y].myfund)

            if (vip.vipLevel > indexOfvipLevel[y].vipLevel) {
                revenue -= z.Award

                if (indexOfsubNodeListIndex[y] && indexOfsubNodeListIndex[y].length > 0) {
                    subNodeList.push.apply(subNodeList, indexOfsubNodeListIndex[y])
                }

            }

            vip.Award = vip.Award + revenue
            subAwardict[allNodeInfo[y].mycode] = revenue
        }

    } else {
        vip.Award = 0
    }

    vip.AwardContribute = subAwardict
    IsMinerAwardCached[i] = 1
    MinerAwardCachedValue[i] = vip

    return vip
}

let indexOfMinerAward = []
let IDMinerAward = {}

function genIndexbyMinerAward() {
    Timer.start("genIndexbyMinerAward")
    IsMinerAwardCached = (new Array(ListLen)).fill(0)
    MinerAwardCachedValue = (new Array(ListLen)).fill(0)
    // let totalMinerAward=0
    for (let i = 0; i < ListLen; i++) {
        z = getMinerAwardbyIndex(i)
        // totalMinerAward+=z.Award
        indexOfMinerAward[i] = z
        let x = allNodeInfo[i].mycode
        IDMinerAward[x] = z
    }

    // saveList("MinerAward", IDMinerAward)
    // console.log("Total Miner Award:"+totalMinerAward)
    Timer.stop("genIndexbyMinerAward")
    return indexOfMinerAward
}

function getNodeInfo(i) {
    let info = {}
    info.index = i
    info.mycode = allNodeInfo[i].mycode
    info.status = allNodeInfo[i].status
    info.staticIncome = indexOfstaticIncome[i]
    info.RecommendAward = indexOfRecommendAward[i].recomend
    info.MinerAward = indexOfMinerAward[i].Award
    info.DynamicAward = info.RecommendAward + info.MinerAward
    info.TotalAward = info.DynamicAward + info.staticIncome
    info.vipTag = indexOfvipTag[i]
    info.vipLevel = indexOfvipLevel[i]
    info.vipTreeBalance = indexOfvipTreeBalance[i]
    info.TreeBalance = indexOfTreeBalance[i]
    info.MinerAwardInfo = indexOfMinerAward[i]
    info.RecommendAwardInfo = indexOfRecommendAward[i]
    info.subNodeListIndex = indexOfsubNodeListIndex[i]
    info.NodeTreeList = indexOfNodeTreeList[i]
    info.allNodeInfo = allNodeInfo[i]

    info.description = "账号:\t" + info.allNodeInfo.mycode + " 手机:\t" + info.allNodeInfo.phone + " 投入本金:\t" + info.allNodeInfo.myfund + " 静态奖励:\t" + info.staticIncome + " 推荐奖励:\t" + info.RecommendAward + " 动态奖励:\t" + info.MinerAward + " VIP等级:\t" + info.vipLevel.vipLevel + " 特殊对待:\t" + info.allNodeInfo.status
    // let strcaclinfo = JSON.stringify(info)
    return info
}

let indexOfNodeInfo = []
let IDNodeInfo = {}

function genNodeInfo() {
    Timer.start("genNodeInfo")
    let totalMinerAward = 0
    let totalRecommendAward = 0
    let totalRecommendOrgAward = 0
    let totalStaticIncomeAward = 0
    let allinfo = ""
    for (let i = 0; i < ListLen; i++) {
        z = getNodeInfo(i)
        totalMinerAward += z.MinerAward
        totalRecommendAward += z.RecommendAward
        totalStaticIncomeAward += z.staticIncome
        totalRecommendOrgAward += z.RecommendAwardInfo.recommendDefault
        allinfo += z.description + "\n"
        indexOfNodeInfo[i] = z
        let x = allNodeInfo[i].mycode
        IDNodeInfo[x] = z
    }
    console.log("Total static Income:" + totalStaticIncomeAward)
    console.log("Total Recommend Income:" + totalRecommendAward)
    console.log("Total orginal Recommend Income:" + totalRecommendOrgAward)
    console.log("Total MinerAward:" + totalMinerAward)

    writeFile("NodeInfo.txt", allinfo)
    saveList("NodeInfo", IDNodeInfo)

    Timer.stop("genNodeInfo")
    return indexOfNodeInfo
}

async function testAllItem() {
    // let t1 = await testMysql()

    let t2 = await getSqLFullResult()

    let t3 = genIndexofmycode()

    let t4 = genIndexofTreeList()

    let t5 = genIndexbyTreeBalance()

    let t6 = genIndexbyvipTag()

    let t7 = genIndexbyvipLevel()

    let t8 = genIndexbyRecommend()

    let t9 = genIndexbyMinerAward()

    let t10 = genNodeInfo()
    console.log(s++, "Finish test!")
    return 0
}

let b = testAllItem()
console.log("Start test!\n")
//process.exit()