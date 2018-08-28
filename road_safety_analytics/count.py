import json
from datetime import datetime

with open('June1.json') as f:
    data = json.load(f)

alarm_type={}
ward_dist={}
hour_dist = {}
speed_dist = {"less than 20": 0, "20-40": 0, "40-50": 0, "50-60": 0, "60-70": 0,"More than 70": 0}

for i in range(500):
    date = datetime.strptime(data[i]["time"], '%Y-%m-%d %H:%M:%S')
    
    if date.hour not in hour_dist:
        hour_dist[date.hour] = 1
    else:
        hour_dist[date.hour] += 1
    
    speed = int(data[i]["speed"])
    if speed < 20:
        speed_dist["less than 20"] +=1
    elif speed >=20 and speed <40:
        speed_dist["20-40"] +=1
    elif speed >=40 and speed <50:
        speed_dist["40-50"] +=1
    elif speed >=50 and speed <60:
        speed_dist["50-60"] +=1
    elif speed >=50 and speed <60:
        speed_dist["60-70"] +=1
    else:
        speed_dist["More than 70"] +=1

    data[i]["humidity"] = 60
    data[i]["rainfall"] = 30
    
    if date.day == 19 and date.hour > 6 and data[i]["ward"] != "other":
       data[i]["humidity"] = 90
    if date.day == 18 and date.hour > 6:
       data[i]["humidity"] = 300

    if data[i]["ward"] not in ward_dist:
        ward_dist[data[i]["ward"]] = 1
    else:
        ward_dist[data[i]["ward"]] += 1

    if data[i]["alarm"] not in alarm_type:
        alarm_type[data[i]["alarm"]] = 1
    else:
        alarm_type[data[i]["alarm"]] += 1

with open('June_with_weather.json', 'w') as fout:
    json.dump(data, fout)
'''

alarm_op = []

for key in alarm_type:
    a = {}
    a["class"] = key
    a["number"] = alarm_type[key]
    alarm_op.append(a)

with open('June_alarm_count.json', 'w') as fout:
    json.dump(alarm_op, fout)

ward_op = []

for key in ward_dist:
    w = {}
    w["class"] = key
    w["number"] = ward_dist[key]
    ward_op.append(w)

with open('June_wards_count.json', 'w') as fout:
    json.dump(ward_op, fout)


hour_op = []

for key in hour_dist:
    h = {}
    h["class"] = key
    h["number"] = hour_dist[key]
    hour_op.append(h)

with open('June_hour_count.json', 'w') as fout:
    json.dump(hour_op, fout)

speed_op = []

for key in speed_dist:
    s = {}
    s["class"] = key
    s["number"] = speed_dist[key]
    speed_op.append(s)


with open('June_speed_count.json', 'w') as fout:
    json.dump(speed_op, fout)'''
