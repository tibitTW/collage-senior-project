from pymodbus.client.sync import ModbusTcpClient

class client:
    def __init__(self, ip:str = '192.168.1.87'):
        self.ip = ip

    def connect(self):
        self.client = ModbusTcpClient(self.ip)

    def disconnect(self):
        self.client.close()
