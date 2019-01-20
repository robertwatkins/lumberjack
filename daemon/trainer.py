#!/usr/bin/python
import sys, time
from daemon import Daemon


class MyDaemon(Daemon):
    def getNextAgentToTrain(self):
        pass

    def trainAgent(self,id):
        pass

    def run(self):
        while True:
            print("Searching for Agent to Train.")
            trainingID = self.getNextAgentToTrain()
            if trainingID is not None:
                print('Starting to train agent with id ' + trainingID)
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
