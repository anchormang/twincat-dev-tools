# TwinCAT Development Tools

## Description
This project provides a Python interface for communicating with Beckhoff PLCs using the ADS protocol. It utilizes the `pyads` library to establish connections, create routes, and interact with PLCs.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/your-username/twincat-dev-tools.git
   cd twincat-dev-tools
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration
1. Create a `plc_config.json` file in the `src/config/` directory with the following structure:
   ```json
   {
       "CLIENT_IP": "192.168.0.10",
       "TARGET_HOSTNAME": "PLC1",
       "TARGET_NETID": "5.1.204.158.1.1",
       "TARGET_IP": "192.168.0.20",
       "TARGET_USERNAME": "Administrator",
       "TARGET_PASSWORD": "1",
       "ROUTE_NAME": "Route1"
   }
   ```
   Replace the values with your specific PLC configuration.

## Usage
The main interface for PLC communication is the `ADSCommunication` class. Here's a basic example of how to use it:

```python
from src.communication.ads_communication import ADSCommunication

# Initialize the PLC communication class
plc = ADSCommunication()

# Create a route
plc.create_route()

# Connect to the PLC
plc.connect()

# Check the connection state
plc.check_connection_state()

