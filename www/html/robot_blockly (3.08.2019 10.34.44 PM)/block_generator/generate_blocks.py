# Copyright (c) 2018, Cyberselves
# Author: Daniel Camilleri
# All rights reserved.
#!/usr/bin/env python2
import json
import os
import shutil
import sys

compressed_flag = False

if len(sys.argv) > 1:
    if sys.argv[1] == "compressed":
        compressed_flag = True

block_notebook_fname = "block_definitions.ipynb"
# block_notebook_fname = "test.ipynb"

python_scripts_fname = "python_scripts"
python_scripts_dest = "../frontend/blockly/generators/python/scripts/miro"

python_js_fname = "python_js.js"
python_js_dest = "../frontend/blockly/generators/python/miro.js"

blocks_js_fname = "blocks_js.js"
blocks_js_dest = "../frontend/blockly/blocks/miro.js"

if compressed_flag:
    with open(os.path.join("blockly_html_p1.txt"), 'r') as b:
        blockly_p1 = b.readlines()
else:
    with open(os.path.join("blockly_html_p1_uncompressed.txt"), 'r') as b:
        blockly_p1 = b.readlines()

with open(os.path.join("blockly_html_p2.txt"), 'r') as b:
    blockly_p2 = b.readlines()

js_header = \
"""/**
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
"""

blocks_js_header = \
"""
goog.provide('Blockly.Blocks.miro');
goog.require('Blockly.Blocks');

/**
 * Common HSV hue for all blocks in this category.
 */
// Blockly.Blocks.miro.HUE = 260;

"""

python_js_header = \
"""
goog.provide('Blockly.Python.miro');
goog.require('Blockly.Python');

"""


def partition(mode, name):
    return "\n#-----------------------------{0} {1}---------------------------------\n".format(mode.upper(), name.upper())


def python_js_template(block_name, input_var_name, return_var, returns, show_image):
    template_p1 = "Blockly.Python['{0}'] = function(block)".format(block_name)

    return_line = "        "
    if return_var is not None:
        block_read_var = "        var varName = Blockly.Python.valueToCode(block, '{0}', " \
                         "Blockly.Python.ORDER_ATOMIC);\n".format(return_var)

        return_line += 'return code + varName + "={0} \\n";'.format(returns)
    else:
        block_read_var = ""
        return_line += "return code;\n\n"

    template_p2 = \
"""        code += Blockly.readPythonFile("../blockly/generators/python/scripts/miro/{0}.py");\n""".format(block_name)

    params_intro = """        var code = "";\n"""
    template_params = ""
    if input_var_name is not None:
        template_params += "        var {0} = block.getFieldValue('{0}');\n".format(input_var_name)
        template_params += '        code += "{0} = \\"" + {0}.toString() + "\\"\\n";\n'.format(input_var_name)

    show_image_str = ""
    if show_image:
        show_image_str = "\n        window.open(\n            '/pages/images/imageViewer.html',\n            " \
                         "'_blank' // <- This is what makes it open in a new window.\n        );\n\n"

    block = template_p1 + "\n    {\n" + show_image_str + block_read_var + params_intro + template_params + \
            template_p2 + return_line + "    };\n\n"

    return block


def blocks_js_template(block_name, input_user_params, input_code_params,
                       input_var_name, return_var, interface_type, colour):
    if colour is None:
        colour = 230
    cap_name = " ".join([k.capitalize() for k in block_name.split("_")])

    template_p1 = "Blockly.Blocks['{0}'] = ".format(block_name)
    template_p2 = "    init: function() \n"
    template_p3 = """            .appendField("{0}")\n""".format(cap_name)
    template_p4 = \
"""        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour({0});
        this.setTooltip("");
        this.setHelpUrl("");
""".format(colour)

    return_line = "        "
    if return_var is None:
        return_line += """this.appendDummyInput()\n"""
    else:
        return_line += """this.appendValueInput("{0}")\n""".format(return_var)

    interface = ""
    if interface_type is not None:
        if interface_type == "dropdown" and len(input_user_params) > 0 and len(input_user_params) == len(input_code_params):
            interface = "            .appendField(new Blockly.FieldDropdown(["
            for op in range(len(input_user_params)):
                interface += """["{0}","{1}"], """.format(input_user_params[op], input_code_params[op])

            interface = interface[:-2] + """]), "{0}");\n""".format(input_var_name)
        elif interface_type == "colour_wheel" or interface_type == "color_wheel":
            interface = "            .appendField(new Blockly.FieldColour('#ff0000'), '{0}');\n".format(input_var_name)

    block = template_p1 + "{\n" + template_p2 + "    {\n" + return_line + \
            template_p3 + interface + template_p4 + "    }\n};\n\n"

    return block


# Empty folders
if os.path.isdir(python_scripts_fname):
    shutil.rmtree(python_scripts_fname)
os.mkdir(python_scripts_fname)

if os.path.isfile(python_js_fname):
    os.remove(python_js_fname)

if os.path.isfile(blocks_js_fname):
    os.remove(blocks_js_fname)

if os.path.isfile("blockly.html"):
    os.remove("blockly.html")

# Prepare js file headers
with open(os.path.join(blocks_js_fname), 'a') as b:
    b.writelines(js_header + blocks_js_header)

with open(os.path.join(python_js_fname), 'a') as b:
    b.writelines(js_header + python_js_header)

# Load Definitions Notebook and read cells
with open(block_notebook_fname, 'r') as f:
    nb = json.loads(f.read())

