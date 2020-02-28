#!/usr/bin/python3
import rospy

from std_msgs.msg import UInt8MultiArray, UInt16MultiArray, Int16MultiArray, String,UInt32MultiArray
from geometry_msgs.msg import TwistStamped, Vector3
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path
import subprocess
import time
import sys
import os
import numpy as np
import wave, struct
import mml
from subprocess import call
import math
from pathlib import Path
#import speech_recognition as sr


# amount to keep the buffer stuffed - larger numbers mean
# less prone to dropout, but higher latency when we stop
# streaming. with a read-out rate of 8k, 4000 samples will
# buffer for half of a second, for instance.
BUFFER_STUFF_SAMPLES = 4000

# messages larger than this will be dropped by the receiver,
# however, so - whilst we can stuff the buffer more than this -
# we can only send this many samples in any single message.
MAX_STREAM_MSG_SIZE = (4096 - 48)

# using a margin avoids sending many small messages - instead
# we will send a smaller number of larger messages, at the cost
# of being less precise in respecting our buffer stuffing target.
BUFFER_MARGIN = 1000
BUFFER_MAX = BUFFER_STUFF_SAMPLES + BUFFER_MARGIN
BUFFER_MIN = BUFFER_STUFF_SAMPLES - BUFFER_MARGIN

# how long to record before playing back in seconds?
RECORD_TIME = 25

# microphone sample rate (also available at miro2.constants)
MIC_SAMPLE_RATE = 20000

# sample count
SAMPLE_COUNT = RECORD_TIME * MIC_SAMPLE_RATE



################################################################

def error(msg):
	print(msg)
	sys.exit(0)

def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True
	
	
def rotate(l,n):
	return l[n:]+l[:n]

class client:
	def control_led(self, led_pos, colour_str, brightness):
		r = int(colour_str[1:3], 16)
		g = int(colour_str[3:5], 16)
		b = int(colour_str[5:7], 16)
		led_value = (int(brightness) << 24) | (r << 16) | (g << 8) | b
		self.illum.data[led_pos] = led_value

	# def callback_stream(self, msg):
		# self.buffer_space = msg.data[0]
		# self.buffer_total = msg.data[1]
		# self.buffer_stuff = self.buffer_total - self.buffer_space
		
	# # def callback_clap(self, msg):
		# # print(msg)
		
	def callback_mics(self, msg):
		new_audio_level = 0
		data = np.array(msg.data).astype('float32') * (1.0 / 32768.0)
		rms_l = np.sqrt(np.mean(data[0:500]**2))
		rms_r = np.sqrt(np.mean(data[500:1000]**2))
		new_audio_level = np.max((new_audio_level, np.mean([rms_l, rms_r])))
		if new_audio_level > self.audio_level:
			self.audio_level = new_audio_level
		data = {}
		data = []
		f=open("/home/miro/ACT/speech.cfg")
		fl = f.readlines()
		threshold = fl[3].split("\"")[1] # Voice Reco threshhold
		#threshold = 0.4
		# if recording
		if not self.micbuf is None and self.audio_level > float(threshold):
			if os.path.exists('/tmp/running.state'):
				self.audio_level = 0
				return None
			#print("self:" + str(self.audio_level))
			#print(new_audio_level)
			#get the ininital time to check length of recording. 
			if self.startTime == 0:
				self.startTime = time.time()
				self.TimeSinceLast = time.time()
				
				if len(self.PID) > 9:
					self.DemoPause = True
					self.PID = os.popen('rosnode info miro_client_demo_main | grep "Pid:"').read()
					os.system("kill -STOP " + self.PID[4:])
					print(self.PID[4:])
				
				
			#Get the time since last possible voice detected.
			if new_audio_level >= 0.04:
				self.TimeSinceLast = time.time()
			
			# append mic data to store
			data = np.array(msg.data, 'int16')
			x = np.reshape(data, (-1, 500))
			self.micbuf = np.concatenate((self.micbuf, x.T))
			
			# change the color of miro to purple and fade in and out to let user know miro is accepting a command.
			if self.illumState == 0:
				self.illumInt += 7
				if self.illumInt > 255:
					self.illumState = 1 ## if equal to 1 reverse direction of fade.
					self.illumInt = 255
			
			if self.illumState == 1:
				self.illumInt -= 7
				if self.illumInt < 0:
					self.illumState = 0 ## if equal to 1 reverse direction of fade.
					self.illumInt = 0
			
			
			self.control_led(0,'#cc33cc',self.illumInt) #lf
			self.control_led(3,'#cc33cc',self.illumInt) #RF
			
			self.control_led(1,'#cc33cc',self.illumInt) #LM
			self.control_led(4,'#cc33cc',self.illumInt) #RM
			
			self.control_led(2,'#cc33cc',self.illumInt) #LR
			self.control_led(5,'#cc33cc',self.illumInt) #RR
			self.pub_illum.publish(self.illum)
			
			
			#sys.stdout.write(".")
			#sys.stdout.flush()
		
			# finished recording?
			if (self.micbuf.shape[0] >= SAMPLE_COUNT) or (time.time()-self.startTime >= 20) or (time.time()-self.TimeSinceLast >= 2):
				# Remove the first 9000 frames of the audio file to remove the clap(.45 seconds from start)
				self.micbuf = np.delete(self.micbuf, range(0, 9000), 0)
				
				# End recording
				print("Recording Complete")
				self.outbuf = self.micbuf
				self.micbuf = None
				self.audio_level = 0
		
	def loop(self):

		# loop
		while not rospy.core.is_shutdown():
			# if recording finished
			if not self.outbuf is None:
			# write output file
