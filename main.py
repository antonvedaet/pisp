from parser import Parser
from translator import Translator

with open("./pisp_code/helloWorld.pisp") as file:
    f = file.read()


parsed_code = Parser.run(f)
print(Translator.to_json("./json/jsonified.json", Translator.translate(parsed_code[0])))
