class DataMemory:

    def __init__(self, size):
        self.memory = [0] * size

    def read(self, address):
        return self.memory[address]

    def write(self, address, data):
        self.memory[address] = data
