ShortcutMapper
==================

This is a keyboard shortcuts visualiser hosted here on Github:
http://waldobronchart.github.io/ShortcutMapper/

The goal of this project is to map out application keyboard shortcuts onto a virtual keyboard, making it easy to find and learn new shortcuts. The shortcut data is scraped from online documentation to reduce error and to keep the data easy to update with newer versions.

![Imgur](http://waldobronchart.github.io/ShortcutMapper/content/images/overview.gif)

# Overview

This project is directly hosted on github from the **master** branch. All changes to this branch are live.

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

Before opening pull requests to contribute, you should test your changes locally.

The easiest way to run locally is to run a simple http server:
1. Install http-server via npm: `npm install -g http-server`
2. Run `http-server` in your terminal
  > Starting up http-server, serving ./
  > Available on:
  >   http://127.0.0.1:8080
  >   http://192.168.86.95:8080
  > Hit CTRL-C to stop the server
3. Go to http://127.0.0.1:8080 in your browser

## Exporting new updated shortcuts

The exporter scripts all use Python3 and some additional libraries. I recommend you use [virtualenv](http://virtualenv.readthedocs.org/en/latest/) like so:

```
# Install pip if you don't have it yet
sudo easy_install pip

# Install virtualenv
pip install virtualenv

# Create a virtual environment in ShortcutMapper/_venv directory
# For Windows, look here for instructions: 
# http://virtualenv.readthedocs.io/en/latest/userguide/#usage
cd ShortcutMapper/
virtualenv -p /usr/bin/python3 _venv

# Activate environment
source _venv/bin/activate
pip install BeautifulSoup4

# Do an export
python exporters/adobe-photoshop/scripts/export.py -a
```

Once your virtualenv in installed, all you need to do is activate it before you run the exporters

```
source _venv/bin/activate

# For windows, you will do this instead
_venv\Source\activate.bat

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


## Pull Requests Flow

I follow the git-flow process to get new features and bugfixes in. You can read about it here:
https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

Basically you'll create a branch like `feature/descriptive-feature-name` from the `master` branch and start working in that. Once you're done, you'll create a pull request that merges into the `dev` branch.
This allows me to test your changes before it is published to the `master` branch.

For bug fixes, you'll name your branch `fix/descriptive-bug-name`.

### Expected contents for new keyboards

Ideally both windows and mac keyboards, created from other existing layouts (Klingon for example):
- content/keyboards/klingon.html
- content/keyboards/klingon_mac.html

These files added to the keyboard list in `content/keyboards/keyboards.js`
```
var sitedata_keyboards = {
    ...
    "Klingon": {
        mac: "klingon_mac.html",
        windows: "klingon.html",
        linux: "klingon.html",
    }
}
```

Make sure to run all tests in the `/tests` folder to ensure all keycodes are valid.

### Expected contents for new applications

Please make sure to read the "Adding shortcuts for a new Application" section above.
It is good practice to keep your commits small and structured so it's easy to review.

First I find a raw source and write a scraper script to generate the intermediate file (Example: https://github.com/waldobronchart/ShortcutMapper/commit/76f7b2f6c895bebebd5a5948c3bc759ac7779189)
-  sources/thefoundry-nuke/raw/nuke_8.0_user_guide_hotkeys.html
-  sources/thefoundry-nuke/raw_to_intermediate_nuke8.py

Generate the intermediate file with the `raw_to_intermediate` script (Example: https://github.com/waldobronchart/ShortcutMapper/commit/f1db1aa3268e0a82b5394d7e1c26335153872cb5)
- sources/thefoundry-nuke/intermediate/thefoundry_nuke_8.0.json

Make some needed hand edits to the intermediate files, like better grouping in contexts and fixing some long names. It's good to have the original untouched one in first, so that you can track your changes more easily (Example: https://github.com/waldobronchart/ShortcutMapper/commit/767556431a983481abd7cc0a30f1878cceef5fe9)
- sources/thefoundry-nuke/intermediate/thefoundry_nuke_8.0.json

Keep re-generating the app content (with `/utils/export_intermediate_data`) until you're happy with the changes. Note to fix the warnings during the export process.

When you're happy with all the changes, commit the generated data (Example: https://github.com/waldobronchart/ShortcutMapper/commit/5533cdf94e9cab5564b9a946f528638cea6420f3)
- content/generated/apps.js (app was added here)
- content/generated/the-foundry-nuke_8.0_mac.json
- content/generated/the-foundry-nuke_8.0_windows.json

Then create a new pull request into the `develop` branch.
