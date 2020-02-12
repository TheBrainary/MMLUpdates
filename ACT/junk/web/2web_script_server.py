#!/usr/bin/python3.5

from bottle import hook, get, post, run, request, response

import os
import sys



################################################################

# params
MIRO_DIR_STATE=os.getenv('MIRO_DIR_STATE')
FILE_WEB_SCRIPT=MIRO_DIR_STATE + "/web_script_user.py"
FILE_WEB_CMD=MIRO_DIR_STATE + "/client_web.cmd"
FILE_CONT_CMD=MIRO_DIR_STATE + "/controller.cmd"
FILE_CONT_RUN=MIRO_DIR_STATE + "/controller.run"

# validate
if not os.path.isdir(MIRO_DIR_STATE):
	print("state directory not found: " + MIRO_DIR_STATE)
	exit()



################################################################

def web_write(val):

	with open(FILE_WEB_SCRIPT, "w") as file:
		file.write(val)

def web_stop():

	# command stop to controller daemon by deleting the
	# RUN file if it exists
	try:
		os.remove(FILE_CONT_RUN)
	except:
		pass

def web_command(val):

	if val == "play":

		# stop any existing controller
		web_stop()

		# for now, we actually use "play" to start
		# the web client, which automatically starts
		# the user script, and "stop" to stop it
		with open(FILE_CONT_CMD, "w", os.O_NONBLOCK) as file:
			file.write("web")
			file.close()

	if val == "resume" or val == "pause":
		with open (FILE_WEB_CMD, "w", os.O_NONBLOCK) as file:
			file.write(val)
			file.close()

	if val == "stop":

		# stop any existing controller
		web_stop()



################################################################

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

@hook('after_request')
def enable_cors():
    '''Add headers to enable CORS'''

    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers

@get('/api')
def hello():
	with open("test/test_page.html", "r") as file:
		html = file.read()
	with open("test/web_script_example.py", "r") as file:
		script = file.read()
	ROS_IP = os.getenv("ROS_IP")
	html = html.replace("###LOCAL_IP###", ROS_IP)
	html = html.replace("###TEST_SCRIPT###", "`" + script + "`")
	return html

@post('/api')
def api():
	err = "no error (fall through)"

	try:
		query = request.body.getvalue().decode('utf-8')
		print ("received new query")

		#print (query)

		if query[0:5] == "data=":

			print ("found data=")

			query = query[5:]
			query = bytearray.fromhex(query).decode('ascii')

			#print(query)

			delim = query.find(' ')
			if delim == -1:
				key = query
				val = ""
			else:
				key = query[0:delim]
				val = query[(delim+1):]

			print ("key is", key)

			if (key == "write" or key == "write_play"):
				web_write(val)
				if (key == "write_play"):
					web_command("play")
					return("OK/wrote file, commanded play")
				else:
					return("OK/wrote file")

			if key == "play" or key == "stop" or key == "pause" or key == "resume":
				web_command(key)
				return("OK/commanded " + key)

			print("unrecognised key [" + key + "]")
			return("ERROR/not handled")

		else:
			return("ERROR/parse error (malformed)")

	except IOError as e:
		err = "IOError:" + str(e)

	except Exception as e:
		err = str(e)

	except:
		err = "unhandled exception type"

	print(err)
	return("ERROR/exception [" + err + "]")

# main
run(host='0.0.0.0', port=8888, debug=True)
