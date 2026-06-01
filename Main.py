from PIL.ImageChops import difference
from websockets.sync.client import connect
import math as math
import json
from Processing import process

def receive_data():
    #max_msg = 10  # Feel free to change this or just let it loop forever. Maybe best to keep it low while testing...
    with connect("ws://192.87.172.82:1338") as websocket:
        count = 0
        while True: #count < max_msg:
            msg = websocket.recv()
            try:
                msg = json.loads(msg)
                handle_message(msg)  # Call function to do the actual data handling
            except json.JSONDecodeError:
                print("Failed to decode json, assuming next packet will be ok...")
                pass
            except Exception as e:
                # Assume something went wrong and stop receiving
                print("Something went horribly wrong!")
                print("Error:", e)
                break

            count += 1
        print("Received %d messages!" % count)

def handle_message(msg):
    #print(msg)
    message = msg
    if "altitude" in message and "latitude" in message and "longitude" in message and "address" in message and "rssi" in message and "receiver" in message and "timestamp" in message:
        altitude = message["altitude"]
        latitude = message["latitude"]
        longitude = message["longitude"]
        ut_latitude = 52.23922416681472
        ut_longitude = 6.856894449721378
        ut_altitude = 47
        #d = 2R × sin⁻¹(√[sin²((θ₂ - θ₁)/2) + cosθ₁ × cosθ₂ × sin²((φ₂ - φ₁)/2)])
        distance = 2*6371*math.asin(math.sqrt(math.pow(math.sin((ut_latitude - latitude)/2), 2) + math.cos(latitude)*math.cos(ut_latitude)*math.pow(math.sin((ut_longitude - longitude)/2), 2)))
        altitude_difference = altitude - ut_altitude
        real_distance = math.sqrt(math.pow(altitude_difference, 2) + math.pow(distance, 2))
        process([message["address"], real_distance, message["rssi"], message["receiver"], message["timestamp"]])
        print([message["address"], real_distance, message["rssi"], message["receiver"], message["timestamp"]])

receive_data()