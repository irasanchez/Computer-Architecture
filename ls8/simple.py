import sys
​
PRINT_TIM = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4
PRINT_REGISTER = 5
ADD = 6
PUSH = 7
POP = 8
​
memory = [0] * 256
​
running = True
pc = 0
sp = 0xF4
​
registers = [0] * 8  # [0, 0, 0, 0, 0, 0, 0, 0]
​
# FF
# FE
# .
# .
# F5: 0 <-- SP
# F4
# F3: 99
​
​
if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} filename")
    sys.exit(2)
​


def load_memory(filename):
    try:
        address = 0
        with open(filename) as file:
            for line in file:
                comment_split = line.split("#")
                number_string = comment_split[0].strip()
                if number_string == '':
                    continue
                # num = int(number_string, 2)
                num = int(number_string)
            # print("{:08b} is {:d}".format(num, num))
            # print(f"{num:>08b} is {num:>0d}")
                memory[address] = num
                address += 1
    except FileNotFoundError:
        print(f"{sys.argv[0]}: could not find {sys.argv[1]}")
        sys.exit(2)


​
load_memory(sys.argv[1])
​
while running is True:
    command = memory[pc]
    if command == PRINT_TIM:
        print("Tim!")
        pc += 1
    elif command == PRINT_NUM:
        print(memory[pc + 1])
        pc += 2
    elif command == SAVE:
        reg_index = memory[pc + 2]
        number_to_save = memory[pc + 1]
        registers[reg_index] = number_to_save
        pc += 3
    elif command == PRINT_REGISTER:
        reg_index = memory[pc + 1]
        print(registers[reg_index])
        pc += 2
    elif command == ADD:
     # reg1 = reg1 + reg2
        reg_1 = memory[pc + 1]
        reg_2 = memory[pc + 2]
        registers[reg_1] = registers[reg_1] + registers[reg_2]
        pc += 3
    elif command == PUSH:
        reg_1 = memory[pc + 1]
        val = registers[reg_1]
        sp -= 1
        memory[sp] = val
        pc += 2
    elif command == POP:
        data = memory[sp]
        reg_address = memory[pc + 1]
        registers[reg_address] = data
        sp -= 1
        pc += 2
    elif command == HALT:
        running = False
    else:
        print("Error!")
        sys.exit(1)
