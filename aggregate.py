import json
import os

logs = os.listdir("./powerevents/")
logNums = [int(file[:-5]) for file in logs]
logNums.sort()

powerEvents = []
for logNum in logNums:
    with open(f"./powerevents/{logNum}.json", "r") as file:
        events = json.load(file)
        powerEvents.extend(events)
        
with open("./powerevents.json", "w") as file:
    json.dump(powerEvents, file)