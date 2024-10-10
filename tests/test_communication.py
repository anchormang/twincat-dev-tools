from src import ADSCommunication

def test_ads_communication():
    plc = ADSCommunication('src/config/plc_config.json')
    plc.create_route()
    plc.connect()
    plc.check_connection_state()

    assert plc is not None
    assert plc.plc.is_open