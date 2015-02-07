# -*- coding: utf-8 -*-

import sys
import os
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
    """This parser scrapes shortcuts and contexts from the unity documentation html file, such as:
    http://docs.unity3d.com/Manual/UnityHotkeys.html

    It assumes the main relevant data is contained in a wrapper div: <div class="section">...</div>
    From the contents of this div, it can extract shortcut contexts, shortcut names and keys for Windows and MacOS
    """

    def __init__(self):
        super(RawDocsParser, self).__init__()
        self.idata = shmaplib.IntermediateShortcutData("Unity 3D")

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
        main_wrapper_div = doc.find("div", class_="section")
        tables = main_wrapper_div.find_all("table")

        # Iterate sections
        # - the first tr is ignored, this is actually the header
        context_name = "Global Context"
        for table in tables:
            rows = table.tbody.find_all("tr")
            for row in rows[1:]:
                # The row contains 2 cols with shortcut on left, and info on right
                cols = row.find_all("td")

                # Skip the non-shortcut cols
                if len(cols) != 2:
                    continue
                if cols[0].em is not None:
                    continue

                keys = cols[0].get_text()
                label = cols[1].get_text()

                # Split up into windows and mac shortcuts
                # Example: CTRL/CMD+ALT+P
                keys_win = keys
                keys_mac = keys
                if '/' in keys:
                    mods, keys = tuple(keys.split('+', 1))
                    mods = mods.split('/')
                    keys_win = mods[0] + "+" + keys
                    keys_mac = mods[1] + "+" + keys

                self.idata.add_shortcut(context_name, label, keys_win, keys_mac)
                log.debug('...found shortcut "%s"', label)

        return self.idata


def main():
    parser = argparse.ArgumentParser(description="Converts Unity's raw files to an intermediate format.")
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











