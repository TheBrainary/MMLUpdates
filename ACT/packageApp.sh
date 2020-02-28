#!/bin/python
import os
import sys
import random

try:
	folderRandom = random.randint(100000,999999)
	home_dir = "/home/miro/ACT/packaged_apps/"
	savedState = False
	while savedState == False:
		if not os.path.exists(home_dir + str(folderRandom)):
			os.makedirs(home_dir + str(folderRandom))
			savedState = True
			
		else:
			folderRandom = random.randint(100000,999999)
except OSError as e:
	if e.errno != errno.EEXIST:
		raise
sys.argv[2:]

