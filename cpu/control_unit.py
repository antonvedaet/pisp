from instruction_memory import InstructionMemory
from data_memory import DataMemory
from data_path import DataPath
import sys
import time

IN = 0
OUT = 1

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
            "mod": self.do_mod,
            "hlt": self.do_hlt,
            # "shiftr": self.do_shiftr,
            # "shiftl":  self.do_shiftl
            "jifz": self.do_jifz,
            "jifnz": self.do_jifnz,
            "jifn": self.do_jifn,
            "jifnn": self.do_jifnn
        }
    
    def run(self):
        while True:
            try:
                self.data_path.fetch_instruction()
                self.ic += 1
                if self.data_path.cr["opcode"] in self.operations:
                    print("n: "+ str(self.ic) +" | "+ self.operations[self.data_path.cr["opcode"]]() + " | " + self.data_path.info())
                    print(self.data_path.ram.memory[0:7])
            except IndexError as _:
                print("------------------------------------------------------------------------------------------\n")
                print("Finished")
                break

    def do_load(self):
        if self.data_path.cr["address"] == False:
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.acc = self.data_path.dr
        else:
            self.data_path.ar = self.data_path.cr["operand"]
            self.data_path.dr = self.data_path.ar
            self.data_path.dr = self.data_path.ram.read(self.data_path.dr)
            self.data_path.acc = self.data_path.dr
        self.data_path.alu_flags()
        return "LOAD: DR => ACC"

    def do_store(self):
        assert self.data_path.cr["address"] == True
        self.data_path.ar = self.data_path.cr["operand"]
        self.data_path.ram.write(self.data_path.ar, self.data_path.acc)
        self.data_path.alu_flags()
        if self.data_path.ar == OUT:
            self.data_path.output.append(self.data_path.acc)
        return "STORE: ACC => RAM[AR]"
    
    def do_jump(self):
        assert self.data_path.cr["address"] == True
        self.data_path.dr = self.data_path.cr["operand"]
        self.data_path.ip = self.data_path.dr
        self.data_path.alu_flags()
        return "JUMP: AR => IP"

    def do_add(self):
        if self.data_path.cr["address"] == False:
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.ALU.add(self.data_path.acc, self.data_path.dr)
            self.data_path.acc = self.data_path.ALU.value
        else:
            self.data_path.dr = self.data_path.ram.read(self.data_path.cr["operand"])
            self.data_path.ALU.add(self.data_path.acc, self.data_path.dr)
            self.data_path.acc = self.data_path.ALU.value
        self.data_path.alu_flags()
        return "ADD: ACC + DR => ACC"
    
    def do_sub(self):
        if self.data_path.cr["address"] == False:
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.ALU.sub(self.data_path.acc, self.data_path.dr)
            self.data_path.acc = self.data_path.ALU.value
        else:
            self.data_path.dr = self.data_path.ram.read(self.data_path.cr["operand"])
            self.data_path.ALU.sub(self.data_path.acc, self.data_path.dr)
            self.data_path.acc = self.data_path.ALU.value
        self.data_path.alu_flags()
        return "SUB: ACC - DR => ACC"

    def do_mod(self):
        if self.data_path.cr["address"] == False:
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.ALU.mod(self.data_path.acc, self.data_path.dr)
            self.data_path.acc = self.data_path.ALU.value
        else:
            self.data_path.dr = self.data_path.ram.read(self.data_path.cr["operand"])
            self.data_path.ALU.mod(self.data_path.acc, self.data_path.dr)
            self.data_path.acc = self.data_path.ALU.value
        self.data_path.alu_flags()
        return "MOD: ACC % DR => ACC"

    def do_hlt(self):
        print("n: "+ str(self.ic) +" | "+ "HLT" + " | " + self.data_path.info())
        print(self.data_path.output)
        sys.exit()

    # def do_shiftr(self):
    #     self.data_path.ALU.shiftr(self.data_path.acc)
    #     self.data_path.acc = self.data_path.ALU.value
    #     self.data_path.alu_flags()
    #     return "SHIFTR: ACC >> 1 => ACC"

    # def do_shiftl(self):
    #     self.data_path.ALU.shiftl(self.data_path.acc)
    #     self.data_path.acc = self.data_path.ALU.value
    #     self.data_path.alu_flags()
    #     return "SHIFTL: ACC << 1 => ACC"

    def do_jifz(self):
        if(self.data_path.ALU.Z == 1):
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.ip = self.data_path.dr
        return "JIFZ: Z: DR => IP"

    def do_jifnz(self):
        if(self.data_path.ALU.Z != 1):
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.ip = self.data_path.dr
        return "JIFNZ:NOT Z: DR => IP"

    def do_jifn(self):
        if(self.data_path.ALU.N == 1):
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.ip = self.data_path.dr
        return "JIFN:N: DR => IP"

    def do_jifnn(self):
        if(self.data_path.ALU.N != 1):
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.ip = self.data_path.dr
        return "JIFNN:NOT N: DR => IP"