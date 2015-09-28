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
from shmaplib.adobe import AdobeDocsParser
log = shmaplib.setuplog(os.path.join(CWD, 'output.log'))


def main():
    parser = argparse.ArgumentParser(description="Converts Illustrator's raw files to an intermediate format.")
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
    docs_idata = AdobeDocsParser("Adobe After Effects").parse(args.source)
    docs_idata.serialize(args.output)


if __name__ == '__main__':
    main()











