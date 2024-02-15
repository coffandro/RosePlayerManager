# Global functions
def IsBundled():
    import sys
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return True
    else:
        return False

# Ports functions
def GetSerialPorts():
    import serial.tools.list_ports
    list = []
    for i in serial.tools.list_ports.comports():
        if "Intel(R) Active Management Technology" in str(i):
            continue
        else:
            list.append(str(i))
    return list


def GetRobotSerialPorts():
    import serial.tools.list_ports
    list = []
    for i in serial.tools.list_ports.comports():
        if "Intel(R) Active Management Technology" in str(i):
            continue
        else:
            list.append(i)
    return list


def GetShortenedSerialPorts():
    import serial.tools.list_ports
    list = []
    for i in serial.tools.list_ports.comports():
        if "Intel(R) Active Management Technology" in str(i):
            continue
        else:
            i = str(i).split(" ")[0]
            list.append(i)
    return list


def TestSerialPorts(port):
    import serial
    import time 
    try:
        ser = serial.Serial(port, 115200, timeout=1, write_timeout=1)  # open serial port

        timeout = time.time() + 3  # 5 Seconds from now
        
        command = b"a\n\r"
        ser.write(command)  # write a string

        ended = False
        reply = b""

        for _ in range(len(command)):
            a = ser.read()  # Read the loopback chars and ignore

        while True:
            if time.time() > timeout:
                break
            a = ser.read()

            if a == b"\r":
                break

            else:
                reply += a

            time.sleep(0.01)

        ser.close()

        if reply == b"b":
            return True
        else:
            return False
    except:
        return False

# Settings functions
import json


def Read_Settings():
    import json
    from sys import platform
    from pathlib import Path
    # Read Settings
    try:
        if platform == "linux" or platform == "linux2":
            f = open(str(Path.home()) + "/.config/RosePlayerManager/Settings.json")
        elif platform == "win32":
            f = open(str(Path.home()) + "\\RosePlayerManager\\Settings.json")

        # returns JSON object as
        # a dictionary
        settings = json.load(f)

        # Closing file
        f.close()
    except:
        settings = {
            "comport": "COM5",
            "multScreens": 1,
            "optionmenu1": "Media info",
            "optionmenu2": "Media info",
        }

    return settings


def Write_Settings(settings):
    import json
    from sys import platform
    from pathlib import Path
    if platform == "linux" or platform == "linux2":
        with open(str(Path.home()) + "/RosePlayerManager/Settings.json", "w") as f:
            json.dump(settings, f)
    elif platform == "win32":
        with open(str(Path.home()) + "\\RosePlayerManager\\Settings.json", "w") as f:
            json.dump(settings, f)


if __name__ == "__main__":
    print("Is bundled:     ", str(IsBundled()))
    print("Short ports:    ", GetShortenedSerialPorts())
    print("Normal ports:   ", GetSerialPorts())
    print("Robot ports:    ", GetRobotSerialPorts())
    print("COM4 Roseplayer:", TestSerialPorts("com4"))
    print(Read_Settings())
    Write_Settings({"uwu": True})
    print(Read_Settings())
