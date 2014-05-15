source venv/bin/activate

python exporters/adobe-lightroom/scripts/export.py -a
python exporters/adobe-photoshop/scripts/export.py -a
sh exporters/blender/scripts/export_latest.sh
