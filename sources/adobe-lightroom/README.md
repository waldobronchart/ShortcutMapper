Adobe Lightroom
==================================

### /raw

The raw data was found here:
http://helpx.adobe.com/lightroom/help/keyboard-shortcuts.html

To convert raw to intermediate run the following script:
`python raw_to_intermediate.py -o intermediate/OUTPUT_FILE_NAME.json raw/SOURCE_FILE_NAME`


### /intermediate

Contains .json data files that were generated from shortcuts scraped from sources in **/raw**

Once converted, the files were hand-edited to make some necessary fixes that just couldn't be automated.

To export this intermediate format to the web application run the following script:
`python utils/export_intermediate_data.py sources/adobe-lightroom/intermediate/XXX.json`
