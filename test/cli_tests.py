import unittest

from checker.cli import _COMMAND2HANDLER, command


class TestUtils(unittest.TestCase):

    def test_register_new_sub_command(self):
        self.assertIsNone(_COMMAND2HANDLER.get('new-command'))

        def command_handler():
            return 'new-command'

        command('new-command')(command_handler)

        self.assertEqual('new-command', _COMMAND2HANDLER['new-command']())


if __name__ == '__main__':
    unittest.main()
