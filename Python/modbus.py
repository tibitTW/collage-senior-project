from pymodbus.client.sync import ModbusTcpClient

from constant import *

class plc:
    def __init__(self, ip:str = '192.168.1.87'):
        self._ip = ip
        self.client = ModbusTcpClient(self._ip)

    ###
    def __str__(self):
        return 'Ip: ' + self._ip

    def set_ip(self, new_ip):
        self._ip = new_ip
        
    def connect(self):
        if client.connect():
            print('Connect Success.')
        else:
            print('Connection failed. Please check error and try again.')

    def disconnect(self):
        if client.connect():
            self.client.close()
            print(f'Connection \'{self._ip}\' closed.')

    ###
    def read_value(self, id:int):
        if id == GUN_SPEED_VALUE: # read coil
            value = self.client.read_holding_registers(10).registers
        elif id == SOLDER_SPEED_VALUE: # read register
            value = self.client.read_holding_registers(12).registers
        elif id == GUN_VOLTAGE:
            value = self.client.read_holding_registers(100).registers
        elif id == GUN_AMP:
            value = self.client.read_holding_registers(200).registers
        else: return

        return value

    def write_value(self, id:int, value:int):
        if id == GUN_SPEED_VALUE:
            self.client.write_register(10, value)
        elif id == SOLDER_SPEED_VALUE:
            self.client.write_register(12, value)
        else: return
