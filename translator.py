#static memory allocation for now
import json

class Translator:
    
    BYTE_MEMORY_START = 100
    INT_MEMORY_START = 200
    
    opcodes = {
               hex(1):"LOAD",
               hex(2): "STORE",
               hex(3): "OUT",
               hex(4): "JMP",
               hex(6): "ADD"
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
                        
                        res.append({"OPCODE" : hex(1),
                                    "INSTRUCTION": Translator.opcodes.get(hex(1)),
                                    "OPERAND": ord(i)})
                        
                        res.append({"OPCODE" : hex(2),
                                    "INSTRUCTION": Translator.opcodes.get(hex(2)),
                                    "OPERAND": hex(n + Translator.BYTE_MEMORY_START)})
                    #jump to start of string
                    res.append({"OPCODE" : hex(4),
                                "INSTRUCTION": Translator.opcodes.get(hex(4)),
                                "OPERAND": hex(Translator.BYTE_MEMORY_START)})
                    #printing each byte
                    for n, _ in enumerate(" ".join(a[-1])):
                        
                        res.append({"OPCODE" : hex(1),
                                    "INSTRUCTION": Translator.opcodes.get(hex(1)),
                                    "OPERAND": hex(n + Translator.BYTE_MEMORY_START)})
                        
                        res.append({"OPCODE" : hex(3),
                                    "INSTRUCTION": Translator.opcodes.get(hex(3)),
                                    "OPERAND": "NO_OPERAND"})
                        
                if a[1] != "\'":
                    res += Translator.translate(a[1])
                    res.append({"OPCODE" : hex(3),
                                "INSTRUCTION": Translator.opcodes.get(hex(3)),
                                "OPERAND": "NO_OPERAND"})
                    
                
                
            case "+":

                if all([isinstance(i, int) or len(i) == 1 for i in a]) and len(a) == 3:
                    
                    res.append({
                        "OPCODE": hex(6),
                        "INSTRUCTION": Translator.opcodes.get(hex(6)),
                        "OPERAND": a[1]
                    })
                    
                    res.append({
                        "OPCODE": hex(6),
                        "INSTRUCTION": Translator.opcodes.get(hex(6)),
                        "OPERAND": a[2]
                    })
                else:
                    for i in a:
                        if len(i) != 1:
                            res+=Translator.translate(i) #  FIXME
                
                    
            case _:
                raise ValueError("Invalid pisp syntax")
        
        return res
    
    def to_json(file, instrs: list):
        with open(file, "w") as f:
            f.write(json.dumps(instrs))
            f.close()