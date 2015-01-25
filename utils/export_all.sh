#!/bin/sh

source ../_venv/bin/activate

python ../exporters/adobe-lightroom/scripts/export.py -a
python ../exporters/adobe-photoshop/scripts/export.py -a
python ../exporters/autodesk-maya/scripts/export.py -a
python ../exporters/autodesk-3dsmax/scripts/export.py -a
python ../exporters/sublime-text/scripts/export.py -a
python ../exporters/unity3d/scripts/export.py -a
sh ../exporters/blender/scripts/export_latest.sh
