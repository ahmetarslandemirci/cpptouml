import glob
import os
import re
import argparse


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
        # print(func)
        # print(split_str)
        index = 0 if len(split_str) == 1 else 1
        left_bracket = split_str[index].find('(')
        right_bracket = split_str[index].find(')')
        name = split_str[index][:left_bracket]
        params = split_str[index][left_bracket + 1:right_bracket].split(',')
        f = CppFunction(split_str[0], name)
        for p in params:
            f.AddParameter(p)
        self.functions.append(f)


def ParseHeader(filename):
    header = CppHeader(filename)
    with open(filename, mode='r') as h:
        for line in h:
            if(line == r'\n'):
                pass
            elif(line.find('#include') != -1):
                header.AddDependency(re.findall('[<"]([^<>"]+)[>"]', line)[0])
            elif(line.find('class') != -1):
                header.ClassName = line.split()[1]
            else:
                prop = re.findall(r".+ +.+[^():](?=;)", line)
                if(len(prop) > 0):
                    s = prop[0].split()
                    # @TODO yorumn satırını ayırt etmiyor
                    header.AddVariavle(s[0], s[1])
                else:
                    func = re.findall(r".+ +.+\(.*\)(?=;)", line)
                    if(len(func) > 0):
                        header.AddFunction(func[0])
    return header


def parse_arguments():
    parser = argparse.ArgumentParser(description="CppTo")
    parser.add_argument("-p", "--path", required=True, help="source path")
    
    return parser.parse_args()


def main():
    args = parse_arguments()
    path = os.path.join(args.path, '**.h')

    for filename in glob.glob(path, recursive=True):
        h = ParseHeader(filename)
        print(h.ClassName)
        print('-'*20)
        for var in h.variables:
            print(var.name + ': ' + var.variable_type)
        print('-'*20)
        for func in h.functions:
            print(func.name + '(', end='')
            print(*func.params, sep=", ", end='')
            print(')')
        print()


if __name__ == "__main__":
    main()
