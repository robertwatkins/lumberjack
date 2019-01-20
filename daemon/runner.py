#!/usr/local/bin/python3
import sys, time, requests, json
from daemon import Daemon

class Runner(Daemon):
    apiServer = "http://127.0.0.1:8888"

    def getNextAgentToRun(self):
        return None

    def runAgent(self,id):
        print("Starting Agent: " + str(id))

    def run(self):
        while True:
            print("Searching for Agent to Run.")
            agentID = self.getNextAgentToRun()
            if agentID is not None:
                print('Starting to train agent with id ' + str(agentID))
                self.runAgent(agentID)
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
