import platform
import os
import json
import sys
import subprocess
import commands

# Retrieve system information from pi and return json
def getSystemInfo():
	system, node, release, version, machine, processor = platform.uname()
	temperature = "".join(filter(lambda x: x.isdigit() or x == ".", list(subprocess.check_output(["vcgencmd", "measure_temp"])))).strip("\n")
	ip_address = "".join(filter(lambda x: x.isdigit() or x ==".", list(subprocess.check_output(["hostname", "-I"])))).strip("\n")
	hostname = subprocess.check_output(["hostname"]).strip("\n")
	ip_address = commands.getoutput("ifconfig | grep 'inet ' | grep -Fv 127.0.0.1 | awk '{print $2}'")
	info = json.dumps({		"system": system,
							"node": node,
							"release": release,
							"version": version,
							"machine": machine,
							"processor": processor,
							"hostname": hostname,
							"temperature": temperature,
							"ip_address": ip_address
							})


	return info

# Reboot pi
def reboot():
	os.system('sudo shutdown -r now')

# Shutdown pi
def shutdown():
	os.system('sudo shutdown -h now')

if __name__ == "__main__":
	try: 
		cmd = sys.argv[1]
		if cmd == "health":
			print(getSystemInfo())
		elif cmd == "reboot":
			reboot()
		elif cmd == "shutdown":
			shutdown()
	except:
		print(getSystemInfo())
