class ALU:
    

    def __init__(self):
        self.result = 0
        #flags
        self.N = 0
        self.Z = 0
        self.C = 0 #если при сдвиге бита направо становиться единичкой то число нечетное
    
    def add(self, a, b):
        return a + b
    
    def sub(self, a, b):
        return a - b