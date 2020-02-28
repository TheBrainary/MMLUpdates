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
 * @author George Bridges, Consequential Robotics
*/

'use strict';

goog.provide('Blockly.Python.miro');
goog.require('Blockly.Python');

////////////////// SETUP //////////////////////////////

Blockly.Python['setup_miro'] = function(block)
    {
      Blockly.Python.definitions_['import_time'] = 'import time';
      Blockly.Python.definitions_['import_miro_interface'] = 'import miro2 as miro';
      Blockly.Python.appendices_['kill_all'] = 'robot.exit()';
      var code="# setup" + "\n";
      code += "robot = miro.interface.PlatformInterface()" + "\n";
      code += "time.sleep(1.0)" + "\n";
      code += "\n# control\n";
      return code;
    };

Blockly.Python['miro_control_loop'] = function(block)
    {
      var loop_contents = Blockly.Python.statementToCode(block, 'control loop');
      loop_contents = Blockly.Python.addLoopTrap(loop_contents, block.id) || Blockly.Python.PASS;
      var code = '\n' + '# main loop' + '\n';
      code += 'while robot.ready():' + '\n' + loop_contents + '\n';
      return code;
    };

// Blockly.Python['send_commands'] = function(block)
//     {
//       var code = 'robot.update()\n';
//       return code;
//     };

///////////////////// SIMPLE MOTION ////////////////////////////

Blockly.Python['lift_head'] = function(block)
    {
      var angle_deg = block.getFieldValue('lift_head_ang');
      var code = 'robot.set_neck(miro.constants.JOINT_LIFT, ' + angle_deg +')' +'\n';
      return code;
    };

Blockly.Python['lift_chin'] = function(block)
    {
      var angle_deg = block.getFieldValue('lift_chin_ang');
      var code = 'robot.set_neck(miro.constants.JOINT_PITCH, ' + angle_deg +')' +'\n';
      return code;
    };

Blockly.Python['look'] = function(block)
    {
      var angle_deg = block.getFieldValue('look_ang');
      var code = 'robot.set_neck(miro.constants.JOINT_YAW, ' + angle_deg +')' +'\n';
      return code;
    };

Blockly.Python['move'] = function(block)
    {
      var move_dir = block.getFieldValue('move_dir');
      var move_vel = block.getFieldValue('move_vel');
      var code = 'robot.set_forward_speed(' + move_dir + move_vel + ')' +'\n';
      return code;
    };

Blockly.Python['stop_moving'] = function(block)
    {
      var code = 'robot.set_forward_speed(0.0)' +'\n';
      return code;
    };

Blockly.Python['turn'] = function(block)
    {
      var turn_dir = block.getFieldValue('turn_dir');
      var turn_vel = block.getFieldValue('turn_vel');
      var code = 'robot.set_turn_speed(' + turn_dir + turn_vel + ')' +'\n';
      return code;
    };

Blockly.Python['stop_turning'] = function(block)
    {
      var code = 'robot.set_turn_speed(0.0)' +'\n';
      return code;
    };

