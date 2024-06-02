from register import Register
from instruction_memory import InstructionMemory
from data_memory import DataMemory
from ALU import ALU

class ControlUnit:
    
    def __init__(self, ram, rom):
        self.acc = Register()
        self.ir = Register()
        self.pc = Register()
        self.ip = Register()
        self.ram = ram
        self.rom = rom
        self.ALU = ALU()
    
    
    
    
        
        