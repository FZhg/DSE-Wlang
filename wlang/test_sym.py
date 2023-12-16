# The MIT License (MIT)
# Copyright (c) 2016 Arie Gurfinkel

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from . import ast
from .sym import SymExec
from .sym_state import SymState
from .test_stat_helper import get_all_normal_exiting_testcases, check_program_states_all_normal_exiting_testcases, \
    get_file_paths, run_all_error_exiting_testcases


class TestSym (unittest.TestCase):
    def setUp(self):
        self.sym_engine = SymExec()

    def test_one(self):
        prg1 = "havoc x; assume x > 20; assert x > 15"
        ast1 = ast.parse_string(prg1)
        engine = SymExec()
        st = SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    def test_all_test_cases(self):
        file_paths = get_file_paths("wlang/sym_exe_testcases")
        normal_exiting_testcases_paths = get_all_normal_exiting_testcases(file_paths)
        check_program_states_all_normal_exiting_testcases(self, normal_exiting_testcases_paths, self.sym_engine)
        run_all_error_exiting_testcases(self, file_paths, self.sym_engine)

    def test_eighteen(self):
        prg1 = "havoc x, y; assume y >= 0; c := 0; r := x; while c < y inv c <= y and r < 1 do { r := r + 1; c := c + 1 }; assert r = x + y"
        ast1 = ast.parse_string(prg1)
        engine = SymExec()
        st = SymState()
        out = [s for s in engine.run(ast1, st)]
        print(out)
        self.assertEqual(len(out), 0)


