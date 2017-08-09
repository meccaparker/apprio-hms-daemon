var db = require('./db.js')

var DBDaemon = function() {
	var self = this
	var id = parseInt(process.argv[2])
	var power = parseInt(process.argv[3])
	var source = parseInt(process.argv[4])

	// Initialize
	self.init = function() {
		console.log('Waking up DBDaemon...')
		self.updateDatabase(function(err) {
			if (err === null) {
				console.log("Database successfully updated.")
			}
			else {
				console.log("Could not update database.")
				console.log(err)
			}
			process.exit(1)
		})
	}
	
	// Update database with new values
	self.updateDatabase = function(completion) {
		var query = "UPDATE hub SET power = $2, source = $3 WHERE id = $1"
		console.log('Attempting to update database...')
		db.none(query, [id, power, source])
			.then(function() {
				completion(null)
		        })
		            .catch(function(err) {
		            completion(err)
		        	})
	}
}

var daemon = new DBDaemon()
daemon.init()








