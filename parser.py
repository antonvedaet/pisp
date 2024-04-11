import re
class Parser:
    def is_pisp(s: str) -> bool:
        return (s.startswith('(pi') and s.endswith('sp)'))

    def remove_comments(s: str) -> str:
        return (re.sub(';[^;]*?;', '', s)).strip()
    
    def remove_spaces(s: str) -> str:
        return re.sub(r'(?<!\S)\s+(?![^(]*\))', '', s)

    def prepare(s: str) -> str:
        s = Parser.remove_comments(s)
        if Parser.is_pisp(s):
            s = s[3:-3]
            s = Parser.remove_spaces(s)
            return s.strip().replace("\n", "")
        else:
            raise Exception("NOT PISP")
    
    # def parse_one_function(code: str) -> str: