# Виртуальные машины
# - JVM, CLR, VM Python, VM Lua, ...
# - Эмуляторы реальных процессоров.
# вариант 27
import argparse
import json
from pprint import pprint

def translate(program):
    program = json.loads(program)
    output = []
    for cmd in program:
        if cmd["op"] == "const":
            value = cmd["value"]
            adress = cmd["adress"]
            output.append(("const", value, adress))
        elif cmd["op"] == "read":
            adressB = cmd["adressB"]
            adressC = cmd["adressC"]
            output.append(("read", adressB, adressC))
        elif cmd["op"] == "write":
            adressB = cmd["adressB"]
            adressC = cmd["adressC"]
            output.append(("write", adressB, adressC))
        elif cmd["op"] == "negate":
            shift = cmd["shift"]
            adressC = cmd["adressC"]
            adressD = cmd["adressD"]
            output.append(("negate", shift, adressC, adressD))
    return output

parser = argparse.ArgumentParser()
parser.add_argument("--path", "-p", help="Путь к исходному файлу с текстом программы")
parser.add_argument("--output", "-o", help="Путь к двоичному файлу-результату")
parser.add_argument("--test", "-t", help="Режим тестирования")

args = parser.parse_args()
print(args)
with open(args.path, "r") as f:
    program = f.read()
ir = translate(program)
with open(args.output, "w") as f:
    f.write(str(ir))
pprint(ir)