########################################## Convert Input ###############################################

			#Change Color to blue to signify Processing of command (what color is best?
				self.control_led(0,'#3366ff',255) #lf
				self.control_led(3,'#3366ff',255) #RF
				
				self.control_led(1,'#3366ff',255) #LM
				self.control_led(4,'#3366ff',255) #RM
				
				self.control_led(2,'#3366ff',255) #LR
				self.control_led(5,'#3366ff',255) #RR
				self.pub_illum.publish(self.illum)

				outfilename = '/tmp/input.wav'
				file = wave.open(outfilename, 'wb')
				file.setparams((1, 4, 20000, 0, 'NONE', 'not compressed'))
				x = np.reshape(self.outbuf[:, [0, 0]], (-1))
				
			# By writing the values once and joining rather than writeframes each itteration saves 10+ seconds of time
				values = []
				for s in x:
					packed_value = struct.pack('<h', s)
					values.append(packed_value)
					
				value_str = b''.join(values)
				file.writeframes(value_str)
				file.close()
				
				#convert via FFMPEG to correct codec and rate
				print("Converting via FFMPEG")
				os.system("ffmpeg -y -i /tmp/input.wav -f s16le -acodec pcm_s16le -ar 16000 -af 'aresample=20000' -ac 1 /tmp/inputConv.wav -loglevel quiet")
				
########################################## PocketSphinx ###############################################
				
			#initialise config for Pocketsphinx 

				self.ps.decode(
				audio_file=("/tmp/inputConv.wav"), #add temp input.wav file
				buffer_size=8192,
				no_search=False,
				full_utt=False)
				
				print("Recognized: ")
				print( self.ps.hypothesis() )
				
