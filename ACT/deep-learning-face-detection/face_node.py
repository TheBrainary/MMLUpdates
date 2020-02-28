import rospy
from sensor_msgs.msg import CompressedImage
import geometry_msgs
import time
import sys
import os
import numpy as np
import curses
import cv2
from cv_bridge import CvBridge, CvBridgeError
import miro2 as miro
import apriltag

# import the necessary packages
import argparse
import cv2

# construct the argument parse and parse the arguments


# load our serialized model from disk
print("[INFO] loading model...")



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

			# swallow error, silently
			#print(e)
			pass

	def callback_caml(self, ros_image):
		self.callback_cam(ros_image, 0)

	def callback_camr(self, ros_image):
		self.callback_cam(ros_image, 1)
		
	def detect_faces(self, im,index):
		
		try:
			face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

			# Read the input image
			img = im

			# Convert into grayscale
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			# Detect faces
			faces = face_cascade.detectMultiScale(gray, 1.1, 4)

			# Draw rectangle around the faces
			for (x, y, w, h) in faces:
				cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

			cv2.imwrite("test.png",img)
			# Display the output
			#cv2.imshow('img', img)
			#cv2.waitKey()

						
		except CvBridgeError as e:

			# swallow error, silently
			#print(e)
			pass

		return im

	def loop(self):
	
		# state
		self.ignoreCamL = False
		self.ignoreCamR = False 
		self.posClose = False
		#self.ignoreCamR = False
		self.tl = 0
		# loop
		while not rospy.core.is_shutdown() and self.ShutdownFlag == False:
			# for each camera
			for index in range(2):
				# get image
				image = self.input_camera[index]
				# if present
				if not image is None:
					# handle
					self.input_camera[index] = None
					
					face = self.detect_faces(image, index)
			# state
			time.sleep(0.2)
			
			resp = robot.read_head_touch_sensors()
			if resp[4] and resp[11]:
				ctime = time.time()
				print("Head Touched")
				while resp[4] and resp[11]:
					resp = robot.read_head_touch_sensors()
					if time.time() - ctime >= 2:
						self.ShutdownFlag = True

	def __init__(self, args):

		# state
		self.ShutdownFlag = False
		self.input_camera = [None, None]
		self.april_detector = True
		# init the robot Kinetic control.
		self.robot = miro.interface.PlatformInterface()
		# handle april

		# ROS -> OpenCV converter
		self.image_converter = CvBridge()
		# robot name
		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
		# subscribe
		self.sub_caml = rospy.Subscriber(topic_base_name + "/sensors/caml/compressed",
					CompressedImage, self.callback_caml, queue_size=1, tcp_nodelay=True)
		self.sub_camr = rospy.Subscriber(topic_base_name + "/sensors/camr/compressed",
					CompressedImage, self.callback_camr, queue_size=1, tcp_nodelay=True)
		
		# report
		print "recording from 2 cameras, press CTRL+C to halt..."

if __name__ == "__main__":

	rospy.init_node("client_video", anonymous=True)
	main = client(sys.argv[1:])
	main.loop()




