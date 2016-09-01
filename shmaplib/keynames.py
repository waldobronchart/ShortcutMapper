# -*- coding: utf-8 -*-

from .logger import getlog
log = getlog()

class DataContainer(object):
    VALID_NAME_LOOKUP = {
        '§': ['SECTION'],
        '!': ['EXCLAMATION'],
        '@': ['AT'],
        '£': ['POUND'],
        '$': ['DOLLAR'],
        '%': ['PERCENT'],
        '^': ['CARET'],
        '&': ['AMPERSAND'],
        '(': ['LEFT_PARENTHESIS'],
        ')': ['RIGHT_PARENTHESIS'],
        '_': ['UNDERSCORE'],
        '[': ['LEFT_BRACKET'],
        ']': ['RIGHT_BRACKET'],
        '{': ['LEFT_BRACE'],
        '}': ['RIGHT_BRACE'],
        ';': ['SEMICOLON'],
        ':': ['COLON'],
        '\'': ['SINGLE_QUOTE'],
        '‘': ['SINGLE_QUOTE'],
        '"': ['DOUBLE_QUOTE'],
        '\\': ['BACKSLASH'],
        '|': ['VERTICAL_BAR'],
        '?': ['QUESTION_MARK'],
        '<': ['LESSTHAN'],
        '>': ['MORETHAN'],
        ',': ['COMMA'],
        '`': ['ACCENT_GRAVE'],
        '~': ['TILDE'],
        '#': ['HASH'],
        '±': ['PLUSMINUS'],

        # Numbers and maths
        'number': ['ONE', 'NUMPAD_ONE', 'TWO', 'NUMPAD_TWO', 'THREE', 'NUMPAD_THREE', 'FOUR', 'NUMPAD_FOUR',
                     'FIVE', 'NUMPAD_FIVE', 'SIX', 'NUMPAD_SIX', 'SEVEN', 'NUMPAD_SEVEN', 'EIGHT', 'NUMPAD_EIGHT',
                     'NINE', 'NUMPAD_NINE','ZERO', 'NUMPAD_ZERO'],
        'number keys': ['ONE', 'NUMPAD_ONE', 'TWO', 'NUMPAD_TWO', 'THREE', 'NUMPAD_THREE', 'FOUR', 'NUMPAD_FOUR',
                     'FIVE', 'NUMPAD_FIVE', 'SIX', 'NUMPAD_SIX', 'SEVEN', 'NUMPAD_SEVEN', 'EIGHT', 'NUMPAD_EIGHT',
                     'NINE', 'NUMPAD_NINE','ZERO', 'NUMPAD_ZERO'],
        '1': ['ONE', 'NUMPAD_ONE'],
        '2': ['TWO', 'NUMPAD_TWO'],
        '3': ['THREE', 'NUMPAD_THREE'],
        '4': ['FOUR', 'NUMPAD_FOUR'],
        '5': ['FIVE', 'NUMPAD_FIVE'],
        '6': ['SIX', 'NUMPAD_SIX'],
        '7': ['SEVEN', 'NUMPAD_SEVEN'],
        '8': ['EIGHT', 'NUMPAD_EIGHT'],
        '9': ['NINE', 'NUMPAD_NINE'],
        '0': ['ZERO', 'NUMPAD_ZERO'],
        '-': ['MINUS', 'NUMPAD_MINUS'],
        '–': ['MINUS', 'NUMPAD_MINUS'],
        '+': ['PLUS', 'NUMPAD_PLUS'],
        '=': ['EQUAL', 'NUMPAD_EQUAL'],
        '*': ['ASTERISK', 'NUMPAD_ASTERISK'],
        '/': ['SLASH', 'NUMPAD_SLASH'],
        '.': ['PERIOD', 'NUMPAD_PERIOD'],
        'numpad_0': ['NUMPAD_ZERO'],
        'numpad_1': ['NUMPAD_ONE'],
        'numpad_2': ['NUMPAD_TWO'],
        'numpad_3': ['NUMPAD_THREE'],
        'numpad_4': ['NUMPAD_FOUR'],
        'numpad_5': ['NUMPAD_FIVE'],
        'numpad_6': ['NUMPAD_SIX'],
        'numpad_7': ['NUMPAD_SEVEN'],
        'numpad_8': ['NUMPAD_EIGHT'],
        'numpad_9': ['NUMPAD_NINE'],
        'numpad 0': ['NUMPAD_ZERO'],
        'numpad 1': ['NUMPAD_ONE'],
        'numpad 2': ['NUMPAD_TWO'],
        'numpad 3': ['NUMPAD_THREE'],
        'numpad 4': ['NUMPAD_FOUR'],
        'numpad 5': ['NUMPAD_FIVE'],
        'numpad 6': ['NUMPAD_SIX'],
        'numpad 7': ['NUMPAD_SEVEN'],
        'numpad 8': ['NUMPAD_EIGHT'],
        'numpad 9': ['NUMPAD_NINE'],
        'numpad -': ['NUMPAD_MINUS'],
        'numpad +': ['NUMPAD_PLUS'],
        'numpad =': ['NUMPAD_EQUAL'],
        'numpad *': ['NUMPAD_ASTERISK'],
        'numpad /': ['NUMPAD_SLASH'],
        'numpad .': ['NUMPAD_PERIOD'],
        'numpad enter': ['NUMPAD_ENTER'],
        'numpad return': ['NUMPAD_ENTER'],

        # Non-English keyboard characters
        # Reference used: http://www.ascii.cl/htmlcodes.htm

        '¡': ['INVERTED_EXCLAMATION'],
        '¢': ['CENT'],
        '¤': ['CURRENCY'],
        '¥': ['YEN'],
        '¦': ['BROKEN_VBAR'],
        '¨': ['UMLAUT'],
        '©': ['COPYRIGHT'],
        'ª': ['FEMININ_ORDINAL'],
        '«': ['LEFT_DOUBLE_ANGLE_QUOTES'],
        '¬': ['NOT_SIGN'],
        '®': ['TRADEMARK'],
        '¯': ['OVERLINE'],

        '°': ['DEGREE_SIGN'],
        '²': ['SQUARED_SIGN'],
        '³': ['CUBED_SIGN'],
        '´': ['ACCENT_ACUTE'],
        'µ': ['MICRO_SIGN'],
        '¶': ['PARAGRAPH_SIGN'],
        '·': ['GEORGIAN_COMMA'],
        '¸': ['CEDILLA_SIGN'],
        '¹': ['SUPERSCRIPT_ONE'],
        'º': ['MASCULIN_ORDINAL_SIGN'],
        '»': ['RIGHT_DOUBLE_ANGLE_QUOTES'],
        '¼': ['ONE_QUARTER_SIGN'],
        '½': ['ONE_HALF_SIGN'],
        '¾': ['ONE_THIRD_SIGN'],
        '¿': ['INVERTED_QUESTION_MARK'],

        'À': ['CAP_A_GRAVE'],
        'Á': ['CAP_A_ACUTE'],
        'Â': ['CAP_A_CIRC'],
        'Ã': ['CAP_A_TILDE'],
        'Ä': ['CAP_A_UML'],
        'Å': ['CAP_A_RING'],
        'Æ': ['CAP_AE'],
        'Ç': ['CAP_C_CEDIL'],
        'È': ['CAP_E_GRAVE'],
        'É': ['CAP_E_ACUTE'],
        'Ê': ['CAP_E_CIRC'],
        'Ë': ['CAP_E_UML'],
        'Ì': ['CAP_I_GRAVE'],
        'Í': ['CAP_I_ACUTE'],
        'Î': ['CAP_I_CIRC'],
        'Ï': ['CAP_I_UML'],

        'Ð': ['CAP_ETH'],
        'Ñ': ['CAP_N_TILDE'],
        'Ò': ['CAP_O_GRAVE'],
        'Ó': ['CAP_O_ACUTE'],
        'Ô': ['CAP_O_CIRC'],
        'Õ': ['CAP_O_TILDE'],
        'Ö': ['CAP_O_UML'],
        '×': ['TIMES'],
        'Ø': ['CAP_O_SLASH'],
        'Ù': ['CAP_U_GRAVE'],
        'Ú': ['CAP_U_ACUTE'],
        'Û': ['CAP_U_CIRC'],
        'Ü': ['CAP_U_UML'],
        'Ý': ['CAP_Y_ACUTE'],
        'Þ': ['CAP_THORN'],
        'ß': ['SZLIG'],

        'à': ['A_GRAVE'],
        'á': ['A_ACUTE'],
        'â': ['A_CIRC'],
        'ã': ['A_TILDE'],
        'ä': ['A_UML'],
        'å': ['A_RING'],
        'æ': ['AE'],
        'ç': ['C_CEDIL'],
        'è': ['E_GRAVE'],
        'é': ['E_ACUTE'],
        'ê': ['E_CIRC'],
        'ë': ['E_UML'],
        'ì': ['I_GRAVE'],
        'í': ['I_ACUTE'],
        'î': ['I_CIRC'],
        'ï': ['I_UML'],

        'ð': ['ETH'],
        'ñ': ['N_TILDE'],
        'ò': ['O_GRAVE'],
        'ó': ['O_ACUTE'],
        'ô': ['O_CIRC'],
        'õ': ['O_TILDE'],
        'ö': ['O_UML'],
        '÷': ['DIVIDE'],
        'ø': ['O_SLASH'],
        'ù': ['U_GRAVE'],
        'ú': ['U_ACUTE'],
        'û': ['U_CIRC'],
        'ü': ['U_UML'],
        'ý': ['Y_ACUTE'],
        'þ': ['THORN'],
        'ÿ': ['Y_UML'],

        'Œ': ['CAP_OE'],
        'œ': ['OE'],
        'Š': ['CAP_S_CARON'],
        'š': ['S_CARON'],
        'Ÿ': ['CAP_Y_UML'],
        'ƒ': ['FUNCTION'],

        '—': ['MINUS'],
        '’': ['SINGLE_QUOTE_RIGHT'],
        '“': ['DOUBLE_QUOTE'],  # this is usually what is meant
        '”': ['DOUBLE_QUOTE_RIGHT'],
        '„': ['DOUBLE_QUOTE_LOW'],
        '†': ['DAGGER'],
        '‡': ['DOUBLE_DAGGER'],
        '•': ['BULLET'],
        '…': ['ELLIPSIS'],
        '‰': ['PER_THOUSAND'],
        '€': ['EURO'],
        '™': ['TRADEMARK'],

        # Other non-character names

        'shift': ['SHIFT'],
        'left_shift': ['SHIFT'],
        'right_shift': ['SHIFT'],
        'ctrl': ['CONTROL'],
        'left_ctrl': ['CONTROL'],
        'right_ctrl': ['CONTROL'],
        'alt': ['ALT'],
        'left_alt': ['ALT'],
        'right_alt': ['ALT'],
        'option': ['ALT'],
        'opt': ['ALT'],
        'left_opt': ['ALT'],
        'right_opt': ['ALT'],
        'cmd': ['COMMAND'],
        'command': ['COMMAND'],
        'left_cmd': ['COMMAND'],
        'right_cmd': ['COMMAND'],
        'win': ['OSKEY'],

        'esc': ['ESCAPE'],
        'caps lock': ['CAPSLOCK'],
        'space': ['SPACE'],
        'spacebar': ['SPACE'],
        'back_space': ['BACKSPACE'],
        'back space': ['BACKSPACE'],
        'return': ['ENTER'],
        'ret': ['ENTER'],
        'del': ['DELETE'],
        'ins': ['INSERT'],
        'hom': ['HOME'],
        'pgup': ['PAGE_UP'],
        'pgdn': ['PAGE_DOWN'],
        'pageup': ['PAGE_UP'],
        'pagedown': ['PAGE_DOWN'],
        'pagedn': ['PAGE_DOWN'],
        'page up': ['PAGE_UP'],
        'page down': ['PAGE_DOWN'],

        'arrow keys': ['UP_ARROW', 'DOWN_ARROW', 'LEFT_ARROW', 'RIGHT_ARROW'],
        'arrows': ['UP_ARROW', 'DOWN_ARROW', 'LEFT_ARROW', 'RIGHT_ARROW'],
        'up': ['UP_ARROW'],
        'up arrow': ['UP_ARROW'],
        'uparrow': ['UP_ARROW'],
        'up arrow key': ['UP_ARROW'],
        'down': ['DOWN_ARROW'],
        'down arrow': ['DOWN_ARROW'],
        'downarrow': ['DOWN_ARROW'],
        'down arrow key': ['DOWN_ARROW'],
        'left': ['LEFT_ARROW'],
        'left arrow': ['LEFT_ARROW'],
        'leftarrow': ['LEFT_ARROW'],
        'left arrow key': ['LEFT_ARROW'],
        'right': ['RIGHT_ARROW'],
        'right arrow': ['RIGHT_ARROW'],
        'rightarrow': ['RIGHT_ARROW'],
        'right arrow key': ['RIGHT_ARROW'],

        'prtscr': ['PRINT_SCREEN'],
        'break': ['PAUSE_BREAK'],
        'pause': ['PAUSE_BREAK'],

        'media_first': ['MEDIA_PREVIOUS'],
        'media_last': ['MEDIA_NEXT']
    }

    VALID_KEYNAMES = None


