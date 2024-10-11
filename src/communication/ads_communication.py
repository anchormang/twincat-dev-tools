import pyads
import json

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
            print(f"Connecting to PLC at {self.TARGET_HOSTNAME}:{self.TARGET_NETID}")
            self.plc = pyads.Connection(self.TARGET_NETID, pyads.PORT_TC3PLC1, self.TARGET_IP)
            print(f"Connection object created: {self.plc}")
            self.plc.open()
            print(f"Connected to PLC to {self.TARGET_HOSTNAME}:{self.TARGET_NETID}")
        except pyads.ADSError as e:
            print(f"Failed to connect to PLC: {e}")

    def check_connection_state(self):
        """
        Check the connection state of the PLC
        """
        try:
            if self.plc and self.plc.is_open:
                plc_state = self.plc.read_state()
                print("Connection state: ", {plc_state})
            else:
                print("PLC connection not open")
        except pyads.ADSError as e:
            print(f"Failed to check connection state: {e}")

    def read_variable(self, variable_name, variable_type):
        """
        Read a variable from the PLC
        """
        try:
            return self.plc.read_by_name(variable_name, variable_type)
        except pyads.ADSError as e:
            print(f"Failed to read variable: {e}")
    
    def write_variable(self, variable_name, value):
        """
        Write a variable to the PLC
        """
        try:
            self.plc.write_by_name(variable_name, value)
            print(variable_name, "set to", self.plc.read_by_name(variable_name))
        except pyads.ADSError as e:
            print(f"Failed to write variable: {e}")

    def close(self):
        """
        Close the connection to the PLC
        """
        if self.plc:
            self.plc.close()
            print(f"Disconnected from PLC at {self.TARGET_HOSTNAME}:{self.TARGET_NETID}")
        else:
            print("No PLC connection to close")

