from isa import *


class Translator:

    def __init__(self):
        self.instructions = []
        self.current_address = 0
    
    def add_instruction(self, instruction):
        if instruction.idx > MAX_INSTR_ADDRESS:
            raise Exception()
        self.instructions.append(instruction)
        self.current_address += 1

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
    


    def translate(self, src):
        data, code = self.sections(src)
        return data, code

class Instruction:

    def __init__(self, idx, opcode, type, operand, address):
        self.idx = idx
        self.opcode = opcode
        self.type = type
        self.operand = operand
        self.address = address