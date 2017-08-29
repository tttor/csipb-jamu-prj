const pg = require('pg');

// var config = {
//   user: 'pmon',
//   database: 'pmon',
//   password: 'pmon_132145',
//   host: '172.18.31.115',
//   port: 5432,
//   max: 10,
//   idleTimeoutMillis: 30000,
// };

var config = {
  user: 'ijah',
  database: 'ijah',
  password: '123',
  host: '127.0.0.1',
  port: 5432,
  max: 10,
  idleTimeoutMillis: 30000,
};

const pool = new pg.Pool(config);

pool.on('error', function (err, client) {
  console.error('idle client error', err.message, err.stack);
});

module.exports.query = function (text, values, callback) {
  console.log('query:', text, values);
  return pool.query(text, values, callback);
};

module.exports.connect = function (callback) {
  return pool.connect(callback);
};
