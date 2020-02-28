
#-----------------------------START PITCH_NECK---------------------------------
if dropdown_pitch == "P_UP":
    p_angle_in_degrees = -15.0
elif dropdown_pitch == "P_DOWN":
    p_angle_in_degrees = 8.0
else:
    p_angle_in_degrees = 0.0
        
kin_joints.position[3] = math.radians(p_angle_in_degrees)
kinematic_joints_pub.publish(kin_joints)
time.sleep(1.5)
#-----------------------------END PITCH_NECK---------------------------------
