
#-----------------------------START GET_DISTANCE---------------------------------
msg_distance = rospy.wait_for_message("/miro/sensors/sonar", Range, timeout=1)

#-----------------------------END GET_DISTANCE---------------------------------
