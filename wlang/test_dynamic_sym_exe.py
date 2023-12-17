from unittest import TestCase
from wlang import ast
from wlang.dynamic_sym_exe import DynamicSysExec
from wlang.dynamic_sym_state import ProgramState
from wlang.test_helper import get_file_paths, get_all_normal_exiting_testcases, \
    check_program_states_all_normal_exiting_testcases, run_all_error_exiting_testcases


class TestDynamicSysExec(TestCase):
    def setUp(self):
        self.engine = DynamicSysExec()
        self.state_constructor = ProgramState

    def test_one(self):
        prg1 = "havoc x; x := 20; assert x > 15"
        ast1 = ast.parse_string(prg1)
        engine = DynamicSysExec()
        st = ProgramState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    def test_all_test_cases(self):
        file_paths = get_file_paths("wlang/dynamic_sym_exe_testcases")
        normal_exiting_testcases_paths = get_all_normal_exiting_testcases(file_paths)
        check_program_states_all_normal_exiting_testcases(self, normal_exiting_testcases_paths, self.engine, self.state_constructor)
        # run_all_error_exiting_testcases(self, file_paths, self.engine, self.state_constructor)



