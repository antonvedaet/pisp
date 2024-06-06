from translator import Translator
import sys
with open(f"./examples/{sys.argv[1]}", "r") as f:
    file = f.readlines()

tr = Translator()
tr.translate(file)
tr.save_as_json('pseudo_machine_code.json')