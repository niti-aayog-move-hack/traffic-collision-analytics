import json

with open('Alerts-Jun18.json') as f:
    data = json.load(f)

modified = []

for i in range(500):
    opdic = {}
    opdic["ward"] = data[i]["location"]["wardName"]
    opdic["lat"] = data[i]["location"]["latitude"]
    opdic["lng"] = data[i]["location"]["longitude"]
    opdic["alarm"] = data[i]["pyld"]["alarmType"] 
    opdic["speed"] = data[i]["pyld"]["speed"] 
    opdic["time"] = data[i]["time"]["recordedTime"]["$date"].replace("Z", "")
    opdic["time"] = opdic["time"].replace("T", " ")
    opdic["time"] = opdic["time"].replace(".000", "")
    modified.append(opdic)
    
with open('June1.json', 'w') as fout:
    json.dump(modified, fout)