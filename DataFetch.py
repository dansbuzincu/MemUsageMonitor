# DATA FETCH
from concurrent.futures import process
from enum import Enum
from datetime import date, datetime
from genericpath import isdir
from logging import shutdown
from mimetypes import init
from multiprocessing import dummy
import os
import subprocess
import psutil
import threading
import time


# Sample once a second
SAMPLE_TIME = 3

# Monitor time in hours - 5 time of monitoring
MONITOR_TIME = 5
# Max size for monitoring MONITOR_TIME of hours
MAX_BUFFER_SIZE = (MONITOR_TIME * 60) / SAMPLE_TIME

# pidList is the shared buffer of the producer and consumer threads
pidList = []

# Mutex for the access of the shared buffer
pidListMutex = threading.Semaphore()

# Shutdown bool to signal the exit of application
shutdownBool = False

# Dummy var to control access of the consumer thread
dummySize = 0

# Data structure that holds the CPU/MEM usage at the time required of one task 
class taskData():
    def __init__(self, pid):
        self.pidNr = pid
        self.proc = psutil.Process(pid)
        self.cpuUsage = self.proc.cpu_percent(interval=0.05)
        self.memUsage = self.proc.memory_percent()
        self.timestamp = datetime.now()

    def printData(self):
        print("At : " + str(self.timestamp)  + " for pid: " + str(self.pidNr) + " Mem Usage: " + str(self.memUsage) + "; CPU Usage: " + str(self.cpuUsage))

# Wrapper for taskData to hold the values of the CPU/MEM usage over time 
class pidStruct():
    def __init__(self, inputPid):
        self.pid = inputPid
        self.resourceDataList = []

    def appendTaskData(self, data):
        self.resourceDataList.append(data)

    def printDataAt(self, index):
        if index < len(self.resourceDataList):
            self.resourceDataList[index].printData()
        else:
            print("Index error!!!")

# Producer thread - creates a taskData object for every pid in the running processes list
class dataProducer(threading.Thread):
    def __init__(self):
        global pidList, pidListMutex, shutdownBool, dummySize
        super(dataProducer, self).__init__()
    
    def run(self):
        while(True != shutdownBool):
            # To put data in the buffer one must acquire its mutex to avoid race conditions
            pidListMutex.acquire()

            pids = psutil.pids()
            count = 0

            for pid in pids:
                try:
                    pidStructObj = pidStruct(pid)
                    taskDataObj = taskData(pid)
                    pidStructObj.appendTaskData(taskDataObj)
                    pidList.append(pidStructObj)
                except:
                    print("pid not existent error?")
                
            print("IN PRODUCER THREAD - PRODUCED A SNAPSHOT")

            dummySize += 1

            # Release the mutex to provide access to the shared buffer 
            pidListMutex.release()

            print("SLEEP FOR ONE SECOND!")
            #Sleep for a designated time
            time.sleep(SAMPLE_TIME)


class dataProcessor(threading.Thread):
    def __init__(self):
        global pidList, pidListMutex, dummySize
        super(dataProcessor, self).__init__()

    def run(self):

        while(dummySize < 20):
            pidListMutex.acquire()
            
            print(pidList[0].printDataAt(0))

            pidListMutex.release()



class Engine(threading.Thread):
    def __init__(self):
        self.consumerThread = dataProcessor()
        self.producerThread = dataProducer()

    def runEngine(self):
        self.producerThread.start()
        self.consumerThread.start()
        self.producerThread.join()
        self.consumerThread.join()

# GENERATE TASK FOR THE DATE AND TIME REQUESTED
# def snapshot():
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

    # pids = psutil.pids()

    # count = 0

    # for pid in pids:
    #     try:
    #         pidStructObj = pidStruct(pid)
    #         taskDataObj = taskData(pid)
    #         pidStructObj.appendTaskData(taskDataObj)
    #         engine.pidList.append(pidStructObj)
    #         # print(str(pid) + " " + str(pidStructObj.cpuUsageList[count]) + " " + str(pidStructObj.memUsageList[count]))
    #     except:
    #         print("pid not existent error?")
        
    # print("--------------------------------------------------")
     
    # print(engine.pidList[0].printDataAt(0))