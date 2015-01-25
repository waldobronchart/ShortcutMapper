# -*- coding: utf-8 -*-

import os
import json
import re
import codecs
from bs4 import BeautifulSoup

from appdata import Shortcut, ApplicationConfig
from constants import DIR_CONTENT_GENERATED

from logger import getlog
log = getlog()


def _get_file_contents(source):
    f = codecs.open(source, encoding='utf-8')
    contents = f.read()
    f.close()
    return contents


class AdobeIntermediateData(object):
    """Intermediate data format for adobe shortcuts.

    This can be used as output from various shortcut document parsers and can be
    merged together at the end.

    A serialized IntermediateData document can then be hand-edited to ensure the data
    going exported to the web application is clean and clear."""

    class Shortcut:
        def __init__(self, name, win_keys, mac_keys):
            self.name = name
            self.win_keys = win_keys
            self.mac_keys = mac_keys

        @staticmethod
        def _escape(text):
            text = text.replace('\\', '\\\\')
            text = text.replace('"', '\\"')
            return text

        def serialize(self):
            return u'        "{0}": ["{1}", "{2}"],\n'.format(self._escape(self.name),
                                                              self._escape(self.win_keys), self._escape(self.mac_keys))

    class Context(object):
        def __init__(self, name):
            self.name = name
            self.shortcuts = []

        def add_shortcut(self, name, win_keys, mac_keys):
            if name in [s.name for s in self.shortcuts]:
                return

            s = AdobeIntermediateData.Shortcut(name, win_keys, mac_keys)
            self.shortcuts.append(s)

        def get_shortcut(self, name):
            for s in self.shortcuts:
                if s.name == name:
                    return s
            return None

        def serialize(self):
            ctx_str = u'    "{0}": {{\n'.format(self.name)
            for s in self.shortcuts:
                ctx_str += s.serialize()
            ctx_str = ctx_str.strip(",\n")
            ctx_str += u'\n    },\n'
            return ctx_str

    def __init__(self):
        super(AdobeIntermediateData, self).__init__()
        self.contexts = []
        self._context_lookup = {}

    def add_shortcut(self, context_name, shortcut_name, win_keys, mac_keys):
        if context_name not in self._context_lookup.keys():
            context = AdobeIntermediateData.Context(context_name)
            self._context_lookup[context_name] = context
            self.contexts.append(context)

        self._context_lookup[context_name].add_shortcut(shortcut_name, win_keys, mac_keys)

    def extend(self, idata):
        assert isinstance(idata, AdobeIntermediateData), "Can only extend (merge) with AdobeIntermediateData type"

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
        self.contexts = []
        self._context_lookup = {}

        with codecs.open(file_path, encoding='utf-8') as idata_file:
            json_idata = json.load(idata_file)
            for context_name, shortcuts in json_idata.iteritems():
                for shortcut_name, os_keys in shortcuts.iteritems():
                    self.add_shortcut(context_name, shortcut_name, os_keys[0], os_keys[1])

    def serialize(self, output_path):
        json_str = "{\n"
        for context in self.contexts:
            json_str += context.serialize()
        json_str = json_str.strip(",\n")
        json_str += "\n}\n"

        f = codecs.open(output_path, encoding='utf-8', mode='w+')
        f.write(json_str)
        f.close()


class AdobeDocsParser(object):
    """This parser scrapes shortcuts and contexts from an adobe shortcuts documentation html file, such as:
    http://helpx.adobe.com/en/photoshop/using/default-keyboard-shortcuts.html

    It assumes the main relevant data is contained in a wrapper div: <div class="parsys main-pars">...</div>
    From the contents of this div, it can extract shortcut contexts, shortcut names and keys for Windows and MacOS
    """

    def __init__(self):
        super(AdobeDocsParser, self).__init__()
        self.idata = AdobeIntermediateData()

    @staticmethod
    def _clean_text(text):
        text = text.replace(u'\n', u' ').strip(u' ').replace(u'\xa0', u' ')
        # Remove stuff within braces
        text = re.sub("([\(]).*?([\)])", "", text)
        # Remove meta-data tags
        text = text.replace(u'†', u'').replace(u'‡', u'').strip(u'*')

        return text.strip(u' ')

    def parse(self, source_file_path):
        if not os.path.exists(source_file_path):
            log.error("Source file '%s' does not exist", source_file_path)
            return

        # Use BeautifulSoup to parse the html document
        doc = BeautifulSoup(_get_file_contents(source_file_path))
        main_wrapper_div = doc.find("div", class_="parsys main-pars")
        sections = main_wrapper_div.find_all("div", class_="parbase")

        # Iterate sections (headers are contexts, tables contain the shortcuts)
        context_name = None
        for section in sections:
            # This section is a header, the only relevant information here is the context
            if 'header' in section['class']:
                h2 = section.find('h2')
                context_name = str(h2.contents[0]).replace('\n', ' ').strip(' ')
                log.debug('Scanning context: "%s"', context_name)

            # This is a section containing the shortcuts table
            elif 'table' in section['class']:
                rows = section.find('tbody').find_all('tr')

                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) != 3:
                        continue

                    shortcut_name = self._clean_text(cols[0].p.get_text())
                    keys_win = self._clean_text(cols[1].get_text())
                    keys_mac = self._clean_text(cols[2].get_text())

                    self.idata.add_shortcut(context_name, shortcut_name, keys_win, keys_mac)
                    log.debug('...found shortcut "%s"', shortcut_name)

        return self.idata


