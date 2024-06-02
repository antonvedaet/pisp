class InstructionMemory:
    
    def __init__(self, size):
        self.memory = [0] * size

    def read(self, address):
        return self.memory[address]

    
