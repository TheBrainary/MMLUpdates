
var ExecutionLogicModule = (function () {

  var CODE_STATUS = {
    RUNNING: "running",
    PAUSED: "paused",
    COMPLETED: "completed",
    NOT_CONNECTED: "not_connected"
  };

  var END_BUTTON_ID = "end_button";
  var REFRESH_BUTTON_ID = "refresh_button";
  var LAUNCH_LABEL_ID = "debugarea";
  var current_status = CODE_STATUS.NOT_CONNECTED;
  var current_block = null;
  var socket = null;

  function update_launch_button() {
    var launch_button = document.getElementById(LAUNCH_LABEL_ID);
    switch (current_status) {
      case CODE_STATUS.PAUSED:
        //launch_button.innerHTML = "Resume";
        break;

      case CODE_STATUS.RUNNING:
        //launch_button.innerHTML = "Pause";
        break;

      case CODE_STATUS.COMPLETED:
        //launch_button.innerHTML = "Launch";
        break;

      case CODE_STATUS.NOT_CONNECTED:
        //launch_button.innerHTML = "Server is down";
        break;

      default:
        console.log('Unknown current status: ' + current_status);
        break;
    }
  }

  function update_workspace() {
    var blocks_tab_selector = "a[href='#home'][data-toggle='tab']";
    var python_tab_selector = "a[href='#profile'][data-toggle='tab']";
    var graph_tab_selector = "a[href='graph.html']";
    var load_from_file_button_selector = "a[id='load_from_file_button']";
    var save_to_file_button_selector = "a[id='save_to_file_button']";
    var end_button_selector = "a[id='end_button']";
    var clean_ws_button_selector = "a[id='clean_ws_button']";
    var manual_mode_button_selector = "a[id='manual_mode_button']";
    var pythondiv_selector = "div[id='pythondiv']";

    switch (current_status) {
      case CODE_STATUS.PAUSED:
      case CODE_STATUS.RUNNING:
        workspace.options.readOnly = true;
        // if (null != workspace.toolbox_) {
        //   workspace.toolbox_.HtmlDiv.hidden = true;
        // }
        // $(blocks_tab_selector).hide();
        // $(python_tab_selector).hide();
        // $(graph_tab_selector).hide();
        // $(load_from_file_button_selector).hide();
        // $(save_to_file_button_selector).hide();
        // $(end_button_selector).show();
        // $(clean_ws_button_selector).hide();
        // $(manual_mode_button_selector).hide();
        // $(pythondiv_selector).hide();

        break;

      case CODE_STATUS.COMPLETED:
      case CODE_STATUS.NOT_CONNECTED:
        current_block = null;
        var blocks = workspace.getAllBlocks();
        for (var i = 0; i < blocks.length; i++) {
          blocks[i].setShadow(false);
        }
        workspace.options.readOnly = false;
        if (null != workspace.toolbox_) {
          workspace.toolbox_.HtmlDiv.hidden = false;
        }
        $(blocks_tab_selector).show();
        $(python_tab_selector).show();
        $(graph_tab_selector).show();
        $(load_from_file_button_selector).show();
        $(save_to_file_button_selector).show();
        $(end_button_selector).hide();
        $(clean_ws_button_selector).show();
        $(manual_mode_button_selector).show();
        $(pythondiv_selector).show();

        break;

      default:
        console.log('Unknown current status: ' + current_status);
        break;
    }
  }

  function set_current_status(value) {
    var statuses = [CODE_STATUS.COMPLETED, CODE_STATUS.RUNNING, CODE_STATUS.PAUSED, CODE_STATUS.NOT_CONNECTED];
    if (0 > statuses.indexOf(value)) {
      console.log('Unknown status: ' + value);
      return;
    }
    current_status = value;
    update_launch_button();
    update_workspace();
  }

  function set_current_block_id(block_id) {
    if ([CODE_STATUS.RUNNING, CODE_STATUS.PAUSED].indexOf(current_status) >= 0) {
      var selected_block = workspace.getBlockById(block_id);
      if (null != selected_block) {
        if (null != current_block) {
          current_block.setShadow(false);
        }
        selected_block.setShadow(true);
        current_block = selected_block;
      } else {
        console.log('Not existing block id: ' + block_id);
      }
    } else {
      console.log('Code is not running. Ignoring current block changed event.')
    }
  }

  function is_connection_closed() {
    return (CODE_STATUS.NOT_CONNECTED == current_status);
  }

  return {

    launch_websockets: function (host_port) {
      var host_name = window.location.hostname;
      var mainhost = host_name.split('-');

      var x = window.location.hostname;
      var y = x.includes('codio');
      if (y) {
        socket = new WebSocket("wss://" + mainhost[0] + '-' + mainhost[1] + "-9000.codio.io");
      }else{
        socket = new WebSocket("ws://" + host_name + ":" + host_port);
      }

      socket.binaryType = "arraybuffer";

      socket.onopen = function () {
        console.log("Connected!");
        set_current_status(CODE_STATUS.COMPLETED);
      };

      socket.onmessage = function (e) {
        if (typeof e.data == "string") {
          //console.log("Text message received: " + e.data);
          var message_data = e.data.split('\n');
          var method_name = '';
          var method_data = '';
          if (message_data.length > 0) {
            method_name = message_data[0];
            if (message_data.length > 1) {
              method_data = message_data[1];
            }
          }

          switch (method_name) {
            case 'set_current_block':
              set_current_block_id(method_data);
              if (CODE_STATUS.COMPLETED == current_status) {
                set_current_status(CODE_STATUS.RUNNING);
              }
              break;

            case 'status_update':
              set_current_status(method_data);
              break;

            default:
              console.log('Unknown method: ' + method_name);
              break;
          }
        } else {
          var arr = new Uint8Array(e.data);
          var hex = '';
          for (var i = 0; i < arr.length; i++) {
            hex += ('00' + arr[i].toString(16)).substr(-2);
          }
          console.log("Binary message received: " + hex);
        }
      };

      socket.onclose = function (e) {
        socket = null;
        set_current_status(CODE_STATUS.NOT_CONNECTED);
        console.log("Connection closed. Reason: " + e.reason);
      };
    },

    launch_user_code: function (user_code) {
      if (is_connection_closed()) {
        console.log("Connection not opened.");
        return;
      }
      var message_data = 'user_code\n';
      if (user_code.length == 0){
        user_code = 'pass\n'
      }
      message_data += user_code
      if (message_data.length > 0) {
        socket.send(message_data);
        console.log("Text message sent.");
      }
    },

    launch_block_code: function () {

      if (is_connection_closed()) {
        console.log("Connection not opened.");
        return;
      }
      var message_data = '';
      switch (current_status) {
        case CODE_STATUS.COMPLETED:
          message_data = 'block_code\n';
          Blockly.Python.addReservedWords('code');
          var saved_statement_prefix = Blockly.Python.STATEMENT_PREFIX;
          try {
            Blockly.Python.STATEMENT_PREFIX = 'check_status(%1)\n';
            var code = Blockly.Python.workspaceToCode(workspace);
            if (0 == code.length) {
              code = 'pass\n'
            }
            message_data += '\ntry:\n' + Blockly.Python.prefixLines(code, Blockly.Python.INDENT) + '\nfinally:\n' +
              Blockly.Python.INDENT + 'send_status_completed()\n';
          }
          finally {
            Blockly.Python.STATEMENT_PREFIX = saved_statement_prefix;
          }
          set_current_status(CODE_STATUS.RUNNING);
          break;

        case CODE_STATUS.RUNNING:
          set_current_status(CODE_STATUS.PAUSED);
          message_data = "pause";
          break;

        case CODE_STATUS.PAUSED:
          set_current_status(CODE_STATUS.RUNNING);
          message_data = "resume";
          break;

        default:
          console.log("Unknown status: " + current_status);
          break;
      }

      if (message_data.length > 0) {
        socket.send(message_data);
        console.log("Text message sent.");
      }
    },

    load_from_file: function() {
      var can_load_file = false;
      if (workspace.getAllBlocks().length > 0) {
        can_load_file = confirm("Current workspace is not empty. Do you want to override it?");
      } else {
        can_load_file = true;
      }

      if (true == can_load_file) {
        var input_field_name = 'load_workspace_from_file_input';
        var file_input = document.getElementById(input_field_name);
        if (null == file_input) {
            file_input = document.createElement('input');
            file_input.type = 'file';
            file_input.accept = ".mirocode";
            file_input.id = input_field_name;
            file_input.name = input_field_name;
            file_input.addEventListener('change',
                      function (evt) {
                          var files = evt.target.files;
                          if (files.length > 0) {
                              var file = files[0];
                              var extension = file.name.substr(file.name.lastIndexOf('.')+1,file.name.length);
                              if (extension == "mirocode"){
                                var reader = new FileReader();
                                reader.onload = function () {
                                    var split_file = this.result.split("\nend_of_xml\n");
                                    if (split_file[0] == this.result) {
                                      alert("\"" + file.name + "\" appears to be corrupted.");
                                      return;
                                    }
                                    var xml_file = split_file[0];
                                    var python_code = split_file[1];
                                    workspace.clear();
                                    xml = Blockly.Xml.textToDom(xml_file);
                                    console.log("Loading workspace from file.");
                                    Blockly.Xml.domToWorkspace(workspace, xml);
                                    load_code(python_code);
                                };
                                reader.readAsText(file);
                              }
                              else {
                                alert("\"" + file.name + "\" is not a valide file type. Please select a \".mirocode\" file");
                              }
                              document.body.removeChild(file_input);
                          }
                      }, false);
            // Hidding element from view
            file_input.style = 'position: fixed; top: -100em';
        document.body.appendChild(file_input);
        }
        file_input.click();
      }
      var burger_button = document.getElementById("burger");
      burger(burger_button);
    },

    save_to_file: function(user_code) {
      var proceed = false;
      var filename = "";
      while (!proceed) {
        filename = prompt("Name your project:", "my_miro_code");
        if (typeof(filename) == "string") {
          if (filename == "") {
            proceed = false;
            alert("Invalid Entry");
          }
          else {
            proceed = true;
          }
        }
        if (filename === null) {
          proceed = false;
          break;
        }
      }
      if (proceed){
        var xml = Blockly.Xml.workspaceToDom(workspace);
        var xml_text = Blockly.Xml.domToText(xml);
        var prj_txt = xml_text + "\nend_of_xml\n" + user_code;
        var prj_blob = new Blob([prj_txt], {type: 'text/mirocode'});
        if (window.navigator.msSaveOrOpenBlob) {
            window.navigator.msSaveBlob(prj_blob, filename + ".mirocode");
          } else {
            var elem = window.document.createElement('a');
            elem.href = window.URL.createObjectURL(prj_blob);
            elem.download = filename + ".mirocode";
            document.body.appendChild(elem);
            elem.click();
            document.body.removeChild(elem);
          }
          console.log("Project Saved.");
        }
        var burger_button = document.getElementById("burger");
        burger(burger_button);
      },

    end_execution: function() {
      var end_button = document.getElementById(END_BUTTON_ID);
      var launch_button = document.getElementById(LAUNCH_LABEL_ID);
      var refresh_button = document.getElementById(REFRESH_BUTTON_ID);
      if (is_connection_closed()) {
          console.log("Connection not opened.");
          return;
      }
      //launch_button.firstChild.data = "EXECUTION CANCELED";
      //launch_button.onclick = null;

      //end_button.style.display = "none";
      //refresh_button.style.display = "block";

      var message_data = 'end';
      socket.send(message_data);
      console.log("Text message sent.");
    },

    clean_ws: function() {
      workspace.clear();
      console.log("Workspace cleaned.");
      var burger_button = document.getElementById("burger");
      burger(burger_button);
    },

    manual_control: function(robot){

        workspace.options.readOnly = true;

        var blocks_tab_selector = "a[href='#home'][data-toggle='tab']";
        var python_tab_selector = "a[href='#profile'][data-toggle='tab']";
        var builder_selector = "a[id='builder']";
        var graph_tab_selector = "a[href='graph.html']";
        var control_spider_button_selector = "a[id='control_spider_button']";
        var control_rover_button_selector = "a[id='control_rover_button']";
        var stop_control_button_selector = "a[id='stop_control_button']";

        $(blocks_tab_selector).hide();
        $(python_tab_selector).hide();
        $(builder_selector).hide();
        $(graph_tab_selector).hide();
        $(stop_control_button_selector).show();

        document.getElementsByClassName('blocklyToolboxDiv')[0].style.visibility='hidden';


        if (robot.toString() == "spider"){
            $(control_rover_button_selector).hide();
            document.getElementById("blocklyDiv").innerHTML = "<div style='margin-left:30px; width:100%;'><img src='/pages/img/ErleSpider_W4.jpg' width='400'><br><img src='/pages/img/keys_spider.png' width='400'></div>";

            $(document).keydown(function(e) {
                switch(e.which) {
                    case 37: // left
                        console.log("left.");
                        var message_data = 'control_spider_left';
                        socket.send(message_data);
                    break;
                    case 38: // up
                        console.log("up.");
                        var message_data = 'control_spider_up';
                        socket.send(message_data);
                    break;

                    case 39: // right
                        console.log("right.");
                        var message_data = 'control_spider_right';
                        socket.send(message_data);
                    break;
                    case 40: // down
                        console.log("down.");
                        var message_data = 'control_spider_down';
                        socket.send(message_data);
                    break;
                    case 27: // ESC
                        console.log("ESC.");
                        var message_data = 'end';
                        socket.send(message_data);
                        window.location.href = "../index.html";
                    break;

                    default: return; // exit this handler for other keys
                }
                e.preventDefault(); // prevent the default action (scroll / move caret)
            });
        }
        if (robot.toString() == "rover"){
            $(control_spider_button_selector).hide();
            document.getElementById("blocklyDiv").innerHTML = "<div style='margin-left:30px; width:100%;'><img src='/pages/img/caution.png' width='400'><br><img src='/pages/img/ErleRover_W6.jpg' width='400'><br><img src='/pages/img/keys_spider.png' width='400'></div>";

            $(document).keyup(function(r) {
                    switch(r.which) {
                        case 37: // left
                            console.log("left.r");
                            var message_data = 'control_rover_left';
                            socket.send(message_data);
                        break;
                        case 38: // up
                            console.log("up.r");
                            var message_data = 'control_rover_up';
                            socket.send(message_data);
                        break;
                        case 39: // right
                            console.log("right.r");
                            var message_data = 'control_rover_right';
                            socket.send(message_data);
                        break;
                        case 40: // down
                            console.log("down.r");
                            var message_data = 'control_rover_down';
                            socket.send(message_data);
                        break;
                        case 27: // ESC
                            console.log("ESC.r");
                            var message_data = 'end';
                            socket.send(message_data);
                            window.location.href = "../index.html";
                        break;

                        default: return; // exit this handler for other keys
                    }
                r.preventDefault(); // prevent the default action (scroll / move caret)
            });
        }
        if (robot.toString() == "stop"){
            var message_data = 'end';
            socket.send(message_data);
            window.location.href = "../index.html";
            //location.reload();
        }


        console.log("Manual control selected.");
    }

  };
})();
