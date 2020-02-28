import rospy
from sensor_msgs.msg import CompressedImage,  JointState
import geometry_msgs
import time
import sys
import os
import numpy as np
import curses
import cv2
from cv_bridge import CvBridge, CvBridgeError
import miro2 as miro
import math
import imutils
import math

kernel = np.ones((5,5),np.uint8)

################################################################

def error(msg):
	print(msg)
	sys.exit(0)

################################################################

class client:

	def callback_kinsen(self,msg):
		if msg.position != [-0.10471975803375244, 1.07686448097229, -0.16465935111045837, 0.12642529606819153]:
			self.kinematic_joints_pub.publish(self.kin_joints)

	def callback_cam(self, ros_image, index):
		try:
			image = self.image_converter.compressed_imgmsg_to_cv2(ros_image, "rgb8")
			self.input_camera[index] = image
		except CvBridgeError as e:
			pass

	def callback_caml(self, ros_image):
		self.callback_cam(ros_image, 0)

	def callback_camr(self, ros_image):
		self.callback_cam(ros_image, 1)
		
	def	callback_lightsense(self, msg):
		self.LightSensors = msg.light.data
		self.SonarRange = msg.sonar.range
		
	def detect_ball(self, index, im):
		if im is None:
			return None

		# define the lower and upper boundaries of the "green"
		# ball in the HSV color space, then initialize the
		# list of tracked points
		greenLower = (0, 0, 0)
		greenUpper = (220, 164, 255) 
		#pts = deque(maxlen=args["buffer"])

		# get image in HSV format
		#frame = im
		frame = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
		#frame = cv2.bitwise_not(frame)
		frame = imutils.resize(frame, width=600)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
		#cv2.imwrite("/home/miro/BallTest.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
		im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		cv2.imwrite("/home/miro/ballRGB.jpg", cv2.cvtColor(im_rgb, cv2.COLOR_RGB2BGR))
		# construct a mask for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.bitwise_not(mask)
		#mask = cv2.erode(mask, None, iterations=2)
		#mask = cv2.dilate(mask, None, iterations=2)
		mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
		#mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
		mask = cv2.erode(mask, None, iterations=3)
		mask = cv2.dilate(mask, None, iterations=2)
		
		# find contours in the mask and initialize the current
		# (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		center = None
		cv2.imwrite("/home/miro/BallMasked.jpg", mask) 
		# only proceed if at least one contour was found
		if len(cnts) > 0: 
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

			# only proceed if the radius meets a minimum size
			if radius > 7 and radius < 45:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				print("I:" + str(index) + "    R: " + str(int(radius)) + "    C:" + str(center))
				#print("center: " + str(center))
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
				cv2.imwrite("/home/miro/ballCircled.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
								
				if index == 0 and self.ignoreCamL == False:
					if center[0] < 350:
						self.robot.set_turn_speed(+30)
						self.robot.set_forward_speed(0)
						#print("Left Camera - Turning left " + str(center[0]))
					elif center[0] > 550:
						self.robot.set_turn_speed(-30)
						#print("Left Camera - Turning right " + str(center[0]))
						self.robot.set_forward_speed(0)
					else:
						self.robot.set_turn_speed(0)
						self.robot.set_forward_speed(+0.2)
						self.ignoreCamR = True
						#if center[1] < 120:
							#self.atKennel == True
							#print("Set AtKennel to true")
									
							
						
					
				if index == 1 and self.ignoreCamR == False:
					if center[0] < 100:
						self.robot.set_turn_speed(+30)
						self.robot.set_forward_speed(0)
					elif center[0] > 250:
						self.robot.set_turn_speed(-30)
						self.robot.set_forward_speed(0)
					else:
						self.robot.set_turn_speed(0)
						self.robot.set_forward_speed(+0.2)
						self.ignoreCamL = True
						#self.robot.sleep(100)
					
					#if center[1] < 120:
					#	self.robot.set_neck(miro.constants.JOINT_PITCH, -15)
					#	self.robot.set_neck(miro.constants.JOINT_LIFT, 0)
				#cv2.imwrite("/home/miro/BallTest.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)) 
				return center				
			elif radius > 45:
				self.robot.set_turn_speed(0)
				self.robot.set_forward_speed(0)
		#else:
			#self.robot.set_turn_speed(0)
			#self.robot.set_forward_speed(0)
		# update the points queue
		#pts.appendleft(center)
		
		return None

	def loop(self):
	
		# state
		self.ignoreCamL = False
		self.ignoreCamR = False 
		self.posClose = False
		self.atKennel = False 
		self.LightSensors = []
		self.SonarRange = 0
		self.kinematic_joints_pub.publish(self.kin_joints)
		self.tl = 0
		# loop
		while not rospy.core.is_shutdown():
			self.timeC = time.time()

			#self.kinematic_joints_pub.publish(self.kin_joints)
			if self.timeC - self.tl > 0.5:
				
				self.robot.set_turn_speed(0)
				self.robot.set_forward_speed(0)
				self.tl = time.time()
				self.ignoreCamL = False
				self.ignoreCamR = False
				


			#image = self.input_camera[index]
			#if not image is None:
				#self.input_camera[index] = None
			if self.ignoreCamL == False and not self.input_camera[0] is None:	
				if self.detect_ball(0,self.input_camera[0]) != None:
					self.tl = time.time()
				else:
					print("not Detecting L2")

			else:
				print("not Detecting L")
					
			#if self.ignoreCamR == False and not self.input_camera[1] is None:	
				#print(self.detect_ball(1,self.input_camera[1]))
			if self.ignoreCamR == False and not self.input_camera[1] is None:	
				if self.detect_ball(1,self.input_camera[1]) != None:
					self.tl = time.time()
				else:
					print("not Detecting R2")
			else: 
				print("not Detecting R")
				
			# state
			resp = "111111111111111111111111111111111111111111"
			#self.robot.read_head_touch_sensors()
			if resp[4] and resp[11]:
				ctime = time.time()
				while resp[4] and resp[11]:
					resp = self.robot.read_head_touch_sensors()
					if time.time() - ctime >= 2:
						print("Shutting Down Application")
						os.system("rosnode kill mml_play")
						for j in range(6):
							self.robot.control_led(j,"#ffffff" ,255)
						os.system("rosnode kill client_web")
						try:
							os.remove("/tmp/running.state")
						except:
							print("An exception occurred")

						sys.exit()

			time.sleep(0.2)

	def __init__(self, args):

		# state
		self.input_camera = [None, None]
		self.april_detector = True
		
		self.kin_joints = JointState()
		self.kin_joints.name = ["tilt", "lift", "yaw", "pitch"]
		
		self.kin_joints.position = [-0.10471975803375244, 1.07686448097229, -0.16465935111045837, 0.12642529606819153]
		self.kin_joints.effort = [1,1,1,1]
		# init the robot Kinetic control.
		self.robot = miro.interface.PlatformInterface()
		
		self.cam_images = [None, None]
		self.ann_images = [None, None]
		self.frame_w = None
		self.frame_h = None
		self.x_cent = None
		self.y_cent = None

		self.found_circle = [None, None]
		self.circle_str = [None, None]
		
		# ROS -> OpenCV converter
		self.image_converter = CvBridge()
		# robot name
		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
		# subscribe
		self.sub_caml = rospy.Subscriber(topic_base_name + "/sensors/caml/compressed", CompressedImage, self.callback_caml, queue_size=1)
		self.sub_camr = rospy.Subscriber(topic_base_name + "/sensors/camr/compressed", CompressedImage, self.callback_camr, queue_size=1)
		#self.sub_lightsens = rospy.Subscriber(topic_base_name + "/sensors/package", miro.msg.sensors_package, self.callback_lightsense, queue_size=1, tcp_nodelay=True)
		#self.sub_kinsens = rospy.Subscriber(topic_base_name + "/sensors/kinematic_joints", JointState, self.callback_kinsen, queue_size=1, tcp_nodelay=True)
		self.kinematic_joints_pub = rospy.Publisher(topic_base_name + "/control/kinematic_joints", JointState, queue_size=1)
		
		# report
		print "recording from 2 cameras, press CTRL+C to halt..."

if __name__ == "__main__":

	rospy.init_node("client_web", anonymous=False)
	main = client(sys.argv[1:])
	main.loop()




