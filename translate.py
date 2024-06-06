import sys

from translator import Translator

with open(f"./examples/{sys.argv[1]}") as f:
    file = f.readlines()

tr = Translator()
tr.translate(file)
tr.save_as_json("pseudo_machine_code.json")
