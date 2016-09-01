# -*- coding: utf-8 -*-

# makes all strings here unicode by default (u'')


from .logger import getlog
log = getlog()

class DataContainer(object):
    VALID_NAME_LOOKUP = {
        u'§': ['SECTION'],
        u'!': ['EXCLAMATION'],
        u'@': ['AT'],
        u'£': ['POUND'],
        u'$': ['DOLLAR'],
        u'%': ['PERCENT'],
        u'^': ['CARET'],
        u'&': ['AMPERSAND'],
        u'(': ['LEFT_PARENTHESIS'],
        u')': ['RIGHT_PARENTHESIS'],
        u'_': ['UNDERSCORE'],
        u'[': ['LEFT_BRACKET'],
        u']': ['RIGHT_BRACKET'],
        u'{': ['LEFT_BRACE'],
        u'}': ['RIGHT_BRACE'],
        u';': ['SEMICOLON'],
        u':': ['COLON'],
        u'\'': ['SINGLE_QUOTE'],
        u'‘': ['SINGLE_QUOTE'],
        u'"': ['DOUBLE_QUOTE'],
        u'\\': ['BACKSLASH'],
        u'|': ['VERTICAL_BAR'],
        u'?': ['QUESTION_MARK'],
        u'<': ['LESSTHAN'],
        u'>': ['MORETHAN'],
        u',': ['COMMA'],
        u'`': ['ACCENT_GRAVE'],
        u'~': ['TILDE'],
        u'#': ['HASH'],
        u'±': ['PLUSMINUS'],

        # Numbers and maths
        u'number': ['ONE', 'NUMPAD_ONE', 'TWO', 'NUMPAD_TWO', 'THREE', 'NUMPAD_THREE', 'FOUR', 'NUMPAD_FOUR',
                     'FIVE', 'NUMPAD_FIVE', 'SIX', 'NUMPAD_SIX', 'SEVEN', 'NUMPAD_SEVEN', 'EIGHT', 'NUMPAD_EIGHT',
                     'NINE', 'NUMPAD_NINE','ZERO', 'NUMPAD_ZERO'],
        u'number keys': ['ONE', 'NUMPAD_ONE', 'TWO', 'NUMPAD_TWO', 'THREE', 'NUMPAD_THREE', 'FOUR', 'NUMPAD_FOUR',
                     'FIVE', 'NUMPAD_FIVE', 'SIX', 'NUMPAD_SIX', 'SEVEN', 'NUMPAD_SEVEN', 'EIGHT', 'NUMPAD_EIGHT',
                     'NINE', 'NUMPAD_NINE','ZERO', 'NUMPAD_ZERO'],
        u'1': ['ONE', 'NUMPAD_ONE'],
        u'2': ['TWO', 'NUMPAD_TWO'],
        u'3': ['THREE', 'NUMPAD_THREE'],
        u'4': ['FOUR', 'NUMPAD_FOUR'],
        u'5': ['FIVE', 'NUMPAD_FIVE'],
        u'6': ['SIX', 'NUMPAD_SIX'],
        u'7': ['SEVEN', 'NUMPAD_SEVEN'],
        u'8': ['EIGHT', 'NUMPAD_EIGHT'],
        u'9': ['NINE', 'NUMPAD_NINE'],
        u'0': ['ZERO', 'NUMPAD_ZERO'],
        u'-': ['MINUS', 'NUMPAD_MINUS'],
        u'–': ['MINUS', 'NUMPAD_MINUS'],
        u'+': ['PLUS', 'NUMPAD_PLUS'],
        u'=': ['EQUAL', 'NUMPAD_EQUAL'],
        u'*': ['ASTERISK', 'NUMPAD_ASTERISK'],
        u'/': ['SLASH', 'NUMPAD_SLASH'],
        u'.': ['PERIOD', 'NUMPAD_PERIOD'],
        u'numpad_0': ['NUMPAD_ZERO'],
        u'numpad_1': ['NUMPAD_ONE'],
        u'numpad_2': ['NUMPAD_TWO'],
        u'numpad_3': ['NUMPAD_THREE'],
        u'numpad_4': ['NUMPAD_FOUR'],
        u'numpad_5': ['NUMPAD_FIVE'],
        u'numpad_6': ['NUMPAD_SIX'],
        u'numpad_7': ['NUMPAD_SEVEN'],
        u'numpad_8': ['NUMPAD_EIGHT'],
        u'numpad_9': ['NUMPAD_NINE'],
        u'numpad 0': ['NUMPAD_ZERO'],
        u'numpad 1': ['NUMPAD_ONE'],
        u'numpad 2': ['NUMPAD_TWO'],
        u'numpad 3': ['NUMPAD_THREE'],
        u'numpad 4': ['NUMPAD_FOUR'],
        u'numpad 5': ['NUMPAD_FIVE'],
        u'numpad 6': ['NUMPAD_SIX'],
        u'numpad 7': ['NUMPAD_SEVEN'],
        u'numpad 8': ['NUMPAD_EIGHT'],
        u'numpad 9': ['NUMPAD_NINE'],
        u'numpad -': ['NUMPAD_MINUS'],
        u'numpad +': ['NUMPAD_PLUS'],
        u'numpad =': ['NUMPAD_EQUAL'],
        u'numpad *': ['NUMPAD_ASTERISK'],
        u'numpad /': ['NUMPAD_SLASH'],
        u'numpad .': ['NUMPAD_PERIOD'],
        u'numpad enter': ['NUMPAD_ENTER'],
        u'numpad return': ['NUMPAD_ENTER'],

        # Non-English keyboard characters
        # Reference used: http://www.ascii.cl/htmlcodes.htm

        u'¡': ['INVERTED_EXCLAMATION'],
        u'¢': ['CENT'],
        u'¤': ['CURRENCY'],
        u'¥': ['YEN'],
        u'¦': ['BROKEN_VBAR'],
        u'¨': ['UMLAUT'],
        u'©': ['COPYRIGHT'],
        u'ª': ['FEMININ_ORDINAL'],
        u'«': ['LEFT_DOUBLE_ANGLE_QUOTES'],
        u'¬': ['NOT_SIGN'],
        u'®': ['TRADEMARK'],
        u'¯': ['OVERLINE'],

        u'°': ['DEGREE_SIGN'],
        u'²': ['SQUARED_SIGN'],
        u'³': ['CUBED_SIGN'],
        u'´': ['ACCENT_ACUTE'],
        u'µ': ['MICRO_SIGN'],
        u'¶': ['PARAGRAPH_SIGN'],
        u'·': ['GEORGIAN_COMMA'],
        u'¸': ['CEDILLA_SIGN'],
        u'¹': ['SUPERSCRIPT_ONE'],
        u'º': ['MASCULIN_ORDINAL_SIGN'],
        u'»': ['RIGHT_DOUBLE_ANGLE_QUOTES'],
        u'¼': ['ONE_QUARTER_SIGN'],
        u'½': ['ONE_HALF_SIGN'],
        u'¾': ['ONE_THIRD_SIGN'],
        u'¿': ['INVERTED_QUESTION_MARK'],

        u'À': ['CAP_A_GRAVE'],
        u'Á': ['CAP_A_ACUTE'],
        u'Â': ['CAP_A_CIRC'],
        u'Ã': ['CAP_A_TILDE'],
        u'Ä': ['CAP_A_UML'],
        u'Å': ['CAP_A_RING'],
        u'Æ': ['CAP_AE'],
        u'Ç': ['CAP_C_CEDIL'],
        u'È': ['CAP_E_GRAVE'],
        u'É': ['CAP_E_ACUTE'],
        u'Ê': ['CAP_E_CIRC'],
        u'Ë': ['CAP_E_UML'],
        u'Ì': ['CAP_I_GRAVE'],
        u'Í': ['CAP_I_ACUTE'],
        u'Î': ['CAP_I_CIRC'],
        u'Ï': ['CAP_I_UML'],

        u'Ð': ['CAP_ETH'],
        u'Ñ': ['CAP_N_TILDE'],
        u'Ò': ['CAP_O_GRAVE'],
        u'Ó': ['CAP_O_ACUTE'],
        u'Ô': ['CAP_O_CIRC'],
        u'Õ': ['CAP_O_TILDE'],
        u'Ö': ['CAP_O_UML'],
        u'×': ['TIMES'],
        u'Ø': ['CAP_O_SLASH'],
        u'Ù': ['CAP_U_GRAVE'],
        u'Ú': ['CAP_U_ACUTE'],
        u'Û': ['CAP_U_CIRC'],
        u'Ü': ['CAP_U_UML'],
        u'Ý': ['CAP_Y_ACUTE'],
        u'Þ': ['CAP_THORN'],
        u'ß': ['SZLIG'],

        u'à': ['A_GRAVE'],
        u'á': ['A_ACUTE'],
        u'â': ['A_CIRC'],
        u'ã': ['A_TILDE'],
        u'ä': ['A_UML'],
        u'å': ['A_RING'],
        u'æ': ['AE'],
        u'ç': ['C_CEDIL'],
        u'è': ['E_GRAVE'],
        u'é': ['E_ACUTE'],
        u'ê': ['E_CIRC'],
        u'ë': ['E_UML'],
        u'ì': ['I_GRAVE'],
        u'í': ['I_ACUTE'],
        u'î': ['I_CIRC'],
        u'ï': ['I_UML'],

        u'ð': ['ETH'],
        u'ñ': ['N_TILDE'],
        u'ò': ['O_GRAVE'],
        u'ó': ['O_ACUTE'],
        u'ô': ['O_CIRC'],
        u'õ': ['O_TILDE'],
        u'ö': ['O_UML'],
        u'÷': ['DIVIDE'],
        u'ø': ['O_SLASH'],
        u'ù': ['U_GRAVE'],
        u'ú': ['U_ACUTE'],
        u'û': ['U_CIRC'],
        u'ü': ['U_UML'],
        u'ý': ['Y_ACUTE'],
        u'þ': ['THORN'],
        u'ÿ': ['Y_UML'],

        u'Œ': ['CAP_OE'],
        u'œ': ['OE'],
        u'Š': ['CAP_S_CARON'],
        u'š': ['S_CARON'],
        u'Ÿ': ['CAP_Y_UML'],
        u'ƒ': ['FUNCTION'],

        u'—': ['MINUS'],
        u'’': ['SINGLE_QUOTE_RIGHT'],
        u'“': ['DOUBLE_QUOTE'],  # this is usually what is meant
        u'”': ['DOUBLE_QUOTE_RIGHT'],
        u'„': ['DOUBLE_QUOTE_LOW'],
        u'†': ['DAGGER'],
        u'‡': ['DOUBLE_DAGGER'],
        u'•': ['BULLET'],
        u'…': ['ELLIPSIS'],
        u'‰': ['PER_THOUSAND'],
        u'€': ['EURO'],
        u'™': ['TRADEMARK'],

        # Other non-character names

        u'shift': ['SHIFT'],
        u'left_shift': ['SHIFT'],
        u'right_shift': ['SHIFT'],
        u'ctrl': ['CONTROL'],
        u'left_ctrl': ['CONTROL'],
        u'right_ctrl': ['CONTROL'],
        u'alt': ['ALT'],
        u'left_alt': ['ALT'],
        u'right_alt': ['ALT'],
        u'option': ['ALT'],
        u'opt': ['ALT'],
        u'left_opt': ['ALT'],
        u'right_opt': ['ALT'],
        u'cmd': ['COMMAND'],
        u'command': ['COMMAND'],
        u'left_cmd': ['COMMAND'],
        u'right_cmd': ['COMMAND'],
        u'win': ['OSKEY'],

        u'esc': ['ESCAPE'],
        u'caps lock': ['CAPSLOCK'],
        u'space': ['SPACE'],
        u'spacebar': ['SPACE'],
        u'back_space': ['BACKSPACE'],
        u'back space': ['BACKSPACE'],
        u'return': ['ENTER'],
        u'ret': ['ENTER'],
        u'del': ['DELETE'],
        u'ins': ['INSERT'],
        u'hom': ['HOME'],
        u'pgup': ['PAGE_UP'],
        u'pgdn': ['PAGE_DOWN'],
        u'pageup': ['PAGE_UP'],
        u'pagedown': ['PAGE_DOWN'],
        u'pagedn': ['PAGE_DOWN'],
        u'page up': ['PAGE_UP'],
        u'page down': ['PAGE_DOWN'],

        u'arrow keys': ['UP_ARROW', 'DOWN_ARROW', 'LEFT_ARROW', 'RIGHT_ARROW'],
        u'arrows': ['UP_ARROW', 'DOWN_ARROW', 'LEFT_ARROW', 'RIGHT_ARROW'],
        u'up': ['UP_ARROW'],
        u'up arrow': ['UP_ARROW'],
        u'uparrow': ['UP_ARROW'],
        u'up arrow key': ['UP_ARROW'],
        u'down': ['DOWN_ARROW'],
        u'down arrow': ['DOWN_ARROW'],
        u'downarrow': ['DOWN_ARROW'],
        u'down arrow key': ['DOWN_ARROW'],
        u'left': ['LEFT_ARROW'],
        u'left arrow': ['LEFT_ARROW'],
        u'leftarrow': ['LEFT_ARROW'],
        u'left arrow key': ['LEFT_ARROW'],
        u'right': ['RIGHT_ARROW'],
        u'right arrow': ['RIGHT_ARROW'],
        u'rightarrow': ['RIGHT_ARROW'],
        u'right arrow key': ['RIGHT_ARROW'],

        u'prtscr': ['PRINT_SCREEN'],
        u'break': ['PAUSE_BREAK'],
        u'pause': ['PAUSE_BREAK'],

        u'media_first': ['MEDIA_PREVIOUS'],
        u'media_last': ['MEDIA_NEXT']
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
