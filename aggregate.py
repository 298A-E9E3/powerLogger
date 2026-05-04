import json
import os

logs = os.listdir("./powerevents/")
logNums = [float(file[:-5]) for file in logs]
logNums.sort()

powerEvents = []
for logNum in logNums:
    with open(f"./powerevents/{logNum}.json", "r") as file:
        events = json.load(file)
        powerEvents.extend(events)

# Source - https://stackoverflow.com/a/6024599
# Posted by John Machin, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-03, License - CC BY-SA 3.0

for i in range(len(powerEvents) - 1, -1, -1):
    try:
        if(powerEvents[i][1] == powerEvents[i-1][1]):
            del powerEvents[i]
    except:
        pass
        
with open("./powerevents.json", "w") as file:
    json.dump(powerEvents, file)
