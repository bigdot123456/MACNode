const mysql = require('./mysql');
let fs = require("fs");
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
    allNodeInfo.sort(function (a0,a1) {
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

function writeFile(filename,strbuf) {
    if(strbuf && strbuf.length>0){
        console.log("写入文件：",filename);
        // 同步读取
        // var data = fs.writeFileSync('write1.txt', '我是被写入的内容1！');
        // var writeData1 = fs.readFileSync('write1.txt', 'utf-8');
        // console.log("同步读取写入的内容1: " + writeData1.toString());
        // 异步读取
        fs.writeFile(filename, strbuf, function (err) {
            if (err) {
                console.log("写入数据错误"+err);
                return console.error(err);
            }
        });
    } else {
        console("No content with file write!")
    }
}
function saveList(filename,List) {
    let strJSON = JSON.stringify(List);
    txt=strJSON.replace(/,/g,',\t\n')
    let myDate=new Date()
    let jsonDate = myDate.toISOString().replace(/:/g,'')

    filename=filename+jsonDate+".txt"
    writeFile(filename,txt)
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

var Timer = {
    data: {},
    start: function (key) {
        Timer.data[key] = new Date();
    },
    stop: function (key) {
        var time = Timer.data[key];
        if (time) {
            Timer.data[key] = new Date() - time;
            console.log( s++, key + " time usage: " + Timer.getTime(key)+" ms");
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

function genIndexofmycode() {
    if (allNodeInfo && ListLen == 0) {
        console.log(s++, "\nError! not initialize the database info")
    }
    Timer.start("genIndexofmycode");
    //for (let i in allNodeInfo) {
    for (let i = 0; i < ListLen; i++) {
        let x = allNodeInfo[i].mycode
        sortedMycodeListdict[x] = i
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
            TreeBalance += allNodeInfo[indexOfNodeTreeList[i][j]].rootfund
        }
        indexOfTreeBalance[i] = TreeBalance
        let x = allNodeInfo[i].mycode
        IDTreeBalancedict[x] = TreeBalance
    }

    saveList("TreeBalance",IDTreeBalancedict)
    Timer.stop("genIndexbyTreeBalance")
    return indexOfTreeBalance
}

async function testAllItem() {
    // let t1 = await testMysql()

    let t2 = await getSqLFullResult()

    let t3 = genIndexofmycode()

    let t4 = genIndexofTreeList()

    let t5 = genIndexbyTreeBalance()

    console.log(s++, "Finish test!")
    return 0
}

let b = testAllItem()
console.log("Start test!\n")
//process.exit()