Blockly.Python['move_robot_to'] = function(block)
{
  var value_point = Blockly.Python.valueToCode(block, 'point', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

/////////////////// COMPLEX MOTION  ///////////////////////////////

Blockly.Python['change_lift_angle'] = function(block)
    {
      var angle_deg = Blockly.Python.valueToCode(block, 'angle_deg', Blockly.Python.ORDER_ATOMIC);
      var code = 'robot.set_neck(miro.constants.JOINT_LIFT, ' + angle_deg +')' +'\n';
      return code;
    };

Blockly.Python['change_pitch_angle'] = function(block)
    {
      var angle_deg = Blockly.Python.valueToCode(block, 'angle_deg', Blockly.Python.ORDER_ATOMIC);
      var code = 'robot.set_neck(miro.constants.JOINT_PITCH, ' + angle_deg +')' +'\n';
      return code;
    };

Blockly.Python['change_yaw_angle'] = function(block)
    {
      var angle_deg = Blockly.Python.valueToCode(block, 'angle_deg', Blockly.Python.ORDER_ATOMIC);
      var code = 'robot.set_neck(miro.constants.JOINT_YAW, ' + angle_deg +')' +'\n';
      return code;
    };

Blockly.Python['set_forward_speed'] = function(block) {
      var value_x_vel = Blockly.Python.valueToCode(block, 'x_vel', Blockly.Python.ORDER_ATOMIC);
      var code = 'robot.set_forward_speed(' + value_x_vel + ')' + '\n';
      return code;
    };

Blockly.Python['set_turn_speed'] = function(block) {
      var value_z_ang_vel = Blockly.Python.valueToCode(block, 'z_ang_vel', Blockly.Python.ORDER_ATOMIC);
      var code ='robot.set_turn_speed(' + value_z_ang_vel + ')'  + '\n';
      return code;
    };

Blockly.Python['move_ears'] = function(block) {
      var dropdown_ear = block.getFieldValue('ear');
      var dropdown_dir = block.getFieldValue('dir');
      if (dropdown_ear == 'JOINT_EARS') {
        var code = 'robot.set_joint(miro.constants.JOINT_EAR_L, ' + dropdown_dir +')' + '\n';
        code += 'robot.set_joint(miro.constants.JOINT_EAR_R, ' + dropdown_dir +')' + '\n';
      } else {
        var code = 'robot.set_joint(miro.constants.' + dropdown_ear + ', ' + dropdown_dir + ')' + '\n';
      }
      return code;
    };

Blockly.Python['move_eyelids'] = function(block) {
      var dropdown_eye = block.getFieldValue('eye');
      var dropdown_dir = block.getFieldValue('dir');
      if (dropdown_eye == 'JOINT_EYES') {
        var code = 'robot.set_joint(miro.constants.JOINT_EYE_L, ' + dropdown_dir +')' + '\n';
        code += 'robot.set_joint(miro.constants.JOINT_EYE_R, ' + dropdown_dir +')' + '\n';
      } else {
        var code = 'robot.set_joint(miro.constants.' + dropdown_eye + ', ' + dropdown_dir + ')' + '\n';
      }
      return code;
    };

Blockly.Python['point_tail'] = function(block) {
      var dropdown_point = block.getFieldValue('point');
      var code = 'robot.set_joint(miro.constants.JOINT_WAG, ' + dropdown_point + ')' + '\n';
      return code;
   };

Blockly.Python['droop_tail'] = function(block) {
      var dropdown_droop = block.getFieldValue('droop');
      var code = 'robot.set_joint(miro.constants.JOINT_DROOP, ' + dropdown_droop + ')' + '\n';
      return code;
   };

Blockly.Python['wag_tail'] = function(block) {
     var dropdown_wag_rate = block.getFieldValue('wag_rate');
     var wag_dur = Blockly.Python.valueToCode(block, 'wag_dur', Blockly.Python.ORDER_ATOMIC);
     var code = 'robot.wag_tail(' + wag_dur + ', ' + dropdown_wag_rate + ')' + '\n';
     return code;
  };

////////////////////// SENSORS //////////////////////////////////

Blockly.Python['read_light_sensor'] = function(block)
    {
      var dropdown_sensor_pos = block.getFieldValue('Sensor_Pos');
      var code = "robot.read_light_level(miro.constants." + dropdown_sensor_pos +")";
      return [code, Blockly.Python.ORDER_FUNCTION_CALL];
    };

Blockly.Python['read_all_light_sensors'] = function(block)
    {
      var code = "robot.read_light_level_list()";
      return [code, Blockly.Python.ORDER_FUNCTION_CALL];
    };

Blockly.Python['read_sonar_range'] = function(block)
    {
      var code = "robot.read_sonar_range()";
      return [code, Blockly.Python.ORDER_FUNCTION_CALL];
    };

Blockly.Python['read_cliff_sensor'] = function(block)
    {
      var dropdown_cliff_pos = block.getFieldValue('Cliff_Pos');
      var code = "robot.read_cliff_sensor(miro.constants." + dropdown_cliff_pos +")";
      return [code, Blockly.Python.ORDER_FUNCTION_CALL];
    };

Blockly.Python['read_both_cliff_sensors'] = function(block)
    {
      var code = "robot.read_cliff_sensor_list()";
      return [code, Blockly.Python.ORDER_FUNCTION_CALL];
    };

Blockly.Python['read_body_touch_sensors'] = function(block)
    {
      var code = "robot.read_body_touch_sensors()";
      return [code, Blockly.Python.ORDER_FUNCTION_CALL];
    };

Blockly.Python['read_head_touch_sensors'] = function(block)
    {
      var code = "robot.read_head_touch_sensors()";
      return [code, Blockly.Python.ORDER_FUNCTION_CALL];
    };

Blockly.Python['clap_in_previous'] = function(block)
    {
      var value_time_secs = Blockly.Python.valueToCode(block, 'time_secs', Blockly.Python.ORDER_ATOMIC);
      var code = "robot.clap_in_previous(" + value_time_secs + ")";
      return [code, Blockly.Python.ORDER_FUNCTION_CALL];
    };

Blockly.Python['time_since_clap'] = function(block)
    {
      var code = "robot.time_since_clap()";
      return [code, Blockly.Python.ORDER_NONE];
    };

Blockly.Python['wait_for_clap'] = function(block)
    {
      var code = 'while robot.clap() == False:';
      code += "\n  time.sleep(0.025) \n"
      return code;
    };

///////////////////// ACTIONS //////////////////////////////

Blockly.Python['find_ball'] = function(block) {
     var dropdown_ball_property = block.getFieldValue('ball_property');
     var colour_ball_colour = block.getFieldValue('ball_colour');
     var dropdown_cam_id = block.getFieldValue('cam_id');
     var code = 'robot.find_ball(\''+ colour_ball_colour + '\', miro.constants.' + dropdown_cam_id + ', ' + dropdown_ball_property + ')' + '\n';
     return [code, Blockly.Python.ORDER_FUNCTION_CALL];
   };

///////////////////// ROBOT ONLY ////////////////////////////
Blockly.Python['play_tone'] = function(block) {
  var value_freq = Blockly.Python.valueToCode(block, 'FREQ', Blockly.Python.ORDER_ATOMIC);
  var value_dur = Blockly.Python.valueToCode(block, 'DUR', Blockly.Python.ORDER_ATOMIC);
  var value_vol = Blockly.Python.valueToCode(block, 'VOL', Blockly.Python.ORDER_ATOMIC);
  var code = 'robot.play_tone(' + value_freq + ', ' + value_vol + ', ' + value_dur + ')' + '\n';
  return code;
};

Blockly.Python['change_led'] = function(block) {
  var dropdown_pos = block.getFieldValue('POS');
  var dropdown_side = block.getFieldValue('SIDE');
  var dropdown_bright = block.getFieldValue('BRIGHT');
  var colour_led_col = block.getFieldValue('LED_COL');
  var code = ''
  if (dropdown_pos != 'ALL' && dropdown_side != 'BOTH') {
    code = 'robot.control_led(miro.constants.' + dropdown_side + dropdown_pos + ', \'' + colour_led_col + '\', ' + dropdown_bright + ')\n';
  }
  else if (dropdown_pos != 'ALL' && dropdown_side == 'BOTH'){
    code = 'robot.control_led(miro.constants.ILLUM_R' + dropdown_pos + ', \'' + colour_led_col + '\', ' + dropdown_bright + ')\n';
    code += 'robot.control_led(miro.constants.ILLUM_L' + dropdown_pos + ', \'' + colour_led_col + '\', ' + dropdown_bright + ')\n';
  }
  else if (dropdown_pos == 'ALL' && dropdown_side != 'BOTH'){
    code = 'robot.control_led(miro.constants.' + dropdown_side + 'F, \'' + colour_led_col + '\', ' + dropdown_bright + ')\n';
    code += 'robot.control_led(miro.constants.' + dropdown_side + 'M, \'' + colour_led_col + '\', ' + dropdown_bright + ')\n';
    code += 'robot.control_led(miro.constants.' + dropdown_side + 'R, \'' + colour_led_col + '\', ' + dropdown_bright + ')\n';
  }
  else if (dropdown_pos == 'ALL' && dropdown_side == 'BOTH'){
    code = 'robot.control_led(miro.constants.ILLUM_RF, \'' + colour_led_col + '\', ' + dropdown_bright + ')\n';
    code += 'robot.control_led(miro.constants.ILLUM_RM, \'' + colour_led_col + '\', ' + dropdown_bright + ')\n';
    code += 'robot.control_led(miro.constants.ILLUM_RR, \'' + colour_led_col + '\', ' + dropdown_bright + ')\n';
    code += 'robot.control_led(miro.constants.ILLUM_LF, \'' + colour_led_col + '\', ' + dropdown_bright + ')\n';
    code += 'robot.control_led(miro.constants.ILLUM_LM, \'' + colour_led_col + '\', ' + dropdown_bright + ')\n';
    code += 'robot.control_led(miro.constants.ILLUM_LR, \'' + colour_led_col + '\', ' + dropdown_bright + ')\n';
  }
  return code;
};

Blockly.Python['miro_say'] = function(block) {
  var value_say_text = Blockly.Python.valueToCode(block, 'say_text', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = '';
  Blockly.Python.definitions_['import_mml'] = 'import mml';
  code += 'mml.say(' + value_say_text + ')\n';
  return code;
};

Blockly.Python['miro_play'] = function(block) {
  var value_play_id = block.getFieldValue('play_path');
  var code = '';
  Blockly.Python.definitions_['import_mml'] = 'import mml';
  code += 'mml.play("' + value_play_id + '")\n';
  return code;
};