"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 32
        self.reg = [0] * 8
        self.pc = 0
        self.opcodes = {}

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,  # NOP
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,  # NOP
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):  # 🤖 ALU
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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

        print()

    def run(self):
        """Run the CPU."""
        IR = self.ram_read(self.pc)
        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)
        print("&&&&&&&", bin(IR), operand_a, operand_b)

        # may need some decode logic see Execution Sequence
        run = True
        HLT = None

        # while run:
        # LDI
        if IR is 0b10000010:
            # Set the value of a register to an integer.
            self.reg[operand_a] = operand_b

        # ADD is done by ALU
        print(self.alu(IR, operand_a, operand_b))

        # AND is done by ALU

        # CALL
        # if HLT
        # halt the CPU
        # exit the emulator
        #    pass

    def ram_read(self, mar):
        # mar = address; mdr = value per readme
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
