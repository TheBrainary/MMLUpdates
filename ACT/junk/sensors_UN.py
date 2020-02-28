#!/usr/bin/python

import rospy
import miro2 as miro
import time
import sys
import os
import numpy as np
import json


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
		data.append({
                'Cliff':{
                'left': msg.cliff.data[0],
                'right': msg.cliff.data[1]}
            })
		data.append({
                'touch':{
                'head': msg.touch_head.data,
                'body': msg.touch_body.data}
            })
		data.append({
                'sonar':{'range': msg.sonar.range}
            })
		data.append({
                'battery':{'voltage': msg.battery.voltage}
            })
		data.append({
                'light':{
					'front':{
						'left': msg.light.data[0],
						'right': msg.light.data[1]
						},
					'back':{
						'left': msg.light.data[2],
						'right': msg.light.data[3]
						},
					}
				})
		with open('/tmp/sensors.txt', 'wb') as fh:
			fh.write(json.dumps(data))
			fh.close()

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
		topic = topic_base + "sensors/package"
		print ("subscribe", topic)
		self.sub_log = rospy.Subscriber(topic, miro.msg.sensors_package, self.callback_sensors)

if __name__ == "__main__":

	rospy.init_node("client_show_cliff", anonymous=False)
	main = client()
	main.loop()





