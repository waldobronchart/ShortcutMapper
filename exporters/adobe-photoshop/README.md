Adobe Photoshop
==================================

### /intermediate

Contains .json data files that were generated from shortcuts scraped from sources in **/raw**

Once exported, the file was hand-edited to make some nessesary fixes that just couldn't be automated.

### /raw

Per photoshop version, there should be 3 raw files:
- photoshop_vXX.X_docs.html: grabbed from http://helpx.adobe.com/en/photoshop/using/default-keyboard-shortcuts.html and isolated the div container wrapping all the relevant data
- photoshop_vXX.X_summary_mac.html: exported html file from Photoshop's edit shortcuts dialog (The "Summarize..." button)
- photoshop_vXX.X_summary_win.html: same as previous but for windows

Shortcuts from these 3 files will then be scraped for shortcuts and exported to an intermediate data format in **/intermediate**

### /scripts

Contains python scripts to:
- create intermediate .json files (You will probably only do this once, and then hand edit the intermediate file)
- export intermediate files to the web application

