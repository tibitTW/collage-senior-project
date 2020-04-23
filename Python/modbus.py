from pymodbus.client.sync import ModbusTcpClient

from constant import *


class plc:
    def __init__(self, ip: str = '192.168.1.87'):
        self.__ip = ip
        self.__client = ModbusTcpClient(self.__ip)
        self.is_connected = self.__client.connect()

    def connect(self):
        if self.__client.connect():
            self.is_connected = True
            return 'Connect Success.'
        else:
            self.is_connected = False
            return 'Connection failed. Please check error and try again.'

    def disconnect(self):
        if self.__client.connect():
            self.__client.close()
            print(f'Connection \'{self.__ip}\' closed.')

    def read_value(self, id: int):
        if not self.__client.connect():
            return

        if id == GUN_SPEED_VALUE:
            return self.__client.read_holding_registers(10).registers
        elif id == SOLDER_SPEED_VALUE:
            return self.__client.read_holding_registers(12).registers
        elif id == GUN_VOLTAGE:
            return self.__client.read_holding_registers(100).registers
        elif id == GUN_AMP:
            return self.__client.read_holding_registers(200).registers
        elif id == MENUAL_MODE:
            return self.__client.read_coils(0xB000+4).bits[0]
        elif id == AUTO_MODE:
            return self.__client.read_coils(0xB000+5).bits[0]
        elif id == SET_GUN_SPEED:
            return self.__client.read_coils(0x2000+13).bits[0]
        elif id == SET_SOLDER_SPEED:
            return self.__client.read_coils(0x2000+14).bits[0]
        else:
            return None

    def write_value(self, id: int, value: int):
        if id == GUN_SPEED_VALUE:
            self.__client.write_register(10, value)
        elif id == SOLDER_SPEED_VALUE:
            self.__client.write_register(12, value)
        else:
            return
