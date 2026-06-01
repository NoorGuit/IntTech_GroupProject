from datetime import datetime
from Sending import send_data
#recieve an array with the data points (address, distance, rssi, receiver, timestamp)
#output per reciever total signal strength, amount of planes, signal strength normalized by distance

data = {
    "Zi-5110_strength" : 0,
    "Zi-5110_planes" : 0,
    "Zi-5110_normalized" : 0,
    "Zi-5067_strength" : 0,
    "Zi-5067_planes" : 0,
    "Zi-5067_normalized" : 0
}
#keep track of when the plane was last detected, drop plane twice of length when normally seen
#store plane_id as key and receiver as value, if both receivers, store the value 2
plane_5110 = []
plane_5067 = []
#plane_id as key and signal strength as value
strength_5110 = dict()
strength_5067 = dict()
#plane_id as key and normalized signal strength as value
norm_strength_5110 = dict()
norm_strength_5067 = dict()
#save last timestamp the plane was seen
time_5110 = dict()
time_5067 = dict()

#proccess gets called every time that there is a new row of data coming in
def process(raw_data):
    global data, plane_5110, plane_5067, strength_5110, strength_5067, norm_strength_5110, norm_strength_5067, time_5110, time_5067
    plane_id = raw_data[0]
    distance = raw_data[1]
    rssi = raw_data[2]
    receiver = raw_data[3]
    time = raw_data[4]

    #check if plane is already in data, append/change when necessary
    if receiver == "zi-5110" and f"{plane_id}" not in plane_5110:
        plane_5110.append(f"{plane_id}")
    elif receiver == "zi-5067" and f"{plane_id}" not in plane_5067:
        plane_5067.append(f"{plane_id}")

    #determine plane count
    data["Zi-5110_planes"] = 0
    data["Zi-5067_planes"] = 0
    for plane in plane_5110:
        data["Zi-5110_planes"] += 1
    for plane in plane_5067:
        data["Zi-5067_planes"] += 1

    #determine signal strength
    if receiver == "zi-5110":
        strength_5110[f"{plane_id}"] = rssi
    elif receiver == "zi-5067":
        strength_5067[f"{plane_id}"] = rssi
    data["Zi-5110_strength"] = 0
    data["Zi-5067_strength"] = 0
    for signal in strength_5110.values():
        data["Zi-5110_strength"] += signal
    for signal in strength_5067.values():
        data["Zi-5067_strength"] += signal

    #normalize signal strength by distance
    if receiver == "zi-5110":
        norm_strength_5110[f"{plane_id}"] = (rssi/distance)*10000
    elif receiver == "zi-5067":
        norm_strength_5067[f"{plane_id}"] = (rssi/distance)*10000
    data["Zi-5110_normalized"] = 0
    data["Zi-5067_normalized"] = 0
    for signal in norm_strength_5110.values():
        data["Zi-5110_normalized"] += signal
    for signal in norm_strength_5067.values():
        data["Zi-5067_normalized"] += signal

    #remove old values
    if receiver == "zi-5110":
        time_5110[f"{plane_id}"] = time
    elif receiver == "zi-5067":
        time_5067[f"{plane_id}"] = time
    for plane, stamp in time_5110.items():
        isolated_stamp = datetime.fromisoformat(stamp)
        isolated_time = datetime.fromisoformat(time)
        diff = isolated_stamp - isolated_time
        seconds = diff.total_seconds()
        if seconds > 60: #if a plane does not appear on the scanner in 60 seconds it will get deleted
            #drop the plane
            plane_5110.remove(plane)
            strength_5110.pop(plane)
            norm_strength_5110.pop(plane)
            time_5110.pop(plane)
    for plane, stamp in time_5067.items():
        isolated_stamp = datetime.fromisoformat(stamp)
        isolated_time = datetime.fromisoformat(time)
        diff = isolated_stamp - isolated_time
        seconds = diff.total_seconds()
        if seconds > 60: #if a plane does not appear on the scanner in 60 seconds it will get deleted
            #drop the plane
            plane_5067.remove(plane)
            strength_5067.pop(plane)
            norm_strength_5067.pop(plane)
            time_5067.pop(plane)

    #send message
    send_data(data)