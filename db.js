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
var cn = {
			host: config.host,
			port: config.port,
			database: config.database,
			user: config.user,
			password: config.password
		}

var db = pgp(cn);

module.exports = db
