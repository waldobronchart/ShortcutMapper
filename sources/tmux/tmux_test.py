#!/usr/bin/env python3

import unittest

import tmux

class TestParseShortcut(unittest.TestCase):

    def assertShortcut(self, raw_shortcut, *args):
        expected_mods, expected_key = args[:-1], args[-1]
        expected_mods = tuple(sorted(expected_mods))
        self.assertEqual(
                tmux.parse_shortcut(raw_shortcut),
                (expected_key, expected_mods))

    def test_simple_key(self):
        self.assertShortcut('a', 'a')

    def test_modifiers(self):
        self.assertShortcut('C-M-S-e', 'CTRL', 'ALT', 'SHIFT', 'e')

    def test_special_kesy(self):
        self.assertShortcut('C-Space', 'CTRL', 'SPACE')

    def test_uppercase_letter(self):
        self.assertShortcut('A', 'SHIFT', 'A')

    def test_minus(self):
        self.assertShortcut('-', '-')

    def test_ctrl_minus(self):
        self.assertShortcut('C--', 'CTRL', '-')

    def test_removes_quotes(self):
        self.assertShortcut('"M-{"', 'ALT', '{')

    def test_removes_escapping(self):
        self.assertShortcut('\~', '~')


class TestParseBinding(unittest.TestCase):

    def test_prefix_mode(self):
        self.assertEqual(tmux.parse_binding(
            'bind-key -T prefix z      resize-pane -Z'), (
                'resize-pane -Z', 'prefix', 'z', ()))

    def test_repeat(self):
        self.assertEqual(tmux.parse_binding(
            'bind-key -r -T prefix Up      select-pane -U'), (
                'select-pane -U', 'prefix', 'UP_ARROW', ()))

    def test_root_mode(self):
        self.assertEqual(tmux.parse_binding(
            'bind-key -T root M-j                  select-pane -D'), (
                'select-pane -D', 'root', 'j', ('ALT',)))


if __name__ == '__main__':
    unittest.main()
