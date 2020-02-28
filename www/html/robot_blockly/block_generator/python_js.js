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

goog.provide('Blockly.Python.miro');
goog.require('Blockly.Python');

Blockly.Python['setup_miro'] = function(block)
    {
        var code = "";
        var miro_type = block.getFieldValue('miro_type');
        code += "miro_type = \"" + miro_type.toString() + "\"\n";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/setup_miro.py");
        return code;

    };
    
Blockly.Python['say'] = function(block) 
	{
		var dropdown_lift = block.getFieldValue('dropdown_lift');
		var value_say_text = Blockly.JavaScript.valueToCode(block, 'say_text', Blockly.JavaScript.ORDER_ATOMIC);
		var code = '';
		code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/say.py");
		
		return code;
	};

Blockly.Python['move_backward'] = function(block)
    {
        var code = "";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/move_backward.py");
        return code;

    };

Blockly.Python['move_forward'] = function(block)
    {
        var code = "";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/move_forward.py");
        return code;

    };

Blockly.Python['turn_left'] = function(block)
    {
        var code = "";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/turn_left.py");
        return code;

    };

Blockly.Python['turn_right'] = function(block)
    {
        var code = "";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/turn_right.py");
        return code;

    };

Blockly.Python['lift_neck'] = function(block)
    {
        var code = "";
        var dropdown_lift = block.getFieldValue('dropdown_lift');
        code += "dropdown_lift = \"" + dropdown_lift.toString() + "\"\n";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/lift_neck.py");
        return code;

    };

Blockly.Python['pitch_neck'] = function(block)
    {
        var code = "";
        var dropdown_pitch = block.getFieldValue('dropdown_pitch');
        code += "dropdown_pitch = \"" + dropdown_pitch.toString() + "\"\n";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/pitch_neck.py");
        return code;

    };

Blockly.Python['yaw_neck'] = function(block)
    {
        var code = "";
        var dropdown_yaw = block.getFieldValue('dropdown_yaw');
        code += "dropdown_yaw = \"" + dropdown_yaw.toString() + "\"\n";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/yaw_neck.py");
        return code;

    };

Blockly.Python['wag_tail'] = function(block)
    {
        var code = "";
        var dropdown_wag = block.getFieldValue('dropdown_wag');
        code += "dropdown_wag = \"" + dropdown_wag.toString() + "\"\n";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/wag_tail.py");
        return code;

    };

Blockly.Python['droop_tail'] = function(block)
    {
        var code = "";
        var dropdown_droop = block.getFieldValue('dropdown_droop');
        code += "dropdown_droop = \"" + dropdown_droop.toString() + "\"\n";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/droop_tail.py");
        return code;

    };

Blockly.Python['move_ears'] = function(block)
    {
        var code = "";
        var dropdown_ears = block.getFieldValue('dropdown_ears');
        code += "dropdown_ears = \"" + dropdown_ears.toString() + "\"\n";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/move_ears.py");
        return code;

    };

Blockly.Python['get_distance'] = function(block)
    {
        var varName = Blockly.Python.valueToCode(block, 'get_distance_var', Blockly.Python.ORDER_ATOMIC);
        var code = "";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/get_distance.py");
        return code + varName + "=msg_distance.range \n";    };

Blockly.Python['capture_image'] = function(block)
    {

        window.open(
            '/pages/images/imageViewer.html',
            '_blank' // <- This is what makes it open in a new window.
        );

        var code = "";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/capture_image.py");
        return code;

    };

Blockly.Python['get_colour_pixels'] = function(block)
    {
        var varName = Blockly.Python.valueToCode(block, 'get_colour_pixels_var', Blockly.Python.ORDER_ATOMIC);
        var code = "";
        var hex_string = block.getFieldValue('hex_string');
        code += "hex_string = \"" + hex_string.toString() + "\"\n";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/get_colour_pixels.py");
        return code + varName + "=result \n";    };

Blockly.Python['get_colour_direction'] = function(block)
    {
        var varName = Blockly.Python.valueToCode(block, 'get_colour_direction_var', Blockly.Python.ORDER_ATOMIC);
        var code = "";
        var hex_string = block.getFieldValue('hex_string');
        code += "hex_string = \"" + hex_string.toString() + "\"\n";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/get_colour_direction.py");
        return code + varName + "=result \n";    };

Blockly.Python['find_circle'] = function(block)
    {
        var varName = Blockly.Python.valueToCode(block, 'find_circle_var', Blockly.Python.ORDER_ATOMIC);
        var code = "";
        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/find_circle.py");
        return code + varName + "=result \n";    };

