from control_unit import ControlUnit
from data_memory import DataMemory
from instruction_memory import InstructionMemory
import json

with open("pseudo_machine_code.json", "r") as file:
    mc = json.load(file)

ram = DataMemory(2048)
rom = InstructionMemory(2048)


instrcopy = mc.copy()

for i in mc:
    if i["opcode"] == "nop":
        ram.write(int(i["idx"], 16), i["operand"])
        instrcopy.remove(i)
    else:
        rom.memory = instrcopy


print(ram.memory)
print(rom.memory)

control_unit = ControlUnit(ram, rom)
    