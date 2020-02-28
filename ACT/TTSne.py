#!/usr/bin/python

import rospy
from std_msgs.msg import UInt8MultiArray, UInt16MultiArray, Int16MultiArray, String
import time
import sys
import os
import numpy as np

# messages larger than this will be dropped by the receiver
MAX_STREAM_MSG_SIZE = (3000)

# amount to keep the buffer stuffed - larger numbers mean
# less prone to dropout, but higher latency when we stop
# streaming. with a read-out rate of 8k, 2000 samples will
# buffer for quarter of a second, for instance.
BUFFER_STUFF_BYTES = 1000

# media source directories
#DIR_SOURCE = ["../../share/media", os.getenv('HOME') + "/lib/miro2x/mdk/share/media"]

################################################################

def error(msg):

	print(msg)
	sys.exit(0)

################################################################

	# and extract its parts
TRACK_FILE = "output.wav"
TRACK_PATH = "/tmp/output.wav"

# if the file is not there, fail
#if not os.path.isfile(TRACK_PATH):
#	error('file not found');



################################################################

class streamer:

	def callback_log(self, msg):

		sys.stdout.write(msg.data)
		sys.stdout.flush()

	def callback_stream(self, msg):

		self.buffer_space = msg.data[0]
		self.buffer_total = msg.data[1]

	def loop(self, args):

		state_file = None
		if len(args):
			state_file = args[0]

		# periodic reports
		count = 0
#		np.insert(self.data,20,[0] * 1000) 
		# safety dropout if receiver not present
		dropout_data_r = -1
		dropout_count = 3

		# loop		
		while not rospy.core.is_shutdown():
			print self.buffer_total
			# check state_file
			if not state_file is None:
				if not os.path.isfile(state_file):
					break

			# if we've received a report
			if self.buffer_total > 0:
				print "buffer Space: ", self.buffer_space
				# compute amount to send
				buffer_rem = self.buffer_total - self.buffer_space
				n_bytes = BUFFER_STUFF_BYTES - buffer_rem
				n_bytes = max(n_bytes, 0)
				n_bytes = min(n_bytes, MAX_STREAM_MSG_SIZE)

				# if amount to send is non-zero
				if n_bytes > 0:
					msg = Int16MultiArray(data = self.data[self.data_r:self.data_r+n_bytes])
					self.pub_stream.publish(msg)
					self.data_r += n_bytes

			# break
			if self.data_r >= len(self.data):
				break

			# report once per second
			if count == 0:
				count = 10
				print "streaming:", self.data_r, "/", len(self.data), "bytes"
				
				# check at those moments if we are making progress, also
				if dropout_data_r == self.data_r:
					if dropout_count == 0:
						print "dropping out because of no progress..."
						break
					print "dropping out in", str(dropout_count) + "..."
					dropout_count -= 1
				else:
					dropout_data_r = self.data_r
			
			# count tenths
			count -= 1
			time.sleep(0.1)

	def __init__(self):
		str = sys.argv[1]
		lang = os.popen('cat /home/miro/ACT/speech.cfg | grep lang').read()
		lang = lang[6:len(lang)-2]
		#lang = "en-US"
		pitch = os.popen('cat /home/miro/ACT/speech.cfg | grep pitch').read()
		pitch = pitch[7:len(pitch)-2]
		tempo = os.popen('cat /home/miro/ACT/speech.cfg | grep tempo').read()
		tempo = tempo[7:len(tempo)-2]
		#pitch = "1"
		#tempo = "1"
		# decode mp3
		if(str.find("miro") >=0 ):
			str = str.replace("miro","mero")
		#cmd= "pico2wave -w /tmp/output.wav '" + str + "'" # && ffmpeg -y -i /tmp/output.wav -f s16le -acodec pcm_s16le -ar 8000 -af 'adelay=1000|1000' -ac 1 /tmp/outputConv.wav"
		cmd= "pico2wave -l='" + lang +"' -w /tmp/output.wav \"" + str + "\" && ffmpeg -y -i /tmp/output.wav -ar 8000  -af volume=1.3,asetrate=16000*1,aresample=16000,atempo=1 -ac 1 /tmp/outputConv.wav"
		#cmd = "ffmpeg -y -i /tmp/output.wav -f s16le -acodec pcm_s16le -ar 8000 -af 'adelay=1000|1000' -ac 1 /tmp/outputConv.wav"
		os.system(cmd)
		#if not os.path.isfile(file):
		#	error('failed decode mp3')

		# load wav
		file = "/tmp/outputConv.wav"
		with open(file, 'rb') as f:
			dat = f.read()
		self.data_r = 0
		
		# convert to numpy array
		dat = np.fromstring(dat, dtype='int16').astype(np.int32) # BINGO BINGO BINGO
		
		# normalise wav
		dat = dat.astype(np.float)
		sc = 32767.0 / np.max(np.abs(dat))
		dat *= sc
		dat = dat.astype(np.int16).tolist()
		dat = np.insert(dat,20,[0] * 1000)
		# store
		self.data = dat
		print self.data
		# state
		self.buffer_space = 800
		self.buffer_total = 0

		# get robot name
		topic_base = "/" + os.getenv("MIRO_ROBOT_NAME") + "/"

		# publish
		topic = topic_base + "control/stream"
		print ("publish", topic)
		self.pub_stream = rospy.Publisher(topic, Int16MultiArray, queue_size=20)

		# subscribe
		topic = topic_base + "sensors/stream"
		print ("subscribe", topic)
		self.sub_stream = rospy.Subscriber(topic, UInt16MultiArray, self.callback_stream)

if __name__ == "__main__":

	rospy.init_node("client_voice", anonymous=False)
	main = streamer()
	main.loop(sys.argv[2:])




