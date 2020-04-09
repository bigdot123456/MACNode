const mysql = require('mysql');
const async = require("async");

// localhost
var pool = mysql.createPool({
  connectionLimit: 50,
  host: '127.0.0.1',
  user: 'root',
  password: 'Root@123',
  database: 'fund_sql',
  multipleStatements: true //是否允许执行多条sql语句
});
//将结果已对象数组返回
var row = (sql, ...params) => {
  return new Promise(function (resolve, reject) {
      pool.getConnection(function (err, connection) {
        if (err) {
          reject(err);
          return;
        }
        connection.query(sql, params, function (error, res) {
          connection.release();
          if (error) {
            reject(error);
            return;
          }
          resolve(res);
        });
      });
    })
    .catch(error => console.log('caught', error));
};
//返回一个对象
var first = (sql, ...params) => {
  return new Promise(function (resolve, reject) {
    pool.getConnection(function (err, connection) {
      if (err) {
        reject(err);
        return;
      }
      connection.query(sql, params, function (error, res) {
        connection.release();
        if (error) {
          reject(error);
          return;
        }
        resolve(res[0] || null);
      });
    });
  });
};
//返回单个查询结果
var single = (sql, ...params) => {
  return new Promise(function (resolve, reject) {
    pool.getConnection(function (err, connection) {
      if (err) {
        reject(err);
        return;
      }
      connection.query(sql, params, function (error, res) {
        connection.release();
        if (error) {
          reject(error);
          return;
        }
        for (let i in res[0]) {
          resolve(res[0][i] || null);
          return;
        }
        resolve(null);
      });
    });
  });
}
//执行代码，返回执行结果
var execute = (sql, ...params) => {
  return new Promise(function (resolve, reject) {
    pool.getConnection(function (err, connection) {
      if (err) {
        reject(err);
        return;
      }
      connection.query(sql, params, function (error, res) {
        connection.release();
        if (error) {
          reject(error);
          return;
        }
        resolve(res);
      });
    });
  });
}

let query = function (sql, values) {
  // 返回一个 Promise
  return new Promise((resolve, reject) => {
    pool.getConnection(function (err, connection) {
      if (err) {
        reject(err)
      } else {
        connection.query(sql, values, (err, rows) => {

          if (err) {
            reject(err)
          } else {
            resolve(rows)
          }
          // 结束会话
          connection.release()
        })
      }
    })
  })
}

const execTrans = function execTrans(sqlparamsEntities, callback) {
  pool.getConnection(function (err, connection) {
    if (err) {
      return callback(err, null);
    }
    connection.beginTransaction(function (err) {
      if (err) {
        return callback(err, null);
      }
      //console.log("开始执行transaction，共执行" + sqlparamsEntities.length + "条数据");
      let funcAry = [];
      sqlparamsEntities.forEach(function (sql_param) {
        let temp = function (cb) {
          let sql = sql_param.sql;
          let param = sql_param.params;
          connection.query(sql, param, function (tErr, rows, fields) {
            if (tErr) {
              connection.rollback(function () {
                console.log("事务失败，" + sql + "，ERROR：" + tErr);
                throw tErr;
              });
            } else {
              return cb(null, 'ok');
            }
          })
        };
        funcAry.push(temp);
      });

      async.series(funcAry, function (err, result) {
        if (err) {
          connection.rollback(function (err) {
            console.log("transaction error: " + err);
            connection.release();
            return callback(err, null);
          });
        } else {
          connection.commit(function (err, info) {
            //console.log("transaction info: " + JSON.stringify(info));
            if (err) {
              console.log("执行事务失败，" + err);
              connection.rollback(function (err) {
                console.log("transaction error: " + err);
                connection.release();
                return callback(err, null);
              });
            } else {
              connection.release();
              return callback(null, info);
            }
          })
        }
      })
    });
  });
}

//模块导出
module.exports = {
  ROW: row,
  execTrans: execTrans,
  FIRST: first,
  SINGLE: single,
  EXECUTE: execute,
  QUERY: query
}