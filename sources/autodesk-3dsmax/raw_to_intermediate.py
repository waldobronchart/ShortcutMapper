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


class RawKBDXParser(object):
    """This parse grabs shortcuts from a .txt file that was exported from 3dsMax directly.

    Lines starting with '---' start a new context, all lines that follow are shortcuts in that context.
    """

    def __init__(self):
        super(RawKBDXParser, self).__init__()
        self.idata = shmaplib.IntermediateShortcutData("Autodesk 3dsMax")

    def parse(self, source_filepath):
        if not os.path.exists(source_filepath):
            log.error("Source file '%s' does not exist", source_filepath)
            return

        # Read file contents
        f = codecs.open(source_filepath, encoding='utf-8')
        kbdx_file_lines = f.readlines()
        f.close()

        # Regexes
        re_ctx = re.compile("-*? ([a-zA-Z0-9 \./:]*) -*?")
        re_shortcut = re.compile("(.*?)\t(.*?)[\r\n]+")

        # Iterate over all lines
        context_name = None
        for line in kbdx_file_lines[1:]:
            if re_ctx.match(line):
                context_name = re_ctx.search(line).group(1)
                log.debug('Scanning context: "%s"', context_name)

            elif re_shortcut.match(line):
                match = re_shortcut.search(line)
                label = match.group(1)
                keys = match.group(2)

                if len(keys) > 0:
                    # Tabs keys are actual \t in the txt file
                    keys = keys.replace('\t', 'TAB')

                    # Multiple shortcuts are separated by a comma, we use a /
                    keys = keys.replace(', ', ' / ')

                    self.idata.add_shortcut(context_name, label, keys, "")
                    log.debug('...found shortcut "%s"', label)

        return self.idata




def main():
    parser = argparse.ArgumentParser(description="Converts 3dsMax's raw files to an intermediate format.")
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help="Verbose output")
    parser.add_argument('-o', '--output', required=True, help="Output filepath")
    parser.add_argument('source', help="Source: a .txt file exported from max (/raw folder)")

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
    docs_idata = RawKBDXParser().parse(args.source)
    docs_idata.serialize(args.output)




if __name__ == '__main__':
    main()











