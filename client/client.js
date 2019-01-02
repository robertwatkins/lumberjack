

function display_agent(agent_json){
    console.log(agent_json);
    var agent_table = document.getElementById("agentTable");
    var table_len=(agent_table.rows.length);
    var agent_name = "test";
    var agent_type = "test";
    var log_path = "test";
    var skill_type = "test";
    var row = agent_table.insertRow(table_len).outerHTML="<tr><td>"+agent_name+"<br>Type: "+agent_type+"</td><td>Log Path: "+log_path+"<br>Skill: "+skill_type+"</td></tr>";
}

function get_agent(id){
fetch('http://localhost:8888/agents/' + id)
  .then(function(response) {
      return response.json();
  })
  .then(function(myJson) {
    display_agent(JSON.stringify(myJson));
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
    display_agents(JSON.stringify(myJson));
  });
}


function display_notification_channels(notification_channels_json){
    console.log(notification_channels_json);

}

function get_notification_channels(){
fetch('http://localhost:8888/notification_channels')
  .then(function(response) {
      return response.json();
  })
  .then(function(myJson) {
    display_notification_channels(JSON.stringify(myJson));
  });
}


get_agents();
get_agent(1);
get_notification_channels();