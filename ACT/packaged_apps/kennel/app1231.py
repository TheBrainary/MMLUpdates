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

		except CvBridgeError as e:

			# swallow error, silently
			#print(e)
			pass

	def callback_caml(self, ros_image):

		self.callback_cam(ros_image, 0)

	def callback_camr(self, ros_image):
		self.callback_cam(ros_image, 1)
		
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
							self.robot.set_turn_speed(+110)
							self.robot.set_forward_speed(0)
							#print("Left Camera - Turning left " + str(tag.center[0]))
						elif tag.center[0] > 475:
							self.robot.set_turn_speed(-110)
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
			if self.timeC - self.tl > 1.5:
				self.robot.set_turn_speed(+110)
				self.robot.set_forward_speed(+0.1)
				print("No tag found")
				self.tl = time.time()
				self.ignoreCamL = False
				self.ignoreCamR = False
				self.robot.set_neck(miro.constants.JOINT_PITCH, 0)
				self.robot.set_neck(miro.constants.JOINT_LIFT, 20)
				
			# for each camera
			for index in range(2):
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
			resp = self.robot.read_head_touch_sensors()
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
		
		# init the robot Kinetic control.
		self.robot = miro.interface.PlatformInterface()
		# handle april

		if "apriltag" not in sys.modules:
			raise ValueError("April Tags library not available")
		options = apriltag.DetectorOptions( \
				families='tag16h5',
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
		self.sub_caml = rospy.Subscriber(topic_base_name + "/sensors/caml/compressed",
					CompressedImage, self.callback_caml, queue_size=1, tcp_nodelay=True)
		self.sub_camr = rospy.Subscriber(topic_base_name + "/sensors/camr/compressed",
					CompressedImage, self.callback_camr, queue_size=1, tcp_nodelay=True)
		
		# report
		print "recording from 2 cameras, press CTRL+C to halt..."

if __name__ == "__main__":

	rospy.init_node("client_web", anonymous=False)
	main = client(sys.argv[1:])
	main.loop()




