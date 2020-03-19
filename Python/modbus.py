from pymodbus.client.sync import ModbusTcpClient

GUN_SPEED_VALUE = 0
SOLDER_SPEED_VALUE = 1

class plc:
    def __init__(self, ip:str = '192.168.1.87'):
        self._ip = ip

    ###
    def __str__(self):
        return 'Ip: ' + self.ip

    def set_ip(self, new_ip):
        self._ip = new_ip
        
    def connect(self):
        self.client = ModbusTcpClient(self._ip)
        if not client.connect():
            print('Connection failed. Please check error and try again.')
        else:
            print('Connect Success.')

    def disconnect(self):
        if client.connect():
            self.client.close()
            print(f'Connection \'{self._ip}\' closed.')

    ###
    def read_value(self, id:int):
        if id == GUN_SPEED_VALUE: # read coil
            value = self.client.read_holding_registers(10)
        elif id == SOLDER_SPEED_VALUE: # read register
            value = self.client.read_holding_registers(12)
        else: pass

        return value

    def write_value(self, id:int, value:int):
        if id == GUN_SPEED_VALUE:
            self.client.write_register(10, value)
        elif id == SOLDER_SPEED_VALUE:
            self.client.write_register(10, value)
        else: pass
