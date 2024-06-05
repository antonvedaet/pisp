from control_unit import ControlUnit
from data_memory import DataMemory
from instruction_memory import InstructionMemory
from data_path import DataPath
import json

with open("pseudo_machine_code.json", "r") as file:
    memory = json.load(file)
ram = DataMemory(2048)
rom = InstructionMemory()
instrcopy = memory.copy()
for i in memory:
    if i["opcode"] == "nop":
        ram.write(i["idx"], i["operand"])
        instrcopy.remove(i)
    else:
        rom.memory = instrcopy

data_path = DataPath(rom, ram)
control_unit = ControlUnit(data_path)

control_unit.run()
