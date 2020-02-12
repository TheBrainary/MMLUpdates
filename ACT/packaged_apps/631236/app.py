#!/usr/bin/python -u
import rospy
rospy.init_node('client_web')
 # imports
import time
import miro2 as miro

# definitions


# setup
robot = miro.interface.PlatformInterface()
time.sleep(1.0)

# control
robot.set_turn_speed(+60)
robot.sleep(10)
# exit
robot.exit()
