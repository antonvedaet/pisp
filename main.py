from parser import Parser

with open("./pisp_code/featuresExample.pisp") as file:
    f = file.read()

print(Parser.parse_one("(set result (+ 41 (+ 1 2)))"))