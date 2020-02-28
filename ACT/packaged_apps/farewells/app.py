#!/usr/bin/python3
import rospy
import geometry_msgs
import time
import sys
import os
import numpy as np
import curses
import cv2
import miro2 as miro
import mml
import random

from datetime import datetime
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import CompressedImage

################################################################

def error(msg):
	print(msg)
	sys.exit(0)

################################################################

class client:

	def callback_cam(self, ros_image, index):

		# silently (ish) handle corrupted JPEG frames
		try:

			# convert compressed ROS image to raw CV image
			image = self.image_converter.compressed_imgmsg_to_cv2(ros_image, "rgb8")

			# store image for display
			self.input_camera[index] = image
			
		except CvBridgeError as e:
			pass

	def callback_caml(self, ros_image):
		self.callback_cam(ros_image, 0)

	def callback_camr(self, ros_image):
		self.callback_cam(ros_image, 1)
		
	def detect_faces(self, im,index):
		faces_detected = 0
		try:
			face_cascade = cv2.CascadeClassifier('/home/miro/ACT/packaged_apps/farewells/haarcascade_frontalface_default.xml')

			# Read the input image
			img = im

			# Convert into grayscale
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			# Detect faces
			faces = face_cascade.detectMultiScale(gray, 1.1, 4)

			# Draw rectangle around the faces
			for (x, y, w, h) in faces:
				cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
				faces_detected += 1
				print("Face Detected " + str(x)) 
						
		except CvBridgeError as e:
			pass

		return faces_detected

	def loop(self):
	
		# state
		self.ignoreCamL = False
		self.ignoreCamR = False 
		self.posClose = False
		#self.ignoreCamR = False
		self.tl = 0
		# loop
		while not rospy.core.is_shutdown():
			# for each camera
			#ctime = time.time()
			for index in range(2):
				# get image
				image = self.input_camera[index]
				# if present
				if not image is None and (time.time() - self.lastDetect) >= 15:
					# handle
					
					self.input_camera[index] = None
					faces = self.detect_faces(image, index)
					if faces > 0:
						self.lastDetect = time.time()
						print("Faces Detected: " + str(faces))
						self.robot.wag_tail(5, 24)
						response = random.randint(1, 2)
						if response == 0:
							#mml.say("It was nice seeing you")
							mml.play("/home/miro/ACT/voice_files/it_was_nice_seeing_you.mp3")
						elif response == 1:
							#mml.say("Goodbye")
							mml.play("/home/miro/ACT/voice_files/goodbye.mp3")
						elif response == 2:
							#mml.say("Thank you for visiting our library")
							mml.play("/home/miro/ACT/voice_files/thank_you_for_visiting_our_library.mp3")
			self.input_camera[0] = None
			self.input_camera[1] = None
			time.sleep(0.2)
			resp = self.robot.read_head_touch_sensors()
			if resp[6] and resp[13]:
				ctime = time.time()
				while resp[6] and resp[13]:
					resp = self.robot.read_head_touch_sensors()
					if time.time() - ctime >= 2:
						print("Shutting Down Application")
						os.system("rosnode kill mml_play")
						for j in range(6):
							self.robot.control_led(j,"#ffffff" ,255)
						os.remove("/tmp/running.state")
						os.system("rosnode kill client_web")
						
						sys.exit()

	def __init__(self, args):
		self.lastDetect = time.time()-15
		# state
		self.input_camera = [None, None]

		# init the robot Kinetic control.
		self.robot = miro.interface.PlatformInterface()

		# ROS -> OpenCV converter
		self.image_converter = CvBridge()
		# robot name
		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
		# subscribe
		self.sub_caml = rospy.Subscriber(topic_base_name + "/sensors/caml/compressed",
					CompressedImage, self.callback_caml, queue_size=1, tcp_nodelay=True)
		self.sub_camr = rospy.Subscriber(topic_base_name + "/sensors/camr/compressed",
					CompressedImage, self.callback_camr, queue_size=1, tcp_nodelay=True)
		


if __name__ == "__main__":

	rospy.init_node("client_web", anonymous=False)
	main = client(sys.argv[1:])
	main.loop()




