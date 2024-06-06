def write_output(output, filename="io/output.txt"):
    with open(filename, "w") as f:
        f.write(output)

def read_input(filename="io/input.txt"):
    with open(filename) as f:
        contents = f.readline()
    return contents
