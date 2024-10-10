#! /usr/bin/env python3

import sys
import os
import json
import time
import argparse

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from communication import ADSCommunication
from programming import PlcProgram
from deployment import Deployer
from code_generation import CodeGenerator
from monitoring import PLCMonitor

class BeckhoffProgrammer:
    def __init__(self):
        with open('config/plc_config.json', 'r') as config_file:
            config = json.load(config_file)
        self.communication = ADSCommunication(config)
        self.program = PlcProgram()
        self.deploy = Deployer()
        self.code_generator = CodeGenerator()
        self.monitor = PLCMonitor()

    def create_program(self):
        pass

    def generate_and_deploy(self):
        code = self.code_generator.generate_code()
        self.deploy.deploy(code)

    def ads_communication(self):
        self.communication.create_route()
        self.communication.connect()
        self.communication.check_connection_state()

        #try:
        #    while True:
        #        print("Connection Open to ", {self.communication.TARGET_HOSTNAME})
        #        time.sleep(2)
        #except KeyboardInterrupt:
        #    print("Connection Closed")
        #finally:
        #    self.communication.close()

def main():
    parser = argparse.ArgumentParser(description="Beckhoff Programmer")
    subparser = parser.add_subparsers(dest='command', help='Available commands')

    read_parser = subparser.add_parser('read', help='Read a variable')
    read_parser.add_argument('variable', type=str, help='Variable to read')
    read_parser.add_argument('-t', '--type', type=str, help='Type of the variable to read')

    write_parser = subparser.add_parser('write', help='Write a variable')
    write_parser.add_argument('variable', type=str, help='Variable to write')
    write_parser.add_argument('value', type=str, help='Value to write')
    write_parser.add_argument('-t', '--type', type=str, help='Type of the variable to write')

    parser.add_argument('-c', '--connect', action='store_true', help='Establish ADS communication')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    programmer = BeckhoffProgrammer()
    
    if args.verbose:
        print(f"Executing comand: {args.command}")

    if args.connect:
        programmer.ads_communication()
    elif args.command == 'read':
        if args.variable:
            programmer.communication.create_route()
            programmer.communication.connect()
            print(programmer.communication.read_variable(args.variable, args.type))
            programmer.communication.close()
        elif args.variable is None or args.type is None:
            print("Error: --variable and --type is required when using --read")
    elif args.command == 'write':
        if args.variable and args.value:
            programmer.communication.create_route()
            programmer.communication.connect()
            programmer.communication.write_variable(args.variable, args.value)
            programmer.communication.close()
        elif args.variable is None or args.value is None:
            print("Error: --variable and --value is required when using --write")

if __name__ == "__main__":
    main()