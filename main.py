from parser import Parser

with open("./pisp_code/featuresExample.pisp") as file:
    f = file.read()

f = Parser.remove_comments(f)
f = f.strip()
print(Parser.parse_pisp_code(f))