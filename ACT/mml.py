#!/usr/bin/python
import subprocess
import sys
import os
import json
from os.path import join, getsize
import os
# initialise ROS node

def list_apps():
    data = {}
    data = []
    i=-1
    for root, dirs, files in os.walk('/home/miro/ACT/packaged_apps/'):
        if i>=0:
            print(root +"/app.info")
            f = open(root +"/app.info")
            line = f.readline()
            f.close()
            line = line.split(">")[1].split("<")[0]
            
            data.append({
                'id': i,
                'foldername': root.replace('/home/miro/ACT/packaged_apps/', ' '),
                'path': root,
                'name': line 
            })
        i=i+1
    return json.dumps(data)
	
def list_sounds():
    data = {}
    data = []
    for root, dirs, files in os.walk('/home/miro/mdk/share/media/'):
        for file in files:
            if file[-4:] == ".mp3":
                data.append({
                    'name': file,
                    'path': root + file
                })
    return json.dumps(data)

def say(text): # MiRo will say using its speakers whatever text is passed through.
    input_text = str(text)
    input_text = 'python /home/miro/ACT/TTS.py \"' + input_text + '\"' # \"' + lang + '\" \"' + str(tempo) + '\" \"' + str(pitch) + '\"'
    print(input_text)
    os.system(input_text)


def play(id_path): # plays Audio from /mdk/share/media at index ID (main difference between say and play is that plays and continues, whereas say waits until its finished to continue.
    pid = subprocess.Popen([sys.executable, '/home/miro/ACT/mml_play.py', id_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	# f = open('/tmp/mml_play_pid', 'w')
	# f.write(pid)
	# f.close()
    print("Playing Audio : " + str(id_path))

def playSync(id_path):
    input_text = "python /home/miro/ACT/mml_play.py " + id_path
    os.system(input_text)
