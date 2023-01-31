#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Generate shortcuts from the running tmux server.

The script calls `tmux list-keys` and transforms its output into format
for ShortcutMapper.
"""

import re
import argparse
import logging
import os
import platform
import collections
import subprocess
import sys

# Add repository root path to sys.path (This will make import shmaplib work)
CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CWD)
sys.path.insert(0, os.path.normpath(os.path.join(CWD, '..', '..')))

# Import common shortcut mapper library
import shmaplib
log = shmaplib.setuplog(os.path.join(CWD, 'output.log'))


def tmux_version():
    """Detect tmux version."""
    output = subprocess.check_output(['tmux', '-V']).decode().strip()
    m = re.match(r'^tmux ([a-z0-9._-]+)$', output)
    assert m, 'Unexpected version output: %s' % output
    return m.group(1)


class ParseException(Exception):
    pass


class InvalidShortcut(Exception):
    pass

# List of keys comes from https://github.com/tmux/tmux/blob/master/key-string.c
KEY_TRANSLATION = {
    'IC': 'INSERT',
    'Insert': 'INSERT',
    'DC': 'DELETE',
    'Delete': 'DELETE',
    'Home': 'HOME',
    'End': 'END',
    'NPage': 'PAGE_DOWN',
    'PageDown': 'PAGE_DOWN',
    'PgDn': 'PAGE_DOWN',
    'PPage': 'PAGE_UP',
    'PageUp': 'PAGE_UP',
    'PgUp': 'PAGE_UP',
    'Tab': 'TAB',
    'BTab': 'TAB',
    'Space': 'SPACE',
    'BSpace': 'BACKSPACE',
    'Enter': 'ENTER',
    'Escape': 'ESCAPE',
    'Up': 'UP_ARROW',
    'Down': 'DOWN_ARROW',
    'Left': 'LEFT_ARROW',
    'Right': 'RIGHT_ARROW',
    'KP/': 'NUMPAD_SLASH',
    'KP*': 'NUMPAD_STAR',
    'KP-': 'NUMPAD_MINUS',
    'KP7': 'NUMPAD_SEVEN',
    'KP8': 'NUMPAD_EIGHT',
    'KP9': 'NUMPAD_NINE',
    'KP+': 'NUMPAD_PLUS',
    'KP4': 'NUMPAD_FOUR',
    'KP5': 'NUMPAD_FIVE',
    'KP6': 'NUMPAD_SIX',
    'KP1': 'NUMPAD_ONE',
    'KP2': 'NUMPAD_TWO',
    'KP3': 'NUMPAD_THREE',
    'KPEnter': 'NUMPAD_ENTER',
    'KP0': 'NUMPAD_ZERO',
    'KP.': 'NUMPAD_PERIOD',
}

# Ignore mouse actions
MOUSE_PREFIXES = [
        'MouseUp',
        'MouseDown',
        'MouseDrag',
        'MouseDragEnd',
        'DoubleClick',
        'SecondClick',
        'TripleClick',
        'WheelDown',
        'WheelUp',
]


def parse_shortcut(shortcut):
    """Parse tmux shortcut into format for ShortcutMapper."""
    # Remove quotes, e.g. "M-}"
    if len(shortcut) > 2 and shortcut[0] == '"' and shortcut[-1] == '"':
        shortcut = shortcut[1:-1]

    mods = set()
    while True:
        if shortcut.startswith('M-'):
            mods.add('ALT')
            shortcut = shortcut[len('M-'):]
        elif shortcut.startswith('C-'):
            mods.add('CTRL')
            shortcut = shortcut[len('C-'):]
        elif shortcut.startswith('S-'):
            mods.add('SHIFT')
            shortcut = shortcut[len('S-'):]
        else:
            break

    key = shortcut

    if any(key.startswith(prefix) for prefix in MOUSE_PREFIXES):
        raise InvalidShortcut

    # Escape sequences, e.g \~
    if len(key) == 2 and key[0] == '\\':
        key = key[1]

    key = KEY_TRANSLATION.get(key, key)

    if len(key) == 1 and key.isupper():
        if 'SHIFT' in mods:
            raise ParseException
        mods.add('SHIFT')

    return key, tuple(sorted(mods))


def parse_binding(line):
    """Parse one binding from the output of `tmux list-keys`."""
    words = line.split()

    if words[0] != 'bind-key':
        raise ParseException

    context = None
    command = None
    shortcut = None
    pos = 1
    while pos < len(words):
        word = words[pos]

        if word == '-r':
            # -r means key might repeat
            pos += 1
        elif word == '-T':
            if pos + 3 >= len(words):
                raise ParseException

            pos += 1
            context = words[pos]
            pos += 1
            shortcut = words[pos]
            pos += 1
            command = ' '.join(words[pos:])
            break
        else:
            raise ParseException

    key, mods = parse_shortcut(shortcut)
    return command, context, key, mods


def extract_shortcuts():
    """Extract all shorctus from the currently running tmux."""
    shortcuts = collections.defaultdict(dict)
    output = subprocess.check_output(['tmux', 'list-keys']).decode()
    for i, line in enumerate(output.splitlines()):
        try:
            name, context, key, mods = parse_binding(line)
        except ParseException as e:
            log.warning('Invalid line: "%s" failing with %s' % (line, e))
            continue
        except InvalidShortcut:
            continue

        shortcuts[context][(key, mods)] = name

    return shortcuts

def extract_shortcut_names(shortcuts):
    """Extract the assigned notes for the shorcuts if possible."""
    for context in shortcuts.keys():
        output = subprocess.check_output([
            'tmux', 'list-keys', '-N', '-T', context]).decode()
        for line in output.splitlines():
            shortcut, name = line.split(maxsplit=1)
            shortcut = parse_shortcut(shortcut)

            if shortcut not in shortcuts[context]:
                raise ParseException('Undefined shortcut: %s' % line)
            shortcuts[context][shortcut] = name
    return shortcuts


def main():
    log.setLevel(logging.INFO)

    version = tmux_version()

    shortcuts = extract_shortcuts()
    shortcuts = extract_shortcut_names(shortcuts)

    app_os = platform.system().lower()
    if app_os == 'darwin':
        app_os = 'mac'

    default_context = 'root' if 'root' in shortcuts else 'prefix'

    app = shmaplib.ApplicationConfig("tmux", version, app_os, default_context)

    for context, keys in shortcuts.items():
        context = app.get_or_create_new_context(context)
        for (key, mods), name in keys.items():
            context.add_shortcut(shmaplib.Shortcut(name, key, mods=mods))

    app.serialize(shmaplib.DIR_CONTENT_GENERATED)

if __name__ == '__main__':
    main()
