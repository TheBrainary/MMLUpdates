#!/usr/bin/python

# Walking Miro along side user on a leash; 
# Miro will move forward at a constant speed until leash is 'pulled up' lifting miro's head at such time miro with be still until the leash is relaxed.


#### NOTE FOR TERMS USED ######

# In order to move Miro's head upwards(neck) to is controlled by the location of 'LIFT' joint in BODY, 
# this is not tobe confused with 'YAW' and 'PITCH' that controls the movement of the neck. 


import numpy as np
import miro2 as miro

# create kc object with default (calibration) configuration
# of joints (and zeroed pose of FOOT in WORLD)
kc = miro.utils.kc_interf.kc_miro()

c = miro.constants

#robot = miro.interface.PlateformInterface()

# create objects in NECK
pos = np.array([c.LOC_LIFT_X, c.LOC_LIFT_Y, c.LOC_LIFT_Z])
vec = np.array([1.0, 0.0, 0.0])

# transform to WORLD (note use of "Abs" and "Rel"
# for positions and directions, respectively)
posw = kc.changeFrameAbs(c.LINK_NECK, c.LINK_WORLD, pos)
vecw = kc.changeFrameRel(c.LINK_NECK, c.LINK_WORLD, vec)

# this is a report of miro's current neck postion
print pos, vec

#kinematic_joints = np.array([c.LIFT_RAD_CALIB, np.radians(30.0), np.radians(15.0), np.radians(0.0)])
#kc.isActive(kinematic_joints)
#	if kinematic_joints > 
 #update configuration based on data (imagine this came
# from /miro/sensors/kinematic_joints)
#
# NB: the immobile joint "TILT" is always at the same
# angle, "TILT_RAD_CALIB"
kinematic_joints = c.LINK_NECK
kc.isActive(kinematic_joints)

# transform to WORLD
posw = kc.changeFrameAbs(miro.constants.LINK_NECK, miro.constants.LINK_WORLD, pos)
vecw = kc.changeFrameRel(miro.constants.LINK_NECK, miro.constants.LINK_WORLD, vec)


# report 
print posw, vecw

#
