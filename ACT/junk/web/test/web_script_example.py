#!/usr/bin/python
#
#import rospy
#
# init node
#rospy.init_node("client_web", anonymous=True)

import os
import time
import numpy as np
import sensor_msgs.msg

# robot name
topic_base = "/" + os.getenv("MIRO_ROBOT_NAME") + "/"

# publish
topic = topic_base + "control/kinematic_joints"
print ("publish", topic)
pub_kin = rospy.Publisher(topic, sensor_msgs.msg.JointState, queue_size=0)

# prepare message
msg_kin = sensor_msgs.msg.JointState()
msg_kin.position = [0.0, np.radians(30.0), 0.0, 0.0]

# state
yaw = 0.0
dyaw = 5.0

# loop
while not rospy.core.is_shutdown():

	# count
	yaw = yaw + dyaw
	
	# reverse
	if np.abs(yaw) >= 30.0:
		dyaw = -dyaw

	# publish
	msg_kin.position[2] = np.radians(yaw)
	pub_kin.publish(msg_kin)

	# pause
	time.sleep(0.05)

