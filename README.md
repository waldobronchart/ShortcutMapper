ShortcutMapper
==================

This is a keyboard shortcuts visualiser hosted on Github: http://waldobronchart.github.io/ShortcutMapper/

![Imgur](http://waldobronchart.github.io/ShortcutMapper/content/images/overview.gif)

# Overview

This project is directly hosted on github from the main **gh-pages** branch. All changes to this branch are live.

```
/content         The website content
    /appdata         Contains exported .json files containing all application shortccuts
    /keyboards       Contains html keyboard layouts
    ...
/exporters       Per application scripts that export a .json file containing all shortcuts to 'content/appdata'
/shmaplib        Python utility library (Shortcut Mapper Lib) to help exporting shortcuts to the webapp.
/tests           Python tests to ensure nothing is broken
/utils           Utilities for exporting and testing 
index.html       Main site page
```

# Contributing

## Running locally

The only page of the website is **index.html**

The application uses ajax calls to load keyboards and application data. These ajax calls will fail using the file:// protocol, so you need to set your browser to allow this. Here's how to enable that for Chrome: http://stackoverflow.com/a/21413534

Once that's done, just open the **index.html** in your browser and you're off!

## Exporting new updated shortcuts

The exporter scripts all use Python2.7 and some additional libraries. I recommend you use [virtualenv](http://virtualenv.readthedocs.org/en/latest/) like so:

```
# Install virtualenv
pip install virtualenv

# Create a virtual environment in ShortcutMapper/_venv directory
cd ShortcutMapper/
virtualenv -p /usr/bin/python2.7 _venv

# Activate environment
source _venv/bin/activate
pip install BeautifulSoup4

# Do an export
python exporters/adobe-photoshop/scripts/export.py -a
```

Once your virtualenv in installed, all you need to do is activate it before you run the exporters

```
source _venv/bin/activate
python exporters/adobe-photoshop/scripts/export.py -a
```









