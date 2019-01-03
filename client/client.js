

function display_agent(json){
    console.log(json);
    var agent_table = document.getElementById("agentTable");
    var table_len=(agent_table.rows.length);
    var agent_name = json.agent[0].agent_name;
    var agent_type = json.agent[0].agent_type;
    var log_path = json.agent[0].log_path;
    var skill_type = json.agent[0].skill_type;
    var row = agent_table.insertRow(table_len).outerHTML="<tr><td>"+agent_name+"<br>Type: "+agent_type+"</td><td>Log Path: "+log_path+"<br>Skill: "+skill_type+"</td></tr>";
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

function display_agents(agents_json){
    console.log(agents_json);
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


function display_notification_channels(json){
    console.log(json);
    var notification_table = document.getElementById("notificationChannelTable");
    var table_len=(notification_table.rows.length);
    var channel_name = json.notification_channels[0].channel_name;
    var channel_type = json.notification_channels[0].channel_type;
    var configuration = json.notification_channels[0].configuration;
    var row = notification_table.insertRow(table_len).outerHTML="<tr><td>"+channel_name+"<br>Type: "+channel_type+"</td><td>url: "+configuration+"</td></tr>";
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


get_agents();
get_agent(1);
get_notification_channels();