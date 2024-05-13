from isa import *


class Translator:

    def __init__(self):
        self.instructions = []
        self.current_address = -1
        
    def next_address(self):
        self.current_address += 1
        return self.current_address
    
    def sections(self, source):
        stripped_src = []

        for l in source:
            l = l.strip()
            stripped_src.append(l)
        
        data, code = [], []
        section = None
        
        for line in stripped_src:
            if ".data" in line:
                section = data
            elif ".code" in line:
                section = code
            elif section is not None:
                section.append(line)
        return data, code
    

    def translate_data(self, data):
        [self.instructions.append({"idx" : self.next_address(),"opcode" : OpCode.NOP.value[0], "operand" : hex(eval(i.split()[-1])), "address" : False}) for i in data]
        return 
    
    def translate(self, src):
        data, code = self.sections(src)
        self.translate_data(data)
        return self.instructions

class Instruction:

    def __init__(self, idx, opcode, type, operand, address):
        self.idx = idx
        self.opcode = opcode
        self.type = type
        self.operand = operand
        self.address = address