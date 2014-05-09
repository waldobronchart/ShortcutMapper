# -*- coding: utf-8 -*-

# makes all strings here unicode by default (u'')
from __future__ import unicode_literals

from logger import getlog
log = getlog()

class DataContainer(object):
    VALID_NAME_LOOKUP = {
        '§' : ['SECTION'],
        '!' : ['EXCLAMATION'],
        '@' : ['AT'],
        '£' : ['POUND'],
        '$' : ['DOLLAR'],
        '%' : ['PERCENT'],
        '^' : ['CARET'],
        '&' : ['AMPERSAND'],
        '(' : ['LEFT_PARENTHESIS'],
        ')' : ['RIGHT_PARENTHESIS'],
        '_' : ['UNDERSCORE'],
        '[' : ['LEFT_BRACKET'],
        ']' : ['RIGHT_BRACKET'],
        '{' : ['LEFT_BRACE'],
        '}' : ['RIGHT_BRACE'],
        ';' : ['SEMICOLON'],
        ':' : ['COLON'],
        '\'': ['SINGLE_QOUTE'],
        '"' : ['DOUBLE_QUOTE'],
        '\\' : ['BACKSLASH'],
        '|' : ['VERTICAL_BAR'],
        '?' : ['QUESTION_MARK'],
        '<' : ['LESSTHAN'],
        '>' : ['MORETHAN'],
        ',' : ['COMMA'],
        '`' : ['ACCENT_GRAVE'],
        '~' : ['TILDE'],
        '#' : ['HASH'],
        '±' : ['PLUSMINUS'],

        # Numbers and maths
        '1' : ['ONE', 'NUMPAD_ONE'],
        '2' : ['TWO', 'NUMPAD_TWO'],
        '3' : ['THREE', 'NUMPAD_THREE'],
        '4' : ['FOUR', 'NUMPAD_FOUR'],
        '5' : ['FIVE', 'NUMPAD_FIVE'],
        '6' : ['SIX', 'NUMPAD_SIX'],
        '7' : ['SEVEN', 'NUMPAD_SEVEN'],
        '8' : ['EIGHT', 'NUMPAD_EIGHT'],
        '9' : ['NINE', 'NUMPAD_NINE'],
        '0' : ['ZERO', 'NUMPAD_ZERO'],
        '-' : ['MINUS', 'NUMPAD_MINUS'],
        '+' : ['PLUS', 'NUMPAD_PLUS'],
        '=' : ['EQUAL', 'NUMPAD_EQUAL'],
        '*' : ['ASTERISK', 'NUMPAD_ASTERISK'],
        '/' : ['SLASH', 'NUMPAD_SLASH'],
        '.' : ['PERIOD', 'NUMPAD_PERIOD'],
        'numpad_0' : ['NUMPAD_ZERO'],
        'numpad_1' : ['NUMPAD_ONE'],
        'numpad_2' : ['NUMPAD_TWO'],
        'numpad_3' : ['NUMPAD_THREE'],
        'numpad_4' : ['NUMPAD_FOUR'],
        'numpad_5' : ['NUMPAD_FIVE'],
        'numpad_6' : ['NUMPAD_SIX'],
        'numpad_7' : ['NUMPAD_SEVEN'],
        'numpad_8' : ['NUMPAD_EIGHT'],
        'numpad_9' : ['NUMPAD_NINE'],

        # Non-Enlish keyboard characters

        '¡' : ['INVERTED_EXCLAMATION'],
        '¢' : ['CENT'],
        '¤' : ['CURRENCY'],
        '¥' : ['YEN'],
        '¦' : ['BROKEN_VBAR'],
        '¨' : ['UMLAUT'],
        '©' : ['COPYRIGHT'],
        'ª' : ['FEMININ_ORDINAL'],
        '«' : ['LEFT_DOUBLE_ANGLE_QUOTES'],
        '¬' : ['NOT_SIGN'],
        '®' : ['TRADEMARK'],
        '¯' : ['OVERLINE'],

        '°' : ['DEGREE_SIGN'],
        '²' : ['SQUARED_SIGN'],
        '³' : ['CUBED_SIGN'],
        '´' : ['ACCENT_ACUTE'],
        'µ' : ['MICRO_SIGN'],
        '¶' : ['PARAGRAPH_SIGN'],
        '·' : ['GEORGIAN_COMMA'],
        '¸' : ['CEDILLA_SIGN'],
        '¹' : ['SUPERSCRIPT_ONE'],
        'º' : ['MASCULIN_ORDINAL_SIGN'],
        '»' : ['RIGHT_DOUBLE_ANGLE_QUOTES'],
        '¼' : ['ONE_QUARTER_SIGN'],
        '½' : ['ONE_HALF_SIGN'],
        '¾' : ['ONE_THIRD_SIGN'],
        '¿' : ['INVERTED_QUESTION_MARK'],

        'ç' : ['C_CEDILLA'],
        'à' : ['A_GRAVE'],
        'ù' : ['U_GRAVE'],

        # BLA BLA BLA, this should do for now. Too lazy:
        #  http://www.ascii.cl/htmlcodes.htm
        # TODO: add all characters for non-english keyboards

        'shift' : ['SHIFT'],
        'left_shift' : ['SHIFT'],
        'right_shift' : ['SHIFT'],
        'ctrl' : ['CONTROL'],
        'left_ctrl' : ['CONTROL'],
        'right_ctrl' : ['CONTROL'],
        'alt' : ['ALT'],
        'left_alt' : ['ALT'],
        'right_alt' : ['ALT'],
        'option' : ['ALT'],
        'opt' : ['ALT'],
        'left_opt' : ['ALT'],
        'right_opt' : ['ALT'],
        'cmd' : ['COMMAND'],
        'command' : ['COMMAND'],
        'left_cmd' : ['COMMAND'],
        'right_cmd' : ['COMMAND'],
        'win' : ['OSKEY'],

        'esc' : ['ESCAPE'],
        'space' : ['SPACE'],
        'spacebar' : ['SPACE'],
        'back_space' : ['BACKSPACE'],
        'return' : ['ENTER'],
        'ret' : ['ENTER'],
        'del' : ['DELETE'],
        'ins' : ['INSERT'],
        'hom' : ['HOME'],
        'pgup' : ['PAGE_UP'],
        'pgdn' : ['PAGE_DOWN'],
        'pageup' : ['PAGE_UP'],
        'pagedown' : ['PAGE_DOWN'],
        'pagedn' : ['PAGE_DOWN'],

        'up' : ['UP_ARROW'],
        'down' : ['DOWN_ARROW'],
        'left' : ['RIGHT_ARROW'],
        'right' : ['LEFT_ARROW'],

        'prtscr' : ['PRINT_SCREEN'],
        'break' : ['PAUSE_BREAK'],

        'media_first' : ['MEDIA_PREVIOUS'],
        'media_last' : ['MEDIA_NEXT']
    }

    VALID_KEYNAMES = None



