import serial


class mySerial:
    timeout = 1

    def __init__(self, port, btl):
        self.port = port
        self.btl = btl
        self.ser = serial.Serial(port, btl, timeout=mySerial.timeout)
