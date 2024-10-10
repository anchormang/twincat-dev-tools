import pyads
class ADSCommunication:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.plc = None

    def connect(self):
        try:
            self.plc = pyads.connect(self.ip_address, self.port)
            self.plc.open()
            print(f"Connected to PLC at {self.ip_address}:{self.port}")
        except pyads.ADSError as e:
            print(f"Failed to connect to PLC: {e}")

    def read_variable(self, variable_name, variable_type):
        try:
            return self.plc.read_by_name(variable_name, pyads.PLCTYPE_DINT)
        except pyads.ADSError as e:
            print(f"Failed to read variable: {e}")
    
    def write_variable(self, variable_name, value):
        pass

    def close(self):
        pass

