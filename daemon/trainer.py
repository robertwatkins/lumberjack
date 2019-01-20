#!/usr/local/bin/python3
import sys, time, requests, json
from daemon import Daemon

class MyDaemon(Daemon):
    apiServer = "http://127.0.0.1:8888"

    def getNextAgentToTrain(self):
        url = self.apiServer+'/agents'
        response = json.loads(requests.get(url).content)
        id = None
        for check_id in response["agents"]:
            url = self.apiServer+"/agents/"+str(check_id)
            agentInfo = json.loads(requests.get(url).content)
            print(agentInfo)
            training_status = agentInfo["agent"][0]["training_status"]
            # training status starts as a string, so converting to integer failing means
            # we haven't started training (yes, this is a code smell)
            try:
                int(training_status)
            except:
                id = check_id

        print("ID to train: " + str(id))
        return id

    def trainAgent(self,id):
        url = self.apiServer+"/agents/"+str(id)
        response = json.loads(requests.get(url).content)
        print("From: " + json.dumps(response))
        response["agent"][0]["training_status"] = str(100)
        print("To:   " + json.dumps(response))
        headers = json.loads('{"Content-Type": "application/json"}')
        requests.put(url, data=json.dumps(response), headers=headers)

    def run(self):
        while True:
            print("Searching for Agent to Train.")
            trainingID = self.getNextAgentToTrain()
            if trainingID is not None:
                print('Starting to train agent with id ' + str(trainingID))
                self.trainAgent(trainingID)
            else:
                time.sleep(30);


if __name__ == "__main__":
    daemon = MyDaemon('/tmp/trainer.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
