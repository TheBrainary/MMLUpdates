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
BUFFER_STUFF_BYTES = 4000

# media source directories
DIR_SOURCE = ["/home/miro/ACT/tmp"]

################################################################

def error(msg):

	print(msg)
	sys.exit(0)

################################################################

# index



# otherwise, choose item from list
TRACK_FILE = "output.mp3"
TRACK_PATH = "/home/miro/ACT/tmp/output.mp3"
# if the file is not there, fail
if not os.path.isfile(TRACK_PATH):
	error('file not found');



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

		# decode mp3
		if os.path.isfile("/home/miro/ACT/tmp/output.mp3.decode"):
			os.remove("/home/miro/ACT/tmp/output.mp3.decode")
		file = "/home/miro/ACT/tmp/" + TRACK_FILE + ".decode"
		if not os.path.isfile(file):
			cmd = "ffmpeg -y -i " + TRACK_PATH + " -f s16le -acodec pcm_s16le -ar 8000 -ac 1 " + file
			os.system(cmd)
			if not os.path.isfile(file):
				error('failed decode mp3')

		# load wav
		with open(file, 'rb') as f:
			dat = f.read()
		self.data_r = 0
		
		# convert to numpy array
		dat = np.fromstring(dat, dtype='int16').astype(np.int32)
		
		# remove dither noise
		#
		# NB: this doesn't really do much any more, I think, since
		# we've moved to int16 representation (from uint8)
		"""
		value = dat[0]
		count = 0
		blanked = 0
		for i in range(len(dat)):
			x = dat[i]
			dx = np.abs(x - value)
			if dx <= 1:
				count += 1
			else:
				count = 0
				value = x
			if count >= 10:
				dat[i] = value
				blanked += 1
		"""

		# normalise wav
		dat = dat.astype(np.float)
		sc = 32767.0 / np.max(np.abs(dat))
		dat *= sc
		dat = dat.astype(np.int16).tolist()

		# breakdown of digit file is recovered manually

		# these are for _0-9_Male_Vocalized-Mike_Koenig-1919515312.mp3
		"""
		digits_0_to_9 = [
			[2900, 7712],
			[12604, 16764],
			[22389, 25911],
			[32517, 36092],
			[42463, 45890],
			[51731, 55433],
			[61791, 65500],
			[71099, 74647],
			[80346, 84116],
			[89304, 94116]
			]
		"""

		# these are for _digits_and_dot_male.mp3
		"""
		digits_and_dot = [
			[1186, 4096],
			[6025, 9321],
			[11388, 14446],
			[16361, 19950],
			[21639, 24616],
			[27150, 29909],
			[32146, 34792],
			[37262, 40014],
			[42032, 44593],
			[46837, 50111],
			[51918, 54070],
			]
		"""
			
		# these are for _digits_and_dot_female.mp3
		digits_and_dot = [
			[550, 5348],
			[6100, 11470],
			[13649, 18257],
			[21551, 26383],
			[29512, 33906],
			[37896, 42336],
			[46378, 50548],
			[54434, 58762],
			[61995, 66019],
			[69027, 73927],
			[76593, 80695],
			]			
				
		# store
		self.data = dat

		# state
		self.buffer_space = 0
		self.buffer_total = 0

		# get robot name
		topic_base = "/" + os.getenv("MIRO_ROBOT_NAME") + "/"

		# publish
		topic = topic_base + "control/stream"
		print ("publish", topic)
		self.pub_stream = rospy.Publisher(topic, Int16MultiArray, queue_size=0)

		# subscribe
		topic = topic_base + "platform/log"
		print ("subscribe", topic)
		self.sub_log = rospy.Subscriber(topic, String, self.callback_log)

		# subscribe
		topic = topic_base + "sensors/stream"
		print ("subscribe", topic)
		self.sub_stream = rospy.Subscriber(topic, UInt16MultiArray, self.callback_stream)

if __name__ == "__main__":

	rospy.init_node("client_stream", anonymous=True)
	main = streamer()
	main.loop(sys.argv[2:])




