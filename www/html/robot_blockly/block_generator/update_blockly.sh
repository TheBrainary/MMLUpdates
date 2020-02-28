#!/usr/bin/env bash

if [ $1 = "generate" ]
then
	if [ $2 = "compressed" ]
	then
		cd ~/lib/mei/blockly_ws/src/robot_blockly/block_generator && python generate_blocks.py compressed
		cd ~/lib/mei/blockly_ws/src/robot_blockly/frontend/blockly/ && python build.py compressed
	else
		cd ~/lib/mei/blockly_ws/src/robot_blockly/block_generator && python generate_blocks.py uncompressed
		cd ~/lib/mei/blockly_ws/src/robot_blockly/frontend/blockly/ && python build.py uncompressed
	fi
fi

cd ~/lib/mei/blockly_ws
catkin_make_isolated -j4 --pkg robot_blockly --install

source ~/lib/mei/blockly_ws/install_isolated/setup.bash
export PYTHONPATH=/usr/local/lib/python3.5/dist-packages/cv2:$MIRO_PATH_MDK/share:$PYTHONPATH
#export ROS_IP=192.168.1.3
#roslaunch robot_blockly robot_blockly.launch
