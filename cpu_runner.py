import json

from cpu.control_unit import ControlUnit
from cpu.data_memory import DataMemory
from cpu.data_path import DataPath
from cpu.instruction_memory import InstructionMemory


class CpuRunner:
    def run(self, input_file="io/input.txt", filename="pseudo_machine_code.json"):
        with open(filename) as file:
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

        data_path = DataPath(rom, ram, input_file)
        control_unit = ControlUnit(data_path)

        control_unit.run()
