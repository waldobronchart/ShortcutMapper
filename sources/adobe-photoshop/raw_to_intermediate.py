# -*- coding: utf-8 -*-

import sys
import os
import glob
import logging
import argparse
import re

# Import common scripts
CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CWD)
sys.path.insert(0, os.path.normpath(os.path.join(CWD, '..', '..')))

# Import common shortcut mapper library
import shmaplib
from shmaplib.adobe import AdobeDocsParser, AdobeSummaryParser
from shmaplib import IntermediateShortcutData
log = shmaplib.setuplog(os.path.join(CWD, 'output.log'))

APP_NAME = "Adobe Photoshop"

def main():
    parser = argparse.ArgumentParser(description="Converts Photoshop's raw files to an intermediate format.")
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help="Verbose output")
    parser.add_argument('-o', '--output', required=True, help="Output filepath")
    parser.add_argument('docs_html', help="A HTML file containing shortcuts saved directly from adobe's online documentation")
    parser.add_argument('summary_mac', help="A summary HTML file exported from photoshop for MacOS")
    parser.add_argument('summary_win', help="A summary HTML file exported from photoshop for Windows")

    args = parser.parse_args()
    args.docs_html = os.path.abspath(args.docs_html)
    args.summary_mac = os.path.abspath(args.summary_mac)
    args.summary_win = os.path.abspath(args.summary_win)

    if not os.path.exists(args.docs_html) or not os.path.exists(args.summary_mac):
        print("Error: One of the provided files does not exist")
        return

    # Verbosity setting on log
    log.setLevel(logging.INFO)
    if args.verbose:
        log.setLevel(logging.DEBUG)

    # Parse the docs html
    docs_idata = AdobeDocsParser(APP_NAME).parse(args.docs_html)

    # Parse both summary docs
    mac_summary_idata = AdobeSummaryParser(APP_NAME).parse(args.summary_mac, "mac")
    win_summary_idata = AdobeSummaryParser(APP_NAME).parse(args.summary_win, "windows")

    # Merge all source data into a single file
    merged_idata = IntermediateShortcutData(APP_NAME)
    merged_idata.extend(mac_summary_idata)
    merged_idata.extend(win_summary_idata)
    merged_idata.extend(docs_idata)
    merged_idata.serialize(args.output)




if __name__ == '__main__':
    main()











