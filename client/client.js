
function process_create_agent_modal(){
  default_agent_type = "Apache";
  default_notification_channel = "";
  default_running_status = "Not Running";
  default_training_status = "";

  var form = document.forms["createAgentModalForm"]
  json = '{"agent":[{"agent_name":"' + form["agentname"].value + '","agent_type":"' + default_agent_type + '","log_path":"'+form["logpath"].value +'","running_status":"'+ default_running_status+'","skill_type":"'+form["skill"].value+'", "notification_channel":"'+ default_notification_channel+'", "training_status": "' + default_training_status + '"}]}';
  add_agent(json);
}

function delete_agent(id){
    fetch('http://localhost:8888/agents/' + id,{
        method: 'delete'
    }).then(function(response) {
      return response.json();
  })
  .then(res => update_display());
}

function add_agent(json){
  console.log(json);
  fetch('http://localhost:8888/agents', {
    method: 'post',
    headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
    },
    //body: JSON.stringify(json)
    body: json
    }).then(res=>res.json())
    .then(res => console.log(res))
    .then(res => update_display());
  close_modal("createAgentModal");
}

function display_agent(json){
    console.log(json);
    var agent_table = document.getElementById("agentTable");
    var table_len=(agent_table.rows.length);
    var agent_name = json.agent[0].agent_name;
    var agent_type = json.agent[0].agent_type;
    var log_path = json.agent[0].log_path;
    var skill_type = json.agent[0].skill_type;
    var agent_id = json.agent[0].agent_id;
    var agent_row = agent_table.insertRow(table_len).outerHTML="<tr><td>"+agent_name+"<br>Type: "+agent_type+"</td><td>Log Path: "+log_path+"<br>Skill: "+skill_type+"</td><td><i class='fas fa-trash' onclick='delete_agent("+ agent_id +");'></i></td></tr>";

    var activate_agent_table = document.getElementById("activateAgentTable");
    var notification_channel = json.agent[0].notification_channel;
    var activate_agent_row = activate_agent_table.insertRow(table_len).outerHTML="<tr><td>" + agent_name + "</td><td>Enabled: <i class='fas fa-toggle-on'></i><br>Notification: " + notification_channel + "</td></tr>";
}

function get_agent(id){
fetch('http://localhost:8888/agents/' + id)
  .then(function(response) {
      return response.json();
  })
  .then(function(myJson) {
    display_agent(myJson);
  });
}

function display_agents(json){
    console.log(json );//+ " : " + agents_json.agents.length);
    for(var i = 0; i < (json.agents.length); i++) {
        var id = json.agents[i];
        get_agent(id);
    }
    get_notification_channels();
}

function get_agents(){
fetch('http://localhost:8888/agents')
  .then(function(response) {
      return response.json();
  })
  .then(function(myJson) {
    display_agents(myJson);
  });
}

function delete_channel(id){
    fetch('http://localhost:8888/notification_channels/' + id,{
        method: 'delete'
    }).then(function(response) {
      return response.json();
  })
  .then(res => update_display());
}


function get_notification_channel(id){
fetch('http://localhost:8888/notification_channels/' + id)
  .then(function(response) {
      return response.json();
  })
  .then(function(myJson) {
    display_notification_channel(myJson);
  });
}

function display_notification_channels(json){
    console.log(json);
        for(var i = 0; i < (json.notification_channels.length); i++) {
        var id = json.notification_channels[i];
        get_notification_channel(id);
    }
 }

 function display_notification_channel(json){
   var notification_table = document.getElementById("notificationChannelTable");
   var table_len=(notification_table.rows.length);
   var row = json.notification_channels[0].channel_id;
   var channel_name = json.notification_channels[0].channel_name;
   var channel_type = json.notification_channels[0].channel_type;
   var configuration = json.notification_channels[0].configuration;
   var channel_id = json.notification_channels[0].channel_id;
   var row = notification_table.insertRow(table_len).outerHTML="<tr><td>"+channel_name+"<br>Type: "+channel_type+"</td><td>url: "+configuration+"</td><td><i class='fas fa-trash' onclick='delete_channel("+ channel_id +");'></i></td></tr>";
}

function get_notification_channels(){
fetch('http://localhost:8888/notification_channels')
  .then(function(response) {
      return response.json();
  })
  .then(function(myJson) {
    display_notification_channels(myJson);
  });
}

function update_display(){
    var table = document.getElementById("agentTable")
    table.innerHTML = "";
    document.getElementById("activateAgentTable").innerHTML = "";
    document.getElementById("notificationChannelTable").innerHTML = "";
    get_agents();
}

function close_modal(id){
  document.getElementById(id).style.display='none'
}
