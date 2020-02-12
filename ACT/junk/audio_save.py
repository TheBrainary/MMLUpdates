#!/usr/bin/python

import rospy
from std_msgs.msg import UInt8MultiArray, UInt16MultiArray, Int16MultiArray, String
from scipy.io.wavfile import write


import time
import sys
import os
import numpy as np

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
RECORD_TIME = 2

# microphone sample rate (also available at miro2.constants)
MIC_SAMPLE_RATE = 20000



################################################################

def error(msg):
	print(msg)
	sys.exit(0)

################################################################

class audio_repeat:

	def callback_stream(self, msg):

		self.buffer_space = msg.data[0]
		self.buffer_total = msg.data[1]
		self.buffer_stuff = self.buffer_total - self.buffer_space
		
	def callback_mics(self, msg): # micdata, b, c, d):
	
		# if recording
		if not self.micbuf is None:

			# append mic data to store	
			x = np.reshape(np.array(msg.data), (-1, 500))
			x = x.T
			self.micbuf = np.concatenate((self.micbuf, x))
			
			# report
			sys.stdout.write(".")
			sys.stdout.flush()
		
			# finished recording?
			N = RECORD_TIME * MIC_SAMPLE_RATE
			if self.micbuf.shape[0] >= N:
		
				# configure playback
				self.playchan = 0
				self.playsamp = 0

				# downsample for playback
				spkrbuf = np.zeros((int(N / 2.5), 0))
				for c in range(4):
					i = np.arange(0, N, 2.5)
					j = np.arange(0, N)
					x = np.interp(i, j, self.micbuf[:, c])
					spkrbuf = np.concatenate((spkrbuf, x[:, np.newaxis]), axis=1)
				
				# end recording
				print ("")
				self.micbuf = None
				
				# start playback
				self.spkrbuf = spkrbuf
		
	def loop(self, args):

		# loop
		while not rospy.core.is_shutdown():
		
			# if in playback
			if not self.spkrbuf is None:

				# stuff output buffer
				if self.buffer_stuff < BUFFER_MIN:
				
					# report
					if self.playsamp == 0:
			
						# report
						print( "playback of channel " + str(self.playchan + 1) + "...")
					
					# desired amount to send
					n_samp = BUFFER_MAX - self.buffer_stuff
					
					# limit by receiver buffer space
					n_samp = np.minimum(n_samp, self.buffer_space)

					# limit by amount available to send
					n_samp = np.minimum(n_samp, self.spkrbuf.shape[0] - self.playsamp)

					# limit by maximum individual message size
					n_samp = np.minimum(n_samp, MAX_STREAM_MSG_SIZE)
					
					# prepare data
					spkrdata = self.spkrbuf[self.playsamp:(self.playsamp+n_samp), self.playchan]
					self.playsamp += n_samp
					
					# send data
					msg = Int16MultiArray()
					msg.data = spkrdata
					print (spkrdata)
					write("voiceREC4.wav", 16000, spkrdata)
						# move to next channel
						#self.playsamp = 0
						#self.playchan += 1
						
						# finished?
						#if self.playchan == 4:
						
							# clear output
							#print "(playback complete)"
					break

			# state
			time.sleep(0.02)

	def __init__(self):

		# state
		self.micbuf = np.zeros((0, 4), 'uint16')
		self.spkrbuf = None
		self.buffer_stuff = 0

		# robot name
		topic_base = "/" + os.getenv("MIRO_ROBOT_NAME") + "/"

		# publish
		topic = topic_base + "control/stream"
		print ("publish", topic)
		self.pub_stream = rospy.Publisher(topic, Int16MultiArray, queue_size=0)

		# subscribe
		topic = topic_base + "sensors/stream"
		print ("subscribe", topic)
		self.sub_stream = rospy.Subscriber(topic, UInt16MultiArray, self.callback_stream)

		# subscribe
		topic = topic_base + "sensors/mics"
		print ("subscribe", topic)
		self.sub_mics = rospy.Subscriber(topic, Int16MultiArray, self.callback_mics)
		
		# report
		print( "recording on 4 microphone channels...")

if __name__ == "__main__":

	rospy.init_node("client_audio_repeat", anonymous=True)
	main = audio_repeat()
	main.loop(sys.argv[1:])




