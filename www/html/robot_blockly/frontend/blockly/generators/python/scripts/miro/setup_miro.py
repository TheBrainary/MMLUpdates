
#-----------------------------START SETUP_MIRO---------------------------------
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import JointState, CompressedImage, Range
from std_msgs.msg import Float32MultiArray
import sys
import rospy
import rospkg
# import cv2
import os
import numpy as np
import time
import math

velocity_pub = rospy.Publisher("/miro/control/cmd_vel", TwistStamped, queue_size=0)
velocity = TwistStamped()

kinematic_joints_pub = rospy.Publisher("/miro/control/kinematic_joints", JointState, queue_size=0)
kin_joints = JointState()
kin_joints.name = ["tilt", "lift", "yaw", "pitch"]
kin_joints.position = [0.0, math.radians(34.0), 0.0, 0.0]

cosmetic_joints_pub = rospy.Publisher("/miro/control/cosmetic_joints", Float32MultiArray, queue_size=0)
cos_joints = Float32MultiArray()
cos_joints.data = [0.0, 0.5, 0.0, 0.0, 0.0, 0.0]

#-----------------------------END SETUP_MIRO---------------------------------
