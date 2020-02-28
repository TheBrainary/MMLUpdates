
#-----------------------------START LIFT_NECK---------------------------------
if dropdown_lift == "L_UP":
    l_angle_in_degrees = 5.0
elif dropdown_lift == "L_DOWN":
    l_angle_in_degrees = 60.0
else:
    l_angle_in_degrees = 34.0
        
kin_joints.position[1] = math.radians(l_angle_in_degrees)
kinematic_joints_pub.publish(kin_joints)
time.sleep(1.5)
#-----------------------------END LIFT_NECK---------------------------------
