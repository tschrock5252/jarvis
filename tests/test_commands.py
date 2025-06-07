# tests/test_commands.py

import unittest
from jarvis.core.commands import COMMANDS

class TestCommands(unittest.TestCase):
    def test_known_command_exists(self):
        self.assertIn("open browser", COMMANDS)

    def test_command_is_callable(self):
        for command in COMMANDS.values():
            self.assertTrue(callable(command))

if __name__ == "__main__":
    unittest.main()

