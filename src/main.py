from communication.ads_communication import AdsCommunication
from programming.plc_program import PlcProgram
from deployment.deploy import Deploy
from code_generation.code_generator import CodeGenerator
from monitoring.plc_monitor import PLCMonitor

class BeckhoffProgrammer:
    def __init__(self):
        self.communication = AdsCommunication()
        self.program = PlcProgram()
        self.deploy = Deploy()
        self.code_generator = CodeGenerator()
        self.monitor = PLCMonitor()

    def create_program(self):
        pass

    def generate_and_deploy(self):
        code = self.code_generator.generate_code()
        self.deploy.deploy(code)


if __name__ == "__main__":
    programmer = BeckhoffProgrammer()
