# Todo: warn if a NAME_OVERRIDE was not used, will usually mean somthing is wrong or something has changed in Photoshop
#

import sys
import os
import glob
import argparse
import json
import logging
from bs4 import BeautifulSoup

# Import common scripts
CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CWD)
sys.path.insert(0, os.path.normpath(os.path.join(CWD, '..', '..', '..')))

# Import common shortcut mapper library
import shmaplib
log = shmaplib.setuplog(os.path.join(CWD, 'output.log'))


# Override these items
#  mainly because the name after the last > is not descriptive enough
NAME_OVERRIDES = {
    "View>Gamut Warning" : "View Gamut Warning",
    "View>Proof Colors" : "View Proof Colors",
    "View>100%" : "Zoom 100%",
    "View>Fit on Screen" : "Zoom Fit on Screen",
    "View>Snap" : "Toggle Snapping",
    "View>Rulers" : "Toggle Rulers",
    "View>Lock Guides" : "Toggle Lock Guides",
    "View>Show>Guides" : "Toggle Guides",
    "View>Show>Target Path" : "Toggle Show Target Path",
    "View>Show>Grid" : "Toggle Grid",

    "Edit>Step Forward" : "Redo Once",
    "Edit>Step Backward" : "Undo Once",
    "Edit>Transform>Again" : "Transform Again",
    "Edit>Menus" : "Menu Preferences",

    "Select>All" : "Select All",
    "Select>All Layers" : "Select All Layers",
    "Select>Inverse" : "Invert Selection",
    "Select>Modify>Feather" : "Feather Selection",
    "Select>Inverse" : "Invert Selection",

    "Filter>Adaptive Wide Angle" : "Adaptive Wide Angle Filter",
    "Filter>Last Filter" : "Apply Last Filter",
    "Filter>Lens Correction" : "Lens Correction Filter",
    "Filter>Liquify" : "Liquify Filter",
    "Filter>Vanishing Point" : "Vanishing Point Filter",

    "Image>New>Layer Via Copy" : "New Layer Via Copy",
    "Image>New>Layer Via Cut" : "New Layer Via Cut",
    "Image>New>Layer" : "New Layer",
    "Image>Adjustments>Invert" : "Invert Image",
    "Image>Adjustments>Curves" : "Adjust Curves",
    "Image>Adjustments>Levels" : "Adjust Levels",

    "Default Foreground/Background Colors" : "Default Picker Colors",
    "Switch Foreground/Background Colors" : "Swap Picker Colors",

    "Photoshop>Hide Others" : "Hide Other Windows",
    "Photoshop>Preferences>General" : "General Preferences",

    "File>Revert" : "Revert File",
    "File>Close" : "Close File",
    "File>Close All" : "Close All Files",

    "3D>Render" : "Render 3D",
    "3D>Show/Hide Polygons>Reveal All" : "Reveal All Polygons",
    "3D>Show/Hide Polygons>Within Selection" : "Hide Polygons in Selection",

    "Window>Arrange>Minimize" : "Minimize Window",
    "Window>Brush" : "Brush Panel",
    "Window>Color" : "Color Panel",
    "Window>Layers" : "Layers Panel",
    "Window>Info" : "Info Panel",
    "Window>Actions" : "Actions Panel",
}

# < is actually Shift+, on a US keyboard
FAULTY_SHORTCUT_KEYCOMBOS_TO_FIX = {
    '<':'Shift+,',
    '>':'Shift+.',
    '{':'Shift+[',
    '}':'Shift+]'
}

# We need to do these manually, lots of duplicates here
KEYCOMBOS_TO_DELETE = [
    "M", "L", "W", "I", "C", "J", "B", "S",
    "Y", "E", "G", "O", "P", "T", "A", "U",
]

# Add tool shortcuts manually
SHORTCUTS_TO_ADD = {
    "Rectangular Marquee Tool" : ["M"],
    "Cycle Marquee Tools" : ["Shift+M"],
    "Lasso Tool" : ["L"],
    "Cycle Lasso Tools" : ["Shift+L"],
    "Quick Selection Tool" : ["W"],
    "Cycle Quick Selection Tools" : ["Shift+W"],
    "Eyedropper Tool" : ["I"],
    "Cycle Utility Tools" : ["Shift+I"],
    "Crop Tool" : ["C"],
    "Cycle Crop/Slice Tools": ["Shift+C"],
    "Spot Healing Brush" : ["J"],
    "Cycle Healing Tools" : ["Shift+J"],
    "Brush Tool" : ["B"],
    "Cycle Brush Tools" : ["Shift+B"],
    "History Brush Tool" : ["Y"],
    "Cycle History Brush Tools" : ["Shift+Y"],
    "Eraser Tool" : ["E"],
    "Cycle Eraser Tools" : ["Shift+E"],
    "Gradient Tool" : ["G"],
    "Cycle Fill Tools" : ["Shift+G"],
    "Dodge Tool" : ["O"],
    "Cycle Effect Brush Tools" : ["Shift+O"],
    "Pen Tool" : ["P"],
    "Cycle Pen Tools" : ["Shift+P"],
    "Text Tool" : ["T"],
    "Cycle Text Tools" : ["Shift+T"],
    "Path Selection Tool" : ["A"],
    "Cycle Path Selection Tools" : ["Shift+A"],
    "Rectangle Tool" : ["U"],
    "Cycle Shape Tools" : ["Shift+U"],
}



