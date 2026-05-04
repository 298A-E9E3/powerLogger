from ast import Tuple
import json
import os
import sys
import time
from datetime import datetime as dt

import aggregate

def formatTime(seconds: float, verbose: bool = False):
    if(verbose):
        return(time.strftime("%I:%M:%S %p on %A, %B %d, %Y", time.localtime(seconds)))
    else:
        return(dt.fromtimestamp(seconds).strftime("%m/%d/%Y %H:%M:%S.%f %Z"))


verboselog = ""
log = ""
inSentence = False
prevState = False
    
def prettify(powerEvents):
    global log, verboselog, inSentence, prevState
    i = 0
    sentenceCompleted = False
    while i < len(powerEvents):
        powerState = powerEvents[i][1]
        currTime = powerEvents[i][0]
    
        log += formatTime(powerEvents[i][0]) + f"> Power {['off', 'on'][powerEvents[i][1]]}\n"

        if(sentenceCompleted):
            sentenceCompleted = False
        elif(i == 0 and powerState):
            verboselog += f"The power was initially {['off', 'on'][powerEvents[i][1]]} at {formatTime(powerEvents[i][0], True)}\n"
                
        elif(not powerState and powerEvents[i+1][1]):
            verboselog += f"The power was off from {formatTime(currTime, True)} to {formatTime(powerEvents[i+1][0], True)}\n"
            sentenceCompleted = True
    
        else:
            verboselog += f"The power was {["off", "on"][powerState]} at {formatTime(currTime, True)}\n"
        
        i += 1
        
if("-s" in sys.argv):
    logs = os.listdir("./powerevents/")
    logNums = [float(file[:-5]) for file in logs]
    logNums.sort()
    
    for logNum in logNums:
        with open(f"./powerevents/{logNum}.json", "r") as file:
            events = json.load(file)
            prettify(events)
            log += "---EOF---\n"
            verboselog += "---EOF---\n"
        
    
else:
    with open("./powerevents.json") as file:
        events = json.load(file)
        prettify(events)
    
with open("./log.txt", "w") as file:
    file.write(log)

with open("./humanLog.txt", "w") as file:
    file.write(verboselog)
