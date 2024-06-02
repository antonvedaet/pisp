from control_unit import ControlUnit
import json

with open("pseudo_machine_code.json", "r") as file:
    instructions = json.load(file)
    

print(instructions)
control_unit = ControlUnit()
    