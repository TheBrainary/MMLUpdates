# Blockly

This ROS package is based on `robot_blockly` (https://github.com/erlerobot/robot_blockly). It provides a visual tool to program Miro (https://consequential.bitbucket.io/). The aim of this package is to provide a simple interface to interact with Miro without prior knowledge of ROS.

## Installation

1. Make sure you have installed ROS and Miro's development kit by following this tutorial: https://consequential.bitbucket.io/Developer_Preparation_Prepare_workstation.html

2. Install `robot_blockly`:
```
mkdir -p ~/blockly_ws/src
cd ~/blockly_ws/src
git clone --recurse-submodules https://github.com/MIRO-Robot/robot_blockly.git
cd ..
catkin_make_isolated -j2 --pkg robot_blockly --install
```
3. Install Python dependencies:
```
sudo pip3 install rospkg
sudo pip3 install catkin_pkg
sudo pip3 install autobahn
```

4. Install `mavros` by following this link: https://github.com/mavlink/mavros

5. Build blockly custom blocks:
```
cd ~/blockly_ws/install_isolated/share/robot_blockly/frontend/blockly/
python build.py
```

## Launch it

```
source ~/blockly_ws/install_isolated/setup.bash
roslaunch robot_blockly robot_blockly.launch
```

## Usage

In order to access the blockly interface after launching it, navigate to: http://localhost:1036/pages/blockly.html#

## Adding Custom blocks
To create your own blocks, follow this link: http://docs.erlerobotics.com/robot_operating_system/ros/blockly/block_creation
