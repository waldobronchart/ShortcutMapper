# Why the hell do I need to do this for python3??
import sys
import os
sys.path.append(os.path.dirname(__file__))

from appdata import Shortcut, ShortcutContext, ApplicationConfig
from keynames import get_all_valid_keynames, get_valid_keynames, is_valid_keyname
from logger import getlog, setuplog
from adobe import AdobeIntermediateData, AdobeDocsParser, AdobeSummaryParser, AdobeDocsExporter
from constants import DIR_ROOT, DIR_EXPORTERS, DIR_PAGES_APPDATA, DIR_PAGES_KEYBOARDS
