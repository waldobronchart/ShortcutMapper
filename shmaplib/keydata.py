import json
import keynames
import copy
import collections

from logger import getlog
log = getlog()

class Shortcut(object):
    def __init__(self, name, key, mods=[], anymod=False):
        self.name = name
        self.key = key
        self.mods = mods
        self.anymod = anymod

    def serialize(self):
        mods = list(set(self.mods))
        mods.sort()
        mods_str = json.dumps(mods)

        return '{"name":"%s", "mods":%s}' % (self.name, mods_str)

    def __str__(self):
        return self.serialize()


class ShortcutContext(object):
    def __init__(self, name):
        self.name = name
        self.shortcuts = []
        self.added_shortcuts_lookup = []
        self.added_keycombos_lookup = []
        self.added_keycombo_to_shortcuts_lookup = {}

    def add_shortcut(self, s, check_for_duplicates=True):
        log.debug("adding shortcut %s", self._get_shortcut_str(s))

        # Validate modifier names
        # Modifier keys cannot be ambiguous (ctrl -> left_ctrl, right_ctrl), but can be added later
        #  if needed
        valid_mod_names = []
        for mod in s.mods:
            valid_mod_keys = keynames.get_valid_keynames(mod)
            assert len(valid_mod_keys) == 1, "Ambiguous modifier keys not supported"
            valid_mod_names.append(valid_mod_keys[0])
        s.mods = valid_mod_names

        # Split up ambiguous keys into multiple shortcuts
        #  a simple example is +, which can be PLUS or NUMPAD_PLUS
        expanded_shortcuts = []
        keys = keynames.get_valid_keynames(s.key)
        for key in keys:
            # if anymod can be used, split it up into individual shortcuts
            if s.anymod:
                for mod in s.mods:
                    s_expanded = Shortcut(s.name, key, [mod])
                    expanded_shortcuts.append(s_expanded)
            else:
                s_expanded = copy.deepcopy(s)
                s_expanded.key = key
                expanded_shortcuts.append(s_expanded)

        # Add all expanded shortcuts
        for shortcut in expanded_shortcuts:
            shortcut_str = self._get_shortcut_str(shortcut)
            keycombo_str = self._get_keycombo_str(shortcut)

            if not check_for_duplicates:
                self.shortcuts.append(shortcut)
                self.added_shortcuts_lookup.append(shortcut_str)
                self.added_keycombo_to_shortcuts_lookup[keycombo_str] = shortcut_str
                continue

            # Don't Add Duplicates
            if keycombo_str in self.added_keycombo_to_shortcuts_lookup.keys():
                existing_shortcut = self.added_keycombo_to_shortcuts_lookup[keycombo_str]
                log.warn('Warning: shortcut with keycombo %s already exists in context\n' +
                    '   ...existing shortcut is: %s\n   ...skipping add shorcut: %s',
                    keycombo_str, existing_shortcut, shortcut.name)
                continue

            if len(expanded_shortcuts) > 1:
                log.debug('   ...expanding into %s', shortcut_str)
            self.shortcuts.append(shortcut)
            self.added_shortcuts_lookup.append(shortcut_str)
            self.added_keycombo_to_shortcuts_lookup[keycombo_str] = shortcut_str

    def _get_shortcut_str(self, shortcut):
        keys = list(shortcut.mods)
        keys.sort()
        keys.append(shortcut.key)

        anymod = ''
        if shortcut.anymod:
            anymod = ' (Any Mod)'

        return shortcut.name.ljust(45) + '+'.join(keys) + anymod

    def _get_keycombo_str(self, shortcut):
        keys = list(shortcut.mods)
        keys.sort()
        keys.append(shortcut.key)
        return '+'.join(keys)


    def serialize(self):
        # todo: check for duplicates somewhere else!
        lookup_table = {}
        for shortcut in self.shortcuts:
            if shortcut.key not in lookup_table.keys():
                lookup_table[shortcut.key] = []
            lookup_table[shortcut.key].append(shortcut)

        output_str = '"%s" : {\n' % (self.name)

        sorted_shortcuts = collections.OrderedDict(sorted(lookup_table.items()))
        for key, shortcuts in sorted_shortcuts.items():
            output_str += '    "%s" : [\n' % (key)

            # Important to sort shortcuts alphabetically, this improves the quality of repo diffs
            serialized_shortcuts = [s.serialize() for s in shortcuts]
            serialized_shortcuts.sort()
            for shortcut_str in serialized_shortcuts:
                output_str += '        %s,\n' % (shortcut_str)

            output_str = output_str.rstrip(',\n')
            output_str += '\n    ],\n'
        output_str = output_str.rstrip(',\n')

        output_str += '\n}'

        return output_str





class ApplicationConfig(object):
    def __init__(self):
        super(ApplicationConfig, self).__init__()
        self.contexts = {}
        self.version = None

    """Gets an existing context by name, or adds a new one to the application"""
    def get_or_create_new_context(self, name):
        if name in self.contexts.keys():
            return self.contexts[name]

        context = ShortcutContext(name)
        self.contexts[context.name] = context
        return context

    def get_mods_used(self):
        mods_used = []
        for context in self.contexts.values():
            for shortcut in context.shortcuts:
                for mod in shortcut.mods:
                    if mod not in mods_used:
                        mods_used.append(mod)
        return sorted(mods_used)

    def serialize(self, output_path):
        log.info('serializing ApplicationConfig to %s', output_path)

        mods_used = self.get_mods_used()

        output_str = '{\n'
        output_str += '    "version" : "%s",\n' % (self.version)
        output_str += '    "mods_used" : %s,\n' % (json.dumps(mods_used))
        output_str += '    "contexts" : {\n'

        contexts_str = ""

        contexts = list(self.contexts.values())
        contexts.sort(key=lambda c: c.name)
        for context in contexts:
            # remove empty contexts
            if len(context.shortcuts) == 0:
                continue

            ctx_str = '        ' + context.serialize()
            ctx_str = ctx_str.replace('\n', '\n        ')

            contexts_str += ctx_str + ',\n'
        contexts_str = contexts_str.rstrip(',\n')

        output_str += contexts_str + '\n'
        output_str += '    }\n'
        output_str += '}'

        # Write to file
        file = open(output_path, "w")
        file.write(output_str)
        file.close()




