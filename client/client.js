
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

function start_agent(id){
  url = 'http://localhost:8888/agents/'+id;
  fetch('http://localhost:8888/agents/' + id + "/activation/start", {
    method: 'post'
    }).then(res=>res.json())
    .then(res => console.log(res))
    .then(res => update_display());

}

function stop_agent(id){
  url = 'http://localhost:8888/agents/'+id;
  fetch('http://localhost:8888/agents/' + id + "/activation/stop", {
    method: 'post'
    }).then(res=>res.json())
    .then(res => console.log(res))
    .then(res => update_display());

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
    var training_status = json.agent[0].training_status;
    var agent_row = agent_table.insertRow(table_len).outerHTML="<tr><td><b>"+agent_name+"</b><br>Type: "+agent_type+"<br>Training Status:<div class='chart-container' style='position: relative; height:30px; width:30px;responsive:false;'><canvas id='trainingChart_" + agent_id + "' width='30' height='30' style='flex:none;'></canvas></div></td><td>Log Path: "+log_path+"<br>Skill: "+skill_type+"</td><td><i class='fas fa-trash' onclick='delete_agent("+ agent_id +");'></i></td></tr>";
    if (training_status == ""){
         training_percent_complete = 0;
    }
    else if (training_status == "Done") {
         training_percent_complete = 100;
    }
    else {
         training_percent_complete = training_status;
    }

    showTrainingProgress(agent_id,training_percent_complete);
    var activate_agent_table = document.getElementById("activateAgentTable");
    var notification_channel = json.agent[0].notification_channel;
    var running_status = json.agent[0].running_status;
    var onclick = "";
    var toggle = "";
    if (running_status  == "Running") {
        toggle = "fa-toggle-on greeniconcolor";
        onclick = "onclick='stop_agent(" + agent_id + ");'"
    } else { if (training_status != "100") {
            toggle = "fa-toggle-off grayiconcolor";
        } else {
            toggle = "fa-toggle-off greeniconcolor";
            onclick = "onclick='start_agent(" + agent_id + ");'"
        }
    }


    var activate_agent_row = activate_agent_table.insertRow(table_len).outerHTML="<tr><td><b>" + agent_name + "</b></td><td>Enabled: <i " + onclick + " class='fas " + toggle + "'></i><br>Notification: " + notification_channel + "</td></tr>";
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

function showTrainingProgress(id,complete){
    ctx = document.getElementById("trainingChart_"+id).getContext("2d");
    ctx.canvas.width = 30;
    ctx.canvas.height = 30;
    data = {
        datasets: [{
            data: [0, 100],
            backgroundColor: ['green', 'lightgray']
        }],
        labels:['Complete','Incomplete']
    };

     options = {
        cutoutPercentage: 50,
        legend: {
                display: false
        }
    };
    console.log(complete);
    console.log(100 - complete);
    console.log(data)
    data.datasets[0].data[0]=complete;
    data.datasets[0].data[1]=100 - complete;
    console.log(data)
    var myPieChart = new Chart(ctx,{
        type: 'pie',
        data: data,
        options: options
    });
};