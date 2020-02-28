/**
 * @license
 * Visual Blocks Editor
 *
 * Copyright 2012 Google Inc.
 * https://developers.google.com/blockly/
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
 * @fileoverview Variable blocks for Blockly.
 * @author fraser@google.com (Neil Fraser)
 */
'use strict';

goog.provide('Blockly.Blocks.control');

goog.require('Blockly.Blocks');


/**
 * Common HSV hue for all blocks in this category.
 */
Blockly.Blocks.control.HUE = "#7FB5E3";


Blockly.Blocks['wait_seconds'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Wait for");
    this.appendValueInput("num_seconds")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("Seconds");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(Blockly.Blocks.control.HUE);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['for_time'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("For")
    this.appendValueInput("num_seconds")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("seconds");
    this.appendStatementInput("DO")
        .setCheck(null)
        .appendField(Blockly.Msg.CONTROLS_WHILEUNTIL_INPUT_DO);
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(Blockly.Blocks.control.HUE);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};
