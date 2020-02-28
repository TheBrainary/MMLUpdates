/**
 * @license
 *
 * Copyright 2015 Erle Robotics
 * http://erlerobotics.com
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
 * @fileoverview Blocks for Erle-Spider.
 * @author victor@erlerobot.com (Víctor Mayoral Vilches)
 * @author ahcorde@erlerobot.com (Alejandro Hernández Cordero)
 */
'use strict';

goog.provide('Blockly.Python.control');
goog.require('Blockly.Python');


Blockly.Python['wait_seconds'] = function(block) {
    var secs = Blockly.Python.valueToCode(block, 'num_seconds', Blockly.Python.ORDER_ATOMIC);
    var code = "robot.sleep("+secs+")\n"
    return code;
};

Blockly.Python['for_time'] = function(block) {
    var seconds = Blockly.Python.valueToCode(block, 'num_seconds', Blockly.Python.ORDER_ATOMIC);
    var loop_contents = Blockly.Python.statementToCode(block, 'DO');
    loop_contents = Blockly.Python.addLoopTrap(loop_contents, block.id) || Blockly.Python.PASS;
    var code = "\n" + "# loop" + "\n";
    code += "robot.start_timer(" + seconds + ")\n";
    code +="while robot.timer():\n" + loop_contents + "\n"
    return code;
};
