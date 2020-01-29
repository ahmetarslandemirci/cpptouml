class CppVariable:
    def __init__(self, varType, name):
        self.variable_type = varType
        self.name = name

    def __str__(self):
        return self.name + ': ' + self.variable_type

    def __repr__(self):
        return str(self)

class CppFunction:
    def __init__(self, retType, name):
        self.return_type = retType
        self.name = name
        self.params = []

    def AddParameter(self, param):
        split = param.split()
        if(len(split) == 2):
            self.params.append(CppVariable(split[0], split[1]))

class CppHeader:
    def __init__(self, name):
        self.name = name
        self.dependencies = []
        self.variables = []
        self.functions = []
        self.ClassName = ""

    def AddDependency(self, dependency):
        self.dependencies.append(dependency)

    def AddVariavle(self, varType, name):
        self.variables.append(CppVariable(varType, name))

    def AddFunction(self, func):
        split_str = func.strip().split(' ', 1)
        left_bracket = split_str[1].find('(')
        right_bracket = split_str[1].find(')')
        name = split_str[1][:left_bracket]
        params = split_str[1][left_bracket + 1:right_bracket].split(',')
        f = CppFunction(split_str[0], name)
        for p in params:
            f.AddParameter(p)
        self.functions.append(f)