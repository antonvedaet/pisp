from isa import *
import json


class Translator:

    def __init__(self):
        self.instructions = []
        self.instr_current_address = -1
        self.data_current_address = 1
        self.labels = {}
        self.vars = {}
        
    def next_instr_address(self):
        self.instr_current_address += 1
        return hex((self.instr_current_address))

    def next_data_address(self):
        self.data_current_address += 1
        return hex((self.data_current_address))
    
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
    

    def parse_instruction(self, line):
        instruction, operand = line.split()
        for opcode in OpCode:
            if str(opcode) == instruction:
                if str(opcode) == "jmp" and operand in self.labels.keys():
                    return {
                        "idx": self.next_instr_address(),
                        "opcode": str(opcode),
                        "operand": hex(eval(self.labels[operand])),
                        "address": True
                    }
                if "&" not in operand:
                    if not operand.isdigit():
                        return {
                            "idx": self.next_instr_address(),
                            "opcode": str(opcode),
                            "operand": self.vars[operand],
                            "address": False
                        }
                    else:    
                        return {
                            "idx": self.next_instr_address(),
                            "opcode": str(opcode),
                            "operand": hex(eval(operand)),
                            "address": False
                        }
                if "&" in operand and operand[1:].isdigit():
                    return {
                        "idx": self.next_instr_address(),
                        "opcode": str(opcode),
                        "operand": hex(eval(operand[1::])),
                        "address": True
                    }
                else:
                    return {
                        "idx": self.next_instr_address(),
                        "opcode": str(opcode),
                        "operand": self.vars[operand[1:]],
                        "address": True
                    }

    def translate_data(self, data):
        for i in data:
            self.instructions.append({"idx" : self.next_data_address(),"opcode" : OpCode.NOP.value[0], "operand" : hex(eval(i.split()[-1])), "address" : False})
            self.vars[i.split(":")[0]] = hex(eval(i.split()[-1]))
        return 

    def translate_code(self, code):
        for line in code:
            if line == "begin:":
                continue
            if line[-1]==":":
                self.labels[line[:-1]] = hex(self.instr_current_address+1)
                continue
            if line[0]==":":
                continue
            if line == "end":
                break
            self.instructions.append(self.parse_instruction(line))

    def translate(self, src):
        data, code = self.sections(src)
        self.translate_data(data)
        self.translate_code(code)
        return self.instructions

    def save_as_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.instructions, f, indent=4)
