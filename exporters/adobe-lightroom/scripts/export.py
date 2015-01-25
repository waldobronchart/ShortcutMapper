import sys
import os
import glob
import logging
import argparse
import re

# Import common scripts
CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CWD)
sys.path.insert(0, os.path.normpath(os.path.join(CWD, '..', '..', '..')))

# Import common shortcut mapper library
import shmaplib
from shmaplib.adobe import AdobeIntermediateData, AdobeDocsParser, AdobeSummaryParser, AdobeExporter
log = shmaplib.setuplog(os.path.join(CWD, 'output.log'))


def export_file(filepath, testmode):
    log.info("Exporting from file: %s", filepath)

    filename, ext = os.path.splitext(os.path.basename(filepath))
    version = filename.split('_')[1]

    exporter = AdobeExporter(filepath, "Adobe Lightroom", version, "Global Context")
    exporter.parse()
    if not testmode:
        exporter.export()


def main():
    parser = argparse.ArgumentParser(description="Converts Lightroom's intermediate json data file to the web application data format.")
    parser.add_argument('-t', '--test', action='store_true', required=False, help="Run in test mode. This does not output any file")
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help="Verbose output")
    parser.add_argument('-a', '--all', action='store_true', required=False, help="Convert all intermediate files to the site format")
    parser.add_argument('file', nargs='?', help="File to convert (Ignored if -a flag is set)")

    args = parser.parse_args()
    if not args.all and args.file is None:
        print("Missing arguments file and outputfile, use -h flag for help")
        return
    if args.file is not None:
        args.file = os.path.abspath(args.file)

    # Verbosity setting on log
    log.setLevel(logging.INFO)
    if args.verbose:
        log.setLevel(logging.DEBUG)

    # Testmode
    testmode = args.test

    # If --all flag is set, convert all intermediate files to the site format
    if args.all:
        searchdir = os.path.join(CWD, '..', 'intermediate', '*.json')
        for filepath in glob.glob(searchdir):
            filepath = os.path.normpath(filepath)
            export_file(filepath, testmode)
            log.info('    \n')
    else:
        export_file(args.file, testmode)

if __name__ == '__main__':
    main()











