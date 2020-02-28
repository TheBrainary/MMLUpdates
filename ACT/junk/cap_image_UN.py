#!/usr/bin/python
import time
import numpy as np 
import cv2 

import miro2 as miro

import math
import roslib
import rospy
import os

# Ros Messages
from sensor_msgs.msg import CompressedImage



#files = len(os.listdir(images_path)) #amount of files in /frontend/images/ folder i
#if files > 7 : #allow 5 images max
#    os.system("find "+images_path+" -name '*.png' | xargs ls -t | tail -n 1 | xargs rm") #remove oldest image


class capture:

	def callback_image(self, msg):
		print("starting callback")
		np_arr = np.frombuffer(msg.data, np.uint8)
		image_np = cv2.imdecode(np_arr, 1)
		images_path = '/home/miro/'
		timestr = time.strftime("%d-%m-%Y_%H-%M-%S.png")
		print("starting Image Save")
		cv2.imwrite(images_path+ 'image_' + timestr, image_np)

	def loop(self):
		# loop
		while not rospy.core.is_shutdown():
			# state
			time.sleep(3)

	def __init__(self):

		# state
		self.wait = False
		# robot name
		topic_base = "/" + os.getenv("MIRO_ROBOT_NAME") + "/"

		# subscribe
		topic = topic_base + "sensors/camr/compressed"
		print ("subscribe", topic)
		self.sub_log = rospy.Subscriber(topic, CompressedImage, self.callback_image)






if __name__ == "__main__":

	rospy.init_node("client_show_cliff", anonymous=True)
	main = capture()
	main.loop()