########################################## Handle Requests ###############################################
				
				## Speech Analysis, (what to start?)
				if self.ps.hypothesis() == "hello" or self.ps.hypothesis() == "hi":
					mml.playSync("/home/miro/ACT/voice_files/hello_there_human.mp3") # Change this to whatever

				elif self.ps.hypothesis() == "how are you" or self.ps.hypothesis() == "hello are you":
					#mml.say("I'm really well, thanks for asking")
					mml.playSync("/home/miro/ACT/voice_files/im_really_well_thanks_for_asking.mp3")
					
				elif self.ps.hypothesis() == "what is your name" or self.ps.hypothesis() == "what's your name" or self.ps.hypothesis() == "tell me your name":
					#mml.say("My name is Miro")
					mml.playSync("/home/miro/ACT/voice_files/my_name_is_miro.mp3")
					
				elif self.ps.hypothesis() == "what's your address" or self.ps.hypothesis() == "what is your address" or self.ps.hypothesis() == "what is your ip address" or self.ps.hypothesis() == "what is your ip":
					ipAddr = os.popen('ifconfig wlan0 | grep "inet "').read()
					mml.playSync("/home/miro/ACT/voice_files/my_ip_address_is.mp3")
					time.sleep(3)
					mml.sayIP()
				elif self.ps.hypothesis() == "twinkle twinkle little star":
					path = 'python ~/ACT/packaged_apps/twinkle.py'
					Path('/tmp/running.state').touch()
					process = subprocess.Popen(path + ' > /dev/null 2> /dev/null &', shell=True)
					while os.path.exists('/tmp/running.state'):
						time.sleep(0.2)
				elif self.ps.hypothesis() == "fetch":
					mml.playSync("/home/miro/ACT/voice_files/ok_lets_play_fetch.mp3")
					path = 'python ~/ACT/packaged_apps/fetch/app.py'
					Path('/tmp/running.state').touch()
					self.control_led(0,'#09db10',255) #lf
					self.control_led(3,'#09db10',255) #RF
				
					self.control_led(1,'#09db10',255) #LM
					self.control_led(4,'#09db10',255) #RM
				
					self.control_led(2,'#09db10',255) #LR
					self.control_led(5,'#09db10',255) #RR
					process = subprocess.Popen(path + ' > /dev/null 2> /dev/null &', shell=True)
					while os.path.exists('/tmp/running.state'):
						time.sleep(0.2)
				elif self.ps.hypothesis() == "go home" or self.ps.hypothesis() == "go to bed":
					path = 'python ~/ACT/packaged_apps/kennel/app.py'
					Path('/tmp/running.state').touch()
					process = subprocess.Popen(path + ' > /dev/null 2> /dev/null &', shell=True)
					while os.path.exists('/tmp/running.state'):
						time.sleep(0.2)
					
				elif self.ps.hypothesis() == "head shoulders knees and toes" or self.ps.hypothesis() == "head and shoulders knees and toes":
					path = 'python ~/ACT/packaged_apps/headsShoulders.py'
					Path('/tmp/running.state').touch()
					process = subprocess.Popen(path + ' > /dev/null 2> /dev/null &', shell=True)
					while os.path.exists('/tmp/running.state'):
						time.sleep(0.2)
					
				elif self.ps.hypothesis() == "spin":
					z_rad = math.radians(100)
					self.velocity.twist.angular.z = z_rad
					self.velocity_pub.publish(self.velocity)
					startt=time.time()
					ctime = 0
					while ctime-startt < 5:
						ctime = time.time()
						self.velocity_pub.publish(self.velocity)
						time.sleep(0.02)
					self.velocity.twist.angular.z = 0
					self.velocity_pub.publish(self.velocity)
					
					
				#elif self.ps.hypothesis() == "stop":
				#	resp = os.popen('python ~/ACT/packaged_apps/Head_shoulders_knees.py').read()
					
				elif self.ps.hypothesis() == "walk":
					#mml.say("a Please attach a collar to me and take me for a walk.")
					mml.playSync("/home/miro/ACT/voice_files/please_attach_a_collar.mp3")
					# sp = subprocess.Popen('python ~/ACT/packaged_apps/miro_walk_collar.py', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					# print(sp.pid)
					# output, error = sp.communicate()
					path = 'python ~/ACT/packaged_apps/miro_walk_collar.py'
					Path('/tmp/running.state').touch()
					process = subprocess.Popen(path + ' > /dev/null 2> /dev/null &', shell=True)
					while os.path.exists('/tmp/running.state'):
						time.sleep(0.2)
					
			#	elif self.ps.hypothesis() == "hug/nuzzle":
			#		resp = os.popen('python ~/ACT/packaged_apps/Head_shoulders_knees.py').read()
					
			#	elif self.ps.hypothesis() == "quiet":
					#resp = os.popen('python ~/ACT/packaged_apps/Head_shoulders_knes.py').read()
					
				elif self.ps.hypothesis() == "do you want to hear a story":
					#mml.say("oh i love stories")
					mml.playSync("/home/miro/ACT/voice_files/oh_i_love_stories.mp3")
					
					
				#elif self.ps.hypothesis().find("go to sleep") >= 0:
				#	mml.say("Okay i will go to sleep now, good-night")
				#	call("sudo reboot -h now", shell=True)
				
				self.control_led(0,'#ffffff',255) #lf
				self.control_led(3,'#ffffff',255) #RF
				
				self.control_led(1,'#ffffff',255) #LM
				self.control_led(4,'#ffffff',255) #RM
				
				self.control_led(2,'#ffffff',255) #LR
				self.control_led(5,'#ffffff',255) #RR
				self.pub_illum.publish(self.illum)
				
				# Reset Variables for next call to mics
				self.micbuf = np.zeros((0, 4), 'uint16')
				self.outbuf = None
				self.buffer_stuff = 0
				self.playchan = 0
				self.playsamp = 0
				self.startTime = 0
				self.TimeSinceLast = 0
				if self.DemoPause == True:
					self.DemoPause == False
					os.system("kill -CONT " + self.PID[4:])
					self.PID = ''

			# state
			time.sleep(0.2)
			

	def __init__(self):

		model_path = get_model_path()
		print(model_path)
		data_path = get_data_path()
		config = {
			'hmm' : os.path.join(model_path, 'en-us'), # Hidden Markov Model, Speech Recongnition model - trained probability scoring system
			'lm': os.path.join(model_path, 'en-us.lm.bin'), #language model
			'dict' : os.path.join(model_path, 'testdict.dict')#, # language dictionary
			}
				
			#Start PocketSphinx Deocde
		self.ps = Pocketsphinx(**config)
		# Variables for Audio
		self.micbuf = np.zeros((0, 4), 'uint16')
		self.outbuf = None
		self.buffer_stuff = 0
		self.audio_level = 0
		self.timeofclap = 0
		self.playchan = 0
		self.playsamp = 0
		self.startTime = 0
		self.TimeSinceLast = 0
		self.DemoPause = False
		self.PID = ''
		self.velocity = TwistStamped()
		
		# Variables for Illumination
		self.illum = UInt32MultiArray()
		self.illum.data = [0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF]
		self.illumInt = 0
		self.illumState = 0
		

		# robot name
		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")

		#Publisher for Illum to control LED's while we are processing requests
		topic = topic_base_name + "/control/illum"
		self.pub_illum = rospy.Publisher(topic, UInt32MultiArray, queue_size=0)
		self.velocity_pub = rospy.Publisher(topic_base_name + "/control/cmd_vel", TwistStamped, queue_size=0)
		# subscribe
		topic = topic_base_name + "/sensors/mics"
		self.sub_mics = rospy.Subscriber(topic, Int16MultiArray, self.callback_mics, queue_size=1, tcp_nodelay=True)
		

		

if __name__ == "__main__":

	rospy.init_node("speech_recog", anonymous=False)
	main = client()
	main.loop()




