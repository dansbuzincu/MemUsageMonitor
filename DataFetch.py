# DATA FETCH
from concurrent.futures import process
from enum import Enum
from datetime import date, datetime
from genericpath import isdir
from mimetypes import init
import os
import subprocess
import psutil

# Sample once a second (1000ms)
SAMPLE_TIME = 1

# Monitor the last 5 hours (5*60min)
# That results in 300 * Sample Frequency(per second)
MAX_SIZE = 1 * 5 * 60

class taskData():
    def __init__(self, pid):
        self.pidNr = pid
        self.proc = psutil.Process(pid)
        self.cpuUsage = self.proc.cpu_percent(interval=0.01)
        self.memUsage = self.proc.memory_percent()
        self.timestamp = datetime.now()
    def printData(self):
        print("At : " + str(self.timestamp)  + " for pid: " + str(self.pidNr) + " Mem Usage: " + str(self.memUsage) + "; CPU Usage: " + str(self.cpuUsage))

class pidStruct():
    def __init__(self, inputPid):
        self.pid = inputPid
        # self.cpuUsageList = []
        # self.memUsageList = []
        self.resourceDataList = []
    def appendTaskData(self, data):
        self.resourceDataList.append(data)
        # self.cpuUsageList.append(data.cpuUsage)
        # self.memUsageList.append(data.memUsage)
    def printDataAt(self, index):
        if index < len(self.resourceDataList):
            self.resourceDataList[index].printData()
        else:
            print("Index error!!!")

class dataProcessor():
    def __init__(self):
        self.pidList = []

engine = dataProcessor()

# GENERATE TASK FOR THE DATE AND TIME REQUESTED
def snapshot():
    # Create the path for logs folder of a single day
    # For every day a log file wil be generated once a minute
    # cwdString = os.getcwd()
    # currentDate = date.today().strftime("%d-%m-%Y")
    # logsPathString = cwdString + "/"
    # logsPath = os.path.join(logsPathString, currentDate)
    
    # # Check if folder already exists
    # if os.path.isdir(logsPath) == False:
    #     os.makedirs(logsPath)
    # else:
    #     print("FOLDER ALREADY EXISTS!!!")
    
    # # Data should be stored in batches of logs at occurence wanted(1 log a minute)
    # currentHour = datetime.now().strftime("%H-%M-%S")
    # cmdCommString = "tasklist > " + currentDate + "/" + currentHour +".txt"
    # p = subprocess.Popen(cmdCommString, stdout=subprocess.PIPE, shell=True)
    # print(p.communicate())

    pids = psutil.pids()

    count = 0

    for pid in pids:
        try:
            pidStructObj = pidStruct(pid)
            taskDataObj = taskData(pid)
            pidStructObj.appendTaskData(taskDataObj)
            engine.pidList.append(pidStructObj)
            # print(str(pid) + " " + str(pidStructObj.cpuUsageList[count]) + " " + str(pidStructObj.memUsageList[count]))
        except:
            print("pid not existent error?")
        
    print("--------------------------------------------------")
     
    print(engine.pidList[0].printDataAt(0))