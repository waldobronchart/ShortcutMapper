
ABSPATH=$(cd "$(dirname "$0")"; pwd)
/Applications/Blender/blender.app/Contents/MacOS/blender -con --python "$ABSPATH/exporter.py"
