from parser import Parser
from translator import Translator

with open("./pisp_code/helloWorld.pisp") as file:
    f = file.read()

print(Parser.run(f))


