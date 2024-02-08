import serial.tools.list_ports
import serial
import time
import sys


def GetSerialPorts():
    list = []
    for i in serial.tools.list_ports.comports():
        if "Intel(R) Active Management Technology" in str(i):
            continue
        else:
            list.append(str(i))
    return list


def GetRobotSerialPorts():
    list = []
    for i in serial.tools.list_ports.comports():
        if "Intel(R) Active Management Technology" in str(i):
            continue
        else:
            list.append(i)
    return list


def GetShortenedSerialPorts():
    list = []
    for i in serial.tools.list_ports.comports():
        if "Intel(R) Active Management Technology" in str(i):
            continue
        else:
            i = str(i).split(" ")[0]
            list.append(i)
    return list


def TestSerialPorts(port):
    ser = serial.Serial(port, 115200, timeout=1, write_timeout=1)  # open serial port

    timeout = time.time() + 3  # 5 Seconds from now

    try:
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
    except serial.SerialTimeoutException:
        ser.close()
        return False


if __name__ == "__main__":
    print(GetShortenedSerialPorts())
    print(GetSerialPorts())
    print(GetRobotSerialPorts())
    print(TestSerialPorts(sys.argv[1]))
