#static memory allocation for now
import json

class Translator:
    opcodes = {
               1:"LOAD",
               2: "STORE",
               3: "OUT",
               4: "JMP",
               5: "LOADA"
               #not finished
               }
    def string_to_bytes(s: str) -> list:
        return [ord(l) for l in s]

    def translate(a: list, c_tick: int) -> list:
        res = []
        match a[0]:
            case "print":
                if a[1] == "\'":
                    #saving in memory
                    
                    for n, i in enumerate(" ".join(a[-1])):
                        
                        res.append({"TICK": c_tick,
                                    "OPCODE" : 1,
                                    "INSTRUCTION": Translator.opcodes.get(1),
                                    "OPERAND": ord(i)})
                        c_tick += 1
                        
                        res.append({"TICK": c_tick,
                                    "OPCODE" : 2,
                                    "INSTRUCTION": Translator.opcodes.get(2),
                                    "OPERAND": hex(n+100)})
                        c_tick += 1
                    #jump to start of string
                    res.append({"TICK": c_tick,
                                "OPCODE" : 4,
                                "INSTRUCTION": Translator.opcodes.get(4),
                                "OPERAND": hex(100)})
                    c_tick+=1
                    #printing each byte
                    for n, _ in enumerate(" ".join(a[-1])):
                        
                        res.append({"TICK": c_tick,
                                    "OPCODE" : 5,
                                    "INSTRUCTION": Translator.opcodes.get(5),
                                    "OPERAND": hex(n+100)})
                        c_tick += 1
                        
                        res.append({"TICK": c_tick,
                                    "OPCODE" : 3,
                                    "INSTRUCTION": Translator.opcodes.get(3),
                                    "OPERAND": "NO_OPERAND"})
                        c_tick += 1
                        
                        
            case _:
                raise ValueError("Invalid pisp syntax")
        
        return [res, c_tick]
    
    def to_json(file, instrs: list):
        with open(file, "w") as f:
            f.write(json.dumps(instrs))
            f.close()