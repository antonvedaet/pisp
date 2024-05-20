from translator import Translator

with open("./examples/hello_world.asm", "r") as f:
    file = f.readlines()

tr = Translator()
tr.translate(file)
tr.save_as_json('pseudo_machine_code.json')