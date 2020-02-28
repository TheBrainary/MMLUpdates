#!/usr/bin/python3
import rospy

from std_msgs.msg import UInt8MultiArray, UInt16MultiArray, Int16MultiArray, String,UInt32MultiArray

from pocketsphinx import Pocketsphinx, get_model_path, get_data_path

import time
import sys
import os
import numpy as np
import wave, struct
import mml
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
RECORD_TIME = 4

# microphone sample rate (also available at miro2.constants)
MIC_SAMPLE_RATE = 20000

# sample count
SAMPLE_COUNT = RECORD_TIME * MIC_SAMPLE_RATE



################################################################

def error(msg):
	print(msg)
	sys.exit(0)

class client:

	def callback_stream(self, msg):

		self.buffer_space = msg.data[0]
		self.buffer_total = msg.data[1]
		self.buffer_stuff = self.buffer_total - self.buffer_space
		
	def callback_clap(self, msg):
		print(msg)
		
	def callback_mics(self, msg):
		data = np.array(msg.data).astype('float32') * (1.0 / 32768.0)
		rms_l = np.sqrt(np.mean(data[0:500]**2))
		rms_r = np.sqrt(np.mean(data[500:1000]**2))
		new_audio_level = np.max((self.audio_level, np.mean([rms_l, rms_r])))
		if new_audio_level > self.audio_level:
			self.illum = UInt32MultiArray()
			self.illum.data = [0xFF00CC, 0xFF00CC, 0xFF00CC, 0xFF00CC, 0xFF00CCFF, 0x00FF00CC]
			self.audio_level = new_audio_level
			self.pub_illum.publish(self.illum)

		# if recording
		if not self.micbuf is None and self.audio_level > 0.5:
			
			# append mic data to store
			data = np.array(msg.data, 'int16')
			x = np.reshape(data, (-1, 500))
			self.micbuf = np.concatenate((self.micbuf, x.T))
			
			# report
			sys.stdout.write(".")
			sys.stdout.flush()
		
			# finished recording?
			if self.micbuf.shape[0] >= SAMPLE_COUNT:
				
				self.micbuf = np.delete(self.micbuf, range(0, 9000), 0)
				# end recording
				self.outbuf = self.micbuf
				print(self.micbuf.shape)
				self.micbuf = None
				print (" OK!")
				self.audio_level = 0
		
	def loop(self):

		# loop
		while not rospy.core.is_shutdown():
			# if recording finished
			if not self.outbuf is None:
			# write output file
				print("writing output file")
				outfilename = '/tmp/input.wav'
				file = wave.open(outfilename, 'wb')
				file.setparams((1, 4, 20000, 0, 'NONE', 'not compressed'))
				print("Starting Reshape")
				x = np.reshape(self.outbuf[:, [0, 0]], (-1))
				print("writing frames")
				print(len(x))
				values = []
				for s in x:
					packed_value = struct.pack('<h', s)
					values.append(packed_value)
					#file.writeframes(struct.pack('<h', s))
				#close file
				value_str = b''.join(values)
				file.writeframes(value_str)
				
				print("Closing file")
				file.close()

				model_path = get_model_path()
				data_path = get_data_path()

				config = {
			
				'hmm' : os.path.join(model_path, 'en-us'), # Hidden Markov Model, Speech Recongnition model - trained probability scoring system
				'lm': os.path.join(model_path, 'en-us.lm.bin'), #language model
				'dict' : os.path.join(model_path, 'cmudict-en-us.dict')#, # language dictionary
				#'samprate' : 16000
				}
				#cmd= "ffmpeg -y -i /tmp/output.wav -ar 8000 -af asetrate=16000*" + pitch + ",aresample=16000,atempo=" + tempo + " -ac 1 /tmp/outputConv.wav"
				#cmd = "ffmpeg -y -i /tmp/input.wav -f s32le -acodec pcm_s32le -ar 16000 -ac 1 /tmp/inputConv.wav"
				#cmd = "sox /tmp/input.wav -r 16000 inputConv.wav"
				#cmd = "ffmpeg -i /tmp/input.wav -ar 16000 /tmp/inputConv.wav"
				print("Converting via FFMPEG")
				cmd = "ffmpeg -y -i /tmp/input.wav -f s16le -acodec pcm_s16le -ar 16000 -af 'aresample=20000' -ac 1 /tmp/inputConv.wav -loglevel quiet"
				os.system(cmd)
				print("Decoding Via Pocketsphinx")
				ps = Pocketsphinx(**config)
				ps.decode(
				audio_file=("/tmp/inputConv.wav"), #add temp input.wav file
				buffer_size=8192,
				no_search=False,
				full_utt=False)
				
				print("Recognized: ")
				print( ps.hypothesis() ) ## output
				
				## Speech Analysis, (what to start?)
				if ps.hypothesis() == "hello":
					mml.say("Hello there human") # Change this to whatever
				elif ps.hypothesis().find("how are you") >= 0:
					mml.say("I'm always good")
				print("END")
				self.micbuf = np.zeros((0, 4), 'uint16')
				self.outbuf = None
				self.buffer_stuff = 0

				self.playchan = 0
				self.playsamp = 0

			# state
			time.sleep(0.02)
			

	def __init__(self):

		# state
		self.micbuf = np.zeros((0, 4), 'uint16')
		self.outbuf = None
		self.buffer_stuff = 0
		self.audio_level = 0
		self.timeofclap = 0
		self.playchan = 0
		self.playsamp = 0
		

		# robot name
		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")

		# publish
		topic = topic_base_name + "/control/stream"
		print ("publish", topic)
		self.pub_stream = rospy.Publisher(topic, Int16MultiArray, queue_size=0)
		
		topic = topic_base_name + "/control/illum"
		print ("publish", topic)
		self.pub_illum = rospy.Publisher(topic, UInt32MultiArray, queue_size=0)
		
		# subscribe
		topic = topic_base_name + "/sensors/stream"
		print ("subscribe", topic)
		self.sub_stream = rospy.Subscriber(topic, UInt16MultiArray, self.callback_stream, queue_size=1, tcp_nodelay=True)

		# subscribe
		topic = topic_base_name + "/sensors/mics"
		print ("subscribe", topic)
		self.sub_mics = rospy.Subscriber(topic, Int16MultiArray, self.callback_mics, queue_size=5, tcp_nodelay=True)
		
		# report
		print ("Clap once to record for", RECORD_TIME, "seconds...")

		

if __name__ == "__main__":

	rospy.init_node("speech_recog", anonymous=False)
	main = client()
	main.loop()




