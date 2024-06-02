from instruction_memory import InstructionMemory
from data_memory import DataMemory
from data_path import DataPath
from ALU import ALU

class ControlUnit:
    
    def __init__(self, data_path):
        self.ALU = ALU()
        self.data_path = data_path
        