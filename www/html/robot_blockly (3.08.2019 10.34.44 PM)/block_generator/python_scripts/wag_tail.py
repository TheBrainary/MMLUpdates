
#-----------------------------START WAG_TAIL---------------------------------
if dropdown_wag == 'Left':
    cos_joints.data[1] = 0.0
elif dropdown_wag == 'Neutral':
    cos_joints.data[1] = 0.5
else:
    cos_joints.data[1] = 1.0

cosmetic_joints_pub.publish(cos_joints)
time.sleep(0.5)
#-----------------------------END WAG_TAIL---------------------------------
