
#-----------------------------START DROOP_TAIL---------------------------------
if dropdown_droop == 'Down':
    cos_joints.data[0] = 1.0
else:
    cos_joints.data[0] = 0.0

cosmetic_joints_pub.publish(cos_joints)
time.sleep(0.5)
#-----------------------------END DROOP_TAIL---------------------------------
