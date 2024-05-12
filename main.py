from translator import Translator

with open("./examples/hello_world.asm", "r") as f:
    file = f.readlines()

tr = Translator()
print(tr.sections(file))