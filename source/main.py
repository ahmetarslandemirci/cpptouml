import glob
import os
import Cpp
import re

def ParseHeader(filename):
    header = Cpp.CppHeader(filename)
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
                    header.AddVariavle(s[0], s[1])
                else:
                    func = re.findall(r".+ +.+\(.*\)(?=;)", line)
                    if(len(func) > 0):
                        header.AddFunction(func[0])
    return header

path = os.path.join(input('Input the directory: '), '**.h')
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