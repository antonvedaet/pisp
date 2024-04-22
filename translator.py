#static memory allocation for now
import json

class Translator:
    
    BYTE_MEMORY_START = 100
    INT_MEMORY_START = 200
    
    opcodes = {
               1:"LOAD",
               2: "STORE",
               3: "OUT",
               4: "JMP",
               5: "LOADA",
               6: "ADD"
               #not finished
               }
    def string_to_bytes(s: str) -> list:
        return [ord(l) for l in s]

    def translate(a: list):
        res = []
        match a[0]:
            
            case "print":
                if a[1] == "\'":
                    #saving in memory
                    
                    for n, i in enumerate(" ".join(a[-1])):
                        
                        res.append({"OPCODE" : 1,
                                    "INSTRUCTION": Translator.opcodes.get(1),
                                    "OPERAND": ord(i)})
                        
                        res.append({"OPCODE" : 2,
                                    "INSTRUCTION": Translator.opcodes.get(2),
                                    "OPERAND": hex(n + Translator.BYTE_MEMORY_START)})
                    #jump to start of string
                    res.append({"OPCODE" : 4,
                                "INSTRUCTION": Translator.opcodes.get(4),
                                "OPERAND": hex(Translator.BYTE_MEMORY_START)})
                    #printing each byte
                    for n, _ in enumerate(" ".join(a[-1])):
                        
                        res.append({"OPCODE" : 5,
                                    "INSTRUCTION": Translator.opcodes.get(5),
                                    "OPERAND": hex(n + Translator.BYTE_MEMORY_START)})
                        
                        res.append({"OPCODE" : 3,
                                    "INSTRUCTION": Translator.opcodes.get(3),
                                    "OPERAND": "NO_OPERAND"})
                        
                if a[1] != "\'":
                    #higher_order_function passed
                    pass
                
                
            case "+":
                if all([isinstance(i, int) or len(i) == 1 for i in a]) and len(a) == 3:
                    
                    res.append({
                        "OPCODE": 1,
                        "INSTRUCTION": Translator.opcodes.get(1),
                        "OPERAND": a[1]
                    })
                    
                    res.append({
                        "OPCODE": 6,
                        "INSTRUCTION": Translator.opcodes.get(6),
                        "OPERAND": a[2]
                    })
                    
            case _:
                raise ValueError("Invalid pisp syntax")
        
        return res
    
    def to_json(file, instrs: list):
        with open(file, "w") as f:
            f.write(json.dumps(instrs))
            f.close()