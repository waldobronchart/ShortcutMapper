ShortcutMapper
==================

This is a keyboard shortcuts visualiser hosted on Github: http://waldobronchart.github.io/ShortcutMapper/

# Overview

This project consists of two things:
- The web application under the branch *gh-pages*
- Exporters in the *master* branch. These are scripts that create a .json file containing all application shortcuts in a specific format.

Directories in *master*:
```
/exporters/<application>                Per application scripts that export a .json file containing all shortcuts
/shmaplib/                              Python utility library (Shortcut Mapper Lib) to help exporting shortcuts to the webapp.
/tests/                                 Python tests to ensure nothings broken
/gh-pages/                              A git submodule into the *gh-pages* branch containing the web application.

```

# Contributing

## Repository Setup

The github page is located
