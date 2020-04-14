let fs = require("fs");

function readFile() {
    console.log("读取开始。");
    // 同步读取
    var data = fs.readFileSync('read.txt', 'utf-8');
    console.log("同步读取: " + data.toString());
    // 异步读取
    fs.readFile('read.txt', 'utf-8', function (err, data) {
        if (err) {
            return console.error(err);
        }
        console.log("异步读取: " + data.toString());
    });
    console.log("读取结束。");
}

function writeFile() {
    console.log("写入开始。");
    // 同步读取
    var data = fs.writeFileSync('write1.txt', '我是被写入的内容1！');
    var writeData1 = fs.readFileSync('write1.txt', 'utf-8');
    console.log("同步读取写入的内容1: " + writeData1.toString());
    // 异步读取
    fs.writeFile('write2.txt', '我是被写入的内容2！', function (err) {
        if (err) {
            return console.error(err);
        }
        var writeData2 = fs.readFileSync('write2.txt', 'utf-8');
        console.log("同步读取写入的内容2: " + writeData2.toString());
    });
    console.log("写入结束。");
}