import sys
import os
import glob
import logging
import argparse

# Import common scripts
CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CWD)
sys.path.insert(0, os.path.normpath(os.path.join(CWD, '..')))

# Import common shortcut mapper library
import shmaplib
from shmaplib.constants import DIR_SOURCES
log = shmaplib.setuplog(os.path.join(CWD, 'output.log'))


def export_intermediate_file(file_path, test_mode, explicit_numpad_mode):
    log.info("Exporting from file: %s", file_path)

    exporter = shmaplib.IntermediateDataExporter(file_path, explicit_numpad_mode)
    exporter.parse()
    if not test_mode:
        exporter.export()


def main():
    parser = argparse.ArgumentParser(description="Converts intermediate json data files to the web application data format.")
    parser.add_argument('-t', '--test', action='store_true', required=False, help="Run in test mode. This does not output any file")
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help="Verbose output")
    parser.add_argument('-a', '--all', action='store_true', required=False, help="Convert all raw files to our json format")
    parser.add_argument('-e', '--explicit-numpad-keys', action='store_true', required=False, help="Numpad keys don't have the same action as main keys")
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

    # Test mode
    test_mode = args.test

    # If --all flag is set, convert all application intermediate data
    if args.all:
        search_dir = os.path.join(DIR_SOURCES, '*', 'intermediate', '*.json')
        for file_path in glob.glob(search_dir):
            file_path = os.path.normpath(file_path)
            export_intermediate_file(file_path, test_mode, args.explicit_numpad_keys)
            log.info('    \n')
    else:
        export_intermediate_file(args.file, test_mode, args.explicit_numpad_keys)

if __name__ == '__main__':
    main()











