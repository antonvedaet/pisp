import re

class Parser:

    Symbol = str             
    Number = (int, float)     
    Atom   = (Symbol, Number) 
    List   = list             
    Exp    = (Atom, List)    
    Env    = dict            

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

    def tokenize(chars: str) -> list:
        return chars.replace('(', ' ( ').replace(')', ' ) ').split()

    def parse(program: str) -> Exp:
        return Parser.read_from_tokens(Parser.tokenize(program))

    def read_from_tokens(tokens: list) -> Exp:
        if len(tokens) == 0:
            raise SyntaxError('unexpected EOF')
        token = tokens.pop(0)
        if token == '(':
            L = []
            while tokens[0] != ')':
                L.append(Parser.read_from_tokens(tokens))
            tokens.pop(0)
            return L
        elif token == ')':
            raise SyntaxError('unexpected )')
        else:
            return Parser.atom(token)

    def atom(token: str) -> Atom:
        try: return int(token)
        except ValueError:
            try: return float(token)
            except ValueError:
                return Parser.Symbol(token)
    
    def parse_whole_file(s: str) -> list:
        code = s
        tokens = Parser.tokenize(code)
        result = []
        while tokens:
            result.append(Parser.read_from_tokens(tokens))
        return result

    def run(s: str, out_file = None) -> list:
        s = Parser.prepare(s)
        res = Parser.parse_whole_file(s)
        if out_file == None:
            return res
