/* 
 * Create and export a database object
 */

var promise = require('bluebird')
var config = require('./config/data.json')

var options = {
  // Initialization Options
  promiseLib: promise
}

var pgp = require('pg-promise')(options)

var db = pgp(config.dbURL);

module.exports = db
