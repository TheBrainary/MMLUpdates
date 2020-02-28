#!/usr/bin/python

import rospy
import miro2 as miro
import time
import sys
import os
import numpy as np
import json
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TwistStamped

ret_data = []
################################################################

def error(msg):

	print(msg)
	sys.exit(0)

def fmt(msg):

	x = msg.data
	s = "{0:.3f} {1:.3f}".format(x[0], x[1])
	return s

################################################################

class client:

	def callback_sensors(self, msg):
		data = {}
		data = []
		print(msg.position[1])

	def control_movement(self, msg):
		data = {}
		data = []
		print(msg.velocity[1])
	
	def loop(self):
		# loop

		if callback_sensors.position =< 0.15
			set_forward_speed(0):
		else
			set_forward_speed(+0.4):
			
		while not rospy.core.is_shutdown():
			# state
			time.sleep(3)

	def __init__(self):

		self.velocity = TwistStamped()

		self.kin_joints = JointState()
		self.kin_joints.name = ["tilt", "lift", "yaw", "pitch"]
		self.kin_joints.position = [0.0, miro.constants.LIFT_RAD_CALIB, 0.0, 0.0]

		# state
		self.wait = False
		# robot name
		topic_base = "/" + os.getenv("MIRO_ROBOT_NAME") + "/"


		# publish
		topic = topic_base + "control/cmd_vel"
		print ("publish", topic)
		self.velocity_pub = rospy.Publisher(topic, TwistStamped, self.control_movement)


		# subscribe
		topic = topic_base + "sensors/kinematic_joints"
		print ("subscribe", topic)
		self.sub_log = rospy.Subscriber(topic, JointState, self.callback_sensors)

	def set_forward_speed(self, x):
		self.pause()
		x = np.clip(x, -miro.constants.WHEEL_MAX_SPEED_M_PER_S, miro.constants.WHEEL_MAX_SPEED_M_PER_S)
		self.velocity.twist.linear.x = x

if __name__ == "__main__":

	rospy.init_node("client_show_cliff", anonymous=True)
	main = client()
	main.loop()





