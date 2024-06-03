from instruction_memory import InstructionMemory
from data_memory import DataMemory
from data_path import DataPath

class ControlUnit:
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.ic = 0 #instr counter
        self.operations={
            "jmp": self.do_jump,
            "load": self.do_load,
            "store": self.do_store,
            "add": self.do_add,
            "sub": self.do_sub,
            "mod": self.do_mod
        }
    
    def run(self):
        while True:
            try:
                self.data_path.fetch_instruction()
                self.ic += 1
                if self.data_path.cr["opcode"] in self.operations:
                    print("n: "+ str(self.ic) +" | "+ self.operations[self.data_path.cr["opcode"]]() + " | " + self.data_path.info())
            except IndexError as _:
                print("------------------------------------------------------------------------------------------\n")
                print("Finished")
                break

    def do_load(self):
        if self.data_path.cr["address"] == False:
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.acc = self.data_path.dr
        else:
            self.data_path.dr = self.data_path.ram.read(int(self.data_path.cr["operand"], 16))
            self.data_path.acc = self.data_path.dr
        self.data_path.alu_flags()
        return "LOAD: DR => ACC"

    def do_store(self):
        assert self.data_path.cr["address"] == True
        self.data_path.ar = self.data_path.cr["operand"]
        self.data_path.dr = self.data_path.ar
        self.data_path.ram.write(int(self.data_path.ar, 16), self.data_path.acc)
        self.data_path.alu_flags()
        return "STORE: ACC => RAM[AR]"
    
    def do_jump(self):
        assert self.data_path.cr["address"] == True
        self.data_path.ar = int(self.data_path.cr["operand"], 16)
        self.data_path.ip = self.data_path.ar
        self.data_path.alu_flags()
        return "JUMP: AR => IP"

    def do_add(self):
        if self.data_path.cr["address"] == False:
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.ALU.add(int(self.data_path.acc, 16), int(self.data_path.dr, 16))
            self.data_path.acc = hex(self.data_path.ALU.value)
        else:
            self.data_path.dr = self.data_path.ram.read(int(self.data_path.cr["operand"], 16))
            self.data_path.ALU.add(int(self.data_path.acc, 16), int(self.data_path.dr, 16))
            self.data_path.acc = hex(self.data_path.ALU.value)
        self.data_path.alu_flags()
        return "ADD: ACC + DR => ACC"
    
    def do_sub(self):
        if self.data_path.cr["address"] == False:
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.ALU.sub(int(self.data_path.acc, 16), int(self.data_path.dr, 16))
            self.data_path.acc = hex(self.data_path.ALU.value)
        else:
            self.data_path.dr = self.data_path.ram.read(int(self.data_path.cr["operand"], 16))
            self.data_path.ALU.sub(int(self.data_path.acc, 16), int(self.data_path.dr, 16))
            self.data_path.acc = hex(self.data_path.ALU.value)
        self.data_path.alu_flags()
        return "SUB: ACC - DR => ACC"

    def do_mod(self):
        if self.data_path.cr["address"] == False:
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.ALU.mod(int(self.data_path.acc, 16), int(self.data_path.dr, 16))
            self.data_path.acc = hex(self.data_path.ALU.value)
        else:
            self.data_path.dr = self.data_path.ram.read(int(self.data_path.cr["operand"], 16))
            self.data_path.ALU.mod(int(self.data_path.acc, 16), int(self.data_path.dr, 16))
            self.data_path.acc = hex(self.data_path.ALU.value)
        self.data_path.alu_flags()
        return "MOD: ACC % DR => ACC"