from parser import Parser

with open("./pisp_code/helloWorld.pisp") as file:
    f = file.read()

print(Parser.parse(Parser.prepare("(pi(defun incrementXTimes (n x) (incrementXTimes (+ 1 n) (- x 1)))sp)")))


