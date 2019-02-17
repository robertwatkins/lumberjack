#!/usr/local/bin/python3
import sys, os

apiServer = "http://127.0.0.1:8888"
trainingDir = "/trainingdata"
testDataDir = "/testdata"

def train(path):
    print('in apache trainer: path='+path)
    if sanityCheckPath(path):
        isSuccessful = start(path)
    else:
        return False
    return isSuccessful

def start(path):
    pass

def sanityCheckPath(path):
    isValidTrainingDir = os.access(path+trainingDir, os.R_OK)
    print("Is Training Directory  " + path + trainingDir + " valid? " + str(isValidTrainingDir))
    isValidTestDataDir = os.access(path+testDataDir, os.R_OK)
    print("Is Test Data Directory " + path + testDataDir + " valid? " + str(isValidTrainingDir))
    return isValidTrainingDir and isValidTestDataDir

if __name__ == '__main__':
    train(sys.argv[1])
