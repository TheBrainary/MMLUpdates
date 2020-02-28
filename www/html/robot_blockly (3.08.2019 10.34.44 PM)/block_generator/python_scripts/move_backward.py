
#-----------------------------START MOVE_BACKWARD---------------------------------
velocity.twist.angular.z = 0
velocity.twist.linear.x = -0.5

velocity_pub.publish(velocity)
velocity.twist.linear.x = 0
time.sleep(1.5)
velocity_pub.publish(velocity)
#-----------------------------END MOVE_BACKWARD---------------------------------
