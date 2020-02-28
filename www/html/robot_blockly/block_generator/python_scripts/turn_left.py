
#-----------------------------START TURN_LEFT---------------------------------
velocity.twist.angular.z = +0.785398

velocity_pub.publish(velocity)
velocity.twist.angular.z = 0
time.sleep(2)
velocity_pub.publish(velocity)
#-----------------------------END TURN_LEFT---------------------------------
