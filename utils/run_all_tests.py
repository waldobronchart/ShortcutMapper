import os
import sys

# Add root dir to PATH env var
CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CWD)
sys.path.insert(0, os.path.normpath(os.path.join(CWD, '..')))

import tests
import shmaplib

shmaplib.setuplog()

if __name__ == '__main__':
    tests.main()
