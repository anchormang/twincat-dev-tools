class PlcProgram:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def define_variable(self, variable_name, variable_type):
        self.variables[variable_name] = variable_type

    def define_function(self, function_name, function_type):
        self.functions[function_name] = function_type

    def get_variable(self, variable_name):
        return self.variables.get(variable_name)
    
    def set_variable(self, variable_name, value):
        if variable_name in self.variables:
            self.variables[variable_name] = value
        else:
            raise ValueError(f"Variable '{variable_name}' is not defined.")
        
        