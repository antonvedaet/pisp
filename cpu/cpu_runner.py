from control_unit import ControlUnit
from data_memory import DataMemory
from instruction_memory import InstructionMemory
from data_path import DataPath
import json

with open("pseudo_machine_code.json", "r") as file:
    mc = json.load(file)
# ПЕРЕНЕСТИ В CONTROL UNIT
ram = DataMemory(2048)
rom = InstructionMemory()


instrcopy = mc.copy()

for i in mc:
    if i["opcode"] == "nop":
        ram.write(int(i["idx"], 16), i["operand"])
        instrcopy.remove(i)
    else:
        rom.memory = instrcopy


# ПЕРЕНЕСТИ В CONTROL UNIT
data_path = DataPath(rom, ram)
control_unit = ControlUnit(data_path)

control_unit.run()
print(ram.memory)
# print(rom.memory)