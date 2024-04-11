import re
import json
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

    def strip_one(s: str) -> str:
        match = re.search(r'\((.*)\)', s)
        if match:
            return match.group(1)
        else:
            return None

    def parse_one(s: str) -> dict:
        match = re.search(r'\((.*)\)', s)
        if match:
            d = match.group(1)
            if "(" in d:
                higher_order_f = Parser.parse_one(d)
                d = d.replace("(" + Parser.strip_one(d) + ")", "")
                d = d.split()
                args = d[1:]
                args.append(higher_order_f)
                return {"name": d[0], "args": args}
            else:
                d = d.split()
                return {"name": d[0], "args": d[1:]}
    
    def parse_whole_file(s: str) -> list:
        code = re.findall(r'\([^()]*\)|\([^()]*\([^()]*\)[^()]*\)', s)
        result = []
        for i in range(len(code)):
            result.append(Parser.parse_one(code[i]))
        return result

    def run(s: str, out_file = None) -> list:
        s = Parser.prepare(s)
        res = Parser.parse_whole_file(s)
        if out_file == None:
            return res
        else:
            with open(out_file, "w") as file:
                file.write(json.dumps({"code":res}))
                file.close()
            return res