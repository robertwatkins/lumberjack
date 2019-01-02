//fetch('http://localhost:8888/agents/1')
//  .then(function(response) {
//    return response.json();
//  })
//  .then(function(myJson) {
//    console.log(JSON.stringify(myJson));
//  });

function get_agent(id){
fetch('http://localhost:8888/agents/1')
  .then(function(response) {
      return response.json();
  })
  .then(function(myJson) {
    return (JSON.stringify(myJson));
  });
}

//console.log('Calling get_agent(1)' + ":" + get_agent(1));