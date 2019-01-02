

function display_agent(agent_json){
    console.log(agent_json);
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