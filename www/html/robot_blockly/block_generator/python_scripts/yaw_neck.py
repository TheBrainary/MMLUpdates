
#-----------------------------START YAW_NECK---------------------------------
if dropdown_yaw == "Y_RIGHT":
    y_angle_in_degrees = 60.0
elif dropdown_yaw == "Y_LEFT":
    y_angle_in_degrees = -60.0
else:
    y_angle_in_degrees = 0.0
        
kin_joints.position[2] = math.radians(y_angle_in_degrees)
kinematic_joints_pub.publish(kin_joints)
time.sleep(1.5)
#-----------------------------END YAW_NECK---------------------------------
