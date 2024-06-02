from control_unit import ControlUnit
import json

with open("pseudo_machine_code.json", "r") as file:
    instructions = json.load(f)
    
control_unit = ControlUnit()
    