#static memory allocation for now
import json

class Translator:
    
    def translate(a: list) -> str:
        res = ""
        match a[0]:
            case "print":
                for n, i in enumerate(sum(a[-1])):
                    res += f"""
                            MNEM:LOAD|OPERAND:{i}\n
                            MNEM:STORE|OPERAND:0x0{N}
                            """
            case _:
                raise ValueError("Invalid pisp syntax")