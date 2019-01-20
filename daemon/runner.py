#!/usr/local/bin/python3
import sys, time, requests, json
from daemon import Daemon

class Runner(Daemon):
    apiServer = "http://127.0.0.1:8888"

    def getAgentsToRun(self):
        url = self.apiServer+'/agents'
        response = json.loads(requests.get(url).content)
        id = None
        agentList = []
        for check_id in response["agents"]:
            url = self.apiServer+"/agents/"+str(check_id)
            agentInfo = json.loads(requests.get(url).content)
            print(agentInfo)
            running_status = agentInfo["agent"][0]["running_status"]
            if (running_status == "Running"):
                agent_id = agentInfo["agent"][0]["agent_id"]
                agentList.append(agent_id)

        print("Agents to run: " + str(agentList) )
        return agentList

    def runAgents(self,agentList):
        print("Starting Agents: " + str(agentList))
        while True:
            for agent_id in agentList:
                self.runAgent(agent_id)


    def runAgent(self,agent_id):
        print("Running Agent " + str(agent_id))
        payload = {
            "username": "lumberjack",
            "text": "Lumberjack Test Log Alert for agent " + str(agent_id) ,
            "attachments": [
                {
                    "author_name": "Owner: rwatkins",
                    "title": "Alert Details",
                    "text": "Connection from 201.1.41.241 at 11:57am cannot be classified as expected usage.\n"
                            + "Additional Details:\n"
                            + "First connection:10:49am\n"
                            + "Average Request Size: 930b\n"
                            + "Max Request Size: 4Mb\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                            + "more?\n"
                }
            ]
        }
        url = self.getSlackForAgent(agent_id)
        while True:
            self.postToSlack(url,payload)
            time.sleep(10)

    def getSlackForAgent(self, agent):
        file = open('/tmp/slack.txt', 'r')
        return file.read()


    def postToSlack(self, slackUrl, payload):
        data_json = json.dumps(payload)
        headers = {'Content-type': 'application/json'}
        response = requests.post(slackUrl, data=data_json, headers=headers)
        print(response)


    def run(self):
        while True:
            print("Searching for Agent to Run.")
            agentID = self.getAgentsToRun()
            if agentID is not None:
                print('Starting to run agent with id ' + str(agentID))
                self.runAgents(agentID)
            else:
                time.sleep(30);

if __name__ == "__main__":
    daemon = Runner('/tmp/runner.pid')
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
