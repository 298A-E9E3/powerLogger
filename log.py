import json
import os
import subprocess
import time
import re

startTime = time.time()

pollTime = 0
while not pollTime:
    try:
        pollTime = float(input("Poll time: "))
        assert pollTime > 0
    except:
        print("Invalid input")

command = "adb shell dumpsys battery".split(" ")

stateInitialized = False
beingCharged = False
powerEvents: list[tuple[float, bool]] = []
powerRegex = r"(?<=AC powered: )(true|false)"
timeFormat = "%Y-%m-%d %H:%M:%S"
try:
    while True:
        dumpsysStr = str(subprocess.run(command, capture_output=True, text=True).stdout).split("\n")[1]
        print(dumpsysStr)
        powerStateStr = re.findall(powerRegex, dumpsysStr)
        currPowerState = False
        try:
            if("false" in powerStateStr):
                currPowerState = False
            elif("true" in powerStateStr):
                currPowerState = True
            else:
                raise Exception("Invalid power state")
            
            if(currPowerState != beingCharged or not stateInitialized):
                stateInitialized = True
                beingCharged = currPowerState
                print(f"{time.strftime(timeFormat)}> The device is {['not ', ''][beingCharged]}being charged")
                powerEvents.append((time.time(), beingCharged))
                with open(f"./powerevents/{startTime}.json", "w") as file:
                    file.write(json.dumps(powerEvents))
                    
                
        except:
            print("Invalid power state") 
                
        time.sleep(pollTime)
finally:
    with open(f"./powerevents/{startTime}.json", "w") as file:
        file.write(json.dumps(powerEvents))