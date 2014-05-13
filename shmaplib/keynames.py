# -*- coding: utf-8 -*-

# makes all strings here unicode by default (u'')
from __future__ import unicode_literals

from logger import getlog
log = getlog()

class DataContainer(object):
    VALID_NAME_LOOKUP = {
        u'§' : ['SECTION'],
        u'!' : ['EXCLAMATION'],
        u'@' : ['AT'],
        u'£' : ['POUND'],
        u'$' : ['DOLLAR'],
        u'%' : ['PERCENT'],
        u'^' : ['CARET'],
        u'&' : ['AMPERSAND'],
        u'(' : ['LEFT_PARENTHESIS'],
        u')' : ['RIGHT_PARENTHESIS'],
        u'_' : ['UNDERSCORE'],
        u'[' : ['LEFT_BRACKET'],
        u']' : ['RIGHT_BRACKET'],
        u'{' : ['LEFT_BRACE'],
        u'}' : ['RIGHT_BRACE'],
        u';' : ['SEMICOLON'],
        u':' : ['COLON'],
        u'\'': ['SINGLE_QUOTE'],
        u'‘' : ['SINGLE_QUOTE'],
        u'"' : ['DOUBLE_QUOTE'],
        u'\\': ['BACKSLASH'],
        u'|' : ['VERTICAL_BAR'],
        u'?' : ['QUESTION_MARK'],
        u'<' : ['LESSTHAN'],
        u'>' : ['MORETHAN'],
        u',' : ['COMMA'],
        u'`' : ['ACCENT_GRAVE'],
        u'~' : ['TILDE'],
        u'#' : ['HASH'],
        u'±' : ['PLUSMINUS'],

        # Numbers and maths
        u'number' : ['ONE', 'NUMPAD_ONE', 'TWO', 'NUMPAD_TWO', 'THREE', 'NUMPAD_THREE', 'FOUR', 'NUMPAD_FOUR',
                     'FIVE', 'NUMPAD_FIVE', 'SIX', 'NUMPAD_SIX', 'SEVEN', 'NUMPAD_SEVEN', 'EIGHT', 'NUMPAD_EIGHT',
                     'NINE', 'NUMPAD_NINE','ZERO', 'NUMPAD_ZERO'],
        u'number keys' : ['ONE', 'NUMPAD_ONE', 'TWO', 'NUMPAD_TWO', 'THREE', 'NUMPAD_THREE', 'FOUR', 'NUMPAD_FOUR',
                     'FIVE', 'NUMPAD_FIVE', 'SIX', 'NUMPAD_SIX', 'SEVEN', 'NUMPAD_SEVEN', 'EIGHT', 'NUMPAD_EIGHT',
                     'NINE', 'NUMPAD_NINE','ZERO', 'NUMPAD_ZERO'],
        u'1' : ['ONE', 'NUMPAD_ONE'],
        u'2' : ['TWO', 'NUMPAD_TWO'],
        u'3' : ['THREE', 'NUMPAD_THREE'],
        u'4' : ['FOUR', 'NUMPAD_FOUR'],
        u'5' : ['FIVE', 'NUMPAD_FIVE'],
        u'6' : ['SIX', 'NUMPAD_SIX'],
        u'7' : ['SEVEN', 'NUMPAD_SEVEN'],
        u'8' : ['EIGHT', 'NUMPAD_EIGHT'],
        u'9' : ['NINE', 'NUMPAD_NINE'],
        u'0' : ['ZERO', 'NUMPAD_ZERO'],
        u'-' : ['MINUS', 'NUMPAD_MINUS'],
        u'–' : ['MINUS', 'NUMPAD_MINUS'],
        u'+' : ['PLUS', 'NUMPAD_PLUS'],
        u'=' : ['EQUAL', 'NUMPAD_EQUAL'],
        u'*' : ['ASTERISK', 'NUMPAD_ASTERISK'],
        u'/' : ['SLASH', 'NUMPAD_SLASH'],
        u'.' : ['PERIOD', 'NUMPAD_PERIOD'],
        u'numpad_0' : ['NUMPAD_ZERO'],
        u'numpad_1' : ['NUMPAD_ONE'],
        u'numpad_2' : ['NUMPAD_TWO'],
        u'numpad_3' : ['NUMPAD_THREE'],
        u'numpad_4' : ['NUMPAD_FOUR'],
        u'numpad_5' : ['NUMPAD_FIVE'],
        u'numpad_6' : ['NUMPAD_SIX'],
        u'numpad_7' : ['NUMPAD_SEVEN'],
        u'numpad_8' : ['NUMPAD_EIGHT'],
        u'numpad_9' : ['NUMPAD_NINE'],

        # Non-Enlish keyboard characters

        u'¡' : ['INVERTED_EXCLAMATION'],
        u'¢' : ['CENT'],
        u'¤' : ['CURRENCY'],
        u'¥' : ['YEN'],
        u'¦' : ['BROKEN_VBAR'],
        u'¨' : ['UMLAUT'],
        u'©' : ['COPYRIGHT'],
        u'ª' : ['FEMININ_ORDINAL'],
        u'«' : ['LEFT_DOUBLE_ANGLE_QUOTES'],
        u'¬' : ['NOT_SIGN'],
        u'®' : ['TRADEMARK'],
        u'¯' : ['OVERLINE'],

        u'°' : ['DEGREE_SIGN'],
        u'²' : ['SQUARED_SIGN'],
        u'³' : ['CUBED_SIGN'],
        u'´' : ['ACCENT_ACUTE'],
        u'µ' : ['MICRO_SIGN'],
        u'¶' : ['PARAGRAPH_SIGN'],
        u'·' : ['GEORGIAN_COMMA'],
        u'¸' : ['CEDILLA_SIGN'],
        u'¹' : ['SUPERSCRIPT_ONE'],
        u'º' : ['MASCULIN_ORDINAL_SIGN'],
        u'»' : ['RIGHT_DOUBLE_ANGLE_QUOTES'],
        u'¼' : ['ONE_QUARTER_SIGN'],
        u'½' : ['ONE_HALF_SIGN'],
        u'¾' : ['ONE_THIRD_SIGN'],
        u'¿' : ['INVERTED_QUESTION_MARK'],

        u'ç' : ['C_CEDILLA'],
        u'à' : ['A_GRAVE'],
        u'ù' : ['U_GRAVE'],

        # BLA BLA BLA, this should do for now. Too lazy:
        #  http://www.ascii.cl/htmlcodes.htm
        # TODO: add all characters for non-english keyboards

        u'shift' : ['SHIFT'],
        u'left_shift' : ['SHIFT'],
        u'right_shift' : ['SHIFT'],
        u'ctrl' : ['CONTROL'],
        u'left_ctrl' : ['CONTROL'],
        u'right_ctrl' : ['CONTROL'],
        u'alt' : ['ALT'],
        u'left_alt' : ['ALT'],
        u'right_alt' : ['ALT'],
        u'option' : ['ALT'],
        u'opt' : ['ALT'],
        u'left_opt' : ['ALT'],
        u'right_opt' : ['ALT'],
        u'cmd' : ['COMMAND'],
        u'command' : ['COMMAND'],
        u'left_cmd' : ['COMMAND'],
        u'right_cmd' : ['COMMAND'],
        u'win' : ['OSKEY'],

        u'esc' : ['ESCAPE'],
        u'caps lock' : ['CAPSLOCK'],
        u'space' : ['SPACE'],
        u'spacebar' : ['SPACE'],
        u'back_space' : ['BACKSPACE'],
        u'back space' : ['BACKSPACE'],
        u'return' : ['ENTER'],
        u'ret' : ['ENTER'],
        u'del' : ['DELETE'],
        u'ins' : ['INSERT'],
        u'hom' : ['HOME'],
        u'pgup' : ['PAGE_UP'],
        u'pgdn' : ['PAGE_DOWN'],
        u'pageup' : ['PAGE_UP'],
        u'pagedown' : ['PAGE_DOWN'],
        u'pagedn' : ['PAGE_DOWN'],
        u'page up' : ['PAGE_UP'],
        u'page down' : ['PAGE_DOWN'],

        u'arrow keys' : ['UP_ARROW', 'DOWN_ARROW', 'LEFT_ARROW', 'RIGHT_ARROW'],
        u'arrows' : ['UP_ARROW', 'DOWN_ARROW', 'LEFT_ARROW', 'RIGHT_ARROW'],
        u'up' : ['UP_ARROW'],
        u'up arrow' : ['UP_ARROW'],
        u'up arrow key' : ['UP_ARROW'],
        u'down' : ['DOWN_ARROW'],
        u'down arrow' : ['DOWN_ARROW'],
        u'down arrow key' : ['DOWN_ARROW'],
        u'left' : ['LEFT_ARROW'],
        u'left arrow' : ['LEFT_ARROW'],
        u'left arrow key' : ['LEFT_ARROW'],
        u'right' : ['RIGHT_ARROW'],
        u'right arrow' : ['RIGHT_ARROW'],
        u'right arrow key' : ['RIGHT_ARROW'],

        u'prtscr' : ['PRINT_SCREEN'],
        u'break' : ['PAUSE_BREAK'],

        u'media_first' : ['MEDIA_PREVIOUS'],
        u'media_last' : ['MEDIA_NEXT']
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
    returns a list of uppercased valid key names.

    If the given name couldn't be converted, an empty list is reteurned.
    """

    if is_valid_keyname(char_or_name.upper()):
        return [char_or_name.upper()]

    if char_or_name.lower() in DataContainer.VALID_NAME_LOOKUP.keys():
        return DataContainer.VALID_NAME_LOOKUP[char_or_name.lower()]

    return []


















