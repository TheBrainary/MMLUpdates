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
			print(self.detect_ball('#ff0000', index))
		except CvBridgeError as e:

			# swallow error, silently
			#print(e)
			pass

	def callback_caml(self, ros_image):

		self.callback_cam(ros_image, 0)

	def callback_camr(self, ros_image):
		#self.callback_cam(ros_image, 1)
		pass
		
	def detect_ball(self, colour_str, index):

		#print(self.input_camera[0])
		im = self.input_camera[index]
		if im is None:
			return None

		# get image in HSV format
		im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
		#print("starting Image Save")
		
		#print("Image Saved")

		#create colour code from user selected colour
		red = int(colour_str[1:3], 16)
		green = int(colour_str[3:5], 16)
		blue = int(colour_str[5:7], 16)
		bgr_colour = np.uint8([[[blue, green, red]]])
		hsv_colour = cv2.cvtColor(bgr_colour, cv2.COLOR_BGR2HSV)
		hue0 = hsv_colour[0,0][0]

		# define hue range
		huer = 30

		# mask image
		hue_min = hue0 - huer
		hue_max = hue0 + huer
		if hue_min < 0:
			lo = np.array([0, 70, 70])
			hi = np.array([hue_max, 255, 255])
			mask1 = cv2.inRange(im_hsv, lo, hi)
			lo = np.array([hue_min + 180, 70, 70])
			hi = np.array([180, 255, 255])
			mask2 = cv2.inRange(im_hsv, lo, hi)
			mask = cv2.bitwise_or(mask1, mask2)
		elif hue_max > 180:
			lo = np.array([hue_min, 70, 70])
			hi = np.array([180, 255, 255])
			mask1 = cv2.inRange(im_hsv, lo, hi)
			lo = np.array([0, 70, 70])
			hi = np.array([hue_max-180, 255, 255])
			mask2 = cv2.inRange(im_hsv, lo, hi)
			mask = cv2.bitwise_or(mask1, mask2)
		else:
			lo = np.array([hue_min, 70, 70])
			hi = np.array([hue_max, 255, 255])
			mask = cv2.inRange(im_hsv, lo, hi)
		
		# debug
		#cv2.imshow('im', mask)
		#cv2.waitKey(1)

		# clean up
		seg = mask
		seg = cv2.GaussianBlur(seg, (5, 5), 0)
		seg = cv2.erode(seg, None, iterations=2)
		seg = cv2.dilate(seg, None, iterations=2)

		cv2.imwrite( "../test" + str(index) + ".jpg", seg );
		# parameters
		canny_high_thresh = 128 # don't think it matters much for binary image, but does affect our grey image
		ball_detect_sensitivity = 20 # was 33 in Tom's code, lower detects more circles, so it's a trade-off
		ball_detect_min_dist_between_cens = 40 # was 40 in Tom's code, arbitrary
		ball_detect_min_radius = 12 # arbitrary, empirical, too small and we'll pick up noise objects
		ball_detect_max_radius = 150 # arbitrary, empirical

		# get circles
		circles = cv2.HoughCircles(seg, cv2.HOUGH_GRADIENT,
				1, ball_detect_min_dist_between_cens, \
				param1=canny_high_thresh, param2=ball_detect_sensitivity, \
				minRadius=ball_detect_min_radius, maxRadius=0)

		# Get largest circle
		max_circle = None
		max_circle_norm = [None, None, None]
		if circles is not None:
			self.max_rad = 0
			circles = np.uint16(np.around(circles))

			for c in circles[0,:]:
			
				# annotate
				#cv2.circle(seg, (c[0], c[1]), c[2], (0, 255, 0), 2)
				
				if c[2] > self.max_rad:
					self.max_rad = c[2]
					max_circle = c
					#print(c[0])
					

			self.found_circle[index] = max_circle

			self.circle_str[index] = "x: " + str(max_circle[0]) + "," + "y: " + str(max_circle[1]) + "," + "r: " + str(max_circle[2])
			#return [m[0], m[1], m[2]]
			
			# accept only exact match
			self.tl = time.time()
			cv2.imwrite( "../test.jpg", seg );

			self.robot.set_neck(miro.constants.JOINT_LIFT, 34)
			self.robot.set_neck(miro.constants.JOINT_YAW, -60)
			self.robot.set_neck(miro.constants.JOINT_PITCH, 7)
			if index == 0 and self.ignoreCamL == False:
				if 12 == 12:
					if max_circle[0] < 425:
						self.robot.set_turn_speed(+85)
						self.robot.set_forward_speed(0)
						#print("Left Camera - Turning left " + str(tag.center[0]))
					if max_circle[0] > 475:
						self.robot.set_turn_speed(-85)
						#print("Left Camera - Turning right " + str(tag.center[0]))
						self.robot.set_forward_speed(0)
					else:
						self.robot.set_turn_speed(0)
						self.robot.set_forward_speed(+0.4)
						
					#self.ignoreCamR = True
				
			if index == 1 and self.ignoreCamR == False:
				if 6 == 6:
					if max_circle[0] < 150:
						self.robot.set_turn_speed(+85)
						self.robot.set_forward_speed(+0.1)
					elif max_circle[0] > 220:
						self.robot.set_turn_speed(-85)
						self.robot.set_forward_speed(+0.1)
					else:
						self.robot.set_turn_speed(0)
						self.robot.set_forward_speed(+0.4)
						if max_circle[1] < 120:
							self.robot.set_neck(miro.constants.JOINT_PITCH, -15)
							self.robot.set_neck(miro.constants.JOINT_LIFT, 0)
					#self.ignoreCamL = True
					self.robot.sleep(100)
			
			return self.circle_str[index]

		else:
			self.robot.set_turn_speed(0)
			self.robot.set_forward_speed(0)
			return None
		
	def detect_april(self, im,index):
		
		# get grey frame
		im_grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

		# get all detected tags
		self.detected_tags = self.april_detector.detect(im_grey)
		self.robot.set_neck(miro.constants.JOINT_LIFT, 5)

		# for each
		for tag in self.detected_tags:
			# accept only exact match
			if tag.hamming < 2 and (tag[1] == 12 or tag[1] == 6):
				print("Tag Detected, ID: " + str(tag[1]) + ", Center: " + str(int(tag.center[0])) + ", Camera: " + str(index))
				self.tl = time.time()
				if index == 0 and self.ignoreCamL == False:
					if tag[1] == 12:
						if tag.center[0] < 425:
							self.robot.set_turn_speed(+85)
							self.robot.set_forward_speed(0)
							#print("Left Camera - Turning left " + str(tag.center[0]))
						elif tag.center[0] > 475:
							self.robot.set_turn_speed(-85)
							#print("Left Camera - Turning right " + str(tag.center[0]))
							self.robot.set_forward_speed(0)
						else:
							self.robot.set_turn_speed(0)
							self.robot.set_forward_speed(+0.4)
							if tag.center[1] < 120:
								self.robot.set_neck(miro.constants.JOINT_PITCH, -15)
								self.robot.set_neck(miro.constants.JOINT_LIFT, 0)
							
						self.ignoreCamR = True
					
				if index == 1 and self.ignoreCamR == False:
					if tag[1] == 6:
						if tag.center[0] < 150:
							self.robot.set_turn_speed(+85)
							#self.robot.set_forward_speed(+0.1)
						elif tag.center[0] > 220:
							self.robot.set_turn_speed(-85)
							#self.robot.set_forward_speed(+0.1)
						else:
							self.robot.set_turn_speed(0)
							self.robot.set_forward_speed(+0.4)
							if tag.center[1] < 120:
								self.robot.set_neck(miro.constants.JOINT_PITCH, -15)
								self.robot.set_neck(miro.constants.JOINT_LIFT, 0)
						self.ignoreCamL = True
						self.robot.sleep(100)
			continue 
		return im

	def loop(self):
	
		# state
		self.ignoreCamL = False
		self.ignoreCamR = False 
		self.posClose = False
		#self.ignoreCamR = False
		self.tl = 0
		# loop
		while not rospy.core.is_shutdown():
			self.timeC = time.time()
			# for each camera
			for index in range(2):
				# get image
				image = self.input_camera[index]
				# if present
				#if not image is None:
					# handle
					#self.input_camera[index] = None
					#x = 
					#if x != None:
					#	print(x)
					#print(self.detect_ball('#3333ff', 0))
					# april tags
					#if not self.april_detector is None:
						#image = self.detect_april(image, index)
			# state
			time.sleep(0.2)

	def __init__(self, args):

		# state
		self.input_camera = [None, None]
		self.april_detector = True
		
		# init the robot Kinetic control.
		self.robot = miro.interface.PlatformInterface()
		# handle april

		# ROS -> OpenCV converter
		self.image_converter = CvBridge()

		self.cam_images = [None, None]
		self.ann_images = [None, None]
		self.frame_w = None
		self.frame_h = None
		self.x_cent = None
		self.y_cent = None

		self.found_circle = [None, None]
		self.circle_str = [None, None]
		# robot name
		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
		self.robot.set_neck(miro.constants.JOINT_LIFT, 34)
		self.robot.set_neck(miro.constants.JOINT_YAW, -60)
		self.robot.set_neck(miro.constants.JOINT_PITCH, 7)
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




