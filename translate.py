import sys

from translator import Translator


def translate(filename=False, target="pseudo_machine_code.json"):
    if filename:
        with open(filename) as f:
            file = f.readlines()
    else:
        with open(f"./examples/{sys.argv[1]}") as f:
            file = f.readlines()

    tr = Translator()
    tr.translate(file)
    tr.save_as_json(target)

