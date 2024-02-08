import json
import serial
import sys
import time
import asyncio

ser = serial.Serial(settings["comport"], 115200)  # open serial port

Data = {}

Data["Disp1"] = settings["optionmenu1"]
Data["Disp2"] = settings["optionmenu2"]

if "Media info" in str(settings):
    try:
        current_media_info = asyncio.run(MediaGetter.get_media_info())
        print(current_media_info)
        Data["Title"] = current_media_info["title"]
        Data["Artist"] = current_media_info["artist"]
        Data["Album"] = current_media_info["album_title"]
        print(Data)
    except:
        pass

ProcessedData = json.dumps(Data)
print(ProcessedData)

command = f"{ProcessedData}\n\r".encode("utf-8")
# command = b'Hello\n\r'
print(f"Sending Command: [{command}]")
ser.write(command)  # write a string

ended = False
reply = b""

for _ in range(len(command)):
    a = ser.read()  # Read the loopback chars and ignore

while True:
    a = ser.read()

    if a == b"\r":
        break

    else:
        reply += a

    time.sleep(0.01)

print(f"Reply was: [{reply}]")

ser.close()
