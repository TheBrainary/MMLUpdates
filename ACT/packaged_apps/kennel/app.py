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
import apriltag
import math

def error(msg):
	print(msg)
	sys.exit(0)


class client:

	def callback_cam(self, ros_image, index):
		try:
			image = self.image_converter.compressed_imgmsg_to_cv2(ros_image, "rgb8")
			self.input_camera[index] = image
		except CvBridgeError as e:

			# swallow error, silently
			#print(e)
			pass

	def callback_caml(self, ros_image):
		self.callback_cam(ros_image, 0)
		
	def setSpeeds(self, turn_speed, forward_speed):
		self.robot.set_turn_speed(turn_speed)
		self.robot.set_forward_speed(forward_speed)

	def callback_camr(self, ros_image):
		self.callback_cam(ros_image, 1)
		
	def	callback_lightsense(self, msg):
		self.LightSensors = msg.light.data

		if self.LightSensors[0] >= 0.04:
			self.robot.set_turn_speed(0)
			self.robot.set_forward_speed(0)
			os.system("rosnode kill client_web")
		# self.SonarRange = msg.sonar.range
		# if self.SonarRange <= 0.15:
			# print("Sonar Distance: " + str(self.SonarRange))
		
	def	callback_kin(self, msg):
		self.kinematic_joints_pub.publish(self.kin_joints)
		
	def detect_april(self, im, index): 
		im_grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # get grey frame
		self.detected_tags = self.april_detector.detect(im_grey)# get all detected tags

		innerTagC = 0
		outerTagC = 0
		for tag in self.detected_tags:
			if tag[1] == 65:
				innerTagC = tag.center[0]
			elif tag[1] == 249:
				outerTagC = tag.center[0]
			continue
			if innerTagC > 0 and outerTagC > 0:
				print("Tag Centers inner:" + str(innerTagC) + " Outer: " + str(outerTagC))

		for tag in self.detected_tags:
			if tag.hamming < 2 and (tag[1] == 65 or tag[1] == 249):
				#print("Tag Detected, ID: " + str(tag[1]) + ", Center: " + str(int(tag.center[0])) + ", " + str(int(tag.center[1])) + ", Camera: " + str(index))
				self.tl = time.time()
				
				#Find Tag Size to determine whether we are close enough to believe we are in the kennel
				tagsize = tag.corners[2][0]-tag.corners[3][0]		
				#print("Tagsize: " + str(tagsize))
				if tagsize >= 110 and tag[1] == 65 and index == 0:
					#print("Tagsize: " + str(tagsize))
					self.atKennel = True
					self.ignoreCamL = True
					self.ignoreCamR = True
					self.robot.set_turn_speed(-40)
					self.robot.set_forward_speed(0)

					self.sub_lightsens = rospy.Subscriber("miro/sensors/package", miro.msg.sensors_package, self.callback_lightsense, queue_size=1, tcp_nodelay=False)
				# if innerTagC > 0 and outerTagC > 0 :
					# diff = innerTagC - outerTagC
					# if diff >= 50 and index == 0:
						# self.tl = time.time()
						# self.robot.set_turn_speed(-20)
						# time.sleep(0.1)
						# self.tl = time.time()
						# self.robot.set_forward_speed(0.2)
						# time.sleep(0.1)
						# self.tl = time.time()
						# self.robot.set_forward_speed(0)
						# self.robot.set_turn_speed(20)
						# time.sleep(0.1)
						# self.tl = time.time()
						# self.robot.set_turn_speed(0)
						# break
					# elif diff <= -50 and index == 0:
						# self.robot.set_turn_speed(20)
						# time.sleep(0.1)
						# self.robot.set_forward_speed(0.2)
						# time.sleep(0.1)
						# self.tl = time.time()
						# self.robot.set_forward_speed(0)
						# self.robot.set_turn_speed(-20)
						# time.sleep(0.1)
						# self.robot.set_turn_speed(0)
						# break
					# elif diff >= 50 and index == 1:
						# self.robot.set_turn_speed(-20)
						# time.sleep(0.1)
						# self.robot.set_forward_speed(0.2)
						# time.sleep(0.1)
						# self.tl = time.time()
						# self.robot.set_forward_speed(0)
						# self.robot.set_turn_speed(-20)
						# time.sleep(0.1)
						# self.robot.set_turn_speed(0)
						# break
					# elif diff <= -50 and index == 1:
						# self.robot.set_turn_speed(20)
						# time.sleep(0.1)
						# self.robot.set_forward_speed(0.2)
						# time.sleep(0.1)
						# self.tl = time.time()
						# self.robot.set_forward_speed(0)
						# self.robot.set_turn_speed(20)
						# time.sleep(0.1)
						# self.robot.set_turn_speed(0)
						# break
						
				if index == 0 and self.ignoreCamL == False:
					if tag[1] == 65 and outerTagC == 0:
						#print("Found Tag 65 Only, Moving Towards")
						if tag.center[0] < 400:
							self.setSpeeds(+20, 0)
						elif tag.center[0] > 500:
							self.setSpeeds(-20, 0)
						else:
							self.setSpeeds(0, +0.2)
					elif tag[1] == 249:
						#print("Found Tag 249, Moving Towards")
						if tag.center[0] < 400:
							self.setSpeeds(+20, 0)
						elif tag.center[0] > 500:
							self.setSpeeds(-20, 0)
						else:
							self.setSpeeds(0, +0.2)
					# self.sub_camr.unregister()
					# self.ignoreCamR = True
							
				if index == 1 and self.ignoreCamR == False:
					if tag[1] == 65 and outerTagC == 0:
						#print("Found Tag 65 Only, Moving Towards")
						if tag.center[0] < 100:
							self.setSpeeds(+20, 0)
						elif tag.center[0] > 280:
							self.setSpeeds(-20, 0)
						else:
							self.setSpeeds(0, +0.2)
					elif tag[1] == 249:
						#print("Found Tag 249, Moving Towards")
						if tag.center[0] < 120:
							self.setSpeeds(+20, 0)
							self.robot.set_forward_speed(0)
						elif tag.center[0] > 210:
							self.setSpeeds(-20, 0) 
						else:
							self.setSpeeds(0, +0.2)
					# self.sub_caml.unregister()
					# self.ignoreCamL = True
			continue 
		return im

	def loop(self):
	
		# state
		self.ignoreCamL = False
		self.ignoreCamR = False  
		self.posClose = False
		self.atKennel = False 
		self.LightSensors = []
		self.SonarRange = 0

		self.tl = 0
		# loop
		while not rospy.core.is_shutdown():
			self.timeC = time.time()

			if (self.timeC - self.tl) > 0.6 and self.atKennel == False:
				self.robot.set_turn_speed(0)
				self.robot.set_forward_speed(0)
				#print("No tag found")
				self.tl = time.time()
				self.ignoreCamL = False
				self.ignoreCamR = False
				# self.sub_caml = rospy.Subscriber("miro/sensors/caml/compressed", CompressedImage, self.callback_caml, queue_size=1, tcp_nodelay=True)
				# self.sub_camr = rospy.Subscriber("miro/sensors/camr/compressed", CompressedImage, self.callback_camr, queue_size=1, tcp_nodelay=True)

			
			# for each camera
			if self.ignoreCamR == False and self.ignoreCamL == False:
				for index in range(1):
					image = self.input_camera[index]
					if not image is None:
						self.input_camera[index] = None
						if not self.april_detector is None:
							image = self.detect_april(image, index)
							
			# elif self.ignoreCamR == True:
				# image = self.input_camera[0]
				# if not image is None:
					# self.input_camera[0] = None
					# if not self.april_detector is None:
						# image = self.detect_april(image, 0)
						  
			# elif self.ignoreCamL == True:
				# image = self.input_camera[1]
				# if not image is None:
					# self.input_camera[1] = None
					# if not self.april_detector is None:
						# image = self.detect_april(image, 1)
			
			# state
			resp = "0000000000000000000000000000000000000000000"
			#self.robot.read_head_touch_sensors()
			if resp[6] and resp[13]:
				ctime = time.time()
				while resp[6] and resp[13]:
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

			#time.sleep(0.2)

	def __init__(self, args):

		# state
		self.input_camera = [None, None]
		self.april_detector = True
		self.rate = 0
		self.kin_joints = JointState()
		self.kin_joints.name = ["tilt", "lift", "yaw", "pitch"]
		self.kin_joints.position = [-0.10471975803375244, 0.9031959176063538, 0.06871610879898071, 0.14394205808639526]
		self.kin_joints.effort = [0,0,0,1]
		# init the robot Kinetic control.
		self.robot = miro.interface.PlatformInterface()
		# handle april

		if "apriltag" not in sys.modules:
			raise ValueError("April Tags library not available")
		options = apriltag.DetectorOptions( \
				families='tag36h11',
				border=0,
				nthreads=128,
				quad_decimate=2.0,
				quad_blur=0.0,
				refine_edges=False,
				refine_decode=False,
				refine_pose=False,
				debug=False,
				quad_contours=True) 
		self.april_detector = apriltag.Detector(options)
		
		# ROS -> OpenCV converter
		self.image_converter = CvBridge()
		# robot name
		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
		# subscribe
		self.sub_caml = rospy.Subscriber(topic_base_name + "/sensors/caml/compressed", CompressedImage, self.callback_caml, queue_size=1, tcp_nodelay=True)
		#self.sub_camr = rospy.Subscriber(topic_base_name + "/sensors/camr/compressed", CompressedImage, self.callback_camr, queue_size=1, tcp_nodelay=True)
		
		self.sub_kin = rospy.Subscriber(topic_base_name + "/sensors/kinematic_joints", JointState, self.callback_kin, queue_size=1, tcp_nodelay=False)
		self.kinematic_joints_pub = rospy.Publisher(topic_base_name + "/control/kinematic_joints", JointState, queue_size=1)

		# report
		#print "recording from 2 cameras, press CTRL+C to halt..."

if __name__ == "__main__":

	rospy.init_node("client_web", anonymous=False)
	main = client(sys.argv[1:])
	main.loop()