def _populate_valid_keynames():
    VALID_KEYNAMES = []
    for char_or_name, names in DataContainer.VALID_NAME_LOOKUP.items():
        VALID_KEYNAMES.extend(names)

    # Valid keynames that aren't in the VALID_NAME_LOOKUP values
    VALID_KEYNAMES.extend([
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11',
        'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19',
        'NUMPAD_ENTER', 'TAB', 'END', 'NUMLOCK', 'EJECT', 'FN_KEY', 'CLEAR',
        'MEDIA_PLAY', 'MEDIA_STOP', 'SCROLL_LOCK', 'CAPSLOCK'
    ])

    # Filter out duplicates & set
    DataContainer.VALID_KEYNAMES = list(set(VALID_KEYNAMES))

def get_all_valid_keynames():
    """Gets a list of all valid keynames used"""

    if DataContainer.VALID_KEYNAMES is None:
        _populate_valid_keynames()

    return DataContainer.VALID_KEYNAMES

def is_valid_keyname(name):
    """Checks if the given name is a valid keyname used in keyboard layouts"""

    if DataContainer.VALID_KEYNAMES is None:
        _populate_valid_keynames()

    return name in DataContainer.VALID_KEYNAMES

def get_valid_keynames(char_or_name):
    """Checks if the given name is a valid keyname used in keyboard layouts
    returns a list of uppercased valid key names
    """

    if is_valid_keyname(char_or_name.upper()):
        return [char_or_name.upper()]

    if char_or_name.lower() in DataContainer.VALID_NAME_LOOKUP.keys():
        return DataContainer.VALID_NAME_LOOKUP[char_or_name.lower()]

    assert 0, "Given name or sign is not valid"
    return [char_or_name]


