class AdobeSummaryParser(object):
    """This parser scrapes shortcuts and contexts from an adobe summary export. This file is exported from
    photoshop's Edit shortcuts dialog."""

    def __init__(self):
        super(AdobeSummaryParser, self).__init__()
        self.idata = AdobeIntermediateData()

    def parse(self, source_filepath, platform_type):
        assert platform_type in ["windows", "mac"], "Platform must be 'windows' or 'mac'"

        if not os.path.exists(source_filepath):
            log.error("Source file '%s' does not exist", source_filepath)
            return

        # Use BeautifulSoup to parse the html document
        doc = BeautifulSoup(_get_file_contents(source_filepath))
        tables = doc.find_all('table')

        for table in tables:
            parent_categories = []
            prev_was_category = False
            indentation = None

            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')

                # Check for category
                if len(cols) == 1:
                    if len(parent_categories):
                        parent_categories = parent_categories[:len(parent_categories)-1]
                    if len(cols[0]):
                        parent_categories.append(cols[0].text + '>')
                    continue

                spacers = row.find_all('td', attrs={'width':'40'})
                shortcutcols = row.find_all('td', attrs={'class':'shortcutcols'})

                # Handle indentation
                if not indentation:
                    indentation = len(spacers)
                if len(spacers) < indentation or (prev_was_category and len(spacers) == indentation):
                    parent_categories = parent_categories[:len(parent_categories)-1]
                indentation = len(spacers)

                # Skip if there are no shortcuts in this row
                if not len(shortcutcols):
                    # Check if it is a parent menu item '>'
                    for col in cols:
                        if '>' in col.text:
                            category = col.text
                            parent_categories.append(category)
                            prev_was_category = True
                    continue
                prev_was_category = False

                # Find the name and shortcut text
                name = None
                keys = None
                for col in shortcutcols:
                    if col.text:
                        if name is None:
                            name = col.text.replace('...', '')
                            continue

                        # Check if content is &nbsp;
                        if col.text == u'\xa0':
                            continue

                        # Shortcut + removing <br>'s
                        keys = u' or '.join(col.findAll(text=True))

                        # No need to continue, we found the the shortcuts
                        break

                if not keys:
                    continue

                # It's a shortcut, but is it set?
                full_name = u''.join(parent_categories) + name
                if platform_type == 'windows':
                    self.idata.add_shortcut("Application", full_name, keys, "")
                else:
                    self.idata.add_shortcut("Application", full_name, "", keys)

        return self.idata


class AdobeExporter(object):
    """Exports an intermediate .json file to the gh-pages appdata dir in the correct file format."""

    def __init__(self, source, app_name, app_version, defualt_context_name):
        super(AdobeExporter, self).__init__()
        self.source_file = source
        self.app_name = app_name
        self.app_version = app_version
        self.default_context_name = defualt_context_name

        # Windows and Mac appconfigs
        self.app_win = ApplicationConfig(self.app_name, self.app_version, 'windows', self.default_context_name)
        self.app_mac = ApplicationConfig(self.app_name, self.app_version, 'mac', self.default_context_name)

    @staticmethod
    def _parse_shortcut(name, keys):
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

            # For numerical key shortcuts, the adobe documentation specifies a "range of keys"
            #  which will result in multiple shortcuts with the same label
            if re.match("[0-9]*.-.[0-9]*", key):
                start = int(key[0])
                end = int(key[-1])
                for i in range(start, end+1):
                    shortcut = Shortcut(name, str(i), mods)
                    shortcuts.append(shortcut)

            # Result is just one shortcut
            else:
                shortcut = Shortcut(name, key, mods)
                shortcuts.append(shortcut)

        return shortcuts

    def parse(self):
        if not os.path.exists(self.source_file):
            log.error("Source file '%s' does not exist", self.source_file)
            return

        # Windows and Mac appconfigs
        self.app_win = ApplicationConfig(self.app_name, self.app_version, 'windows', self.default_context_name)
        self.app_mac = ApplicationConfig(self.app_name, self.app_version, 'mac', self.default_context_name)

        # Load intermediate data
        idata = AdobeIntermediateData()
        idata.load(self.source_file)

        # WINDOWS: Iterate contexts and shortcuts
        log.info("Parsing intermediate data for Windows shortcuts")
        for context in idata.contexts:
            context_win = self.app_win.get_or_create_new_context(context.name)
            for shortcut in context.shortcuts:
                for s in self._parse_shortcut(shortcut.name, shortcut.win_keys):
                    context_win.add_shortcut(s)

        # MAC: Iterate contexts and shortcuts
        log.info("Parsing intermediate data for MacOS shortcuts")
        for context in idata.contexts:
            context_mac = self.app_mac.get_or_create_new_context(context.name)
            for shortcut in context.shortcuts:
                for s in self._parse_shortcut(shortcut.name, shortcut.mac_keys):
                    context_mac.add_shortcut(s)

    def export(self):
        self.app_win.serialize(DIR_CONTENT_GENERATED)
        self.app_mac.serialize(DIR_CONTENT_GENERATED)





