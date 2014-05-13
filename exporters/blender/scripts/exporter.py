import sys
import os
import logging

CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CWD)
sys.path.insert(0, os.path.normpath(os.path.join(CWD, '..', '..', '..')))

# Import common shortcut mapper library
import shmaplib
log = shmaplib.setuplog(os.path.join(CWD, 'output.log'))

# Import blender related stuff
import bpy
import exporter_utils as util


def parse_main_keyconfig():
    """The beef, this gets all keyconfigs from blender and converts blender data into
    our specific format."""

    app = shmaplib.ApplicationConfig()
    keyconfig = bpy.context.window_manager.keyconfigs[0]

    # Find all keymaps
    for keymap in keyconfig.keymaps:
        if keymap.name in util.KEYMAPS_IGNORE:
            continue

        # Apply keymap name overrides
        keymap_name = keymap.name
        if keymap.name in util.KEYMAP_NAME_OVERRIDES.keys():
            keymap_name = util.KEYMAP_NAME_OVERRIDES[keymap.name]

        # Create a new ShortcutContext
        log.info('parsing keymap: %s', keymap_name)
        context = app.get_or_create_new_context(keymap_name)

        # Iterate on KeymapItems
        for item in keymap.keymap_items:
            # todo: Only keyboard items now
            if item.map_type != 'KEYBOARD':
                continue
            if (not item.active) and (item.value != "PRESS"):
                continue
            if item.type == 'NONE':
                continue

            shortcut = util.keymapitem_to_shortcut(context, item)
            context.add_shortcut(shortcut)

    return app


def export():
    # Verbosity setting on log
    log.setLevel(logging.INFO)
    #log.setLevel(logging.DEBUG)

    # Get Blender platform and version
    import platform
    version = bpy.app.version_string
    platform = platform.system().lower()
    if platform == 'darwin':
        platform = 'mac'

    app = parse_main_keyconfig()
    app.version = 'v' + bpy.app.version_string.split(' ')[0]

    outputdir = shmaplib.DIR_PAGES_APPDATA
    outputfile = os.path.join(outputdir, 'blender_%s_%s.json' % (app.version, platform))

    app.serialize(outputfile)


try:
    export()
except:
    import traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb = traceback.format_exception(exc_type, exc_value, exc_traceback)
    tb_str = ''.join(tb)
    log.fatal('Unexpected Exception: \n%s', tb_str)
finally:
    exit()
