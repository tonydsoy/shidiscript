#!/usr/bin/env python3
import os,sys,random

errortext = "\033[0;31mERROR"

inputFile = None
developer = [False,False]
for i,v in enumerate(sys.argv[1:]):
    if v == "-i" and i+1<=len(sys.argv[1:]):
        inputFile = sys.argv[i+2]
    if v == "--print-variables":
        developer[0] = True
    if v == "--print-labels":
        developer[1] = True

program = None
if inputFile == None:
    print("No input files. try -h?")
    exit(1)

if not os.path.exists(inputFile) or not os.path.isfile(inputFile):
    print(f"{sys.argv[0]}: '{inputFile}': No such file")
    exit(127)

with open(inputFile,'r') as file:
    program = file.read().splitlines()

def shidierr(command:str,variant:str,extra:str,line):
    print(errortext)
    print(command)
    print(f"{variant} error. on line {line}")
    print(extra)
    exit(1)

# preload labels (this makes functions work!!)
labels = []

for i,v in enumerate(program):
    if v.startswith("label "):
        labels.append((v[len("label "):],i))

# main
variables = []

ptr = 0
while ptr < len(program):
    line = program[ptr]
    ptr += 1
    if line.startswith("//"): # comments
        pass
    if line.startswith("#!"): # shebang
        pass
    elif line.startswith("goto "):
        if len(line.split(" ")) != 2:
            shidierr("goto","syntax","gotos must have one argument",ptr)
        gotowhat = line[len("goto "):]
        linetogoto = None
        found = False
        for i in labels:
            if i[0] == gotowhat:
                found = True
                linetogoto = i[1]
        if linetogoto != None:
            ptr = linetogoto
        if found == False:
            shidierr("goto","value",f"cant find label '{gotowhat}'",ptr)
    elif line.startswith("variable "):
        parts = line.split(" ")
        if len(parts) <= 3:
            shidierr("variable","syntax","ifs must have at least three arguments",ptr)
        found = False
        for i,v in enumerate(variables):
            if v[0] == parts[2]:
                found = True
                if parts[1] == "string":
                    variables[i][1] = line[len(f"variable string {parts[2]} "):]
                    variables[i][2] = 0
                elif parts[1] == "integer":
                    try:
                        variables[i][1] = int(line[len(f"variable integer {parts[2]} "):])
                        variables[i][2] = 1
                    except ValueError:
                        shidierr("variable","type",f"'{parts[3]}' isnt an integer",ptr)
                else:
                    shidierr("variable","syntax",f"cannot find variable type: '{parts[1]}'",ptr)
        if found == False:
            if parts[1] == "string":
                variables.append(
                        [
                            parts[2],
                            line[len(f"variable string {parts[2]} "):],
                            0
                        ]
                    )
            elif parts[1] == "integer":
                try:
                    variables.append(
                        [
                            parts[2],
                            int(line[len(f"variable integer {parts[2]} "):]),
                            1
                        ]
                    )
                except ValueError:
                    shidierr("variable","type",f"'{parts[3]}' isnt an integer",ptr)
            else:
                shidierr("variable","syntax",f"cannot find variable type: '{parts[1]}'",ptr)
    elif line.startswith("print "):
        parts = line.split(" ")
        if len(parts) != 2:
            shidierr("print","syntax","prints must have one argument",ptr)
        for i in variables:
            if i[0] == parts[1]:
                print(i[1])
    elif line.startswith("printexa "):
        print(line[len("printexa "):])
    elif line.startswith("if "):
        parts = line.split(" ")
        if len(parts) != 4:
            shidierr("if","syntax","ifs must have three arguments",ptr)
        type = None
        if parts[2] == "matchnt":
            part1 = None
            part2 = parts[3]
            try:
                part2 = int(part2)
            except ValueError:
                shidierr("if","type",f"'{parts[3]}' is not an integer",ptr)
            for i in variables:
                if i[0] == parts[1]:
                    part1 = i[1]
            if part1 == None:
                shidierr("if","value",f"cannot find variable '{parts[1]}'",ptr)
            if part1 == part2:
                ptr += 1
        if parts[2] == "matches":
            part1 = None
            part2 = parts[3]
            try:
                part2 = int(part2)
            except ValueError:
                shidierr("if","type",f"'{parts[3]}' is not an integer",ptr)
            for i in variables:
                if i[0] == parts[1]:
                    part1 = i[1]
            if part1 == None:
                shidierr("if","value",f"cannot find variable '{parts[1]}'",ptr)
            if not part1 == part2:
                ptr += 1
        if parts[2] == "==":
            part1 = None
            part2 = None
            for i in variables:
                if i[0] == parts[1]:
                    part1 = i[1]
                if i[0] == parts[3]:
                    part2 = i[1]
            if part1 == None or part2 == None:
                shidierr("if","value","cannot find variables",ptr)
            if not part1 == part2:
                ptr += 1
        if parts[2] == "!=":
            part1 = None
            part2 = None
            for i in variables:
                if i[0] == parts[1]:
                    part1 = i[1]
                if i[0] == parts[3]:
                    part2 = i[1]
            if part1 == None or part2 == None:
                shidierr("if","value","cannot find variables",ptr)
            if part1 == part2:
                ptr += 1
    elif line.startswith("prompt "):
        parts = line.split(" ")
        found = False
        for i,v in enumerate(variables):
            if v[0] == parts[1]:
                found = True
                if v[2] == 1:
                    shidierr("prompt","type",f"'{parts[1]}' is not a string",ptr)
                uinput = input("> ")
                variables[i][1] = uinput
                variables[i][2] = 0
        if found == False:
            shidierr("prompt","value",f"could not find variable '{parts[1]}'",ptr)
    elif line.startswith("append"):
        # append string varname thing to add
        # append variable varname varname2
        parts = line.split(" ")
        if len(parts) < 4:
            shidierr("prompt","syntax","appends must have at least three arguments",ptr)
        if parts[1] == "string":
            found = False
            for i,v in enumerate(variables):
                if v[0] == parts[2]:
                    if v[2] == 1:
                        shidierr("append","type","cannot append to integers",ptr)
                    variables[i][1] += line[len(f"append string {parts[2]} "):]
                    found = True
            if found == False:
                shidierr("append","value",f"cannot find variable '{parts[2]}'",ptr)
        elif parts[1] == "variable":
            vindex1 = None
            part1 = None
            part2 = None
            for i,v in enumerate(variables):
                if v[0] == parts[2]:
                    if v[2] == 1:
                        shidierr("append","type",f"'{parts[2]}' is not a string",ptr)
                    vindex1 = i
                    part1 = v[1]
                if v[0] == parts[3]:
                    part2 = str(v[1])
            if part1 == None or part2 == None:
                shidierr("append","value","cannot find variables",ptr)
            variables[vindex1][1] = part1 + part2
        else:
            shidierr("variable","syntax",f"cannot recognize '{parts[1]}' selector",ptr)
    elif line.startswith("math "):
        # math add/sub/mult vv var1 var2 outvar
        # math add/sub/mult vi var1 (int) outvar
        # math add/sub/mult ii (int) (int) outvar
        parts = line.split(" ")
        if len(parts) != 6:
            shidierr("math","syntax","maths must have five arguments",ptr)
        part1 = None
        part2 = None
        if parts[2] == "vv":
            for i in variables:
                if i[0] == parts[3]:
                    part1 = i[1]
                if i[0] == parts[4]:
                    part2 = i[1]
        elif parts[2] == "vi":
            for i in variables:
                if i[0] == parts[3]:
                    part1 = i[1]
            try:
                part2 = int(parts[4])
            except ValueError:
                shidierr("math","type",f"'{parts[4]}' is not an integer",ptr)
        elif parts[2] == "ii":
            try:
                part1 = int(parts[3])
                part2 = int(parts[4])
            except ValueError:
                shidierr("math","type","arguments are not integers",ptr)
        else:
            shidierr("math","syntax",f"cannot recognize '{parts[2]}' selector",ptr)
        if part1 == None or part2 == None:
                shidierr("math","value","cannot find variables",ptr)
        found = False
        for i,v in enumerate(variables):
            if v[0] == parts[5]:
                found = True
                if parts[1] == "add":
                    variables[i][1] = part1 + part2
                    variables[i][2] = 1
                elif parts[1] == "neg":
                    variables[i][1] = part1 - part2
                    variables[i][2] = 1
                elif parts[1] == "mult":
                    variables[i][1] = part1 * part2
                    variables[i][2] = 1
                else:
                    shidierr("math","syntax",f"cannot find '{parts[1]}' selector",ptr)
        if found == False:
            shidierr("math","value",f"cannot find variable '{parts[5]}'",ptr)
    elif line.startswith("stop"):
        quit(0)
    elif line.startswith("clear"):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    elif line.startswith("random "):
        # random vv var1 var2 result
        # random vi var1 (int) result
        # random ii (int) (int) result
        parts = line.split(" ")
        if len(parts) != 5:
            shidierr("random","syntax","randoms must have four arguments",ptr)
        part1 = None
        part2 = None
        if parts[1] == "vv":
            for v in variables:
                if v[0] == parts[2]:
                    if v[2] == 0:
                        shidierr("random","type",f"variable '{parts[2]}' is not an integer",ptr)
                    part1 = v[1]
                if v[0] == parts[3]:
                    if v[2] == 0:
                        shidierr("random","type",f"variable '{parts[3]}' is not an integer",ptr)
                    part2 = v[1]
        elif parts[1] == "vi":
            for v in variables:
                if v[0] == parts[2]:
                    if v[2] == 0:
                        shidierr("random","type",f"variable '{parts[2]}' is not an integer",ptr)
                    part1 = v[1]
            try:
                part2 = parts[3]
            except ValueError:
                shidierr("random","type",f"'{parts[3]}' is not an integer",ptr)
        elif parts[1] == "ii":
            try:
                part1 = parts[2]
                part2 = parts[3]
            except ValueError:
                shidierr("random","type","arguments are not integers1",ptr)
        else:
            shidierr("random","syntax",f"cannot recognize '{parts[1]}' selector",ptr)
        if part1 == None:
            shidierr("random","value",f"could not find variable '{parts[2]}'",ptr)
        if part2 == None:
            shidierr("random","value",f"could not find variable '{parts[3]}'",ptr)
        try:
            part1 = int(part1)
            part2 = int(part2)
            if part1 < part2:
                result = random.randint(part1,part2)
            else:
                result = random.randint(part2,part1)
        except ValueError:
            shidierr("random","type","arguments are not integers",ptr)
        found = False
        for i,v in enumerate(variables):
            if v[0] == parts[4]:
                variables[i][1] = result
                variables[i][2] = 1
                found = True
        if found == False:
            shidierr("random","value",f"cannot find variable '{parts[4]}'",ptr)

if developer[0] == True:
    print("\033[0;36mprintvariables variables\033[0m")
    print(variables)
if developer[1] == True:
    print("\033[0;36mprintlabels labels\033[0m")
    print(labels)