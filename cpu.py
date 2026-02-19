class Mini16CPU:
    def __init__(self, mem_size=256):
        self.reg = [0] * 16          # 16 general purpose registers
        self.pc = 0                 # program counter
        self.mem = [0] * mem_size   # 16-bit memory
        self.running = False
        self.zero = 0               # zero flag

    def reset(self):
        self.reg = [0] * 16
        self.pc = 0
        self.zero = 0
        self.running = False

    def load_program(self, program, start_addr=0):
        for i, instr in enumerate(program):
            self.mem[start_addr + i] = instr & 0xFFFF

    def fetch(self):
        instr = self.mem[self.pc]
        self.pc = (self.pc + 1) & 0xFFFF
        return instr

    def decode(self, instr):
        opcode = (instr >> 12) & 0xF
        r1 = (instr >> 8) & 0xF
        r2 = (instr >> 4) & 0xF
        imm = instr & 0xFF
        return opcode, r1, r2, imm

    def step(self):
        instr = self.fetch()
        opcode, r1, r2, imm = self.decode(instr)

        if opcode == 0x0:        # LOAD
            self.reg[r1] = self.mem[imm]

        elif opcode == 0x1:      # ADD
            self.reg[r1] = (self.reg[r1] + self.reg[r2]) & 0xFFFF
            self.zero = int(self.reg[r1] == 0)

        elif opcode == 0x2:      # SUB
            self.reg[r1] = (self.reg[r1] - self.reg[r2]) & 0xFFFF
            self.zero = int(self.reg[r1] == 0)

        elif opcode == 0x3:      # AND
            self.reg[r1] &= self.reg[r2]
            self.zero = int(self.reg[r1] == 0)

        elif opcode == 0x4:      # OR
            self.reg[r1] |= self.reg[r2]
            self.zero = int(self.reg[r1] == 0)

        elif opcode == 0x5:      # JMP
            self.pc = imm

        elif opcode == 0x6:      # STORE
            self.mem[imm] = self.reg[r1] & 0xFFFF

        elif opcode == 0x7:      # JZ
            if self.zero:
                self.pc = imm

        elif opcode == 0xF:      # HALT
            self.running = False

    def run(self, max_cycles=1000):
        self.running = True
        cycles = 0
        while self.running and cycles < max_cycles:
            self.step()
            cycles += 1


cpu = Mini16CPU()
cpu.mem[20] = 9
cpu.mem[21] = 6

program = [
    0x0014,  # LOAD r0, [20]
    0x0115,  # LOAD r1, [21]

    0x2010,  # SUB  r0, r1
    0x3010,  # AND  r0, r1
    0x1200,  # ADD  r2, r0
    0x6216,  # STORE r2, [22]

    0x0014,  # LOAD r0, [20]

    0x4020,  # OR   r2, r0
    0x1010,  # ADD  r0, r1
    0x1300,  # ADD  r3, r0
    0x700C,  # JZ   12
    0x6317,  # STORE r3, [23]

    0x0115,  # LOAD r1, [21]

    0x2010,  # SUB  r0, r1
    0x3010,  # AND  r0, r1
    0x1200,  # ADD  r2, r0
    0x6216,  # STORE r2, [22]
    
    0x0014,  # LOAD r0, [20]
    0xF000   # HALT
]

cpu.load_program(program)
cpu.run()

print("Inputs: ",cpu.mem[20], cpu.mem[21])
print("Outputs: ",cpu.mem[22], cpu.mem[23])