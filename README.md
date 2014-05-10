ShortcutMapper
==================

This is a keyboard shortcuts visualiser hosted on Github: http://waldobronchart.github.io/ShortcutMapper/

# Overview

This project consists of two things:
- The web application under the branch **gh-pages**
- Exporters in the **master** branch. These are scripts that create a .json file containing all application shortcuts in a specific format.

Directories in **master**:
```
/exporters       Per application scripts that export a .json file containing all shortcuts
/shmaplib        Python utility library (Shortcut Mapper Lib) to help exporting shortcuts to the webapp.
/tests           Python tests to ensure nothings broken
/gh-pages        Git submodule into the *gh-pages* branch containing the web application.

```

# Contributing

## Running locally

The web application is located in the *gh-pages* branch, but it is accessible from the *master* branch as a submodule. The application uses ajax calls to load keyboards and application data. These ajax calls will fail using the file:// protocol, so you need to set your browser to allow this.

For chrome, use this: http://stackoverflow.com/a/21413534

Once that's done, just open the **index.html** in your browser.

## Forking

Forking is probably a bit awkward at the moment because of the git submodule to the gh-pages branch.
