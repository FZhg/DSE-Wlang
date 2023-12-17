# UTILITY FUNCTIONS FOR TESTING THE INTERPRETER

import unittest
from pathlib import Path

from wlang import ast


# return
def parse_test_case(filepath: str):
    """
    @param filepath: a relative path for the testcase file
    @return: a prg str
    @return: env dictionary that stores the expected values for variables at the end of the program
    """
    with open(filepath, "r") as testcase_file:
        testcase_str = testcase_file.read()
    seperator = "________"
    prg, expected_results = testcase_str.split(seperator, maxsplit=1)
    return prg, seperator + "\n" + expected_results.strip()


def get_file_paths(parent_dir_path: str) -> list[Path]:
    """
    @param parent_dir_path:
    @return: the relative paths of files in the parent directory
    """
    parent_dir = Path(parent_dir_path)
    return [f for f in parent_dir.glob('**/*') if f.is_file()]


def get_all_normal_exiting_testcases(file_paths: list[Path]) -> list[Path]:
    return [path for path in file_paths if "error" not in path.as_posix()]


def run_all_normal_exiting_testcases(tester: unittest.TestCase, normal_exiting_testcases_paths: list[Path], do,
                                     engine, state_constructor):
    for testcase_path in normal_exiting_testcases_paths:
        with tester.subTest(msg=testcase_path.name, filepath=testcase_path):
            prg, expected_results = parse_test_case(testcase_path.as_posix())
            # do(tester, engine, prg, expected_results, state_constructor)
            write_new_files(testcase_path.as_posix(), prg, engine, state_constructor)


def write_new_files(path, prg, engine, state_constructor):
    abstract_syntax_tree = ast.parse_string(prg)
    # initial_state = state_constructor()
    end_states = engine.run(abstract_syntax_tree)
    result_str = get_str_result(states=end_states)
    file_content = prg + result_str
    with open(path, "w") as testcase_file:
        testcase_file.write(file_content)


def get_str_result(states):
    result_str = "________\n"
    for out in states:
        result_str += out.__str__()
        result_str += "________\n"
    result_str += f"num_states: {len(states)}"
    return result_str


def check_program_states_all_normal_exiting_testcases(tester: unittest.TestCase, file_paths: list[Path],
                                                      engine, state_constructor):
    run_all_normal_exiting_testcases(
        tester,
        file_paths,
        check_results,
        engine,
        state_constructor
    )


def check_results(tester: unittest.TestCase, engine, prg, expected_results, state_constructor):
    abstract_syntax_tree = ast.parse_string(prg)
    initial_state = state_constructor()
    end_states = engine.run(abstract_syntax_tree, initial_state)
    results_str = get_str_result(states=end_states)
    tester.assertEqual(results_str, expected_results)


def run_all_error_exiting_testcases(tester: unittest.TestCase, file_paths: list[Path],
                                    engine, state_constructor):
    testcases_paths = [path for path in file_paths if "error" in path.as_posix() and "parsing" in path.as_posix()]
    for testcase_path in testcases_paths:
        with tester.subTest(msg=testcase_path.name, filepath=testcase_path):
            prg, expected_results = parse_test_case(testcase_path.as_posix())
            with tester.assertRaises(Exception):
                check_results(tester, engine, prg, expected_results, state_constructor)
    testcases_paths = [path for path in file_paths if "error" in path.as_posix() and "parsing" not in path.as_posix()]
    for testcase_path in testcases_paths:
        with tester.subTest(msg=testcase_path.name, filepath=testcase_path):
            prg, expected_results = parse_test_case(testcase_path.as_posix())
            check_results(tester, engine, prg, expected_results, state_constructor)
            #write_new_files(testcase_path.as_posix(), prg, engine, state_constructor)


if __name__ == "__main__":
    raise Exception("Can't run test_helper as script.")
