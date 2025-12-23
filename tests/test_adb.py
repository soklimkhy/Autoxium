import unittest
from autoxium.core.adb_wrapper import adb


class TestADB(unittest.TestCase):
    def test_adb_path_exists_or_handled(self):
        # This test just checks if the wrapper initiates without crash
        self.assertIsNotNone(adb.adb_path)


if __name__ == "__main__":
    unittest.main()
