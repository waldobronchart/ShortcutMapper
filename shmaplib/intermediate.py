# -*- coding: utf-8 -*-

import os
import json
import codecs
import re

from .logger import getlog
log = getlog()

from .appdata import Shortcut, ApplicationConfig
from .constants import DIR_CONTENT_GENERATED, VALID_OS_NAMES, OS_WINDOWS, OS_MAC


class IntermediateShortcutData(object):
    """Intermediate shortcut data format for applications.

    This can be used as output from various shortcut document parsers and can be merged together at the end.

    A serialized IntermediateShortcutData document can then be hand-edited to ensure the data going exported
    to the web application is clean and clear.

    The data format for intermediate data (JSON) is as follows:
    {
        "name": "Application Name",
        "version": "v1.2.3",
        "default_context": "Global Context",
        "os": ["windows", "mac"],
        "contexts": {
            "CONTEXT NAME": {
                "SHORTCUT NAME": ["WINDOWS SHORTCUT KEYS", "MAC SHORTCUT KEYS"],
                ...
            },
            ...
        }
    }

    Linux is usually the same as windows shortcuts, so we conveniently ignore that for now.

    The shortcut keys can be in the following formats:
    - "T"               Just one key
    - "Ctrl + T"        Short form allowed
    - "Control + T"
    - "Alt + +"         Special cases handled correctly
    - "Shift + 0-9"     Range of numbers (Equivalent to having the same shortcut name on all buttons)
    - "Space / Z"       '/' is used as a separator if shortcut has multiple options
    """

    class Shortcut:
        """Intermediate Shortcut structure"""
        def __init__(self, name, win_keys, mac_keys):
            self.name = name
            self.win_keys = win_keys
            self.mac_keys = mac_keys

        def _escape(self, text):
            text = text.replace('\\', '\\\\')
            text = text.replace('"', '\\"')
            return text

        def serialize(self):
            return u'            "{0}": ["{1}", "{2}"],\n'.format(self._escape(self.name),
                                                                  self._escape(self.win_keys),
                                                                  self._escape(self.mac_keys))

    class Context(object):
        """Intermediate application context structure that contains a list of shortcuts"""
        def __init__(self, name):
            self.name = name
            self.shortcuts = []
            self._shortcut_lookup = {}

        def add_shortcut(self, name, win_keys, mac_keys):
            # Add keys to existing shortcut
            existing_shortcut = self.get_shortcut(name)
            if existing_shortcut is not None:
                if len(win_keys) and win_keys not in existing_shortcut.win_keys:
                    existing_shortcut.win_keys += " / " + win_keys
                if len(mac_keys) and mac_keys not in existing_shortcut.mac_keys:
                    existing_shortcut.mac_keys += " / " + mac_keys

                return

            # Create new
            s = IntermediateShortcutData.Shortcut(name, win_keys, mac_keys)
            self._shortcut_lookup[name] = s
            self.shortcuts.append(s)

        def get_shortcut(self, name):
            if name not in self._shortcut_lookup:
                return None

            return self._shortcut_lookup[name]

        def serialize(self):
            ctx_str = u'        "{0}": {{\n'.format(self.name)
            for s in self.shortcuts:
                ctx_str += s.serialize()
            ctx_str = ctx_str.strip(",\n")
            ctx_str += u'\n        },\n'
            return ctx_str

    def __init__(self, app_name="", version="", default_context="", os_supported=None):
        """
        IntermediateShortcutData is a json format that can be easily hand-edited to fix shortcut errors.

        :param app_name: display name of the application (Adobe Photoshop)
        :param version: string format of the version (eg: 2015, v1.2, v1.6a)
        :param default_context: the name of the context that will be active by default on the website
        :param os_supported: list of supported os names as a list
        """
        super(IntermediateShortcutData, self).__init__()

        # Validation
        if os_supported:
            assert isinstance(os_supported, list), "the os_supported parameter must be a list"
            assert len(os_supported) > 0, "the os_supported parameter cannot be empty"
            assert len([o for o in os_supported if o in VALID_OS_NAMES]) > 0, \
                "the os_supported param contains invalid os names. Valid names are: " + str(VALID_OS_NAMES)
        else:
            os_supported = list(VALID_OS_NAMES)

        # Properties
        self.name = app_name
        self.version = version
        self.default_context = default_context
        self.os = os_supported
        self.contexts = []
        self._context_lookup = {}

    def add_shortcut(self, context_name, shortcut_name, win_keys, mac_keys):
        if context_name not in self._context_lookup.keys():
            context = IntermediateShortcutData.Context(context_name)
            self._context_lookup[context_name] = context
            self.contexts.append(context)
            print('Adding Context: ' + context.name)

        self._context_lookup[context_name].add_shortcut(shortcut_name, win_keys, mac_keys)

    def extend(self, idata):
        """Merges the data from one intermediate data object into this one"""
        assert isinstance(idata, IntermediateShortcutData), "Can only extend (merge) with IntermediateShortcutData type"

        for source_context in idata.contexts:
            for source_shortcut in source_context.shortcuts:
                self.add_shortcut(source_context.name, source_shortcut.name, source_shortcut.win_keys, source_shortcut.mac_keys)

                # Merge key contents
                if source_context.name in self._context_lookup.keys():
                    shortcut = self._context_lookup[source_context.name].get_shortcut(source_shortcut.name)
                    if shortcut.win_keys is None or len(shortcut.win_keys) == 0:
                        shortcut.win_keys = source_shortcut.win_keys
                    if shortcut.mac_keys is None or len(shortcut.mac_keys) == 0:
                        shortcut.mac_keys = source_shortcut.mac_keys

    def load(self, file_path):
        """Load the intermediate data from a json file"""
        self.contexts = []
        self._context_lookup = {}

        with codecs.open(file_path, encoding='utf-8') as idata_file:
            json_idata = json.load(idata_file)

            self.name = json_idata["name"]
            self.version = json_idata["version"]
            self.default_context = json_idata["default_context"]
            self.os = json_idata["os"]

            for context_name, shortcuts in json_idata["contexts"].iteritems():
                for shortcut_name, os_keys in shortcuts.iteritems():
                    self.add_shortcut(context_name, shortcut_name, os_keys[0], os_keys[1])

    def serialize(self, output_filepath):
        """Save the intermediate data to a json file"""
        json_str = "{\n"

        # Config
        json_str += u'    "name": "{0}",\n'.format(self.name)
        json_str += u'    "version": "{0}",\n'.format(self.version)
        json_str += u'    "default_context": "{0}",\n'.format(self.default_context)
        json_str += u'    "os": {0},\n'.format(json.dumps(self.os))

        # Contexts
        json_str += u'    "contexts": {\n'
        for context in sorted(self.contexts, key=lambda c: c.name):
            json_str += context.serialize()
        json_str = json_str.strip(",\n")
        json_str += "\n    }\n"

        json_str += "}\n"

        f = codecs.open(output_filepath, encoding='utf-8', mode='w+')
        f.write(json_str)
        f.close()


