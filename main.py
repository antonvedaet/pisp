from parser import Parser

with open("./pisp_code/helloWorld.pisp") as file:
    f = file.read()

print(Parser.prepare(f))