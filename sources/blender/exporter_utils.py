import sys
import os
import bpy

# Import common shortcut mapper library
CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(CWD, '..', '..')))
import shmaplib
log = shmaplib.getlog()


KEYMAPS_IGNORE = [
    "File Browser Buttons",
]

KEYMAP_NAME_OVERRIDES = {
    "3D View Generic": "3D View",
    "Object Mode": "3D View",
    "Mesh": "3D View: Mesh",
    "Curve": "3D View: Curve",
    "Armature": "3D View: Armature",
    "Metaball": "3D View: Metaball",
    "Lattice": "3D View: Lattice",
    "Font": "3D View: Font",
    "Pose": "3D View: Pose",
    "Vertex Paint": "3D View: Vertex Paint",
    "Weight Paint": "3D View: Weight Paint",
    "Weight Paint Vertex Selection": "3D View: Weight Paint",
    "Face Mask": "3D View: Face Mask",
    "Image Paint": "3D View: Image Paint",
    "Sculpt": "3D View: Sculpt",
    "Armature Sketch": "3D View: Armature Sketch",
    "Particle": "3D View: Particle",
    "Knife Tool Modal Map": "3D View: Knife Tool Modal Map",
    "Paint Stroke Modal": "3D View: Paint Stroke Modal",
    "Object Non-modal": "3D View",

    "Text Generic": "Text",
    "Node Generic": "Node Editor",
    "Image Generic": "Image",
    "Graph Editor Generic": "Graph Editor",
    "NLA Generic": "NLA Editor",
    "SequencerCommon": "Sequencer",
    "File Browser Main": "File Browser",

    "Gesture Straight Line": "Extra: Gesture Straight Line",
    "Gesture Zoom Border": "Extra: Gesture Zoom Border",
    "Gesture Border": "Extra: Gesture Border",
    "Standard Modal Map": "Extra: Standard Modal Map",
    "Transform Modal": "Extra: Transform Modal",
    "View3D Gesture Circle": "Extra: View3D Gesture Circle",
    "View3D Fly Modal": "Extra: View3D Fly Modal",
    "View3D Rotate Modal": "Extra: View3D Rotate Modal",
    "View3D Move Modal": "Extra: View3D Move Modal",
    "View3D Zoom Modal": "Extra: View3D Zoom Modal",
    "View3D Dolly Modal": "Extra: View3D Dolly Modal",
}



def get_keymap_item_mods(keymap_item):
    mods = []
    if keymap_item.shift:
        mods.append('SHIFT')
    if keymap_item.ctrl:
        mods.append('CTRL')
    if keymap_item.oskey: #yes, oskey is command not "windows key"
        mods.append('COMMAND')
    if keymap_item.alt:
        mods.append('ALT')
    return mods

def enum_value_to_name(enum, val):
    for enum_val in enum:
        if enum_val.value == val:
            return enum_val.name
    return "UNDEFINED"

def enum_value_to_id(enum, val):
    for enum_val in enum:
        if enum_val.value == val:
            return enum_val.identifier
    return "UNDEFINED"








def override_deselectall(shortcut_context, item):
    """name_overrides = {
        "action-0": "Toggle Select All",
        "action-1": "Select All",
        "action-2": "Deselect All",
        "action-3": "Invert Selection",
        "invert-0": "Toggle Select All",
        "invert-1": "Invert Selection"
    }
    key = ''.join(["%s-%s," % (propKey, item.properties.get(propKey)) for propKey in item.properties.keys()]).strip(',')
    log.warn(item.value)
    log.warn(item.value)
    log.warn(item.properties.keys())
    name = name_overrides[key]"""

    name = "Toggle Select All"
    mods = get_keymap_item_mods(item)
    return shmaplib.Shortcut(name, item.type, mods, item.any)

def override_setobjectmode(shortcut_context, item):
    name_overrides = {
        "mode-1,toggle-1": "Toggle Object/Edit Mode",
        "mode-4,toggle-1": "Toggle Vertex Paint Mode",
        "mode-8,toggle-1": "Toggle Weight Paint Mode",
        "mode-64,toggle-1": "Toggle Pose Mode"
    }
    key = ''.join(["%s-%s," % (propKey, item.properties.get(propKey)) for propKey in item.properties.keys()]).strip(',')
    name = name_overrides[key]

    mods = get_keymap_item_mods(item)
    return shmaplib.Shortcut(name, item.type, mods, item.any)

def override_callmenu(shortcut_context, item):
    name = item.properties.get("name").split('_MT_')[1]
    name = name.replace('_', " ")
    name = name.title() + " Menu"

    mods = get_keymap_item_mods(item)
    return shmaplib.Shortcut(name, item.type, mods, item.any)

def override_layers(shortcut_context, item):
    mods = get_keymap_item_mods(item)
    nr = item.properties.get("nr")
    if nr == 0:
        return shmaplib.Shortcut("Toggle All Layers", item.type, mods, item.any)

    # Add missing ALT shortcuts
    shortcut = shmaplib.Shortcut("Switch To Layer %s" % (nr+10), item.type, ['ALT'])
    shortcut_context.add_shortcut(shortcut)

    # Add missing SHIFT shortcuts
    shortcut = shmaplib.Shortcut("Toggle Layer %s" % (nr), item.type, ['SHIFT'])
    shortcut_context.add_shortcut(shortcut)
    shortcut = shmaplib.Shortcut("Toggle Layer %s" % (nr+10), item.type, ['SHIFT', 'ALT'])
    shortcut_context.add_shortcut(shortcut)

    # Default shortcut
    return shmaplib.Shortcut("Switch To Layer %s" % (nr), item.type, [])

