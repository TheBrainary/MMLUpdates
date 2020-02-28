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

@get('/api/sensors')
def read_sensors(): # Should the webpage itself read the file? less GET requests
    data = ''
    with open('/tmp/sensors.txt', 'r') as file:
        data = file.read()
    file.close()    
    return data
    
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
            
            if key == "say":
                mml.say(val)
                return("saying: " + val)
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
