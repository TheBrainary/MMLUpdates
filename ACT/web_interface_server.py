#!/usr/bin/python3.5
from bottle import hook, get, post, run, request, response

import os
import json
from os.path import join, getsize
import sys
import subprocess
#from synthesize_text import synthesize_text
import shutil
import mml
import random
from pathlib import Path


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

def web_package(input):
	try:
		appname, code = input.split("</appName>")
		print(appname)
		folderRandom = random.randint(100000,999999)
		home_dir = "/home/miro/ACT/packaged_apps/"
		savedState = False
		code = "#!/usr/bin/python -u\nimport rospy\nrospy.init_node('client_web')\n" + code
		while savedState == False:
			if not os.path.exists(home_dir + str(folderRandom)):
				os.makedirs(home_dir + str(folderRandom))
				savedState = True
				f= open(home_dir + str(folderRandom) +"/app.py","w+")
				f.write(code)
				f.close()
				f= open(home_dir + str(folderRandom) +"/app.info","w+")
				f.write("<App_name>" + appname[9:] + "</App_name>")
				f.write("<locked>false</locked>")
				f.close()
			else:
				folderRandom = random.randint(100000,999999)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
		
def web_say(input):
	python3_command = "/home/miro/ACT/synthesize_text.py --text '" + input + "'"  # launch your python2 script using bash
		
	sudoPassword = 'miro'
	command = "python2.7 /home/miro/ACT/synthesize_text.py --text '" + input + "'"
	p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
	command = "python2.7 /home/miro/ACT/client_stream.py 1"
	p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

def web_stop():

	# command stop to controller daemon by deleting the
	# RUN file if it exists
	try:
		os.remove(FILE_CONT_RUN)
	except:
		pass
		
def web_play(id):

	# command stop to controller daemon by deleting the
	# RUN file if it exists
	try:
		path = ''
		i=-1
		for root, dirs, files in os.walk('/home/miro/ACT/packaged_apps/'):
			if i==int(id):
				path = root
			i=i+1
		print(path)
		Path('/tmp/running.state').touch()
		process = subprocess.Popen('python ' + path + '/app.py', shell=True)
		
		#Path('/tmp/running.state').touch()
		#while os.path.exists('/tmp/running.state'):
		#	time.sleep(0.2) 
		#resp = os.popen('python ' + path + '/app.py').read()
		#print(resp)
	except:
		pass

		
def kill_apps():

	# command stop to controller daemon by deleting the
	# RUN file if it exists
	try:
		os.system("rosnode kill mml_play")
		os.system("rosnode kill client_web")
		os.remove("/tmp/running.state")
	except:
		pass

def web_delete(id):

	data = []
	i=-1
	for root, dirs, files in os.walk('/home/miro/ACT/packaged_apps/'):
		if i==int(id):
		   return shutil.rmtree(root)
		i=i+1

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

@get('/api/list_apps')
def list_apps():
	data = mml.list_apps()
	return data
	
@get('/api/checkupdatesw')
def checkupdate():
	data = subprocess.check_output("/home/miro/checkupdate.sh", shell=True);
	return data

@get('/api/updatesw')
def update():
	data = subprocess.check_output("/home/miro/update.sh", shell=True);
	return data
	
@get('/api/list_sounds')
def list_sounds():
	data = mml.list_sounds()
	return data

@get('/api/sensors')
def read_sensors(): # Should the webpage itself read the file? less GET requests
	try:
		data = ''
		with open('/tmp/sensors.txt', 'r') as file:
			data = file.read()
		file.close()	
		return data
	except:
		print("error in Data")
	
@get('/api/demo/config')
def read_demoConfig(): # Should the webpage itself read the file? less GET requests
	data = subprocess.check_output("cat ~/.miro2/config/platform_parameters | grep 'demo_flags='", shell=True);
	flags = str(data).split('=')[1].split("\\n")[0]
	resp = []
	flagspl = []
	for x in flags:
		flagspl.append({'data':x})
	resp.append({
				'flags': flagspl
			})
	return json.dumps(resp)
	
@post('/api/settings')
def set_settings():
	try:
		query = request.body.getvalue().decode('utf-8')
		query = bytearray.fromhex(query).decode('ascii')
		data = json.loads(query)
		if data['key'] == 'setwireless':
			ssid = data['data']['SSID']
			passphrase = data['data']['passphrase']
			os.system("sudo /home/miro/ACT/setWifiCreds.sh " + "'" + ssid + "' '" + passphrase + "'")
			return "Connecting to " + ssid
		if data['key'] == 'setTTS':
			lang = data['data']['lang']
			pitch = data['data']['pitch']
			tempo = data['data']['tempo']
			voice_reco = data['data']['recoThresh']
			os.system("/home/miro/ACT/speechSettings.sh " + lang + " " + pitch + " " + tempo + " " + voice_reco)
			
	except:
		print("error in Data")
		
		
@get('/stopallapps')
def stop_apps():
	try:
		os.system("rosnode kill mml_play")
		os.remove("/tmp/running.state")
		os.system("rosnode kill client_web")
		return "Killed Apps"
	except:
		pass


@get('/api/get_settings')
def get_settings():
	try:
		data = {}
		data = []
		f=open("/home/miro/ACT/speech.cfg")
		fl = f.readlines()
		data.append(fl[3].split("\"")[1]) # Voice Reco threshhold
		data.append(fl[2].split("\"")[1]) # Tempo
		data.append(fl[1].split("\"")[1]) #pitch
		data.append(fl[0].split("\"")[1]) #lang
		
		return json.dumps(data)
	except:
		print("error in Data")
		
@post('/api/demo/config')
def set_demoConfig():
	try:
		query = request.body.getvalue().decode('utf-8')
		query = bytearray.fromhex(query).decode('ascii')
		data = json.loads(query)
		if data['key'] == 'democonfig':
			flags = data['data']['flags']
			os.system('sed -i "s/\(demo_flags *= *\).*/demo_flags=' + flags + '/" "/home/miro/.miro2/config/platform_parameters"')
			return "Demo Parameters set to" + query
	except:
		print("error in Data")

	
@post('/api')
def api():
	err = "no error (fall through)"

	try:
		query = request.body.getvalue().decode('utf-8')
		print ("received new query")
		print(query)
		if query[0:5] == "data=":

			print ("found data=")

			query = query[5:]
			query = bytearray.fromhex(query).decode('ascii')
		
			print(query)

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

			if key == "deleteApp":
				web_delete(val)
				return "Deleted App"
				
			if key == "playApp":
				web_play(val)
				return "played app " + val
			
			if key == "say":
				mml.say(val)
				return("saying: " + val)
				
			if key == "package":
				web_package(val)
				return("packed")
			
			if key =="setwireless":
				os.system("sudo /home/miro/ACT/setWifiCreds.sh " + val)
				return("wireless Updated")

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
run(host='0.0.0.0', port=1337, debug=True)
