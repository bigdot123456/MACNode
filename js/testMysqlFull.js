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
    let txt0=""
    let dim=strJSON.match('},')
    if( dim !== null){
        txt0=strJSON.replace(/},/g,'},\n')
    }else{
        txt0=strJSON.replace(/,/g,',\n')
    }

    let myDate=new Date()
    let jsonDate = myDate.toISOString().replace(/:/g,'')

    filename=filename+jsonDate+".txt"
    writeFile(filename,txt0)
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

let indexOfRecommendAward=[]
let IDRecommendAwarddict={}
function genIndexbyRecommend() {
    Timer.start("genIndexbyRecommend")
    for (let i = 0; i < ListLen; i++) {
        let validsubNodeL1Num = 0
        let r1 = 0
        let r2 = 0
        let rootfund=allNodeInfo[i].rootfund
        let grandSonNodeListIndex=[]
        // for (let j = 0; j < indexOfsubNodeListIndex[i].length; j++) {
        //     let subrootfund = allNodeInfo[indexOfsubNodeListIndex[i][j]].rootfund
        for (let j of indexOfsubNodeListIndex[i]) {
            let subrootfund = allNodeInfo[j].rootfund

            if (subrootfund>0) {
                r1 += getRecommendValue(subrootfund, rootfund)

                validsubNodeL1Num++
            }
            //grandSonNodeListIndex.push.apply(grandSonNodeListIndex,indexOfsubNodeListIndex[j])
            grandSonNodeListIndex=[...grandSonNodeListIndex,...indexOfsubNodeListIndex[j]]
            // reference:
            // let subTreeList = getNodeTreeListbyIndex(y)
            // // TreeList.push.apply(TreeList,subTreeList)
            // TreeList = [...TreeList, ...subTreeList]
        }
        if (validsubNodeL1Num >= 3) {
            for (let k of grandSonNodeListIndex) {
                let subrootfund = allNodeInfo[k].rootfund

                if (subrootfund > 0) {
                    r2 += getRecommendValue(subrootfund, rootfund)
                }
            }
        }
        let R={}
        R.recomend1 = r1 * 0.5
        R.recomend2 = r2 * 0.2 // if error, we replace it with eval(r2.join("+")); or use sumfun
        R.recomend = R.recomend1+R.recomend2
        indexOfRecommendAward[i]=R
        let x = allNodeInfo[i].mycode
        IDRecommendAwarddict[x] = R

    }

    saveList("Recommend",IDRecommendAwarddict)
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
            let x=indexOfsubNodeListIndex[i][j]
            let y = indexOfTreeBalance[x]
            sum += y
            max = y > max ? y : max
        }
        z=sum-max
        if(z>=vipquota){
            indexOfvipTag[i]=1
        }else{
            indexOfvipTag[i]=0
        }
        indexOfvipTreeBalance[i] = z
        let x = allNodeInfo[i].mycode
        IDvipTreeBalancedict[x] = z
    }

    saveList("vipTreeBalance",IDvipTreeBalancedict)
    Timer.stop("genIndexbyvipTag")
    return indexOfvipTreeBalance
}

let IsvipLevelCached=[]
let vipLevelCachedValue=[]

function getvipLevelbyIndex(i) {
    if(IsvipLevelCached[i]){
        return vipLevelCachedValue[i]  
    }

    let vip={}

    let vipLevel = indexOfvipTag[i]
    let minerCoeff=0
    if(vipLevel>0) {

        let no1 = 0
        let no2 = 0

        for (let j of indexOfsubNodeListIndex[i]) {

            let x = getvipLevelbyIndex(j)
            let y=x.vipLevel
            if (y >= no1) {
                no2 = no1
                no1 = y
            } else if (y >= no2) {
                no2 = y
            }
         }

        // vipLevel = no2 === 0 ? 1 : (no2 + 1)
        vipLevel =  no2 + 1
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

    vip.minerCoeff=minerCoeff
    vip.vipLevel=vipLevel
    IsvipLevelCached[i]=1
    vipLevelCachedValue[i]=vip

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
         z=getvipLevelbyIndex(i)

        indexOfvipLevel[i] = z
        let x = allNodeInfo[i].mycode
        IDvipLevel[x] = z
    }

    saveList("vipLevel",indexOfvipLevel)
    Timer.stop("genIndexbyvipLevel")
    return indexOfvipTreeBalance
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

    console.log(s++, "Finish test!")
    return 0
}

let b = testAllItem()
console.log("Start test!\n")
//process.exit()