#!/usr/bin/python
# coding:utf-8

import re
import copy
import json
import sys
import os
import glob
import logging
import argparse
import codecs

# Import common scripts
CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CWD)
sys.path.insert(0, os.path.normpath(os.path.join(CWD, '..', '..')))

# Import common shortcut mapper library
import shmaplib
from shmaplib.intermediate import IntermediateShortcutData
log = shmaplib.setuplog(os.path.join(CWD, 'output.log'))


p_name = re.compile(r'\[(.*)\]')
p_shortcut = re.compile(r'<kbd>(.*?)</kbd>')
p_fake = re.compile(r'^\*(.*?)<kbd>')
p_op = re.compile(r'\*(.*):')


def _get_file_contents(source):
    f = codecs.open(source)
    contents = f.read()
    f.close()
    return contents.split('\n')


class StEmmetParser(IntermediateShortcutData):

    def __init__(self):
        super(StEmmetParser, self).__init__("Sublime Text")

    def _replall(self, text):
        """Replace the char with the word.
        """
        return text.decode('utf-8').replace(u'⌃', 'Ctrl + ').replace(u'⇧', 'Shift + ').replace(u'⌘', 'Command + ').replace(u'⌥', 'Option + ').replace(u'\u2191', 'Up Arrow').encode('utf-8').replace('→', 'Right Arrow').replace('←', 'Left Arrow').replace('↓', 'Down Arrow')

    def _clean_text(self, text):
        """Convert the text into the shortcut format which we can serialize. 
        """
        if text[0].find('+') != -1:
            return ' + '.join([self._replall(i) for i in text[0].split('+')])
        else:
            return self._replall(text[0])

    def _convert_shortcut(self, origin):
        """Extract the mac keys and the windows keys.
        """
        origin = origin.split(' / ')
        if len(origin) == 1:    # If there is only one shortcuts, we should duplicate it for both OS.
            origin.append(copy.deepcopy(origin[0]))
        keys_mac = [self._clean_text(p_shortcut.findall(i)) for i in origin[0].split('or')]
        keys_win = [self._clean_text(p_shortcut.findall(i)) for i in origin[1].split('or')]
        return ' or '.join(keys_win), ' or '.join(keys_mac)

    def parse(self, source_filepath):
        if not os.path.exists(source_filepath):
            log.error("Source file '%s' does not exist", source_filepath)
            return

        # Use BeautifulSoup to parse the html document
        md_doc = _get_file_contents(source_filepath)

        # Iterate sections (headers are contexts, tables contain the shortcuts)
        context_name = source_filepath.replace('\\', '/').split('/')[-1].split('.')[0]
        log.debug('Scanning context: "%s"', context_name)
        for line in md_doc:
            if line.startswith("## Extensions support ##"):
                break
            if '<kbd>' in line:
                if p_name.findall(line):
                    shortcut_name = p_name.findall(line)[0].decode('utf-8')
                    keys_win, keys_mac = self._convert_shortcut(line[line.find('<kbd>'):])
                elif p_op.findall(line):
                    shortcut_name = p_op.findall(line)[0].strip().decode('utf-8')
                    keys_win, keys_mac = self._convert_shortcut(line[line.find('<kbd>'):])
                elif line.startswith("*"):
                    shortcut_name = p_fake.findall(line)[0].replace('–', '').replace('—', '').strip(' ').decode('utf-8')
                    keys_win, keys_mac = self._convert_shortcut(line[line.find('<kbd>'):])

                self.add_shortcut(context_name, shortcut_name, keys_win, keys_mac)
                log.debug('...found shortcut "%s"', shortcut_name)

        return


def main():
    parser = argparse.ArgumentParser(description="Converts Sublime Text's raw files to an intermediate format.")
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help="Verbose output")
    parser.add_argument('-o', '--output', required=True, help="Output filepath")

    args = parser.parse_args()
    args.output = os.path.abspath(args.output)

    # Verbosity setting on log
    log.setLevel(logging.INFO)
    if args.verbose:
        log.setLevel(logging.DEBUG)

    # Parse the docs html
    docs_idata = StEmmetParser()
    searchdir = os.path.join(CWD, '..', 'raw', '*.*')
    for filepath in glob.glob(searchdir):
        filepath = os.path.normpath(filepath)
        docs_idata.parse(filepath)
        log.info('    \n')
    docs_idata.serialize(args.output)




if __name__ == '__main__':
    main()
