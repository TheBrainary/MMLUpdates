/**
 * @license
 *
 * Copyright 2018 Cyberselves
 * http://cyberselves.org
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


/**
 * @fileoverview Blocks for Miro.
 * @author Daniel Camilleri, Natalie Wood
*/

'use strict';

goog.provide('Blockly.Blocks.miro');
goog.require('Blockly.Blocks');

/**
 * Common HSV hue for all blocks in this category.
 */
// Blockly.Blocks.miro.HUE = 260;

////////////////////// SETUP ////////////////////////////

Blockly.Blocks['setup_miro'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Program Start")
    this.setNextStatement(true, null);
    this.setColour("#70A27E");
 this.setTooltip("Every program you make should start with this block.\
 It sets up your Python script and ensures that your program finishes correctly.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['miro_say'] = {
  init: function() {
    this.appendValueInput("say_text")

        .appendField("Say");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("Miro Will say what is in this box");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['miro_play'] = {
  init: function() {
	 var str = window.location.origin;
    var res = str.split("/");
    var ipInput = res[res.length - 1];
	var SoundFiles = []
	
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open("GET", 'http://' + ipInput + ':1337' + '/api/list_sounds', false); // false for synchronous request
	xmlHttp.send(null);
	var jsonResponse = JSON.parse(xmlHttp.responseText);
		var i;
		for (i = 0; i < jsonResponse.length; i++) { 
			SoundFiles.push([jsonResponse[i].name, jsonResponse[i].path]);
		}
    this.appendDummyInput() 
        .appendField("Play Audio")
        .appendField(new Blockly.FieldDropdown(SoundFiles), "play_path");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['miro_control_loop'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Periodic Control Loop");
    this.appendStatementInput("control loop")
        .setCheck(null)
        .appendField("do");
    this.setPreviousStatement(true, null);
    this.setColour("#70A27E");
 this.setTooltip("Use this block as your outer loop if you want to build a 'periodic' controller.\
The code inside this block will be run ten times a second.");
 this.setHelpUrl("");
  }
};

// Blockly.Blocks['send_commands'] = {
//   init: function() {
//     this.appendDummyInput()
//         .appendField("Send Commands");
//     this.setPreviousStatement(true, null);
//     this.setNextStatement(true, null);
//     this.setColour("#70A27E");
//  this.setTooltip("Use this block to send commands to the robot");
//  this.setHelpUrl("");
//   }
// };

///////////////////// SIMPLE MOTION /////////////////////////////

Blockly.Blocks['lift_head'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Raise/Lower Head")
        .appendField(new Blockly.FieldDropdown([["Raise","5"], ["Middle","34"], ["Lower","60"]]), "lift_head_ang")
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This block raises or lowers MiRo's head.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['lift_chin'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Look Up/Down")
        .appendField(new Blockly.FieldDropdown([["Up","-15"], ["Middle","0"], ["Down","7"]]), "lift_chin_ang")
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This block tilts MiRo's head up or down (for example, to create a nodding motion).");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['look'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Look Left/Right")
        .appendField(new Blockly.FieldDropdown([["Left","60"], ["Forwards","0"], ["Right","-60"]]), "look_ang")
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This block turns MiRo's head left or right.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['move'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Start Moving")
        .appendField(new Blockly.FieldDropdown([["Forwards","+"], ["Backwards","-"]]), "move_dir")
        .appendField(new Blockly.FieldDropdown([["Slow","0.1"], ["Fast","0.25"], ["Fastest", "0.4"]]), "move_vel")
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This block starts MiRo moving forwards or backwards.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['stop_moving'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Stop Moving")
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This block stops MiRo moving forwards or backwards.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['turn'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Start Turning")
        .appendField(new Blockly.FieldDropdown([["Left","+"], ["Right","-"]]), "turn_dir")
        .appendField(new Blockly.FieldDropdown([["Slow","10"], ["Fast","60"], ["Fastest", "150"]]), "turn_vel")
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This block makes MiRo turn its body left or right.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['stop_turning'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Stop Turning")
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This block stops MiRo turning its body.");
 this.setHelpUrl("");
  }
};

// Blockly.Blocks['move_robot_to'] = {
//   init: function() {
//     this.appendValueInput("point")
//         .setCheck("point")
//         .appendField("Move Robot to ");
//     this.setPreviousStatement(true, null);
//     this.setNextStatement(true, null);
//     this.setColour(230);
//  this.setTooltip("");
//  this.setHelpUrl("");
//   }
// };

////////////////////// COMPLEX MOTION ////////////////////////////

Blockly.Blocks['change_lift_angle'] = {
  init: function()
  {
    this.appendDummyInput()
        .appendField("Move Neck Lift To");
    this.appendValueInput("angle_deg")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("degrees");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
    this.setTooltip("This block adjusts MiRo's neck lift to any angle (from 5 to 60 degrees - the default is 35 degrees).");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['change_pitch_angle'] = {
  init: function()
  {
    this.appendDummyInput()
        .appendField("Move Neck Pitch To");
    this.appendValueInput("angle_deg")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("degrees");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
    this.setTooltip("This block adjusts MiRo's neck pitch (nodding) to any angle (from 8 to -22 degrees - the default is 0 degrees).");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['change_yaw_angle'] = {
  init: function()
  {
    this.appendDummyInput()
        .appendField("Move Neck Yaw To");
    this.appendValueInput("angle_deg")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("degrees");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
    this.setTooltip("This block adjusts MiRo's neck yaw (head turning) to any angle (from -60 to 60 degrees - negative values turn the head to the right).");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['set_forward_speed'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Set Forward Speed to");
    this.appendValueInput("x_vel")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("meters per second");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This block starts MiRo moving at the specified speed (negative speeds will move MiRo backwards, and the maximum values are -0.4 m/s and 0.4 m/s).");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['set_turn_speed'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Set Turn Speed to");
    this.appendValueInput("z_ang_vel")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("degrees per second");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This block starts MiRo's body turning at the specified speed (from -280 to 280 degrees/sec - negative values turn MiRo's body to the right).");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['move_ears'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Move")
        .appendField(new Blockly.FieldDropdown([["Left","JOINT_EAR_L"], ["Right","JOINT_EAR_R"], ["Both","JOINT_EARS"]]), "ear")
        .appendField("Ear(s) to face ")
        .appendField(new Blockly.FieldDropdown([["Forwards","0.0"], ["Outwards","1.0"]]), "dir");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This moves the selected ear(s) to the desired position.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['move_eyelids'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Move")
        .appendField(new Blockly.FieldDropdown([["Left","JOINT_EYE_L"], ["Right","JOINT_EYE_R"], ["Both","JOINT_EYES"]]), "eye")
        .appendField("Eyelid(s) to")
        .appendField(new Blockly.FieldDropdown([["Open","0.0"], ["Closed","1.0"]]), "dir");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This moves the selected eyelid(s) to the desired position.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['point_tail'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Point Tail")
        .appendField(new Blockly.FieldDropdown([["Left","0.0"], ["Straight","0.5"], ["Right","1.0"]]), "point");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This moves MiRo's tail to the desired position.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['droop_tail'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Droop Tail")
        .appendField(new Blockly.FieldDropdown([["Up","0.0"], ["Down","1.0"]]), "droop");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This lifts MiRo's tail to the desired position.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['wag_tail'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Wag Tail")
        .appendField(new Blockly.FieldDropdown([["Slow","30"], ["Fast","18"], ["Fastest","7"]]), "wag_rate")
        .appendField("for");
    this.appendValueInput("wag_dur")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("Seconds");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#4AB9AF");
 this.setTooltip("This will move MiRo's tail from side to side (in a wagging motion) at the desired speed for the specified duration of time.");
 this.setHelpUrl("");
  }
};

///////////////////// SENSORS ////////////////////////////////////

Blockly.Blocks['read_light_sensor'] = {
    init: function()
    {
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Front Left", "LIGHT_LF"], ["Front Right", "LIGHT_RF"], ["Back Left", "LIGHT_LR"], ["Back Right", "LIGHT_RR"]]), "Sensor_Pos")
            .appendField("Light Sensor");
        this.setOutput(true, "Number");
        this.setColour("#9A4E62");
        this.setTooltip("This block returns the value of the selected light sensor as a value between 0.0 (dark) and 1.0 (bright).");
        this.setHelpUrl("");
  }
};

Blockly.Blocks['read_all_light_sensors'] = {
    init: function()
    {
        this.appendDummyInput()
            .appendField("All Light Sensors")
        this.setOutput(true, "Array");
        this.setColour("#9A4E62");
        this.setTooltip("This block returns a list of all the light sensor values.");
        this.setHelpUrl("");
  }
};

Blockly.Blocks['read_sonar_range'] = {
    init: function()
    {
        this.appendDummyInput()
            .appendField("Sonar Range")
        this.setOutput(true, "Number");
        this.setColour("#9A4E62");
        this.setTooltip("This block returns the distance in metres between MiRo's nose and the object/obstacle in front of it - a value of 0.0 means that no obstacle was detected. Detected obstacles will lie in the range 0.03 to 1.00 metres.");
        this.setHelpUrl("");
  }
};

Blockly.Blocks['read_cliff_sensor'] = {
    init: function()
    {
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Left", "CLIFF_L"], ["Right", "CLIFF_R"]]), "Cliff_Pos")
            .appendField("Cliff Sensor");
        this.setOutput(true, "Boolean");
        this.setColour("#9A4E62");
        this.setTooltip("This block returns true or false (boolean) where true means a 'cliff' is detected.");
        this.setHelpUrl("");
  }
};

Blockly.Blocks['read_both_cliff_sensors'] = {
    init: function()
    {
        this.appendDummyInput()
            .appendField("Both Cliff Sensors")
        this.setOutput(true, "Array");
        this.setColour("#9A4E62");
        this.setTooltip("This returns a list containing the raw cliff sensor values as [left, right]. Each value is between 0.0 and 1.0 and indicates the confidence that a surface is present - 1.0 means there is certainly a surface, and 0.0 means that there is certainly a cliff.");
        this.setHelpUrl("");
  }
};

Blockly.Blocks['read_body_touch_sensors'] = {
    init: function()
    {
        this.appendDummyInput()
            .appendField("Body Touch sensors")
        this.setOutput(true, "Array");
        this.setColour("#9A4E62");
        this.setTooltip("This block returns the state of the body touch sensors.");
        this.setHelpUrl("");
  }
};

Blockly.Blocks['read_head_touch_sensors'] = {
    init: function()
    {
        this.appendDummyInput()
            .appendField("Head Touch Sensors")
        this.setOutput(true, "Array");
        this.setColour("#9A4E62");
        this.setTooltip("This block returns the state of the head touch sensors.");
        this.setHelpUrl("");
  }
};

Blockly.Blocks['clap_in_previous'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("clap detected in previous");
    this.appendValueInput("time_secs")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("seconds");
    this.setInputsInline(true);
    this.setOutput(true, "Boolean");
    this.setColour("#9A4E62");
 this.setTooltip("This block returns true or false depending on whether a clap was detected in the specified time period.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['time_since_clap'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("seconds since clap");
    this.setInputsInline(true);
    this.setOutput(true, "Number");
    this.setColour("#9A4E62");
 this.setTooltip("This block returns the amount of time in seconds since a clap was detected.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['wait_for_clap'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Wait for clap");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#9A4E62");
 this.setTooltip("This is a blocking function, this prevents the code from continuing until a clap is detected.");
 this.setHelpUrl("");
  }
};

///////////////////////// ACTIONS ////////////////////////////////

Blockly.Blocks['find_ball'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Find")
        .appendField(new Blockly.FieldDropdown([["x-coordinate","0"], ["y-coordinate","1"], ["size","2"], ["[x, y, size]", "3"]]), "ball_property")
        .appendField("of")
        .appendField(new Blockly.FieldColour("#ff0000"), "ball_colour")
        .appendField("ball in")
        .appendField(new Blockly.FieldDropdown([["Left","CAM_L"], ["Right","CAM_R"]]), "cam_id")
        .appendField("camera image");
    this.setOutput(true, null);
    this.setColour("#9A4E62");
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['play_tone'] = {
  init: function() {
    this.appendValueInput("FREQ")
        .setCheck("Number")
        .appendField("Play tone of ");
    this.appendValueInput("DUR")
        .setCheck("Number")
        .appendField("Hz for");
    this.appendValueInput("VOL")
        .setCheck("Number")
        .appendField("seconds at volume");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("This block will play a tone at the specified frequency (200Hz - 2000Hz), volume (0 - 255) and duration in seconds.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['change_led'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Change")
        .appendField(new Blockly.FieldDropdown([["Front","F"], ["Middle","M"], ["Back","R"], ["All","ALL"]]), "POS")
        .appendField("LED on ")
        .appendField(new Blockly.FieldDropdown([["Left","ILLUM_L"], ["Right","ILLUM_R"], ["Both","BOTH"]]), "SIDE")
        .appendField("side to")
        .appendField(new Blockly.FieldDropdown([["Bright","255"], ["Mid","122"], ["Dim","30"], ["Off","0"]]), "BRIGHT")
        .appendField(new Blockly.FieldColour("#ff0000"), "LED_COL");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("This will set the colour and brightness of the specified LED(s).");
 this.setHelpUrl("");
  }
};
///////////////////////// ROBOT ONLY ////////////////////////////////


///////////// FUNCTIONS FOR USING PROTRACTORS FOR KIN ///////////////////////////
// function constrain_lift_angle(user_angle)
//   {
//     var constrained_angle = Math.min(60, Math.max(5, user_angle));
//     return constrained_angle;
//   }
//
// function constrain_pitch_angle(user_angle)
//   {
//     var constrained_angle = Math.min(8, Math.max(-15, user_angle));
//     return constrained_angle;
//   }
//
// function constrain_yaw_angle(user_angle)
//   {
//     var constrained_angle = Math.min(60, Math.max(-60, user_angle));
//     return constrained_angle;
//   }
// Blockly.Blocks['change_lift_angle'] = {
//   init: function()
//   {
//     Blockly.FieldAngle.ROUND=1;
//     Blockly.FieldAngle.OFFSET=90;
//     Blockly.FieldAngle.CLOCKWISE=1;
//     Blockly.FieldAngle.WRAP=180;
//     Blockly.FieldAngle.HALF=100;
//     Blockly.FieldAngle.RADIUS=99;
//     var angle_field = new Blockly.FieldAngle(34, constrain_lift_angle);
//
//     this.appendDummyInput()
//         .appendField("Move Neck Lift To")
//         .appendField(angle_field, "angle_deg");
//     this.setPreviousStatement(true, null);
//     this.setNextStatement(true, null);
//     this.setColour("#4AB9AF");
//     this.setTooltip("");
//     this.setHelpUrl("");
//   }
// };
//
// Blockly.Blocks['change_pitch_angle'] = {
//   init: function()
//   {
//     Blockly.FieldAngle.ROUND=1;
//     Blockly.FieldAngle.OFFSET=0;
//     Blockly.FieldAngle.CLOCKWISE=1;
//     Blockly.FieldAngle.WRAP=180;
//     Blockly.FieldAngle.HALF=100;
//     Blockly.FieldAngle.RADIUS=99;
//     var angle_field = new Blockly.FieldAngle(0, constrain_pitch_angle);
//
//     this.appendDummyInput()
//         .appendField("Move Neck Pitch To")
//         .appendField(angle_field, "angle_deg");
//     this.setPreviousStatement(true, null);
//     this.setNextStatement(true, null);
//     this.setColour("#4AB9AF");
//     this.setTooltip("");
//     this.setHelpUrl("");
//   }
// };
//
// Blockly.Blocks['change_yaw_angle'] = {
//   init: function()
//   {
//     Blockly.FieldAngle.ROUND=1;
//     Blockly.FieldAngle.OFFSET=90;
//     Blockly.FieldAngle.CLOCKWISE=0;
//     Blockly.FieldAngle.WRAP=180;
//     Blockly.FieldAngle.HALF=100;
//     Blockly.FieldAngle.RADIUS=99;
//     var angle_field = new Blockly.FieldAngle(0, constrain_yaw_angle);
//
//     this.appendDummyInput()
//         .appendField("Move Neck Yaw To")
//         .appendField(angle_field, "angle_deg");
//     this.setPreviousStatement(true, null);
//     this.setNextStatement(true, null);
//     this.setColour("#4AB9AF");
//     this.setTooltip("");
//     this.setHelpUrl("");
//   }
// };