cells = nb["cells"]

# Cell number 1 is always
# import rospy
# rospy.init_node('blockly_server', anonymous=True)
# So notebook can be used to test code with gazebo before compiling

block_names = []
block_groups = []
group_colours = []

if len(cells) > 1:
    for c in cells[1:]:
        return_code = None
        return_var_name = None
        user_interface = None
        input_var_name = None
        input_params_list = None
        input_vars_list = None
        block_color = None
        show_image_flag = False

        if c["cell_type"] == "code":
            src_code = c["source"]
            # Functions defined with 'def' are the ones extracted into blocks. This leaves developer free to test
            # and call blocks of code
            # A cell containing a function MUST ONLY contain ONE function definition
            def_lnum = [n for n, j in enumerate(src_code) if "def " in j]
            if len(def_lnum) == 1:
                def_lnum = def_lnum[0]
                def_parts = src_code[def_lnum].split("def ")[1].split("(")
                block_name = def_parts[0]
                if def_parts[1] != "):\n":
                    input_var_name = def_parts[1].split(")")[0]
                block_names.append(block_name)
                block_groups.append("Miro")
                group_colours.append(None)

                # Create script
                with open(os.path.join(python_scripts_fname, block_name + ".py"), 'a') as b:
                    unindented_code = []
                    unindented_code.append(partition("start", block_name))
                    for k in src_code:
                        if "return " in k:
                            return_code = k.split("return ")[1]
                            return_var_name = block_name + "_var"
                        elif "Interface:" in k and "#" in k:
                            user_interface = k.split("Interface:")[1].replace(" ", "").replace("\n", "")
                        elif "Parameters:" in k and "#" in k:
                            if user_interface == "dropdown" or user_interface == "checkbox":
                                if "UserParameters" in k:
                                    input_params_list = k.split("UserParameters:")[1] \
                                                            .replace(" ", "").replace("\n", "")[1:-1].split(",")
                                elif "CodeParameters" in k:
                                    input_vars_list = k.split("CodeParameters:")[1] \
                                                            .replace(" ", "").replace("\n", "")[1:-1].split(",")
                            elif user_interface is None:
                                raise TypeError("Specify Interface before Parameters")
                            else:
                                raise ValueError(str(user_interface) + "not yet supported")
                        elif "GroupColour:" in k and "#" in k:
                            try:
                                group_colours[-1] = int(k.split("GroupColour:")[1].replace(" ", "").replace("\n", ""))
                            except Exception as e:
                                pass
                        elif "GroupColor:" in k and "#" in k:
                            try:
                                group_colours[-1] = int(k.split("GroupColor:")[1].replace(" ", "").replace("\n", ""))
                            except Exception as e:
                                pass
                        elif "Group:" in k and "#" in k:
                            try:
                                block_groups[-1] = k.split("Group:")[1].replace(" ", "").replace("\n", "").replace("_", " ")
                            except Exception as e:
                                pass
                        elif "Colour:" in k and "#" in k:
                            try:
                                block_color = int(k.split("Colour:")[1].replace(" ", "").replace("\n", ""))
                            except Exception as e:
                                block_color = None
                        elif "def " in k and "(" in k and "):" in k or "global" in k:
                            pass
                        elif "# Show Image" in k:
                            show_image_flag = True
                        elif k != "\n":
                            unindented_code.append(k[4:])
                        else:
                            unindented_code.append(k)
                    unindented_code.append(partition("end", block_name))
                    b.writelines(unindented_code)

                # Append to blocks_js
                with open(os.path.join(blocks_js_fname), 'a') as b:
                    b.writelines(blocks_js_template(block_name=block_name,
                                                    input_var_name=input_var_name,
                                                    input_user_params=input_params_list,
                                                    input_code_params=input_vars_list,
                                                    return_var=return_var_name,
                                                    interface_type=user_interface,
                                                    colour=block_color))

                # Append to python_js
                with open(os.path.join(python_js_fname), 'a') as b:
                    b.writelines(python_js_template(block_name=block_name,
                                                    input_var_name=input_var_name,
                                                    return_var=return_var_name,
                                                    returns=return_code,
                                                    show_image=show_image_flag))
    last_group = None

    def set_colors(ggcolors, ggnames, gname, gcolor):
        for a, b in enumerate(ggnames):
            if b == gname:
                ggcolors[a] = gcolor

    for n, gc in enumerate(group_colours):
        if gc is None:
            group_colours[n] = 260
        else:
            set_colors(ggcolors=group_colours, ggnames=block_groups, gname=block_groups[n], gcolor=gc)


    last_group = None
    with open(os.path.join("blockly.html"), 'a') as b:
        b.writelines(blockly_p1)
        for n, g in enumerate(list(block_groups)):
            if g != last_group:
                if last_group is not None:
                    b.write('        </category>\n')
                b.write('        <category id="{1}" name="{0}" colour="{2}">\n'.format(g, g.lower(), group_colours[n]))
                last_group = g
            b.write('            <block type="{0}"></block>\n'.format(block_names[n]))
        b.write('        </category>\n')
        b.writelines(blockly_p2)

    shutil.copy(python_js_fname, python_js_dest)
    shutil.copy(blocks_js_fname, blocks_js_dest)
    shutil.rmtree(python_scripts_dest)
    shutil.copytree(python_scripts_fname, python_scripts_dest)
    #shutil.copy("blockly.html", "../frontend/pages/blockly.html")
    print "Finished Compiling Blocks"
