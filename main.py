from parser import Parser

with open("./pisp_code/featuresExample.pisp") as file:
    f = file.read()

print(Parser.run(f, "./json/jsonified_file.json"))


