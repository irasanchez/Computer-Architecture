"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.count = 0
        self.running = False
        self.pc = 0x00
        self.ram = [0] * 256
        self.fl = [8] * 8
        self.reg = [0] * 8
        self.reg[7] = 0xF4  # hexcode
        self.opcodes = {
            # this key value order allows us to pass in operands to find the instruction
            0b00000001: "HLT",
            0b10000010: "LDI",
            0b01000111: "PRN",
            0b10100010: "MUL",
            0b01000101: "PUSH",
            0b01000110: "POP",
            0b01010000: "CALL",
            0b00010001: "RET",
            0b10100000: "ADD",
            0b10100111: "CMP",
            0b01010100: "JUMP",
            0b01010101: "JEQ",
            0b01010110: "JNE"
        }
        self.branchtable = {
            "HLT": self.hlt,
            "LDI": self.ldi,
            "PRN": self.prn,
            "PUSH": self.push,
            "POP": self.pop,
            "CALL": self.call,
            "RET": self.ret,
            "JUMP": self.jump,
            "JEQ": self.jeq,
            "JNE": self.jne
        }

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as file:
                for line in file:
                    comment_split = line.split("#")
                    number_string = comment_split[0].strip()

                    if number_string == '':
                        continue

                    num = int(number_string, 2)
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: could not find {sys.argv[1]}')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            a = self.reg[reg_a]
            b = self.reg[reg_b]

            if a == b:
                self.fl[-1] = 1  # E flag on
            else:
                self.fl[-1] = 0  # E flag off

            if a < b:
                self.fl[-2] = 1  # L flag on
            else:
                self.fl[-2] = 0  # L flag off

            if a > b:
                self.fl[-3] = 1  # G flag on
            else:
                self.fl[-3] = 0  # G flag off
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"\n\nTRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def ram_read(self, mar):
        # mar = address; mdr = value per readme
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU."""

        self.running = True

        while self.running:
            self.count += 1
            IR = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # isolate first 2 digits
            num_operands = (IR >> 6)

            # AABCDDDD
            # check position C for 0 or 1 for set pc instruction
            sets_pc = ((IR >> 4) & 0b001) == 1
            # check position B for 0 or 1 for alu instruction
            is_alu_operation = (IR >> 5 & 0b001)

            opcode = self.opcodes[IR]

            if not sets_pc:
                self.pc += 1 + num_operands

            if is_alu_operation:
                self.alu(opcode, operand_a, operand_b)
            else:
                # self.branchtable[opcode] is gonna be something like self.hlt() or self.ldi()
                # execute non-arithmetic commands
                self.branchtable[opcode](operand_a, operand_b)

    def hlt(self, _, __):
        print("HALTING")
        self.running = False  # can also do sys.exit instead

    def prn(self, operand_a, _):
        print("PRINTING ==>", self.reg[operand_a])

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def push(self, operand_a, _):  # "bury" in Turing's version
        self.reg[7] -= 1  # update sp
        sp = self.reg[7]  # new sp
        value = self.reg[operand_a]  # copy value from reg
        self.ram_write(sp, value)  # write it to memory

    def pop(self, operand_a, _):
        sp = self.reg[7]
        value = self.reg[sp]
        self.reg[7] += 1

    def call(self, operand_a, _):
        self.reg[7] -= 1
        sp = self.reg[7]
        self.ram_write(sp, self.pc + 2)
        self.jump(operand_a, _)

    def ret(self, operand_a, _):
        sp = self.reg[7]
        return_address = self.ram_read(sp)
        self.pc = return_address

    def jump(self, operand_a, _):
        self.pc = self.reg[operand_a]

    def jeq(self, operand_a, _):
        if self.fl[-1] == 1:  # E flag
            self.jump(operand_a, _)
        else:
            self.pc += 2

    def jne(self, operand_a, _):
        if self.fl[-1] == 0:  # E flag
            self.jump(operand_a, _)
        else:
            self.pc += 2
