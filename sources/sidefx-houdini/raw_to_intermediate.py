# -*- coding: utf-8 -*-

import sys
import os
import logging
import argparse
import codecs
import re

# Import common scripts
CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CWD)
sys.path.insert(0, os.path.normpath(os.path.join(CWD, '..', '..')))

# Import common shortcut mapper library
import shmaplib
log = shmaplib.setuplog(os.path.join(CWD, 'output.log'))

class RawHoudiniConfigParser(object):
    """This parser reads files from Houdini's key config and finds shortcuts and contexts in them

    Example of file:
    //
    // Handle list definitions
    //

    HCONTEXT h.pane.parmsheet	"Parameter Spreadsheet"	"These keys apply to the Parameter Spreadsheet pane."

    h.pane.parmsheet.copy_parm		"Copy Parameters"		"Copy parameters"
    h.pane.parmsheet.paste_vals		"Paste Copied Values"		"Paste copied values"
    h.pane.parmsheet.paste_exprs		"Paste Copied Expressions"	"Paste copied expressions"			Cmd+E
    """

    def __init__(self):
        super(RawHoudiniConfigParser, self).__init__()
        self.idata = shmaplib.IntermediateShortcutData("SideFx Houdini", "NA", "Houdini")
        self._context_id_to_name_lookup = {}

        # HCONTEXT deskmgr "Desktop Manager" "These keys are used in the Desktop Manager dialog."
        self._re_context = re.compile('HCONTEXT\s+(.*?)\s+"(.*?)"\s+"(.*?)"')
        # deskmgr.new		"New"		"Create a new desktop"		Alt+N N
        self._re_shortcut = re.compile('(.*?)\s+"(.*?)"\s+"(.*?)"\s+(.*?)$')

    def parse(self, source_dir):
        if not os.path.exists(source_dir):
            log.error("Source directory '%s' does not exist", source_dir)
            return

        name = os.path.basename(source_dir)
        self.idata.version = name[name.index('_v')+1:-4]

        files = os.listdir(source_dir)
        for filename in files:
            filepath = os.path.join(source_dir, filename)
            log.debug('Parsing file "%s"', filepath)
            self._parse_file(filepath)

        return self.idata


    def _parse_file(self, filepath):
        # Read file contents
        f = codecs.open(filepath, encoding='utf-8')
        file_lines = f.readlines()
        f.close()

        # Scan lines
        for line in file_lines:
            line = line.replace('\t', ' ').strip('\n')
            log.debug("Parsing line: %s", line)

            # Ignore comments, includes and empty lines
            if line.startswith('//') or line.startswith('#') or not len(line):
                continue

            # Some lines have comments at the end, remove that
            if '//' in line:
                line = line[:line.index('//')]

            # Context line
            if line.startswith('HCONTEXT '):
                self._parse_context_name(line)
                continue

            # Shortcut line
            shortcut_match = self._re_shortcut.search(line)
            if shortcut_match:
                command, label, description, keys = shortcut_match.groups()

                # / is separator for multiple keys
                keys = keys.replace(' ', ' / ')
                keys = keys.replace('\\\\', '\\').replace('\\\'', "'")
                keys_win = keys.replace('Cmd', 'Ctrl')
                if not len(keys):
                    continue

                context_id = command[0:command.rfind('.')]
                context_name = self._context_id_to_name_lookup[context_id]

                self.idata.add_shortcut(context_name, label, keys_win, keys)
                log.debug('...found shortcut "%s"', label)


    def _parse_context_name(self, line):
        match = self._re_context.search(line)
        if not match:
            log.error("Invalid context line: %s", line)
            return

        id, name, description = match.groups()
        if id in self._context_id_to_name_lookup:
            return self._context_id_to_name_lookup[id]

        # Special treatment for pane contexts
        # h.pane.parms
        # h.pane.parms.effects (get parent: h.pane.parms and then append context name to that)
        if '.pane.' in id:
            if id.count('.') > 2:
                parts = id.split('.')
                parent_id = '.'.join(parts[:3])
                name = "{0} ({1})".format(self._context_id_to_name_lookup[parent_id], name)
            else:
                name = "Pane: " + name

        # Put everything under h.* in Houdini context
        elif id.startswith('h.'):
            name = "Houdini"

        self._context_id_to_name_lookup[id] = name
        return name




def main():
    parser = argparse.ArgumentParser(description="Converts Houdini's keyboard config files to an intermediate format that can be hand-edited.")
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help="Verbose output")
    parser.add_argument('-o', '--output', required=True, help="Output filepath")
    parser.add_argument('source', help="Source: path to directory of Houdini keyboard shortcuts (found under raw dir)")

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

    # Parse the keyconfig data
    docs_idata = RawHoudiniConfigParser().parse(args.source)
    docs_idata.serialize(args.output)




if __name__ == '__main__':
    main()
