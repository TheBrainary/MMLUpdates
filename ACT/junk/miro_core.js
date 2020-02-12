/*
  MEI functions
*/

function showSnackBar() {
  var x = document.getElementById("snackbar");
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

function vh(v) {
  var h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
  return (v * h) / 100;
}

function vw(v) {
  var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
  return (v * w) / 100;
}

function vmin(v) {
  return Math.min(vh(v), vw(v));
}

function vmax(v) {
  return Math.max(vh(v), vw(v));
}
console.info(vh(20), Math.max(document.documentElement.clientHeight, window.innerHeight || 0));
console.info(vw(30), Math.max(document.documentElement.clientWidth, window.innerWidth || 0));
console.info(vmin(20));
console.info(vmax(20));

$(document).ready(function(){
  var x = "Total Width: " + screen.width + "px";
  //var oText = document.getElementById('debugarea');
  // oText.innerHTML = x;
});

$(window).resize(function(){
  var x = "Total Width: " + screen.width + "px";
  var innerHeight = window.innerHeight;
  var innerWidth = window.innerWidth;
  //var oText = document.getElementById('debugarea');
  // oText.innerHTML = innerHeight +"x"+ innerWidth;
});

$(document).ready(function(){
  var oResult = document.getElementById('alert');
  var nCount = 0;
  $("#navigate_left_btn").click(function() {
      nCount -= 1;
      nCount = pagesSwitch (nCount, oResult);
      // nCount = borderSwitch (nCount, oResult);
  });
  $("#navigate_right_btn").click(function() {
      nCount += 1;
      nCount = pagesSwitch (nCount, oResult);
      // nCount = borderSwitch (nCount, oResult);
  });
});

function pagesSwitch (nCount, oResult) {
  switch (nCount) {
      case 1:
          oResult.innerHTML = 'One';
          break;
      case 2:
          oResult.innerHTML = 'Two';
          break;
      case 3:
          oResult.innerHTML = 'Three';
          break;
      case 4:
          oResult.innerHTML = 'Four';
          break;
      case 5:
          oResult.innerHTML = 'Five';
          break;
      default:
          oResult.innerHTML = 'Finish';
          nCount = 0;
  }
  return nCount;
}

function borderSwitch (nCount, oResult) {
  var gazebo = document.getElementById('gazebo');
  var blockly = document.getElementById('blocklyDiv');
  blockly.style.border = 'none';
  gazebo.style.borderRadius = 'none';
  gazebo.style.border = 'none';
  switch (nCount) {
      case 1:
          $("#gazebo").css({"border": "2px solid #4195fc", "border-radius": "7px", "box-shadow" : "0 0 10px #9ecaed;", "-webkit-box-shadow" : "0px 0px 4px #4195fc;"});
          break;
      case 2:
          $("#blocklyDiv").css({"border": "2px solid #4195fc", "border-radius": "7px", "box-shadow" : "0 0 10px #9ecaed;", "-webkit-box-shadow" : "0px 0px 4px #4195fc;"});
          break;
      case 3:
          oResult.innerHTML = 'Three';
          break;
      case 4:
          oResult.innerHTML = 'Four';
          break;
      case 5:
          oResult.innerHTML = 'Five';
          break;
      default:
          oResult.innerHTML = 'Finish';
          nCount = 0;
  }
  return nCount;
}

function switchContext() {
  var checkBox = document.getElementById("myonoffswitch");
  if (checkBox.checked == true){
    show_blockly();
  } else {
    hide_blockly();
  }
}

function switchView() {
  var checkBox = document.getElementById("myviewonoffswitch");
  if (checkBox.checked == true){
    show_view();
  } else {
    hide_view();
  }
}

function show_view () {
  var loc = "http://localhost:9001/stream_viewer?topic=/miro/sensors/caml&width=720&height=500";
  $('#miro_view').attr('src', loc);
  console.log("show view");
}

function hide_view () {
  var loc = "http://localhost:8080";
  $('#miro_view').attr('src', loc);
  console.log("hide view");
}

function burger(item) {
  var menu = document.getElementById("menu");
   if(item.name == "on") {
      item.name="off";
      menu.style.display = 'none';
   } else {
      item.name="on";
      menu.style.display = 'block';
   }
}

function openForm(item){
  var editor = ace.edit("editor");
  console.log(editor.getValue());

  var simulate = document.getElementById("simulate");
  if(item.name == "on") {
     item.name="off";
     simulate.style.display = 'none';
  } else {
     item.name="on";
     simulate.style.display = 'block';
  }
}

function robot_play(event, elem){
  var ipInput = document.getElementById("inputUrl");
  var ipaddr = $("input#inputUrl").val();
  //var oText = document.getElementById('debugarea');

  console.log("ipaddress input :" +ipaddr);
  var hex = convertToHex('play');
  if(validateIp(ipaddr)){
    console.log("valid ipaddress");
    $.ajax({
      type: 'POST',
      url: 'http://' + ipaddr + ':1337' + '/api',
      data: {
        data: hex,
      },
      success: function(response){
        console.log('response '+response);
      },
      error: function(request) {
        if (request.status == 0){
          //oText.innerHTML = 'No connection to MiRo';
        }
      }
    });
    event.preventDefault();
  }else{
    console.log("invalid ipaddress");
  }
}

function robot_pause(){
  var pause_btn = document.getElementById("pause_button");
  var ipInput = document.getElementById("inputUrl");
  var pause_label = document.getElementById("pause_label");
  var ipaddr = $("input#inputUrl").val();
  //var oText = document.getElementById('debugarea');
  var command = 'command';
  console.log("ipaddress input :" +ipaddr);
  if (pause_btn.className == "btn pause-btn") {
    var hex = convertToHex('pause');
  } else {
    var hex = convertToHex('resume');
  }
  if(validateIp(ipaddr)){
    console.log("valid ipaddress");
    $.ajax({
      type: 'POST',
      url: 'http://' + ipaddr + ':1337' + '/api',
      data: {
        data: hex,
      },
      success: function(msg){
        console.log('wow' + msg);
        if (pause_btn.className == "btn pause-btn") {
          pause_btn.className = "btn resume-btn";
          pause_label.innerHTML = "Resume";
        } else {
          pause_btn.className = "btn pause-btn";
          pause_label.innerHTML = "Pause";
        }
      },
      error: function(request) {
        if (request.status == 0){
          //oText.innerHTML = 'No connection to MiRo';
        }
      }
    });
  }else{
    console.log("invalid ipaddress");
  }
}

function robot_stop(){
  var ipInput = document.getElementById("inputUrl");
  var ipaddr = $("input#inputUrl").val();
  //var oText = document.getElementById('debugarea');
  console.log("ipaddress input :" +ipaddr);
  var hex = convertToHex('stop');
  if(validateIp(ipaddr)){
    console.log("valid ipaddress");
    $.ajax({
      type: 'POST',
      url: 'http://' + ipaddr + ':1337' + '/api',
      data: {
        data: hex,
      },
      success: function(msg){
        console.log('wow' + msg);
      },
      error: function(request) {
        if (request.status == 0){
          //oText.innerHTML = 'No connection to MiRo';
        }
      }
    });
  }else{
    console.log("invalid ipaddress");
  }
}

function robot_replay(){
  var ipInput = document.getElementById("inputUrl");
  var ipaddr = $("input#inputUrl").val();
  //var oText = document.getElementById('debugarea');
  console.log("ipaddress input :" +ipaddr);
  var hex = convertToHex('clipboard');
  if(validateIp(ipaddr)){
    console.log("valid ipaddress");
    $.ajax({
      type: 'POST',
      url: 'http://' + ipaddr + ':1337' + '/api',
      data: {
        data: JSON.stringify({'write' : 'code'}),
      },
      success: function(msg){
        console.log('wow' + msg);
      }
    });
  }else{
    console.log("invalid ipaddress");
  }
}

function sendData(event, elem){
  var blockly_area = document.getElementById("blocklyArea");
  //  var editor = ace.edit("editor");
  if (window.getComputedStyle(blockly_area).display === "block")
  {
    Blockly.Python.addReservedWords('code'); 
    var clipBoard = Blockly.Python.workspaceToCode(workspace);
    console.log(clipBoard);
  }
  else
  {
    var clipBoard = editor.getValue();
    console.log(clipBoard);
  }
  //var oText = document.getElementById('debugarea');
  var hex = hexEncode('write ' + clipBoard);
  var str = window.location.origin;
  var res = str.split("/"); 
  var ipInput = res[res.length - 1];
  if(validateIp(ipInput)){
    console.log("valid ipaddress");
    $.ajax({
      type: 'POST',
      url: 'http://' + ipInput + ':1337' + '/api',
      data: {
        data: (hex),
      },
      success: function(msg){
        console.log(msg);
      },
      error: function(request) {
        if (request.status == 0){
          //oText.innerHTML = 'No connection to MiRo';
        }
      }
    });
  }else{
    console.log("invalid ipaddress");
  }
  event.preventDefault();
}

function robot_say(event, elem){
  var str = window.location.origin;
  var res = str.split("/");
  var ipInput = res[res.length - 1];
  
  var oText = document.getElementById('dialogInput').value;
  var hex = hexEncode('say ' + oText);
  
    if(validateIp(ipInput)){
    console.log("valid ipaddress");
    $.ajax({
      type: 'POST',
      url: 'http://' + ipInput + ':1337' + '/api',
      data: {
        data: (hex),
      },
      success: function(msg){
        console.log(msg);
      },
      error: function(request) {
        if (request.status == 0){
          //oText.innerHTML = 'No connection to MiRo';
        }
      }
    });
  }else{
    console.log("invalid ipaddress");
  }
  event.preventDefault();
}



function list_apps(event, elem){
  var str = window.location.origin;
  var res = str.split("/");
  var ipInput = res[res.length - 1];

  
  

    if(validateIp(ipInput)){
    console.log("valid ipaddress");
    $.ajax({
      type: 'GET',
      url: 'http://' + ipInput + ':1337' + '/api/list_apps',
      success: function(msg){
        console.log(msg);
      },
      error: function(request) {
        if (request.status == 0){
          //oText.innerHTML = 'No connection to MiRo';
        }
      }
    });
  }else{
    console.log("invalid ipaddress");
  }
}




function convertToHex(str) {
    var hex = '';
    for(var i=0;i<str.length;i++) {
        hex += ''+str.charCodeAt(i).toString(16);
    }
    return hex;
}

function hexEncode (str){
    var hex, i;

    var result = "";
    for (i=0; i < str.length; i++) {
        hex = str.charCodeAt(i).toString(16);
        result += ("000"+hex).slice(-2);
    }

    return result;
}

function validateIp(value){
  var split = value.split('.');
  if (split.length != 4)
  return false;

  for (var i=0; i<split.length; i++) {
    var s = split[i];
    if (s.length==0 || isNaN(s) || s<0 || s>255)
    return false;
  }
  return true;
}

/*
  Blockly functions
*/

var workspace = null;
var isChanged = false;
var editable_code = false;
var user_code = "";

function loadToolBox(){
  var blocklyDiv = document.getElementById("blocklyDiv");
  workspace = Blockly.inject(blocklyDiv,
    {toolbox: document.getElementById('toolbox'),
     scrollbars: true,
     rtl: false,
     zoom:
         {enabled: true,
          controls: true,
          wheel: true,
          maxScale: 4,
          minScale: .25,
          scaleSpeed: 1.1
         },
     grid:
         {spacing: 25,
          length: 3,
          colour: '#ccc',
          snap: false},
     trashcan: true});

     restorelocal();
}

function tojavascript(){
  Blockly.JavaScript.addReservedWords('code');
  var code = Blockly.JavaScript.workspaceToCode(workspace);
  try {
    //eval(code);
    alert(code);
  } catch (e) {
    alert(e);
  }
};

function tophp(){
  Blockly.JavaScript.addReservedWords('code');
  var code = Blockly.PHP.workspaceToCode(workspace);
  try {
    //eval(code);
    alert(code);
  } catch (e) {
    alert(e);
  }
};

function topython(){
  Blockly.Python.addReservedWords('code');
  var code = Blockly.Python.workspaceToCode(workspace);
  try {
    //eval(code);
    alert(code);
  } catch (e) {
    alert(e);
  }
};

// hide blockly and show the code
function hide_blockly() {
  document.getElementById("blocklyDiv").style.display = 'none';
  document.getElementById("blocklyArea").style.display = 'none';
  document.getElementById("editor").style.display = 'block';
  var toolbarDiv = document.getElementById("toolbar");
  Blockly.Python.addReservedWords('code');
  var code = Blockly.Python.workspaceToCode(workspace);
  var editor = ace.edit("editor");
  editor.getSession().setMode("ace/mode/python");
  editor.getSession().setUseWrapMode(true);
  editor.setShowPrintMargin(true);
  toolbarDiv.style.display = "block";
  if (editable_code == false) {
    editor.setValue(code)
    editor.setTheme("ace/theme/chrome");
    document.getElementById("toolbar_reset_btn").disabled = true;
  }
  else {
    editor.setTheme("ace/theme/terminal");
    editor.setValue(user_code);
  }

  window.dispatchEvent(new Event('resize'));
};

function toggleEditCode() {
  var editor = ace.edit("editor");
  var toolbarDiv = document.getElementById("toolbar");
  if (editable_code == false) {
    editable_code = true;
    editor.setValue(user_code)
    editor.setTheme("ace/theme/terminal");
    document.getElementById("toolbar_reset_btn").disabled = false;
  }
  else {
    editable_code = false;
    user_code = editor.getValue();
    Blockly.Python.addReservedWords('code');
    var code = Blockly.Python.workspaceToCode(workspace);
    editor.setValue(code);
    editor.setTheme("ace/theme/chrome");
    document.getElementById("toolbar_reset_btn").disabled = true;
  }
}

function load_code(from_file) {
  var editor = ace.edit("editor");
  user_code = from_file;
  if (editable_code == true) {
    editor.setValue(user_code);
  }
}

function blocklyToUser() {
  var editor = ace.edit("editor");
  Blockly.Python.addReservedWords('code');
  code = Blockly.Python.workspaceToCode(workspace);
  editor.setValue(code);
}

function sim_play() {
  var editor = ace.edit("editor");
  if (editable_code == false) {
    ExecutionLogicModule.launch_block_code();
  }
  else {
    user_code = editor.getValue();
    ExecutionLogicModule.launch_user_code(user_code);
  }
}

function show_blockly() {
  var toolbarDiv = document.getElementById("toolbar");
  var editor = ace.edit("editor");
  if (editable_code == true){
    user_code = editor.getValue();
  }
  editable_code = false;
  document.getElementById("blocklyDiv").style.display = 'block';
  document.getElementById("blocklyArea").style.display = 'block';
  document.getElementById("editor").style.display = 'none';
  window.dispatchEvent(new Event('resize'));
  toolbarDiv.style.display = "none";
};

function save_project() {
  var editor = ace.edit("editor");
  if (editable_code == true) {
    user_code = editor.getValue();
  }
  ExecutionLogicModule.save_to_file(user_code)
}

// restore at the beginning.
// This is launched after the page has finished loading
function restorelocal(){
  var xml_text = localStorage.getItem("blocks_cache");
  try {
    var xml = Blockly.Xml.textToDom(xml_text);
    Blockly.Xml.domToWorkspace(workspace, xml);
    automate_localstorage();
  }
  catch(err) {
      // alert(err);
      console.log(err);
      // console.log("This is generally because there's no tree information");
      automate_localstorage();
  }

  ExecutionLogicModule.launch_websockets(9000);
  // Recursively store everything after x miliseconds
  // automate_localstorage();
}

function automate_localstorage(){
    localstorage();
    setTimeout(automate_localstorage, 120000); 
}

// Save stuff on local storage
function localstorage() {
  var xml = Blockly.Xml.workspaceToDom(workspace);
  var xml_text = Blockly.Xml.domToText(xml);
  localStorage.setItem("blocks_cache", xml_text);
  console.log("Saved: "+xml_text);
  console.log("-------------");
  var xml_text_stored = localStorage.getItem("blocks_cache");
  console.log("Rtved: "+xml_text_stored)
  // alert("Saved: "+xml_text);
}

// document.getElementById('editor').style.fontSize='16px';
// document.onkeyup = function(e) {
//   if (e.which == 77) {
//     alert("M key was pressed"); 
//   } else if (e.ctrlKey && e.which == 66) {
//     console.log("Ctrl + B shortcut combination was pressed");
//     alert("Ctrl + B shortcut combination was pressed");
//   } else if (e.ctrlKey && e.altKey && e.which == 89) {
//     alert("Ctrl + Alt + Y shortcut combination was pressed");
//   } else if (e.ctrlKey && e.altKey && e.shiftKey && e.which == 85) {
//     alert("Ctrl + Alt + Shift + U shortcut combination was pressed");
//   }
// };

function stopRunning(){
  ExecutionLogicModule.end_execution();
  ExecutionLogicModule.launch_websockets('9000');
}
 