class IntermediateDataExporter(object):
    """Exports an intermediate .json file to the contents/generated directory in the correct file format."""

    def __init__(self, source, explicit_numpad_mode=False):
        super(IntermediateDataExporter, self).__init__()
        assert os.path.exists(source), "Source file '%s' does not exist" % source

        self.explicit_numpad_mode = explicit_numpad_mode

        # Load intermediate data
        self.idata = IntermediateShortcutData()
        self.idata.load(source)

        # Get app prefs from intermediate data format
        self.app_name = self.idata.name
        self.app_version = self.idata.version
        self.default_context_name = self.idata.default_context

        # Windows and Mac app configs
        self.data_windows = None
        self.data_mac = None
        if OS_WINDOWS in self.idata.os:
            self.data_windows = ApplicationConfig(self.app_name, self.app_version, OS_WINDOWS, self.default_context_name)
        if OS_MAC in self.idata.os:
            self.data_mac = ApplicationConfig(self.app_name, self.app_version, OS_MAC, self.default_context_name)

    def _parse_shortcut(self, name, keys):
        if len(keys) == 0:
            return []

        # All cases we need to handle:
        #  "A"
        #  "Shift + A"
        #  "Ctrl + 0 - 8"     this is a range of keys from 0 to 8
        #  "Shift + ] / Shift + ["
        #  ". (period) / , (comma)"
        #  "Spacebar or Z"
        #  "Up Arrow / Down Arrow or + / -"
        #  "Shift + Up Arrow / Shift + Down Arrow or Shift + + / Shift + -"

        # Cleanup the string and replace edge cases
        keys = re.sub("numpad \+", "NUMPAD_PLUS", keys, flags=re.IGNORECASE)
        keys = re.sub("numpad /", "NUMPAD_SLASH", keys, flags=re.IGNORECASE)
        keys = keys.replace(" or +", " or TEMP_PLUS")
        keys = keys.replace(" or /", " or TEMP_SLASH")
        keys = keys.replace(" + +", " + TEMP_PLUS")
        keys = keys.replace(" + /", " + TEMP_SLASH")
        keys = keys.strip(" ")
        if keys == '/':
            keys = "TEMP_SLASH"
        if keys == '+':
            keys = "TEMP_PLUS"

        # If we split by ' or ' and then ' / ' we can parse each combo separately
        combo_parts = []
        for parts1 in keys.split(' or '):
            for parts2 in parts1.split('/'):
                combo_parts.append(parts2)

        # Parse each combo
        shortcuts = []
        for combo in combo_parts:
            # TODO: skip mouse shortcuts for now
            if 'click' in combo.lower() or 'drag' in combo.lower():
                continue

            parts = combo.split("+")

            # Parse main key
            key = parts[-1]  # last element
            key = key.strip(' ')
            if key == 'TEMP_SLASH':
                key = '/'
            elif key == 'TEMP_PLUS':
                key = '+'

            # Has no key
            if len(key) == 0:
                continue

            # Parse modifiers
            mods = [m.strip(u' ') for m in parts[:-1]]  # all but last

            # Handle a range of keys (Example: "Ctrl + 0-9" or "Ctrl + Numpad 0-9")
            #  which will result in multiple shortcuts with the same label
            results = re.findall(".*?([0-9])-([0-9])", key)
            if results:
                start = int(results[0][0])
                end = int(results[0][1])
                is_numpad_key = 'numpad' in key.lower()

                for i in range(start, end+1):
                    key_name = str(i)
                    if is_numpad_key:
                        key_name = 'Numpad ' + key_name
                    shortcut = Shortcut(name, key_name, mods)
                    shortcuts.append(shortcut)

            # Result is just one shortcut
            else:
                shortcut = Shortcut(name, key, mods)
                shortcuts.append(shortcut)

        return shortcuts

    def parse(self):
        # WINDOWS: Iterate contexts and shortcuts
        if self.data_windows:
            log.info("Parsing intermediate data for Windows shortcuts")
            for context in self.idata.contexts:
                context_win = self.data_windows.get_or_create_new_context(context.name)
                for shortcut in context.shortcuts:
                    for s in self._parse_shortcut(shortcut.name, shortcut.win_keys):
                        context_win.add_shortcut(s, True, self.explicit_numpad_mode)
            log.info("...DONE\n")

        # MAC: Iterate contexts and shortcuts
        if self.data_mac:
            log.info("Parsing intermediate data for MacOS shortcuts")
            for context in self.idata.contexts:
                context_mac = self.data_mac.get_or_create_new_context(context.name)
                for shortcut in context.shortcuts:
                    for s in self._parse_shortcut(shortcut.name, shortcut.mac_keys):
                        context_mac.add_shortcut(s, True, self.explicit_numpad_mode)
            log.info("...DONE\n")

    def export(self):
        if self.data_windows:
            self.data_windows.serialize(DIR_CONTENT_GENERATED)
        if self.data_mac:
            self.data_mac.serialize(DIR_CONTENT_GENERATED)
