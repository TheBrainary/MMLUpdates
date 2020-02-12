#!/usr/bin/python
import time
import numpy as np 
import cv2 

import miro2 as miro

import math
import roslib
import rospy
import os
import sys
from pyzbar import pyzbar
# Ros Messages
from sensor_msgs.msg import CompressedImage


# state
# robot name
topic_base = "/" + os.getenv("MIRO_ROBOT_NAME") + "/"
rospy.init_node("client_barcode", anonymous=True)
# subscribe
topic = topic_base + "sensors/caml/compressed"
#sub_log = rospy.Subscriber(topic, e, self.callback_image)
msg = rospy.wait_for_message(topic, CompressedImage)
np_arr = np.frombuffer(msg.data, np.uint8)

image = cv2.imdecode(np_arr, 1)
#images_path = '/home/miro/' 
#timestr = time.strftime("%d-%m-%Y_%H-%M-%S.png")
#print("starting Image Save")
#cv2.imwrite(images_path+ 'image_' + timestr, image_np)

barcodes = pyzbar.decode(image)

# loop over the detected barcodes
for barcode in barcodes:
	# extract the bounding box location of the barcode and draw the
	# bounding box surrounding the barcode on the image


	# the barcode data is a bytes object so if we want to draw it on
	# our output image we need to convert it to a string first
	barcodeData = barcode.data.decode("utf-8")
	barcodeType = barcode.type


	# print the barcode type and data to the terminal
	print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
