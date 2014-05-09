# Why the hell do I need to do this for python3??
import sys
import os
sys.path.append(os.path.dirname(__file__))

from keydata import Shortcut, ShortcutContext, ApplicationConfig
from keynames import get_all_valid_keynames, get_valid_keynames, is_valid_keyname
from logger import getlog, setuplog


# Utility path vars to common directories
DIR_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

DIR_EXPORTERS = os.path.normpath(os.path.join(DIR_ROOT, "exporters"))
DIR_PAGES_APPDATA = os.path.normpath(os.path.join(DIR_ROOT, "gh-pages/appdata"))
DIR_PAGES_KEYBOARDS = os.path.normpath(os.path.join(DIR_ROOT, "gh-pages/keyboards"))
