from pymodbus.client.sync import ModbusTcpClient

from constant import *

class plc:
    def __init__(self, ip:str = '192.168.1.87'):
        self.__ip = ip
        self.__client = ModbusTcpClient(self.__ip)

    def connect(self):
        if self.__client.connect():
            print('Connect Success.')
        else:
            print('Connection failed. Please check error and try again.')

    def disconnect(self):
        if self.__client.connect():
            self.__client.close()
            print(f'Connection \'{self.__ip}\' closed.')

    def read_value(self, id:int):
        if not self.__client.connect(): return

        if id == GUN_SPEED_VALUE:
            return self.__client.read_holding_registers(10).registers
        elif id == SOLDER_SPEED_VALUE:
            return self.__client.read_holding_registers(12).registers
        elif id == GUN_VOLTAGE:
            return self.__client.read_holding_registers(100).registers
        elif id == GUN_AMP:
            return self.__client.read_holding_registers(200).registers
        else: return None

    def write_value(self, id:int, value:int):
        if id == GUN_SPEED_VALUE:
            self.__client.write_register(10, value)
        elif id == SOLDER_SPEED_VALUE:
            self.__client.write_register(12, value)
        else: return
