#! /usr/bin/env python3

import sys
import os
import json
import time
import argparse

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from communication import ADSCommunication, ADSState
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
        self.communication.read_device_state()

def main():
    parser = argparse.ArgumentParser(description="Beckhoff Programmer")
    subparser = parser.add_subparsers(dest='command', help='Available commands')

    read_parser = subparser.add_parser('read', help='Read a variable')
    read_group = read_parser.add_mutually_exclusive_group(required=True)
    read_group.add_argument('variable', type=str, nargs='?', help='Variable to read')
    read_group.add_argument('-a', '--all', action='store_true', help='Read all symbols in PLC project')
    read_parser.add_argument('-c', '--continuous', action='store_true', help='Read variable continuously until stopped')
    read_parser.add_argument('-i', '--interval', type=float, default=1, help='Interval between reads in seconds')
    
    read_state_parser = subparser.add_parser('readstate', help='Read the device state')

    write_parser = subparser.add_parser('write', help='Write a variable')
    write_group = write_parser.add_mutually_exclusive_group(required=True)
    write_parser.add_argument('variable', type=str, help='Variable to write')
    write_group.add_argument('value', type=str, nargs='?', help='Value to write')
    write_group.add_argument('-s', '--structure', action='store_true', help='Write to a structure')
    
    #parser.add_argument('-c', '--connect', action='store_true', help='Establish ADS communication')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    programmer = BeckhoffProgrammer()

    test_path = create_path()
    
    if args.verbose:
        print(f"Executing comand: {args.command}")

    if args.command == 'read':
        if args.all:
            programmer.communication.create_route()
            programmer.communication.connect()
            programmer.communication.get_symbols()
            programmer.communication.close()
        elif args.variable:
            programmer.communication.create_route()
            programmer.communication.connect()
            if args.continuous:
                while True:
                    try:
                        print(args.variable + ":", str(programmer.communication.read_variable(args.variable)))
                        time.sleep(args.interval)
                    except KeyboardInterrupt:
                        print("Continuous reading interrupted")
                        break
            else:
                print(args.variable + ":", programmer.communication.read_variable(args.variable))
            programmer.communication.close()
        elif args.variable is None:
            print("Error: variable is required when using read")
    elif args.command == 'write':
        if args.variable and args.value and not args.structure:
            programmer.communication.create_route()
            programmer.communication.connect()
            programmer.communication.write_variable(args.variable, str_to_bool(args.value))
            programmer.communication.close()
        elif args.variable and args.structure:
            programmer.communication.create_route()
            programmer.communication.connect()
            start_time = time.time()
            programmer.communication.write_structure(args.variable, test_path)
            end_time = time.time()
            print(f"Time taken to write structure: {end_time - start_time} seconds")
            programmer.communication.close()
        elif args.variable is None or (not args.structure and args.value is None):
            print("Error: --variable and --value is required when using --write")
    elif args.command == 'readstate':
        programmer.communication.create_route()
        programmer.communication.connect()
        print(programmer.communication.read_device_state())
        programmer.communication.close()

def str_to_bool(value):
    return value.lower() == 'true'

def create_path():
    path = []
    for i in range(0, 999):
        path.append([
            i*10,
            i*10,
            i*10,
            i*10,
            i*10
        ])
    return path

#test_path = [{
#    'T_Pos': 10,
#    'A_Pos': 10,
#    'B_Pos': 10,
#    'W_Pos': 10,
#    'TimeStamp': 10
#},
# {'T_Pos': 20,
#    'A_Pos': 20,
#    'B_Pos': 20,
#    'W_Pos': 20,
#    'TimeStamp': 20
#}]

if __name__ == "__main__":
    main()