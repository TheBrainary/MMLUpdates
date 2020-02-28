
#-----------------------------START MOVE_EARS---------------------------------
if dropdown_ears == 'Forward':
    cos_joints.data[4] = 1.0
    cos_joints.data[5] = 1.0
elif dropdown_ears == 'Neutral':
    cos_joints.data[4] = 0.5
    cos_joints.data[5] = 0.5
else:
    cos_joints.data[4] = 0
    cos_joints.data[5] = 0

cosmetic_joints_pub.publish(cos_joints)
time.sleep(1.5)
#-----------------------------END MOVE_EARS---------------------------------
