from unittest import TestCase

from wlang import ast
from wlang.dynamic_sym_exe import DynamicSysExec
from wlang.dynamic_sym_state import ProgramState


class TestDynamicSysExec(TestCase):
    def test_one(self):
        prg1 = "havoc x; x := 20; assert x > 15"
        ast1 = ast.parse_string(prg1)
        engine = DynamicSysExec()
        st = ProgramState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

# Concretely only, symbolic and concrete, while, if
