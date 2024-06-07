import io
import logging
import os
import tempfile

import pytest
from cpu_runner import CpuRunner

import translator


@pytest.mark.golden_test("golden/*.yml")
def test_cat(golden):
    # Setup temporary directories and files
    with tempfile.TemporaryDirectory() as tmpdirname:
        asm_file = os.path.join(tmpdirname, "examples/input.asm")
        json_file = os.path.join(tmpdirname, "pseudo_machine_code.json")

        with open(asm_file, "w") as f:
            f.write(golden["in_src"])

        tr = translator.Translator()
        with open(asm_file) as f:
            tr.translate(f.readlines())
        tr.save_as_json(json_file)

        log_stream = io.StringIO()
        logging.basicConfig(stream=log_stream, level=logging.INFO)

        CpuRunner().run(json_file)

        assert log_stream.getvalue() == golden["out_log"]
