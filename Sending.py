import serial
import json

# import serial.tools.list_ports
#
# for p in serial.tools.list_ports.comports():
#     print(p.device)

ser = serial.Serial(
    port='COM7',      # Change this
    baudrate=115200,
    timeout=1
)

def send_data(message):
    global ser
    data = json.dumps(message) + "\n"
    ser.write(data.encode("utf-8"))
    print(f"Send: {data}")