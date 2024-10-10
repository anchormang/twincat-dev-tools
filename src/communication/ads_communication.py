import pyads
import json

class ADSCommunication:
    def __init__(self, CLIENT_NETID, CLIENT_IP, TARGET_HOSTNAME, TARGET_NETID, TARGET_IP, TARGET_USERNAME, TARGET_PASSWORD, ROUTE_NAME):
        with open('plc_config.json', 'r') as config_file:
            config = json.load(config_file)
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
        try:
            pyads.add_route_to_plc(self.CLIENT_NETID, self.CLIENT_IP, self.TARGET_IP, self.TARGET_USERNAME, self.TARGET_PASSWORD, route_name=self.ROUTE_NAME)
            print(f"Route created from {self.target_net_id} to {self.client_net_id}")
        except pyads.ADSError as e:
            print(f"Failed to create route: {e}")
        
    def connect(self):
        try:
            self.plc = pyads.Connection(self.net_id, self.port, self.ip_address)
            self.plc.open()
            print(f"Connected to PLC at {self.net_id}:{self.port}")
        except pyads.ADSError as e:
            print(f"Failed to connect to PLC: {e}")

    def check_connection_state(self):
        try:
            plc_state = self.plc.read_state()
            print("Connection state: ", plc_state)
        except pyads.ADSError as e:
            print(f"Failed to check connection state: {e}")

    def read_variable(self, variable_name, variable_type):
        try:
            return self.plc.read_by_name(variable_name, pyads.PLCTYPE_DINT)
        except pyads.ADSError as e:
            print(f"Failed to read variable: {e}")
    
    def write_variable(self, variable_name, value):
        pass

    def close(self):
        if self.plc:
            self.plc.close()
            print(f"Disconnected from PLC at {self.net_id}:{self.port}")
        else:
            print("No PLC connection to close")

