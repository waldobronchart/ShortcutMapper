ShortcutMapper
==================

This is a keyboard shortcuts visualiser hosted on Github: http://waldobronchart.github.io/ShortcutMapper/

![Imgur](http://waldobronchart.github.io/ShortcutMapper/content/images/overview.gif)

# Overview

This project is directly hosted on github from the main **gh-pages** branch. All changes to this branch are live.

```
/content         The website content
    /generated   Contains generated json/js files containing application
                  shortcut data in the site format
    /keyboards   Contains html keyboard layouts
    ...
/sources         Source data for shortcuts per application.
/shmaplib        Python utility library (Shortcut Mapper Lib) to help 
                  exporting shortcuts to the webapp.
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
# Install pip if you don't have it yet
sudo easy_install pip

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

# Export all intermediate json files to content/generated/
python utils/export_intermediate_data.py -a
```


## Adding shortcuts for a new Application

**The best example you can look at is Autodesk Maya under /sources/autodesk-maya**

### Exporters directory setup

First, try and find an online resource that lists all the application shortcuts for each platform. For adobe applications for example, I use the ones from their online documentation: http://helpx.adobe.com/lightroom/help/keyboard-shortcuts.html

Make sure it's up-to-date and the list is complete.

You're going to use that resource to create an intermediate data format that can be edited by hand easily.

Create a directory structure under **/sources** like this:
```
/sources
    /my-app
        /intermediate           One-time conversions from raw data, which have been hand edited to
                                 fix faulty shortcuts and shorten labels that are too long.
        /raw                    Source(s) used to build a full shortcut list in the intermediate data format
```

Then ideally, you're going to write a script that converts the raw source to intermediate: `/sources/my-app/raw_to_intermediate.py`

Past the intermediate data creation step, everything can be automated. Much of the heavy lifting code lives under the `shmaplib` folder.

### Using SHMAPlib

SHMAPlib is short for "Shortcut Mapper Lib". It's a Python library that will help you export data in the right format to the right location.

If your script lives and runs directly in **/sources/app/**, then you can import the lib like so:

```
# Add repository root path to sys.path (This will make import shmaplib work)
CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CWD)
sys.path.insert(0, os.path.normpath(os.path.join(CWD, '..', '..')))

# Import common shortcut mapper library
import shmaplib
```

From there you can parse your raw files (HTML, XML, etc..) and create an intermediate data file which can then be hand edited.

```
import shmaplib

# Create the intermediate data container
idata = shmaplib.IntermediateShortcutData("Application Name")

# Parse the raw file
# ...and add shortcuts to the container like this:
context_name = "Global Context"
label = "Select All"
keys_win = "Ctrl + A"
keys_mac = "Cmd + A"
idata.add_shortcut(context_name, label, keys_win, keys_mac)

# Save out the file
idata.serialize('intermediate/my-application_v3.json')
```

You can then export this intermediate data file after making hand-edits (there are always edge cases to fix).

```
# Export intermediate to the frontend data format
python utils/export_intermediate_data.py sources/application-name/intermediate/SOURCE.json
```

If your application doesn't have an intermediate format (like Blender), you can use these structures to build up the data:
- *shmaplib.ApplicationConfig*: Main application data format (name, os, version, and shortcut-contexts)
- *shmaplib.ShortcutContext*: A container for shortcuts for a specific context (Lightroom: Global, Develop, Library)
- *shmaplib.Shortcut*: Data format for a shortcut (name, key and modifiers)

You'll create an AppConfig first. Then create a new context to the application, to which the shortcuts are added

AppConfig has multiple ShortcutContexts, which has multiple Shortcuts.

The AppConfig has a serialize function that exports it into the correct directory under /content/generated

Look in `shmaplib/appdata.py` for more specific docs.




