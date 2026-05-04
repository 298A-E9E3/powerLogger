from ast import Tuple
import json
import time

import aggregate

powerEvents: list[tuple[float, bool]] = []
with open("./powerevents.json") as file:
    powerEvents = json.load(file)
    
def formatTime(seconds: float, verbose: bool = False):
    if(verbose):
        return(time.strftime("%I:%M:%S %p on %A, %B %d, %Y", time.localtime(seconds)))
    else:
        return(time.strftime("%m/%d/%Y %H:%M:%S z%z"))
    
verboselog = ""
log = ""
inSentence = False
prevState = False

for i in range(len(powerEvents)):
    powerState = powerEvents[i][1]
    currTime = powerEvents[i][0]
    
    log += formatTime(powerEvents[i][0]) + f"> Power {['off', 'on'][powerEvents[i][1]]}\n"
    
    if(i == 0):
        verboselog = f"The power was initially {['off', 'on'][powerEvents[i][1]]} at {formatTime(powerEvents[i][0], True)}."
        if(not powerEvents[i][1]):
            inSentence = True
            prevState = False
        else:
            verboselog += "\n"
            
    elif(inSentence and not prevState and powerState):
        verboselog += f" It turned back on at {formatTime(currTime, True)}.\n"
        prevState = True
        inSentence = False
    
    elif(not powerState):
        verboselog += f"{'\n' if not inSentence else ""}The power {['was', 'turned'][inSentence]} off at {formatTime(currTime, True)}"
        prevState = False
        inSentence = True
    
    else:
        verboselog += f"The power was {["off", "on"][powerState]} at {formatTime(currTime, True)}\n"
        prevState = powerState
        inSentence = False
        
with open("./log.txt", "w") as file:
    file.write(log)

with open("./humanLog.txt", "w") as file:   
    file.write(verboselog)     