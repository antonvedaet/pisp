import utils.ioutils

import sys

IN = 0
OUT = 1

class ControlUnit:
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.ic = 0 #instr counter
        self.ticks = 0 
        self.operations={
            "jmp": self.do_jump,
            "load": self.do_load,
            "store": self.do_store,
            "add": self.do_add,
            "sub": self.do_sub,
            "mod": self.do_mod,
            "hlt": self.do_hlt,
            "jifz": self.do_jifz,
            "jifnz": self.do_jifnz,
            "jifn": self.do_jifn,
            "jifnn": self.do_jifnn
        }
        self.log = ""
    
    def run(self):
        print("Input:" + str(self.data_path.input))
        while True:
            try:
                self.data_path.fetch_instruction()
                self.ic += 1
                if self.data_path.cr["opcode"] in self.operations:
                    self.log += ("INSTRUCTION: "+ str(self.ic) +" | "+ self.operations[self.data_path.cr["opcode"]]() + " | " + self.data_path.info() + " | TICK: " + str(self.ticks) + "\n")
            except IndexError as _:
                break

    def do_load(self):
        self.data_path.ar = self.data_path.cr["operand"]
        if self.data_path.ar == IN and self.data_path.cr["address"]:
            self.data_path.dr = self.data_path.input[0]
            self.data_path.input.pop(0)
            self.data_path.acc = self.data_path.dr
        elif self.data_path.cr["address"] is False:
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.acc = self.data_path.dr
        else:
            if self.data_path.cr["relative"] is False:
                self.data_path.dr = self.data_path.ar
                self.data_path.dr = self.data_path.ram.read(self.data_path.dr)
                self.data_path.acc = self.data_path.dr
            else:
                self.data_path.dr = self.data_path.ar
                self.data_path.dr = self.data_path.ram.read(self.data_path.dr)
                self.data_path.dr = self.data_path.ram.read(self.data_path.dr)
                self.data_path.acc = self.data_path.dr
        self.data_path.alu_flags()
        self.ticks += 3
        return "LOAD: DR => ACC"

    def do_store(self):
        assert self.data_path.cr["address"]
        self.data_path.ar = self.data_path.cr["operand"]
        self.data_path.ram.write(self.data_path.ar, self.data_path.acc)
        self.data_path.alu_flags()
        if self.data_path.ar == OUT and self.data_path.acc!="\u0000":
            self.data_path.output.append(self.data_path.acc)
        self.ticks += 2
        return "STORE: ACC => RAM[AR]"
    
    def do_jump(self):
        assert self.data_path.cr["address"]
        self.data_path.ar = self.data_path.cr["operand"]
        self.data_path.dr = self.data_path.ar 
        self.data_path.ip = self.data_path.dr
        self.data_path.alu_flags()
        self.ticks += 3
        return "JUMP: DR => IP"

    def do_add(self):
        if self.data_path.cr["address"] is False:
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.ALU.add(self.data_path.acc, self.data_path.dr)
            self.data_path.acc = self.data_path.ALU.value
        else:
            self.data_path.dr = self.data_path.ram.read(self.data_path.cr["operand"])
            self.data_path.ALU.add(self.data_path.acc, self.data_path.dr)
            self.data_path.acc = self.data_path.ALU.value
        self.data_path.alu_flags()
        self.ticks += 3
        return "ADD: ACC + DR => ACC"
    
    def do_sub(self):
        if self.data_path.cr["address"] is False:
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.ALU.sub(self.data_path.acc, self.data_path.dr)
            self.data_path.acc = self.data_path.ALU.value
        else:
            self.data_path.dr = self.data_path.ram.read(self.data_path.cr["operand"])
            self.data_path.ALU.sub(self.data_path.acc, self.data_path.dr)
            self.data_path.acc = self.data_path.ALU.value
        self.data_path.alu_flags()
        self.ticks += 3
        return "SUB: ACC - DR => ACC"

    def do_mod(self):
        if self.data_path.cr["address"] is False:
            self.data_path.dr = self.data_path.cr["operand"]
            self.data_path.ALU.mod(self.data_path.acc, self.data_path.dr)
            self.data_path.acc = self.data_path.ALU.value
        else:
            self.data_path.dr = self.data_path.ram.read(self.data_path.cr["operand"])
            self.data_path.ALU.mod(self.data_path.acc, self.data_path.dr)
            self.data_path.acc = self.data_path.ALU.value
        self.data_path.alu_flags()
        self.ticks += 3
        return "MOD: ACC % DR => ACC"

    def do_hlt(self):
        self.ticks += 1
        self.log += ("INSTRUCTION: "+ str(self.ic) +" | "+ "HLT" + " | " + self.data_path.info() + " | TICK: " + str(self.ticks) + "\n")
        print(self.log)
        utils.ioutils.write_output(self.log, "io/cpu.log")
        print(self.data_path.output)
        utils.ioutils.write_output(str(self.data_path.output))
        sys.exit()

    def do_jifz(self):
        if(self.data_path.ALU.Z == 1):
            self.data_path.ar = self.data_path.cr["operand"]
            self.data_path.dr = self.data_path.ar 
            self.data_path.ip = self.data_path.dr
        self.ticks += 3
        return "JIFZ: Z: DR => IP"

    def do_jifnz(self):
        if(self.data_path.ALU.Z != 1):
            self.data_path.ar = self.data_path.cr["operand"]
            self.data_path.dr = self.data_path.ar 
            self.data_path.ip = self.data_path.dr
        self.ticks += 3
        return "JIFNZ:NOT Z: DR => IP"

    def do_jifn(self):
        if(self.data_path.ALU.N == 1):
            self.data_path.ar = self.data_path.cr["operand"]
            self.data_path.dr = self.data_path.ar 
            self.data_path.ip = self.data_path.dr
        self.ticks += 3
        return "JIFN:N: DR => IP"

    def do_jifnn(self):
        if(self.data_path.ALU.N != 1):
            self.data_path.ar = self.data_path.cr["operand"]
            self.data_path.dr = self.data_path.ar 
            self.data_path.ip = self.data_path.dr
        self.ticks += 3
        return "JIFNN:NOT N: DR => IP"