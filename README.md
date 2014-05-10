ShortcutMapper
==================

This is a keyboard shortcuts visualiser hosted on Github: http://waldobronchart.github.io/ShortcutMapper/

# Overview

This project consists of two things:
- The web application under the **gh-pages** branch.
- Exporters in the **master** branch. These are scripts that create a .json file containing all application shortcuts in a specific format.

Directories in **master**:
```
/exporters       Per application scripts that export a .json file containing all shortcuts
/shmaplib        Python utility library (Shortcut Mapper Lib) to help exporting shortcuts to the webapp.
/tests           Python tests to ensure nothings broken
/gh-pages        Git submodule into the *gh-pages* branch containing the web application.
```

# Contributing

## Cloning & Forking

Forking is probably a bit awkward at the moment because of the git submodule to the gh-pages branch. Just keep in mind that you'll need to change the git url of the submodule to your own fork (.gitmodules file).

```
cd Workspace/
git clone https://github.com/waldobronchart/ShortcutMapper ShortcutMapper
cd ShortcutMapper/
git submodule init
git submodule update
```

## Running locally

The web application is located in the **gh-pages** branch, but it is accessible from the **master** branch as a submodule. The application uses ajax calls to load keyboards and application data. These ajax calls will fail using the file:// protocol, so you need to set your browser to allow this.

For chrome, use this: http://stackoverflow.com/a/21413534

Once that's done, just open the **index.html** in your browser.

## Exporting new updated shortcuts

The exporter scripts all use Python2.7 and some additional libraries. I recommend you use [virtualenv](http://virtualenv.readthedocs.org/en/latest/) like so:

```
# Install virtualenv
pip install virtualenv

# Create a virtual environment in venv directory
cd ShortcutMapper/
virtualenv -p /usr/bin/python2.7 venv

# Activate environment
source venv/bin/activate
pip install BeautifulSoup4

# Do an export
python exporters/photoshop/scripts/convert.py -a
```

Once your virtualenv in installed, all you need to do is activate it before you run the exporters

```
source venv/bin/activate
python exporters/photoshop/scripts/convert.py -a
```









