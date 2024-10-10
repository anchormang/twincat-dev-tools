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

    print("Test passed")

    assert plc is not None
    assert plc.plc.is_open

test_ads_communication()