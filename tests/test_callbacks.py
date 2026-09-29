import unittest
from kik_unofficial.utilities.threading_utils import run_in_new_thread


class CallbackTests(unittest.TestCase):
    def test_submissions_remain_ordered(self):
        values = []

        @run_in_new_thread
        def record(value):
            values.append(value)

        pending = [record(i) for i in range(10)]
        for future in pending:
            future.result(timeout=5)
        self.assertEqual(values, list(range(10)))

    def test_errors_are_observable(self):
        @run_in_new_thread
        def broken():
            raise ValueError("synthetic")

        with self.assertRaises(ValueError):
            broken().result(timeout=5)


if __name__ == "__main__":
    unittest.main()
