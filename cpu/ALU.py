MIN_VALUE = -(2**32)
MAX_VALUE = (2**32) - 1

class ALU:
    

    def __init__(self):
        self.value = 0
        #flags
        self.N = 0
        self.Z = 1
        self.C = 0 #если при сдвиге бита направо становиться единичкой то число нечетное
    
    def refresh_flags(self):
        if self.value > MAX_VALUE or self.value < MIN_VALUE:
            self.C = 1
            self.value %= (MAX_VALUE + 1)
        else:    
            if self.value < 0:
                self.N = 1
            else:
                self.N = 0

            if self.value == 0:
                self.Z = 1
            else:
                self.Z = 0

    def flags(self):
        return self.N * 100 + self.Z * 10 + self.C

    def add(self, a, b):
        self.value = a + b
        self.refresh_flags()
    
    def sub(self, a, b):
        self.value = a - b
        self.refresh_flags()

    def mod(self, a, b):
        self.value = a % b
        self.refresh_flags()