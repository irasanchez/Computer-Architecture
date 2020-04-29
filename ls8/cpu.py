"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 32
        self.reg = [0] * 8
        self.pc = 0

    def load(self, filename):
        """Load a program into memory."""
        print("Loading program...")
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
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def run(self):
        """Run the CPU."""

        # may need some decode logic see Execution Sequence

        while True:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            if IR == HLT:
                print("Exit")
                break
            # LDI
            if IR == LDI:
                # Set the value of a register to an integer.

                self.reg[operand_a] = operand_b

                self.pc += 3
            if IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            if IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

        # ADD is done by ALU
        # print(self.alu(IR, operand_a, operand_b))

        # AND is done by ALU

        # CALL
        #    pass

    def ram_read(self, mar):
        # mar = address; mdr = value per readme
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
