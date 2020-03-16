from pymodbus.client.sync import ModbusTcpClient

GUN_SPEED = 0
SOLDER_SPEED = 1

class client:
    def __init__(self, ip:str = '192.168.1.87'):
        self._ip = ip

    ###
    def __str__(self):
        pass

    def set_ip(self, new_ip):
        self._ip = new_ip
        
    def connect(self):
        self.client = ModbusTcpClient(self._ip)
        try:
            self.client.read_coil(0)
            print('Connect Success.')
        except:
            print('Connection failed. Please check error and try again.')

    def disconnect(self):
        self.client.close()
        print(f'Connection \'{self._ip}\' closed.')

    ###
    def set_value(self, name, value:int):
        if name == 0:
            # 設定走速
            pass
        elif name == 1:
            # 設定焊料速度
            pass
        else:
            pass

    ###
    def read_value(self, name):

        value = 0

        return value