"""
Parses the Exported HTML document from Photoshop

returns a dictionary of {name:[keycombo strings]}
"""
def parse_document(doc):
    doc = BeautifulSoup(doc)
    data = {}

    tables = doc.find_all('table')
    for table in tables:
        parent_categories = []
        prev_was_category = False
        indentation = None

        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')

            # Check for category
            if len(cols) == 1:
                if len(parent_categories):
                    parent_categories = parent_categories[:len(parent_categories)-1]
                if len(cols[0]):
                    parent_categories.append(cols[0].text + '>')
                continue

            spacers = row.find_all('td', attrs={'width':'40'})
            shortcutcols = row.find_all('td', attrs={'class':'shortcutcols'})

            # Handle indentation
            if not indentation:
                indentation = len(spacers)
            if len(spacers) < indentation or (prev_was_category and len(spacers) == indentation):
                parent_categories = parent_categories[:len(parent_categories)-1]
            indentation = len(spacers)

            # Skip if there are no shortcuts in this row
            if not len(shortcutcols):
                # Check if it is a parent menu item '>'
                for col in cols:
                    if '>' in col.text:
                        category = col.text
                        parent_categories.append(category)
                        prev_was_category = True
                continue
            prev_was_category = False

            # Find the name and shortcut text
            name = None
            shortcuts = None
            for col in shortcutcols:
                if col.text:
                    if name is None:
                        name = col.text.replace('...', '')
                        continue

                    # Check if content is &nbsp;
                    if col.text == u'\xa0':
                        continue

                    # Shortcut + removing <br>'s
                    shortcuts = col.contents
                    if col.br:
                        shortcuts = []
                        for c in col.contents:
                            if isinstance(c, basestring):
                                shortcuts.append(c)
                            else:
                                txt_br = str(c).replace('/br', 'br').strip('<br>')
                                shortcuts.extend(txt_br.split('<br>'))

                    # No need to contiue, we found the the shortcuts
                    break

            if not shortcuts:
                continue

            # It's a shortcut, but is it set?
            full_name = ''.join(parent_categories) + name
            data[full_name] = shortcuts

    return data

def modify_shortcut_name(shortcut):
    name = shortcut.name
    if name in NAME_OVERRIDES.keys():
        name = NAME_OVERRIDES[name]

    splits = name.split('>')
    shortcut.name = splits[len(splits)-1]

"""
Takes in data from the parse_document function and creates our common data structure
"""
def parse_shortcuts(data):
    app = shmaplib.ApplicationConfig()
    context = app.get_or_create_new_context('Default')

    # Delete selective keycombos
    for name, keycombos in data.items():
        for s in keycombos:
            if s in KEYCOMBOS_TO_DELETE:
                del data[name]
                log.debug("deleted keycombo for %s (%s)", name, str(keycombos))

    # Add our manual shortcuts to data
    for name, keycombos in SHORTCUTS_TO_ADD.items():
        data[name] = keycombos

    # Iterate on each keycombo in
    for name, keycombos in data.items():
        for keycombo in keycombos:
            # Fix photoshop faulty shortcut documentation
            for k,r in FAULTY_SHORTCUT_KEYCOMBOS_TO_FIX.items():
                # todo: make sure to add a plus if needed
                keycombo = keycombo.replace(k, r)

            # Before we split, replace + with PLUS_TEMP
            keycombo = keycombo.replace('++', '+PLUS_TEMP')
            combokeys = keycombo.split('+')

            # Parse main key
            key = combokeys[len(combokeys)-1] #last element
            if key == 'PLUS_TEMP':
                key = '+'

            # Parse modifiers
            mods = combokeys[:len(combokeys)-1] #all but last

            # Modify name and add to context
            shortcut = shmaplib.Shortcut(name, key, mods)
            modify_shortcut_name(shortcut)

            context.add_shortcut(shortcut)

    # Output all shortcuts again
    log.debug("\n\n")
    log.debug("All shortcuts:")
    snames = context.added_shortcuts_lookup
    snames.sort()
    for sname in snames:
        log.debug(sname)

    return app



def convert_file(source, target):
    log.info("Converting raw file '%s'", source)
    if not os.path.exists(source):
        log.error("Source file '%s' does not exist", source)
        return

    f = open(source, 'r')
    contents = f.read()
    f.close()

    # Parse document and serialize
    doc_data = parse_document(contents)
    app_config = parse_shortcuts(doc_data)
    app_config.serialize(target)

def main():
    parser = argparse.ArgumentParser(description="Converts Photoshop's exported shortcuts html file to our data format")
    parser.add_argument('-t', '--test', action='store_true', required=False, help="Run in test mode. This does not output any file")
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help="Verbose output")
    parser.add_argument('-a', '--all', action='store_true', required=False, help="Convert all raw files to our json format")
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

    # If --all flag is set, convert all html file in raw to our json format
    outputdir = shmaplib.DIR_PAGES_APPDATA
    if args.all:
        app_dir = os.path.normpath(os.path.join(CWD, '..'))

        for source in glob.glob(os.path.join(app_dir, 'raw', '*.html')):
            source_name = os.path.basename(source)
            target = os.path.join(outputdir, os.path.splitext(source_name)[0] + '.json')
            convert_file(source, target)
            log.info('    \n\n')
    else:
        source_name = os.path.basename(args.file)
        target = os.path.join(outputdir, os.path.splitext(source_name)[0] + '.json')
        convert_file(args.file, target)

if __name__ == '__main__':
    main()











