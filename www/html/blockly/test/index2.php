\<!DOCTYPE html>
<html>
 <?php
  if (isset($_POST['runCode']))	 {
     showCode();
     exec("$(which /home/miro/stream.sh)");
  }
  if (isset($_POST['CreateFolder'])) { exec("sudo /home/miro/test.sh");
  }
  if (isset($_POST['Stop'])) { exec("sudo /home/miro/testcode.sh");
  }
?>
 <head>
  <meta charset="utf-8">
  <title>Blockly Demo: Generating JavaScript</title>
  <script src="../blockly_compressed.js"></script>
  <script src="../blocks_compressed.js"></script>
  <script src="../python_compressed.js"></script>
  <script src="../msg/js/en.js"></script>
  <style>
    body {
      background-color: #fff;
      font-family: sans-serif;
    }
    h1 {
      font-weight: normal;
      font-size: 140%;
    }
  </style> </head> <body>
  <h1><a href="https://developers.google.com/blockly/">Blockly</a> &gt;
    <a href="../index.html">Demos</a> &gt; Generating JavaScript</h1>
  <p>This is a simple demo of generating code from blocks and running
  the code in a sandboxed JavaScript interpreter.</p>
  <p>&rarr; More info on <a 
href="https://developers.google.com/blockly/guides/configure/web/code-generators">Code Generators</a> and <a 
href="https://developers.google.com/blockly/guides/app-integration/running-javascript">Running 
JavaScript</a>.</p>
  <p>
  <form method="post">
  <button name="RunCode" class="btn">Run Code</button>&nbsp; 
  <button name="CreateFolder" class="btn">Create Folder</button><br><br>
  <button name="Stop" class="btn">Stop</button> </form>
  <button onclick="showCode()">Show JavaScript</button>
  <button name="runCode" class="btn">Run JavaScript</button>
  </p>
  <div id="blocklyDiv" style="height: 480px; width: 600px;"></div>
  <xml id="toolbox" style="display: none">
    <category name="Logic" colour="%{BKY_LOGIC_HUE}">
      <block type="controls_if"></block>
      <block type="logic_compare"></block>
      <block type="logic_operation"></block>
      <block type="logic_negate"></block>
      <block type="logic_boolean"></block>
    </category>
    <category name="Loops" colour="%{BKY_LOOPS_HUE}">
      <block type="controls_repeat_ext">
        <value name="TIMES">
          <block type="math_number">
            <field name="NUM">10</field>
          </block>
        </value>
      </block>
      <block type="controls_whileUntil"></block>
    </category>
    <category name="Math" colour="%{BKY_MATH_HUE}">
      <block type="math_number">
        <field name="NUM">123</field>
      </block>
      <block type="math_arithmetic"></block>
      <block type="math_single"></block>
    </category>
    <category name="Text" colour="%{BKY_TEXTS_HUE}">
      <block type="text"></block>
      <block type="text_length"></block>
      <block type="text_print"></block>
    </category>
  </xml>
  <xml id="startBlocks" style="display: none">
    <block type="controls_if" inline="false" x="20" y="20">
      <mutation else="1"></mutation>
      <value name="IF0">
        <block type="logic_compare" inline="true">
          <field name="OP">EQ</field>
          <value name="A">
            <block type="math_arithmetic" inline="true">
              <field name="OP">MULTIPLY</field>
              <value name="A">
                <block type="math_number">
                  <field name="NUM">6</field>
                </block>
              </value>
              <value name="B">
                <block type="math_number">
                  <field name="NUM">7</field>
                </block>
              </value>
            </block>
          </value>
          <value name="B">
            <block type="math_number">
              <field name="NUM">42</field>
            </block>
          </value>
        </block>
      </value>
      <statement name="DO0">
        <block type="text_print" inline="false">
          <value name="TEXT">
            <block type="text">
              <field name="TEXT">Don't panic</field>
            </block>
          </value>
        </block>
      </statement>
      <statement name="ELSE">
        <block type="text_print" inline="false">
          <value name="TEXT">
            <block type="text">
              <field name="TEXT">Panic</field>
            </block>
          </value>
        </block>
      </statement>
    </block>
  </xml>
  
<?php function testCode(){
  exec("sudo /home/miro/testcode.sh");
  return 1;
}
function PlaySound(){
  exec("$(which /home/miro/stream.sh)");
  return 1;
}
?>
  <script>
    var demoWorkspace = Blockly.inject('blocklyDiv',
        {media: '../media/',
         toolbox: document.getElementById('toolbox')});
    Blockly.Xml.domToWorkspace(document.getElementById('startBlocks'),
                               demoWorkspace);
    function showCode() {
      // Generate JavaScript code and display it.
      Blockly.Python.INFINITE_LOOP_TRAP = null;
      var code = Blockly.Python.workspaceToCode(demoWorkspace);
      alert(code);
      document.getElementById("Python_Code").innerHTML = code;


var exec = require('child_process').exec, child;

child = exec("$(which /home/miro/stream.sh)",
    function (error, stdout, stderr) {
        console.log('stdout: ' + stdout);
        console.log('stderr: ' + stderr);
        if (error !== null) {
             console.log('exec error: ' + error);
        }
    });
 child();




exec("$(which /home/miro/stream.sh)");   
 }
    function runCode() {
      // Generate JavaScript code and run it.
      window.LoopTrap = 1000;
      Blockly.Python.INFINITE_LOOP_TRAP =
          'if (--window.LoopTrap == 0) throw "Infinite loop.";\n';
      var code = Blockly.Python.workspaceToCode(demoWorkspace);
      Blockly.Python.INFINITE_LOOP_TRAP = null;
      try {
exec("$(which /home/miro/stream.sh)");
      } catch (e) {
        alert(e);
      }
    }
  </script> <div id="Python_Code"></div> </body> </html>
