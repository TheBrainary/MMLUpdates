#!/usr/bin/python -u

import rospy
import sys
# initialise ROS node
rospy.init_node("ColorSetter")

################################################################

# imports
import time
import miro2 as miro

# definitions


# setup
constants = [miro.constants.ILLUM_LF,miro.constants.ILLUM_LM,miro.constants.ILLUM_LR,miro.constants.ILLUM_RF,miro.constants.ILLUM_RM,miro.constants.ILLUM_RR]
robot = miro.interface.PlatformInterface()
time.sleep(1.0)

color = sys.argv[1]
PositionArray = sys.argv[2].replace(']','').replace('[','')
position = PositionArray.replace('"','').split(",")

for x in position:
	print(x)
	robot.control_led(constants[int(x)], color, 255)
	#self.control_led(int(x),color,255) #LM 
robot.sleep(1)
# control
# exit
robot.exit()