def _populate_valid_keynames():
    valid_keynames = []
    for char_or_name, names in DataContainer.VALID_NAME_LOOKUP.items():
        valid_keynames.extend(names)

    # Valid keynames that aren't in the VALID_NAME_LOOKUP values
    valid_keynames.extend([
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11',
        'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19',
        'TAB', 'END', 'NUMLOCK', 'EJECT', 'FN_KEY', 'CLEAR',
        'MEDIA_PLAY', 'MEDIA_STOP', 'SCROLL_LOCK', 'CAPSLOCK'
    ])

    # Filter out duplicates & set
    DataContainer.VALID_KEYNAMES = list(set(valid_keynames))


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


def get_valid_keynames(char_or_name, treat_numpad_keys_explicitly=False):
    """Checks if the given name is a valid keyname used in keyboard layouts
    returns a list of uppercased valid key names.

    If the given name couldn't be converted, an empty list is returned.

    /:param treat_numpad_keys_explicitly    if true, will not expand ambiguous keys to numpad keys (0 and Numpad 0 have different functions)
    """

    valid_keynames = []

    if is_valid_keyname(char_or_name.upper()):
        valid_keynames =  [char_or_name.upper()]
    elif char_or_name.lower() in DataContainer.VALID_NAME_LOOKUP.keys():
        valid_keynames =  DataContainer.VALID_NAME_LOOKUP[char_or_name.lower()]

    # Remove numpad keys
    if treat_numpad_keys_explicitly and 'numpad' not in char_or_name.lower():
        valid_keynames = [n for n in valid_keynames if 'numpad' not in n.lower()]

    return valid_keynames
