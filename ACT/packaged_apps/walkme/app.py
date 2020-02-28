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
		
		miroWalkSpeed = .4 #((Liftpos+0.4)/0.4)/10   #speed vs postion of neck(lift). 
		miroTurnLeftSpeed = (YawPos*200)   #speed vs postion of neck left angel(yaw).
		miroTurnRightSpeed = (YawPos*240)   #speed vs postion of neck right angel(yaw).
		
		#print(YawPos)

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
		
		resp = self.robot.read_head_touch_sensors()
		if resp[6] and resp[13]:
			ctime = time.time()
			while resp[4] and resp[11]:
				resp = self.robot.read_head_touch_sensors()
				if time.time() - ctime >= 2:
					print("Shutting Down Application")
					os.system("rosnode kill mml_play")
					for j in range(6):
						self.robot.control_led(j,"#ffffff" ,255)
					os.remove("/tmp/running.state")
					os.system("rosnode kill client_web")
					
					sys.exit()
			
	
	def loop(self):
		# loop
		while not rospy.core.is_shutdown():
			# state

		
			time.sleep(0.02)

	def __init__(self):

		self.robot = miro.interface.PlatformInterface()
		# state
		self.wait = False
		
		# self.robot name
		topic_base = "/" + os.getenv("MIRO_ROBOT_NAME") + "/"


		# publish
		topic = topic_base + "control/cmd_vel"
		self.pub_cmd_vel = rospy.Publisher(topic, TwistStamped, queue_size=0)

		# subscribe
		topic = topic_base + "sensors/kinematic_joints"
		print ("subscribe", topic)
		self.sub_log = rospy.Subscriber(topic, JointState, self.callback_sensors)



if __name__ == "__main__":

	rospy.init_node("client_web", anonymous=False)
	main = client()
	main.loop()





