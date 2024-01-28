import serial.tools.list_ports
from time import sleep, time


def GetSerialPorts():
    list = []
    for i in serial.tools.list_ports.comports():
        list.append(str(i))
    return list


def GetRobotSerialPorts():
    list = []
    for i in serial.tools.list_ports.comports():
        list.append(i)
    return list


def GetShortenedSerialPorts():
    list = []
    for i in serial.tools.list_ports.comports():
        i = str(i).split(" ")[0]
        list.append(i)
    return list


if __name__ == "__main__":
    print("main")
    print(GetShortenedSerialPorts())
    print(GetSerialPorts())
    print(GetRobotSerialPorts())
