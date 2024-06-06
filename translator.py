import json

from isa import OpCode, OpType


class Translator:

    def __init__(self):
        self.instructions = []
        self.instr_current_address = -1
        self.data_current_address = 1
        self.labels = {}
        self.vars = {"in": {"val":0, "adr":0}, "out": {"val":0, "adr":1}}

    def next_instr_address(self):
        self.instr_current_address += 1
        return (self.instr_current_address)

    def next_data_address(self):
        self.data_current_address += 1
        return (self.data_current_address)

    def sections(self, source):
        stripped_src = []

        for line in source:
            line = line.strip()
            stripped_src.append(line)

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
        if len(line.split())>1:
            instruction, operand = line.split()
        else:
            instruction = line.split()[0]
        for opcode in OpCode:
            if str(opcode) == instruction and opcode.get_type() == OpType.NARG:
                return {
                        "idx": self.next_instr_address(),
                        "opcode": str(opcode),
                        "operand": None,
                        "address": False,
                        "relative": False,
                    }
            if str(opcode) == instruction and (opcode.get_type() == OpType.ARG or opcode.get_type() == OpType.JUMP):
                if str(opcode) == instruction and opcode.get_type() == OpType.JUMP and operand in self.labels.keys():
                    return {
                        "idx": self.next_instr_address(),
                        "opcode": str(opcode),
                        "operand": eval(self.labels[operand]),
                        "address": True,
                        "relative": False,
                    }
                if "&" not in operand and str(opcode) == instruction:
                    if not operand.isdigit() and operand[0] != "-":
                        return {
                            "idx": self.next_instr_address(),
                            "opcode": str(opcode),
                            "operand": self.vars[operand]["adr"],
                            "address": True,
                            "relative": False,
                        }
                    else:
                        return {
                            "idx": self.next_instr_address(),
                            "opcode": str(opcode),
                            "operand": eval(operand),
                            "address": False,
                            "relative": False,
                        }
                if "&" in operand and operand[1:].isdigit():
                    return {
                        "idx": self.next_instr_address(),
                        "opcode": str(opcode),
                        "operand": eval(operand[1::]),
                        "address": True,
                        "relative": False,
                    }
                else:
                    try:
                        return {
                            "idx": self.next_instr_address(),
                            "opcode": str(opcode),
                            "operand": self.labels[operand],
                            "address": True,
                            "relative": False,
                        }
                    except KeyError:
                        return {
                            "idx": self.next_instr_address(),
                            "opcode": str(opcode),
                            "operand": self.vars[operand[1:]]["adr"],
                            "address": True,
                            "relative": True,
                        }

    def translate_data(self, data):
        for i in data:
            if i.split()[-1].isdigit():
                self.instructions.append({"idx" : self.next_data_address(),"opcode" : OpCode.NOP.value[0], "operand" : eval(i.split()[-1]), "address" : False})
                self.vars[i.split(":")[0]] = {"val":eval(i.split()[-1]), "adr":self.data_current_address}
            else:
                self.vars[i.split(":")[0]] = {"val":0, "adr":self.data_current_address + 1}
                for j in " ".join(i.split()[1:])[1:-1:]:
                    self.instructions.append({"idx" : self.next_data_address(),"opcode" : OpCode.NOP.value[0], "operand" : (j), "address" : False})
                self.instructions.append({"idx" : self.next_data_address(),"opcode" : OpCode.NOP.value[0], "operand" : "\0", "address" : False})

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
        with open(filename, "w") as f:
            json.dump(self.instructions, f, indent=4)
