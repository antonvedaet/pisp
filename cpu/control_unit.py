from instruction_memory import InstructionMemory
from data_memory import DataMemory
from data_path import DataPath
from ALU import ALU

class ControlUnit:
    
    def __init__(self, data_path):
        self.ALU = ALU()
        self.data_path = data_path
        

    def do_load(self):
        if self.data_path.cr["address"] == False:
            self.data_path.acc = self.data_path.cr["operand"]
        else:
            self.data_path.acc = self.data_path.ram.read(int(self.data_path.cr["operand"], 16))

    def do_store(self):
        assert self.data_path.cr["address"] == True
        self.data_path.ram.write(int(self.data_path.cr["operand"], 16), self.data_path.acc)
            