def override_subdivisionset(shortcut_context, item):
    name = "Set Subdivision Level To %s" % item.properties.get("level")
    mods = get_keymap_item_mods(item)
    return shmaplib.Shortcut(name, item.type, mods, item.any)

def override_radialcontrol(shortcut_context, item):
    data_path_primary = item.properties.get("data_path_primary").rsplit('.', 1)[1].capitalize()
    name = "Brush %s" % data_path_primary
    mods = get_keymap_item_mods(item)
    return shmaplib.Shortcut(name, item.type, mods, item.any)

def override_setbrushnumber(shortcut_context, item):
    name = "Brush %s" % item.properties.get("index")
    mods = get_keymap_item_mods(item)
    return shmaplib.Shortcut(name, item.type, mods, item.any)

def override_context_toggle(shortcut_context, item):
    context = item.properties.get("data_path").rsplit('.', 1)[1].replace('_', ' ').title()
    name = "Toggle %s" % context
    mods = get_keymap_item_mods(item)
    return shmaplib.Shortcut(name, item.type, mods, item.any)

def override_context_toggle_values(shortcut_context, item):
    context = item.properties.get("data_path").rsplit('.', 1)[1].replace('_', ' ').title()
    value1 = item.properties.get("value_1")
    value2 = item.properties.get("value_2")
    if len(value1) and len(value2):
        if value1 == "DISABLED":
            name =  "Toggle %s" % context
        else:
            name = "%s %s/%s" % (context, value1, value2)
    else:
        name = "Toggle %s" % context

    mods = get_keymap_item_mods(item)
    return shmaplib.Shortcut(name, item.type, mods, item.any)

def override_context_set(shortcut_context, item):
    context = item.properties.get("data_path").rsplit('.', 1)[1].replace('_', ' ').title()
    name =  "Set %s %s" % (context, item.properties.get("value"))
    mods = get_keymap_item_mods(item)
    return shmaplib.Shortcut(name, item.type, mods, item.any)

def override_context_set_enum(shortcut_context, item):
    context = item.properties.get("data_path")
    if context.startswith("area"):
        name = item.properties.get("value").replace('_', ' ').title()
    elif context.startswith("space_data.pivot"):
        name = "Set Pivot: %s" % item.properties.get("value").replace('_', ' ').title()

    mods = get_keymap_item_mods(item)
    return shmaplib.Shortcut(name, item.type, mods, item.any)

def override_context_enum_menu(shortcut_context, item):
    context = item.properties.get("data_path").rsplit('.', 1)[1].replace('_', ' ').title()
    name = "%s Menu" % context
    mods = get_keymap_item_mods(item)
    return shmaplib.Shortcut(name, item.type, mods, item.any)

def override_context_type_cycle(shortcut_context, item):
    context = item.properties.get("data_path").rsplit('.', 1)[1].replace('_', ' ').title()
    name = "Cycle %s" % context
    mods = get_keymap_item_mods(item)
    return shmaplib.Shortcut(name, item.type, mods, item.any)

def override_brush_select(shortcut_context, item):
    paint_mode_val = item.properties.get("paint_mode")
    paint_mode_enum = bpy.types.PAINT_OT_brush_select.bl_rna.properties['paint_mode'].enum_items
    paint_mode_identifier = enum_value_to_id(paint_mode_enum, paint_mode_val).lower()
    tool_name = paint_mode_identifier + "_tool"
    brush_val = item.properties.get(tool_name)
    brush_enum = bpy.types.PAINT_OT_brush_select.bl_rna.properties[tool_name].enum_items
    brush_name = enum_value_to_name(brush_enum, brush_val)
    if item.properties.get("toggle"):
        name =  "Toggle %s Brush" % brush_name
    else:
        name = "%s Brush" % brush_name

    mods = get_keymap_item_mods(item)
    return shmaplib.Shortcut(name, item.type, mods, item.any)


# Override values can be: string, dictionary of property values or a function
KEYMAPITEM_CUSTOM_RULES = {
    "(De)select All": override_deselectall,
    "Set Object Mode": override_setobjectmode,
    "Call Menu": override_callmenu,
    "Layers": override_layers,
    "Subdivision Set": override_subdivisionset,
    "Radial Control": override_radialcontrol,
    "Set Brush Number": override_setbrushnumber,
    "Context Toggle": override_context_toggle,
    "Context Toggle Values": override_context_toggle_values,
    "Context Set": override_context_set,
    "Context Set Enum": override_context_set_enum,
    "Context Enum Menu": override_context_enum_menu,
    "Context Enum Cycle": override_context_type_cycle,
    "Context Int Cycle": override_context_type_cycle,
    "Brush Select": override_brush_select,
}







def keymapitem_to_shortcut(shortcut_context, keymap_item):
    name = keymap_item.name
    if len(name) == 0:
        name = keymap_item.idname
    if len(name) == 0:
        name = keymap_item.propvalue

    #log.debug('parsing keymap item: %s', name)

    # Apply overrides if needed
    if name in KEYMAPITEM_CUSTOM_RULES.keys():
        override_func = KEYMAPITEM_CUSTOM_RULES[name]
        shortcut = override_func(shortcut_context, keymap_item)
        return shortcut

    # Default behaviour
    mods = get_keymap_item_mods(keymap_item)
    return shmaplib.Shortcut(name, keymap_item.type, mods, keymap_item.any)
















