import sys
import os
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.communication import ADSCommunication

def test_ads_communication():
    with open('src/config/plc_config.json', 'r') as config_file:
        config = json.load(config_file)
    plc = ADSCommunication(config)

    plc.create_route()
    plc.connect()
    plc.check_connection_state()
    if plc.plc and plc.plc.is_open and plc.plc.read_state() != None:
        print("Test passed")
    else:
        print("Test failed")

    assert plc is not None
    assert plc.plc.is_open
    assert plc.plc.read_state() is not None

if __name__ == "__main__":
    test_ads_communication()