import re
class Parser:
    def is_pisp(s: str) -> bool:
        return (s.startswith('(pi') and s.endswith('sp)'))

    def remove_comments(s: str) -> str:
        return (re.sub(';[^;]*?;', '', s)).strip()

    def parse_pisp_code(code: str) -> list:
        instructions = []
        code = code.strip()[3:-3]
        lines = code.strip().split(';')
        for line in lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            if line.startswith('(') and line.endswith(')'):
                instruction = {}
                parts = line[1:-1].split()
                instruction_name = parts[0]
                instruction['name'] = instruction_name
                if instruction_name == 'defun':
                    instruction['arguments'] = parts[1:-1]
                elif instruction_name == 'set':
                    instruction['variable'] = parts[1]
                    instruction['value'] = parts[2:]
                elif instruction_name == 'if':
                    instruction['condition'] = parts[1]
                    instruction['true_value'] = parts[2]
                    instruction['false_value'] = parts[3]
                elif instruction_name == 'make-arr':
                    instruction['elements'] = parts[1][1:-1].split()
                elif instruction_name == 'make-string':
                    instruction['elements'] = parts[1][1:-1].split()
                else:
                    instruction['arguments'] = parts[1:]
                instructions.append(instruction)
        return instructions