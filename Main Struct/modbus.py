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
            return True
        else:
            self.is_connected = False
            return False

    def disconnect(self):
        if self.__client.connect():
            self.__client.close()
            print(f'Client \'{self.__ip}\' closed.')

    def get_status(self):
        if not self.__client.connect():
            return

        try:
            if self.__client.read_coils(0xB000+4).bits[0]:
                return MENUAL_MODE
            elif self.__client.read_coils(0xB000+5).bits[0]:
                return AUTO_MODE
        except Exception as e:
            print(e)
            return -1

    def is_setting_value(self, id: int):
        if not self.__client.connect():
            return

        try:
            if id == SET_GUN_SPEED:
                return self.__client.read_coils(0x2000+13).bits[0]
            elif id == SET_SOLDER_SPEED:
                return self.__client.read_coils(0x2000+14).bits[0]
        except Exception as e:
            print(e)
            return -1

    def read_value(self, id: int):
        if not self.__client.connect():
            return

        try:
            if id == GUN_VOLTAGE:
                return self.__client.read_holding_registers(100).registers[0]
            elif id == GUN_AMP:
                return self.__client.read_holding_registers(200).registers[0]

        except Exception as e:
            print(e)
            return -1

    def write_value(self, id: int, value: int):
        try:
            if id == TORCH_SPEED_VALUE:
                self.__client.write_register(10, int(value*2//3))
            elif id == SOLDER_SPEED_VALUE:
                self.__client.write_register(13, int(value*400))

        except Exception as e:
            print('e2', e)
            pass

    def check_value(self, id: int):
        if not self.__client.connect():
            return

        try:
            if id == TORCH_SPEED_VALUE:
                return self.__client.read_holding_registers(10).registers[0]
            elif id == SOLDER_SPEED_VALUE:
                return self.__client.read_holding_registers(12).registers[0]

        except Exception as e:
            print(e)
            return -1
