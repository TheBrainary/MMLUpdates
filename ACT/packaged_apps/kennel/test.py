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
		
	def	callback_lightsense(self, msg):
		self.LightSensors = msg.light.data
		self.SonarRange = msg.sonar.range
		
	def detect_april(self, im, index):
		im_grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # get grey frame
		self.detected_tags = self.april_detector.detect(im_grey)# get all detected tags
		# for each
		for tag in self.detected_tags:
			# accept only exact match
			#print("Tag Detected: " + str(tag))
			if tag.hamming < 2 and (tag[1] == 65 or tag[1] == 249):
				print("Tag Detected, ID: " + str(tag[1]) + ", Center: " + str(int(tag.center[0])) + ", " + str(int(tag.center[1])) + ", Camera: " + str(index))
				self.tl = time.time()
				if self.atKennel == True and index == 0:
					self.robot.set_forward_speed(0)
					if tag[1] == 249:
						if tag.center[0] < 425:
							self.robot.set_turn_speed(+30)
							self.robot.set_forward_speed(0)
						elif tag.center[0] > 475:
							self.robot.set_turn_speed(-30)
							self.robot.set_forward_speed(0)
						else:
							while self.SonarRange < .35:
								self.robot.set_turn_speed(-30)
								print("facing out of kennel")
							self.robot.set_turn_speed(0)
							#self.atKennel == True
							print(self.SonarRange)
					#self.robot.set_turn_speed(0)
								
				if index == 0 and self.ignoreCamL == False:
					if tag[1] == 65:
						if tag.center[0] < 400:
							self.robot.set_turn_speed(+20)
							self.robot.set_forward_speed(0)
							#print("Left Camera - Turning left " + str(tag.center[0]))
						elif tag.center[0] > 500:
							self.robot.set_turn_speed(-20)
							#print("Left Camera - Turning right " + str(tag.center[0]))
							self.robot.set_forward_speed(0)
						else:
							self.robot.set_turn_speed(0)
							self.robot.set_forward_speed(+0.2) 
							if tag.center[1] < 120:
								#self.robot.set_neck(miro.constants.JOINT_PITCH, 7)
								#self.robot.set_neck(miro.constants.JOINT_LIFT, 5)
								#self.robot.set_neck(miro.constants.JOINT_YAW, 0)
								self.atKennel == True
								print("Set AtKennel to true")
									
							
						self.ignoreCamR = True
					
				if index == 1 and self.ignoreCamR == False:
					if tag[1] == 65:
						if tag.center[0] < 140:
							self.robot.set_turn_speed(+30)
							self.robot.set_forward_speed(0)
						elif tag.center[0] > 190:
							self.robot.set_turn_speed(-30)
							self.robot.set_forward_speed(0)
						else:
							self.robot.set_turn_speed(0)
							self.robot.set_forward_speed(+0.2)
							
							#if tag.center[1] < 120:
							#	self.robot.set_neck(miro.constants.JOINT_PITCH, 7)
							#	self.robot.set_neck(miro.constants.JOINT_LIFT, 5)
							#	self.robot.set_neck(miro.constants.JOINT_YAW, 0)
						self.ignoreCamL = True
						#self.robot.sleep(100)
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
			
			#self.robot.set_neck(miro.constants.JOINT_PITCH, 7)
			#self.robot.set_neck(miro.constants.JOINT_LIFT, 5)
			#self.robot.set_neck(miro.constants.JOINT_YAW, 0)
			if self.timeC - self.tl > 0.5:
				self.kinematic_joints_pub.publish(self.kin_joints)
				self.robot.set_turn_speed(0)
				self.robot.set_forward_speed(0)
				print("No tag found")
				self.tl = time.time()
				self.ignoreCamL = False
				self.ignoreCamR = False
				#self.robot.set_neck(miro.constants.JOINT_PITCH, 7)
				#self.robot.set_neck(miro.constants.JOINT_LIFT, 5)
				#self.robot.set_neck(miro.constants.JOINT_YAW, 0)
				
			# for each camera
			for index in range(1):
				# get image
				image = self.input_camera[index]
				# if present
				if not image is None:
					# handle
					self.input_camera[index] = None
					
					# april tags
					if not self.april_detector is None:
						image = self.detect_april(image, index)
			# state
			resp = "111111111111111111111111111111111111111111"
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

			time.sleep(0.2)

	def __init__(self, args):

		# state
		self.input_camera = [None, None]
		self.april_detector = True
		
		self.kin_joints = JointState()
		self.kin_joints.name = ["tilt", "lift", "yaw", "pitch"]
		self.kin_joints.position = [0.0, math.radians(5), math.radians(1), math.radians(7)]
		# init the robot Kinetic control.
		self.robot = miro.interface.PlatformInterface()
		# handle april

		if "apriltag" not in sys.modules:
			raise ValueError("April Tags library not available")
		options = apriltag.DetectorOptions( \
				families='tag36h11',
				border=1,
				nthreads=4,
				quad_decimate=1.0,
				quad_blur=0.0,
				refine_edges=True,
				refine_decode=False,
				refine_pose=False,
				debug=True,
				quad_contours=True)
		self.april_detector = apriltag.Detector(options)
		
		# ROS -> OpenCV converter
		self.image_converter = CvBridge()
		# robot name
		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
		# subscribe
		self.sub_caml = rospy.Subscriber(topic_base_name + "/sensors/caml/compressed", CompressedImage, self.callback_caml, queue_size=1, tcp_nodelay=True)
		self.sub_camr = rospy.Subscriber(topic_base_name + "/sensors/camr/compressed", CompressedImage, self.callback_camr, queue_size=1, tcp_nodelay=True)
		self.sub_lightsens = rospy.Subscriber(topic_base_name + "/sensors/package", miro.msg.sensors_package, self.callback_lightsense, queue_size=1, tcp_nodelay=True)
		self.kinematic_joints_pub = rospy.Publisher(topic_base_name + "/control/kinematic_joints", JointState, queue_size=0)
		
		# report
		print "recording from 2 cameras, press CTRL+C to halt..."

if __name__ == "__main__":

	rospy.init_node("client_web", anonymous=False)
	main = client(sys.argv[1:])
	main.loop()




