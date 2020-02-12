#!/usr/bin/python2

import rospy
import miro2 as miro
import time
import sys
import os
import numpy as np
import json
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TwistStamped

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
		#print(msg.position[1])
		#print(msg.position[2])
		Liftpos = msg.position[1]
		YawPos = msg.position[2]
		
		miroWalkSpeed = .5 #((Liftpos+0.4)/0.4)/10   #speed vs postion of neck(lift). 
		miroTurnLeftSpeed = (YawPos*100)   #speed vs postion of neck left angel(yaw).
		miroTurnRightSpeed = (YawPos*140)   #speed vs postion of neck right angel(yaw).

		
		print(YawPos)

		if Liftpos < 0.5:
			self.robot.set_forward_speed(0)
			if YawPos < -0.9:
				self.robot.set_turn_speed(miroTurnRightSpeed)
			elif YawPos > 0.9:
				self.robot.set_turn_speed(miroTurnLeftSpeed)
			else:
				self.robot.set_turn_speed(0)
		elif (YawPos < 0 and Liftpos > 0.4):
			self.robot.set_forward_speed(miroWalkSpeed)
			self.robot.set_turn_speed(miroTurnRightSpeed)
		elif (YawPos > 0 and Liftpos > 0.4):
			self.robot.set_forward_speed(miroWalkSpeed)
			self.robot.set_turn_speed(miroTurnLeftSpeed)
		else:
			self.robot.set_forward_speed(miroWalkSpeed)
		
		

			
	
	def loop(self):
		# loop
		while not rospy.core.is_shutdown():
			# state
			time.sleep(0.02)

	def __init__(self):

		# state
		self.wait = False
		self.robot = miro.interface.PlatformInterface()
		# robot name
		topic_base = "/" + os.getenv("MIRO_ROBOT_NAME") + "/"


		# publish
		topic = topic_base + "/control/cmd_vel"
		self.pub_cmd_vel = rospy.Publisher(topic, TwistStamped, queue_size=0)

		# subscribe
		topic = topic_base + "sensors/kinematic_joints"
		print ("subscribe", topic)
		self.sub_log = rospy.Subscriber(topic, JointState, self.callback_sensors)



if __name__ == "__main__":

	rospy.init_node("walk_miro", anonymous=False)
	main = client()
	main.loop()





