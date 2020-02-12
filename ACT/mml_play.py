#!/usr/bin/python
import rospy
from std_msgs.msg import UInt8MultiArray, UInt16MultiArray, Int16MultiArray, String
import time
import sys
import os
import numpy as np

# messages larger than this will be dropped by the receiver
MAX_STREAM_MSG_SIZE = (4096 - 48)

# amount to keep the buffer stuffed - larger numbers mean
# less prone to dropout, but higher latency when we stop
# streaming. with a read-out rate of 8k, 2000 samples will
# buffer for quarter of a second, for instance.
BUFFER_STUFF_BYTES = 1000

################################################################

def error(msg):

	print(msg)
	sys.exit(0)

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
		
		# safety dropout if receiver not present
		dropout_data_r = -1
		dropout_count = 3

		# loop
		while not rospy.core.is_shutdown():

			# check state_file
			if not state_file is None:
				if not os.path.isfile(state_file):
					break

			# if we've received a report
			if self.buffer_total > 0:

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
		
		print(sys.argv[1])
		TRACK_PATH = sys.argv[1]
		TRACK_PATH_PARTS = TRACK_PATH.split("/")
		TRACK_FILE = TRACK_PATH_PARTS[len(TRACK_PATH_PARTS)-1]
		
		# decode mp3
		file = "/tmp/" + TRACK_FILE + ".decode"
		if not os.path.isfile(file):
			cmd = "ffmpeg -y -i '" + TRACK_PATH + "' -f s16le -acodec pcm_s16le -ar 8000 -ac 1 -af 'adelay=1000|1000' " + file
			os.system(cmd)
			if not os.path.isfile(file):
				error('failed decode mp3')

		# load wav
		with open(file, 'rb') as f:
			dat = f.read()
		self.data_r = 0
		
		# convert to numpy array
		dat = np.fromstring(dat, dtype='int16').astype(np.int32)
		
		# normalise wav
		dat = dat.astype(np.float)
		sc = 32767.0 / np.max(np.abs(dat))
		dat *= sc
		dat = dat.astype(np.int16).tolist()

		# store
		self.data = dat
		

		# state
		self.buffer_space = 0
		self.buffer_total = 0

		# get robot name
		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")

		# publish
		topic = topic_base_name + "/control/stream"
		print ("publish", topic)
		self.pub_stream = rospy.Publisher(topic, Int16MultiArray, queue_size=0)

		# subscribe
		topic = topic_base_name + "/platform/log"
		print ("subscribe", topic)
		self.sub_log = rospy.Subscriber(topic, String, self.callback_log, queue_size=5, tcp_nodelay=True)

		# subscribe
		topic = topic_base_name + "/sensors/stream"
		print ("subscribe", topic)
		self.sub_stream = rospy.Subscriber(topic, UInt16MultiArray, self.callback_stream, queue_size=1, tcp_nodelay=True)

if __name__ == "__main__":
	os.system("rosnode kill mml_play") # Kill Any previous node of mml_play
	rospy.init_node("mml_play", anonymous=False)
	main = streamer()
	main.loop(sys.argv[2:])




