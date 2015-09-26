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
    """This parser scrapes shortcuts and contexts from the NUKE documentation html file, such as:
    help.thefoundry.co.uk/nuke/8.0/content/user_guide/hotkeys/hotkeys.html

    It assumes "contexts" are wrapped by a div with class MCDropDown: <div class="MCDropDown">
    From the contents of this div, it can extract shortcut contexts, shortcut names and keys for Windows and MacOS
    """

    def __init__(self):
        super(RawDocsParser, self).__init__()
        self.idata = shmaplib.IntermediateShortcutData("The Foundry: Nuke")

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
        sections = doc.find_all("div", class_="MCDropDown")

        # Iterate sections
        # - <span class="MCDropDownHead dropDownHead"> contains the context name
        # - The shortcuts are contained in a child element table
        context_name = None
        for section in sections:
            header = section.find("span", class_="MCDropDownHead")
            context_name = self._clean_text(header.get_text())
            log.debug('Scanning context: "%s"', context_name)

            rows = section.find("table").find("tbody").find_all("tr")
            for row in rows:
                cols = row.find_all("td")

                keys = self._clean_text(cols[0].get_text())
                label = self._clean_text(cols[1].get_text())

                keys_win = keys
                keys_mac = keys_win.replace('Ctrl', 'Cmd')

                self.idata.add_shortcut(context_name, label, keys_win, keys_mac)
                log.debug('...found shortcut "%s"', label)


        return self.idata




def main():
    parser = argparse.ArgumentParser(description="Scrapes a list of shortcuts from NUKE's documentation")
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help="Verbose output")
    parser.add_argument('-o', '--output', required=True, help="Output filepath")
    parser.add_argument('source', help="Source: HTML file containing shortcuts saved directly from the NUKE online documentation (/raw folder)")

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











