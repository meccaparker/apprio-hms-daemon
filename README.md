# Apprio HMS
###### Mecca Parker
###### 2017 Summer Internship Project
###### App: https://github.com/meccaparker/apprio-hms.git
###### Server: https://github.com/meccaparker/apprio-hms-server.git
###### Daemon: https://github.com/meccaparker/apprio-daemon.git

The Apprio HMS project is a project that interfaces the Raspberry Pi 3 with the Microsoft Surface Hub. Its objective is to provide a way to manage and control a system of Microsoft Hubs all wrapped up within a hybrid mobile app. Written using the [Ionic framework](https://ionicframework.com/), the app  connects the user to the Hubs through dedicated Raspberry Pi servers interfacing via serial connection with the Hubs. This allows the Hubs to be accessed remotely from the application from anywhere. In addition to this, the app and Raspberry Pi's store and receive information about the Hubs within a PostgresQL database. 

## About 

#### Daemon

The Apprio HMS daemon is a process that is configured with Cronjobs to run every five minutes on the Raspberry Pi. On a high level, it opens a serial port connection with the Hub, retrieves information about the Hub, runs a quick system check on the Raspberry Pi itself, and updates a PostgresQL database with the gathered data. The output of the process is written to the daemon.log file.

#### Server 

The Apprio HMS server is a server that runs on the Raspberry Pi that handles all the routing from the Apprio HMS app. When the user on the Apprio HMS app taps buttons to perform commands that require the serial port of the Microsoft Hub, the requests are sent the server on the Raspberry Pi and the Raspberry Pi executes the necessary code to perform the requested function. The server always responds with the most up to date information on all Hubs in JSON format or an error message. If a state change of the Hub occurs, the Raspberry Pi updates the database with the new state information of the Microsoft Hub. 

## Configuration steps 

1. Download **apprio-hms-daemon** and **apprio-hms-server** directories into the **pi** directory. 

1. Move to the **apprio-hms-server** directory and install the npm dependencies by executing `npm install`.
		
1. We'd like to run the **sp_daemon.py** script every five minutes and write the output to the **daemon.log** file. To do this, edit the Crontab file to run the daemon every five minutes by opening the Crontab file editor `crontab -e`  and changing the last line to `bash * /5 * * * * cd apprio-hms-daemon daemon && python ./sp_daemon.py >> daemon.log 2>&1`.

1. Finally, run the server initialization script **init_server.sh** at startup. Open an editor for the **rc.local** script with `sudo nano /etc/rc.local` and append the following to the end of the file: 
		
```bash
bash /home/pi/apprio-hms-server/init_server.sh &

exit 0
``` 

