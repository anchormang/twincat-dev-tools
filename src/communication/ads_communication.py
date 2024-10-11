import pyads
from ctypes import sizeof
from enum import Enum

class ADSCommunication:
    def __init__(self, config):
        self.CLIENT_NETID = config['CLIENT_NETID']
        self.CLIENT_IP = config['CLIENT_IP']
        self.TARGET_HOSTNAME = config['TARGET_HOSTNAME']
        self.TARGET_NETID = config['TARGET_NETID']
        self.TARGET_IP = config['TARGET_IP']
        self.TARGET_USERNAME = config['TARGET_USERNAME']
        self.TARGET_PASSWORD = config['TARGET_PASSWORD']
        self.ROUTE_NAME = config['ROUTE_NAME']
        self.plc = None

    def create_route(self):
        """
        Create a route from the client to the PLC
        
        ADS requires that a route be created on the target 
        device and the client device.  Adding a route on the
        client is done via the set_local_address() method. For
        the target device we utilize add_route_to_plc() 
        """
        
        try:
            pyads.open_port()
            pyads.set_local_address(self.CLIENT_NETID)
            pyads.add_route_to_plc(self.CLIENT_NETID, self.CLIENT_IP, self.TARGET_IP, self.TARGET_USERNAME, self.TARGET_PASSWORD, route_name=self.ROUTE_NAME)
            pyads.close_port()
            print(f"Route created from {self.TARGET_NETID} to {self.CLIENT_NETID}")
        except pyads.ADSError as e:
            print(f"Failed to create route: {e}")
        
    def connect(self):
        """
        Connect to the PLC
        """
        try:
            print(f"Connecting to PLC - {self.TARGET_HOSTNAME}:{self.TARGET_NETID}")
            self.plc = pyads.Connection(self.TARGET_NETID, pyads.PORT_TC3PLC1, self.TARGET_IP)
            print(f"Connection object created: {self.plc}")
            self.plc.open()
            print(f"Connected to PLC - {self.TARGET_HOSTNAME}:{self.TARGET_NETID}")
        except pyads.ADSError as e:
            print(f"Failed to connect to PLC: {e}")

    def read_device_state(self):
        """
        Check the connection state of the PLC
        """
        try:
            if self.plc and self.plc.is_open:
                plc_state = self.plc.read_state()
                print("ADS State:", ADSState.get_state_name(plc_state[0]))
                print("Device State:", ADSState.get_state_name(plc_state[1]))
            else:
                print("PLC connection not open")
        except pyads.ADSError as e:
            print(f"Failed to check connection state: {e}")

    def get_symbols(self):
        """
        Get the symbols from the PLC
        """
        symbols = self.plc.get_all_symbols()
        for i in range(len(symbols)):
            #print('\n'.join("%s: %s" % item for item in vars(symbols[i]).items()), '\n')
            print('Name:', symbols[i].name)
            print('Index Group:', symbols[i].index_group)
            print('Index Offset:', symbols[i].index_offset)
            print('PLC Type: ', symbols[i].plc_type, '\n')

    def read_variable(self, variable_name):
        """
        Read a variable from the PLC
        """
        try:
            return self.plc.read_by_name(variable_name)
        except pyads.ADSError as e:
            print(f"Failed to read variable: {e}")
    
    def write_variable(self, variable_name, value):
        """
        Write a variable to the PLC
        """
        var_handle = self.plc.get_handle(variable_name)
        try:
            self.plc.write_by_name('', value, self.plc.get_symbol(variable_name).plc_type, handle=var_handle)
            print(self.plc.read_by_name(variable_name, self.plc.get_symbol(variable_name).plc_type))
            self.plc.release_handle(var_handle)
        except pyads.ADSError as e:
            print(f"Failed to write variable: {e}")

    def write_structure(self, structure_name, structure_def, value):
        """
        Write a structure to the PLC
        """
        pass
    
    def activate_configuration(self):
        """
        Activate the configuration on the PLC
        """
        pass

    def close(self):
        """
        Close the connection to the PLC
        """
        if self.plc:
            self.plc.close()
            print(f"Disconnected from PLC - {self.TARGET_HOSTNAME}:{self.TARGET_NETID}")
        else:
            print("No PLC connection to close")

class ADSState(Enum):
    INVALID = 0,
    IDLE =1,
    RESET = 2,
    INIT = 3,
    START = 4,
    RUN = 5,
    STOP = 6,
    SAVECFG = 7,
    LOADCFG = 8,
    POWERFAILURE = 9,
    POWERGOOD = 10,
    ERROR = 11,
    SHUTDOWN = 12,
    SUSPEND = 13,
    RESUME = 14,
    CONFIG = 15,
    RECONFIG = 16,
    STOPPING = 17,
    INCOMPATIBLE = 18,
    EXCEPTION = 19

    @classmethod
    def get_state_name(cls, state_value):
        try:    
            return cls(int(state_value)).name
        except ValueError:
            return f"UNKNOWN_STATE_{state_value}"
    