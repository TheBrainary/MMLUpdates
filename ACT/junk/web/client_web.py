#!/usr/bin/python

import time
import sys
import os

DIR_HOME=os.getenv("HOME")

################################################################

def start_script():
	os.system("./control_web_script.sh start")

def stop_script():
	os.system("./control_web_script.sh stop")

################################################################

# keep running while this file is present
FILE_RUN = sys.argv[1]

# command file receives commands from MEI
FILE_WEB_CMD = os.getenv("MIRO_DIR_STATE") + "/client_web.cmd"

# start script
start_script()

# loop until we receive a stop command
while os.path.isfile(FILE_RUN):

	# report
	#print time.time()

	# if command from MEI is waiting
	if os.path.exists(FILE_WEB_CMD):

		# receive command
		with open(FILE_WEB_CMD, "r") as file:
			cmd = file.read()

		print "received command from MEI", cmd

		# handle command
		if cmd == "stop":
			pass

		# handle command
		if cmd == "play":
			pass

		# handle command
		if cmd == "pause":
			pass

		if cmd == "resume":
			pass

	# sleepy time
	time.sleep(0.1)

# stop script
stop_script()
