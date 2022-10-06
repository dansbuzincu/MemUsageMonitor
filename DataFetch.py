#DATA FETCH
from enum import Enum
from datetime import date
from genericpath import isdir
import os
import subprocess


# PROCESS DATA
class tasksData(Enum):
    IMAGE_NAME = 1
    PID = 2
    SESSION = 3
    MEM_USAGE = 4

#


# GENERATE PROCESS FOR THE DATE AND TIME REQUESTED
def dataFetch():
    cwdString = os.getcwd()
    currentDate = date.today().strftime("%d-%m-%Y")

    logsPathString = cwdString + "/"

    logsPath = os.path.join(logsPathString, currentDate)
    
    #Check if folder already exists
    if os.path.isdir(logsPath) == False:
        os.makedirs(logsPath)
    else:
        print("FOLDER ALREADY EXISTS!!!")

    # shellString = './generateData.sh ' + logsPathString + 'test.txt'
    # subprocess.run(["sh E:\work\CPU-MemoryUsageMonitor\generateData.sh"], shell=True)
    # cmdCommString = "cmd /c tasklist > " + logsPath
    # os.system(cmdCommString)