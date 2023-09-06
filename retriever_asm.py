"""
File:    retriever_asm.py
Author:  Mofe Okonedo
E-mail:  eokoned1@umbc.edu
Description: A version of the simplified Assembly Language in Python
  Knobs
"""


def create_ram(size):
    """
    Create and return a list of size filled with zeros
    """
    return [0] * size


def read_program(filename):
    """
    Read program from file and return a list of lines
    """
    with open(filename, 'r') as f:
        program = f.readlines()
    return program


def parse_value(value, ram):
    """
    Parse the value and return its corresponding integer value
    """
    if '[' in value and ']' in value:
        return ram[int(value.strip('[]'))]
    else:
        return int(value)


def mov(instruction, ram):
    """
    Move data from one memory location to another
    """
    _, dest, src = instruction.split()
    dest = int(instruction.split()[1].strip('[]'))
    src = parse_value(src, ram)
    ram[dest] = src


def add(instruction, ram):
    """
    Add two values and store result in destination
    """
    _, dest, arg1, arg2 = instruction.split()
    dest = int(instruction.split()[1].strip('[]'))
    arg1 = parse_value(arg1, ram)
    arg2 = parse_value(arg2, ram)
    ram[dest] = arg1 + arg2


def sub(instruction, ram):
    """
    Subtract two values and store result in destination
    """
    _, dest, arg1, arg2 = instruction.split()
    dest = int(instruction.split()[1].strip('[]'))
    arg1 = parse_value(arg1, ram)
    arg2 = parse_value(arg2, ram)
    ram[dest] = arg1 - arg2


def mul(instruction, ram):
    """
    Multiply two values and store result in destination
    """
    _, dest, arg1, arg2 = instruction.split()
    dest = int(instruction.split()[1].strip('[]'))
    arg1 = parse_value(arg1, ram)
    arg2 = parse_value(arg2, ram)
    ram[dest] = arg1 * arg2


def div(instruction, ram):
    """
    Divide two values and store result in destination
    """
    _, dest, arg1, arg2 = instruction.split()
    dest = int(instruction.split()[1].strip('[]'))
    arg1 = parse_value(arg1, ram)
    arg2 = parse_value(arg2, ram)
    if arg2 == 0:
        print("Division by zero error")
        return
    ram[dest] = arg1 // arg2


def mod(instruction, ram):
    """
    Calculate remainder of division and store result in destination
    """
    _, dest, arg1, arg2 = instruction.split()
    dest = int(instruction.split()[1].strip('[]'))
    arg1 = parse_value(arg1, ram)
    arg2 = parse_value(arg2, ram)
    if arg2 == 0:
        print("Division by zero error")
        return
    ram[dest] = arg1 % arg2


def jmp(instruction, ram, ic, flags):
    """
    Set instruction counter to specified location
    """
    location = parse_value(instruction.split()[1], ram)

    # Check for conditional jump instructions
    if instruction[0:2] == "JL":
        if flags['less']:
            ic[0] = location
        else:
            ic[0] += 1
    elif instruction[0:2] == "JG":
        if flags['greater']:
            ic[0] = location
        else:
            ic[0] += 1
    elif instruction[0:3] == "JLE":
        if flags['less'] or flags['equal']:
            ic[0] = location
        else:
            ic[0] += 1
    elif instruction[0:3] == "JGE":
        if flags['greater'] or flags['equal']:
            ic[0] = location
        else:
            ic[0] += 1
    elif instruction[0:2] == "JE":
        if flags['equal']:
            ic[0] = location
        else:
            ic[0] += 1
    elif instruction[0:3] == "JNE":
        if not flags['equal']:
            ic[0] = location
        else:
            ic[0] += 1
    else:
        ic[0] = location



def cmp(instruction, ram, flags):
    """
    Compare two values and set flags accordingly
    """
    _, arg1, arg2 = instruction.split()
    arg1 = parse_value(arg1, ram)
    arg2 = parse_value(arg2, ram)
    if arg1 < arg2:
        flags['less'] = True
        flags['equal'] = False
    elif arg1 > arg2:
        flags['less'] = False
        flags['equal'] = False
    else:
        flags['less'] = False
        flags['equal'] = True


def interrupt(instruction, ram):
    """
    Read integer input from user and store it in destination memory location
    :param split_instruction:
    :param ram:
    """
    split_instruction = instruction.split()
    if 'print' in instruction.lower():
        if '[' in split_instruction[2]:
            print(ram[int(split_instruction[2].strip('[]'))])
        else:
            print(' '.join(split_instruction[2:]))
    else:
        input2 = int(input(">> "))
        dest = int(split_instruction[2].strip("[]"))
        ram[dest] = input2


def hlt(ic):
    """
    Halt the program by setting the instruction counter to -1
    """
    ic[0] = -2


def nop(instruction, ram):
    """
    Do nothing
    """
    pass


def run_program(program, ram):
    """
    Execute program on RAM
    """
    ic = [0]  # Instruction counter
    flags = {'less': False, 'equal': False, 'greater': False}
    jump_flag = False

    while ic[0] < len(program):
        instruction = program[ic[0]].strip()
        if instruction == "":  # NOP
            pass
        elif instruction.split()[0] == "MOV":
            mov(instruction, ram)
        elif instruction.split()[0] == "ADD":
            add(instruction, ram)
        elif instruction.split()[0] == "SUB":
            sub(instruction, ram)
        elif instruction.split()[0] == "MUL":
            mul(instruction, ram)
        elif instruction.split()[0] == "DIV":
            div(instruction, ram)
        elif instruction.split()[0] == "MOD":
            mod(instruction, ram)
        elif "J" in instruction.split()[0]:
            jmp(instruction, ram, ic, flags)
            jump_flag = True
        elif instruction.split()[0] == "CMP":
            cmp(instruction, ram, flags)
        elif instruction.split()[0] == 'HLT':
            hlt(ic)
            return
        elif instruction.split()[0] == "INT":
            interrupt(instruction, ram)
        else:
            print(f"Invalid instruction: {instruction}")

        if not jump_flag:
            ic[0] += 1
        else:
            jump_flag = False


if __name__ == "__main__":
    user_file = input("Enter program filename: ")
    file_name, size = user_file.split()[0], user_file.split()[1]
    ram = create_ram(int(size))
    run_program(read_program(file_name), ram) # pass filename and ram as arguments to run_program()
    print("Program execution complete")




