MIN_VALUE = -(2**32)
MAX_VALUE = (2**32) - 1

class ALU:
    

    def __init__(self):
        self.value = 0
        #refresh_flags
        self.N = 0
        self.Z = 0
        self.C = 0 #если при сдвиге бита направо становиться единичкой то число нечетное
    
    def refresh_flags(self):
        if self.value == 0:
            self.N = True
        else:
            self.N = False
        
        if self.value > MAX_VALUE or self.value < MIN_VALUE:
            self.C = True
        else:
            self.C = False

        if self.value < 0:
            self.Z = True
        else:
            self.Z = False

    def add(self, a, b):
        self.value = a + b
        self.refresh_flags()
    
    def sub(self, a, b):
        self.value = a - b
        self.refresh_flags()

    def div(self, a, b):
        self.value = a / b
        self.refresh_flags()

    def mul(self, a, b):
        self.value = a * b
        self.refresh_flags()

    def mod(self, a, b):
        self.value = a % b
        self.refresh_flags()