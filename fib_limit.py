class Mini16CPU:
    def __init__(self, mem_size=256):
        self.reg = [0] * 16          
        self.pc = 0                 
        self.mem = [0] * mem_size   
        self.running = False
        self.zero = 0               
        self.carry = 0

    def reset(self):
        self.reg = [0] * 16
        self.pc = 0
        self.zero = 0
        self.carry = 0
        self.running = False

    def load_program(self, program, start_addr=0):
        for i, instr in enumerate(program):
            if instr > 0xFFFF : self.carry = 1
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
            self.carry = 0
            if self.reg[r1] + self.reg[r2] > 0xFFFF : self.carry = 1
            self.reg[r1] = (self.reg[r1] + self.reg[r2]) & 0xFFFF
            self.zero = int(self.reg[r1] == 0)

        elif opcode == 0x2:      # SUB
            self.carry = 0
            if self.reg[r1] - self.reg[r2] < 0xFFFF : self.carry = 1
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

        elif opcode == 0x8:      # JNZ 
            if not self.zero:
                self.pc = imm

        elif opcode == 0x9:      # JC
            if self.carry:
                self.pc = imm

        elif opcode == 0xA:      # JNC
            if not self.carry:
                self.pc = imm

        elif opcode == 0xB:     #INC
            self.reg[r1] += 1

        elif opcode == 0xC:     #MOV
            self.reg[r1] = self.reg[r2]

        elif opcode == 0xF:      # HALT
            self.running = False

    def run(self, max_cycles=1000): 
        self.running = True
        cycles = 0
        while self.running :
            self.step()
            cycles += 1


cpu = Mini16CPU()

# print("Enter number of terms of fibonacci : ")
# nfib = int(input())
# cpu.mem[20] = nfib
cpu.mem[21] = 0
cpu.mem[22] = 1

program = [

    0x0015,  #LOAD r0 0
    0x0116,  #LOAD r1 1
    0xB300,  #INC r3

    0xC200,  #MOV r0 -> r2
    0x1210,  #ADD r2, r1 -> r2
    0x920D,  #JC end = 12

    0xB300,  #INC r3
    0x930D,  #JC end = 12
    0x6317,  #STORE r3 -> mem[23]
    0x6218,  #STORE r1 -> mem[24]

    0xC010,  #MOV r1 -> r0
    0xC120,  #MOV r2 -> r1

    0x5003,  #JMP 2

    0xFFFF   #HLT


]

cpu.load_program(program)
cpu.run()

print("Inputs: ",cpu.mem[20], cpu.mem[21])
print("No. of fibonacci terms calculated :",cpu.mem[23]+1)
print("Largest Fibonacci Possible fpr 16 bit CPU : ",cpu.mem[24])