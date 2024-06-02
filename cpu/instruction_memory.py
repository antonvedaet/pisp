class InstructionMemory:
    
    def __init__(self):
        self.memory = []

    def read(self, address):
        return self.memory[address]

    
