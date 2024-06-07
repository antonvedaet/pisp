import logging
import os
import tempfile

import pytest

import translate
from cpu_runner import CpuRunner


@pytest.mark.golden_test("golden/*.yml")
def test(golden, caplog):

    caplog.set_level(logging.INFO)

    with tempfile.TemporaryDirectory() as tmpdirname:
        src = os.path.join(tmpdirname, "src.asm")
        input_text = os.path.join(tmpdirname, "input.txt")
        target = os.path.join(tmpdirname, "machine_code.json")

        with open(src, "w", encoding="utf-8") as file:
            file.write(golden["in_src"])
        with open(input_text, "w", encoding="utf-8") as file:
            file.write(golden["in_input"])

        translate.translate(src, target)
        CpuRunner().run(input_text, target)

        with open(target, encoding="utf-8") as file:
            code = file.read()

        caplog_text = caplog.text.replace("\x00", " ")

        assert code == golden.out["out_src"]
        assert caplog_text == golden.out["out_log"]

