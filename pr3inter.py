import argparse
import pprint

mem = [0, 0, 0, 0, 0]

def execute(program):
    for op, *args in program:
        if op == "const":
            const = args[0]
            adressC = args[1]
            mem[adressC] = const
            
        elif op == "negate":
            shift = args[0]
            adressC = args[1]
            adressD = args[2]
            adress = mem[adressC] + shift
            value = mem[adress]
            mem[mem[adressD]] = -value
            
        elif op == "read":
            adressB = args[0]
            adressC = args[1]
            mem[adressC] = mem[adressB]
            
        elif op == "write":
            adressB = args[0]
            adressC = args[1]
            mem[adressB] = mem[adressC]

parser = argparse.ArgumentParser()
parser.add_argument("--path", "-p", help="Путь к файлу с промежуточным представлением")
parser.add_argument(
    "--dump",
    "-d",
    help="Путь к файлу, куда будет сохранен дамп памяти после выполнения программ",
)
parser.add_argument("--range", "-r", help="Диапазон адресов памяти для вывода дампа")
args = parser.parse_args()
print(args)
with open(args.path, "r") as f:
    program = f.read()
program = eval(program)
pprint.pprint(program)
execute(program)
print(mem)
