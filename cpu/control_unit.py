from register import Register
from instruction_memory import InstructionMemory
from data_memory import DataMemory
from ALU import ALU

class ControlUnit:
    
    def __init__():
        self.acc = Register()
        self.ir = Register()
        self.pc = Register()
        self.ip = Register()
        self.ram = DataMemory(2048)
        self.rom = InstructionMemory(2048)
        self.ALU = ALU()
    
    
    
    
        
        