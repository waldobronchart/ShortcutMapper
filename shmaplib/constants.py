import os

# Utility path vars to common directories
DIR_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

DIR_SOURCES = os.path.normpath(os.path.join(DIR_ROOT, "sources"))
DIR_CONTENT_GENERATED = os.path.normpath(os.path.join(DIR_ROOT, "content", "generated"))
DIR_CONTENT_KEYBOARDS = os.path.normpath(os.path.join(DIR_ROOT, "content", "keyboards"))

CONTENT_APPS_JS_FILE = os.path.normpath(os.path.join(DIR_ROOT, "content", "generated", "apps.js"))

OS_WINDOWS = 'windows'
OS_MAC = 'mac'
OS_LINUX = 'linux'

VALID_OS_NAMES = [OS_WINDOWS, OS_MAC, OS_LINUX]
