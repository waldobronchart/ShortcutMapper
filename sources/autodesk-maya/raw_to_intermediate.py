# -*- coding: utf-8 -*-

import sys
import os
import glob
import logging
import argparse
import re
import codecs
from bs4 import BeautifulSoup

# Import common scripts
CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CWD)
sys.path.insert(0, os.path.normpath(os.path.join(CWD, '..', '..')))

# Import common shortcut mapper library
import shmaplib
log = shmaplib.setuplog(os.path.join(CWD, 'output.log'))


class RawDocsParser(object):
    """This parser scrapes shortcuts and contexts from the maya documentation html file, such as:
    http://download.autodesk.com/global/docs/maya2014/en_us/index.html?url=files/Keyboard_Shortcuts.htm

    It assumes the main relevant data is contained in a wrapper div: <div class="body_content">...</div>
    From the contents of this div, it can extract shortcut contexts, shortcut names and keys for Windows and MacOS
    """

    def __init__(self):
        super(RawDocsParser, self).__init__()
        self.idata = shmaplib.IntermediateShortcutData("Autodesk Maya")

    def _clean_text(self, text):
        text = text.replace(u'\n', u' ').strip(u' ').replace(u'\xa0', u' ')
        # Remove stuff within braces
        text = re.sub("([\(]).*?([\)])", "", text)
        # Remove meta-data tags
        text = text.replace(u'†', u'').replace(u'‡', u'').strip(u'*')

        return text.strip(u' ')

    def parse(self, source_filepath):
        if not os.path.exists(source_filepath):
            log.error("Source file '%s' does not exist", source_filepath)
            return

        # Read file contents
        f = codecs.open(source_filepath, encoding='utf-8')
        contents = f.read()
        f.close()

        # Use BeautifulSoup to parse the html document
        doc = BeautifulSoup(contents)
        main_wrapper_div = doc.find("div", class_="body_content")
        sections = main_wrapper_div.find_all("table", class_="ruled")

        # Iterate sections
        # - tr.ruledHeading is assumed as context name
        # - other tr's contain 3 cols: "Modifier buttons", "Keys", "Label"
        context_name = None
        for section in sections:
            rows = section.find_all("tr")
            for row in rows:
                # This row is a header, the only relevant information here is the context name in first col
                if u"ruledHeading" in row['class']:
                    context_name = self._clean_text(str(row.th.get_text()))
                    log.debug('Scanning context: "%s"', context_name)

                # This row contains 3 cols with shortcut information
                else:
                    cols = row.find_all("td")
                    mods, or_mac_cmd_mod, keys, label = ("", False, "", "")

                    if cols[0].find('p') is not None:
                        mods_rawtext = cols[0].p.get_text()
                        mods = self._clean_text(mods_rawtext)
                        or_mac_cmd_mod = '(or' in mods_rawtext
                    if cols[1].find('p') is not None:
                        keys = self._clean_text(cols[1].p.get_text())
                    if cols[2].find('p') is not None:
                        label = self._clean_text(cols[2].p.get_text())

                    keys_win = keys
                    if len(mods) > 0:
                        keys_win = mods + " + " + keys

                    keys_mac = keys_win
                    if or_mac_cmd_mod:
                        keys_mac = keys_mac + " / " + keys_mac.replace('Ctrl', 'Cmd')

                    self.idata.add_shortcut(context_name, label, keys_win, keys_mac)
                    log.debug('...found shortcut "%s"', label)


        return self.idata




def main():
    parser = argparse.ArgumentParser(description="Converts Maya's raw files to an intermediate format.")
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help="Verbose output")
    parser.add_argument('-o', '--output', required=True, help="Output filepath")
    parser.add_argument('source', help="Source: HTML file containing shortcuts saved directly from adobe's online documentation (/raw folder)")

    args = parser.parse_args()
    args.source = os.path.abspath(args.source)
    args.output = os.path.abspath(args.output)

    if not os.path.exists(args.source):
        print("Error: the input source file doesn't exist.")
        return

    # Verbosity setting on log
    log.setLevel(logging.INFO)
    if args.verbose:
        log.setLevel(logging.DEBUG)

    # Parse the docs html
    docs_idata = RawDocsParser().parse(args.source)
    docs_idata.serialize(args.output)




if __name__ == '__main__':
    main()











