from enum import Enum
from typing import NamedTuple

# DATA
IN = 0
OUT = 1
MIN_ADDRESS = 2
MAX_ADDRESS = 2 ** 11 - 1
MIN_VALUE = -(1 << 32)
MAX_VALUE = (1 >> 32) - 1

# INSTRUCTION
MAX_INSTR_ADDRESS = 2 ** 11 - 1

class OpType(Enum):
    ARG = "arg"
    NARG = "narg"
    JUMP = "jump"

class Operation(NamedTuple):
    opcode: str
    op_type: OpType

class OpCode(Enum):
    LOAD = Operation("load", OpType.ARG)
    STORE = Operation("store", OpType.ARG)
    NOP = Operation("nop", OpType.NARG)
    JMP = Operation("jmp", OpType.JUMP)
    HLT = Operation("hlt", OpType.NARG)
    ADD = Operation("add", OpType.ARG)
    SUB = Operation("sub", OpType.ARG)
    MOD = Operation("mod", OpType.ARG)
    JIFZ = Operation("jifz", OpType.JUMP)
    JIFNZ = Operation("jifnz", OpType.JUMP)
    JIFN = Operation("jifn", OpType.JUMP)
    JIFNN = Operation("jifnn", OpType.JUMP)

    def get_type(self):
        return self.value.op_type

    def __str__(self):
        return self.value.opcode
