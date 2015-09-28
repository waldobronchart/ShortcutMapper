Adobe Photoshop
==================================

### /raw

Per photoshop version, there should be 3 raw files:
- photoshop_vXX.X_docs.html: grabbed from http://helpx.adobe.com/en/photoshop/using/default-keyboard-shortcuts.html and isolated the div container wrapping all the relevant data
- photoshop_vXX.X_summary_mac.html: exported html file from Photoshop's edit shortcuts dialog (The "Summarize..." button)
- photoshop_vXX.X_summary_win.html: same as previous but for windows

Shortcuts from these 3 files will then be scraped for shortcuts and exported to an intermediate data format in **/intermediate**

To convert raw to intermediate run the following script:
`python raw_to_intermediate.py -o intermediate/OUTPUT_FILE_NAME.json raw/SOURCE_FILE_NAME`

### /intermediate

Contains .json data files that were generated from shortcuts scraped from sources in **/raw**

Once exported, the file was hand-edited to make some necessary fixes that just couldn't be automated.

To export this intermediate format to the web application run the following script:
`python utils/export_intermediate_data.py sources/adobe-photoshop/intermediate/XXX.json`