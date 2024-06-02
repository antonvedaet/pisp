class InstructionMemory:
    
    def __init__(self, size):
        self.memory = [0] * size

    def read(self, address):
        return self.memory[address]

    def write(self, address, instr, operand):
        self.memory[address] = {instr: operand}
