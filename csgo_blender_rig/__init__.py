bl_info = {
    "name": "CSGO_RIG",
    "author": "Mpsterprod",
    "version": (1, 0),
    "blender": (2, 81, 0),
    "location": "View3D > Panel",
    "description": "Rigs for CSGO models",
    "warning": "",
    "wiki_url": "https://github.com/mpsterprod",
    "category": "Animation"
}

import bpy
from bpy.types import (
    AddonPreferences,
    PropertyGroup,
    Operator
)
from bpy.props import (
    BoolProperty,
    #EnumProperty,
    PointerProperty
)
from bpy.utils import register_class, unregister_class

#####################################################################
####################### Blender Source Tool #########################
#####################################################################
BLENDER_SOURCE_TOOL_IMPORT_SCENE_OPEAROR = 'smd'

def check_smd_operator():
    good = False
    for i in dir(bpy.ops.import_scene):
        if i == BLENDER_SOURCE_TOOL_IMPORT_SCENE_OPEAROR:
            good = True
            break
    return good

######################################################################


class MP_TOOL_Addon_Preferences_Property(PropertyGroup):
    mptool_csgo_panel_vis : BoolProperty(
        name='CSGO Panel Visibility',
        default=True,
    )

    mptool_csgo_rig_panel_vis : BoolProperty(
        name='CSGO Rig Panel Visibility',
        default=True
    )


class MP_TOOL_Addon_Preferences_Panel(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        if not check_smd_operator():
            layout = self.layout
            col = layout.column()
            bx = col.box()
            bx.scale_x = bx.scale_y = 1.4
            bx.label(text='NOT Install or Enabled "Blender Source Tool" <-- Addon!')
            bx.label(text='"Blender Source Tool": " https://developer.valvesoftware.com/wiki/Blender_Source_Tools "',icon='URL')
            bx.operator(operator=URL_OP_Open_Site.bl_idname, text='Open "Blender Source Tool" download site!', icon='URL')

            bx = col.box()
            bx.label(text='Please Enabled and REENABLED --> "CSGO_RIG" <-- Addon!')
        else:
            layout = self.layout
            props = context.scene.mp_csgo_addons_prefs

            layout.label(text='CSGO Rigs/Animations')
            bx = layout.box()

            col = bx.column()
            col.label(text='CSGO Rigging Generator Panel')
            col.prop(props, 'mptool_csgo_panel_vis')

            col.label(text='Animation Rig Panel for Character/Pov')
            col.prop(props, 'mptool_csgo_rig_panel_vis')

class URL_OP_Open_Site(Operator):
    bl_label = 'Open Url in Browser'
    bl_idname = 'object.mpcsgo_open_blender_source_download_site'
    bl_options = {'UNDO'}

    def execute(self, context):
        return {'FINISHED'}
            
# self classes
init_classes = [
    URL_OP_Open_Site,

    MP_TOOL_Addon_Preferences_Property,
    MP_TOOL_Addon_Preferences_Panel,
]

from . import (
    PT_Character,
    PT_Weapons,
    PT_Pov,
    PT_Props,

    # rig panels
    RIG_PANEL_Character,
    RIG_PANEL_POV
)

init_modules = [
    PT_Character,
    PT_Weapons,
    PT_Pov,
    PT_Props,

    RIG_PANEL_Character,
    RIG_PANEL_POV
]

def register():
    if not check_smd_operator():
        # register message in preferences
        try:
            unregister_class(MP_TOOL_Addon_Preferences_Panel)
        except: pass
        register_class(MP_TOOL_Addon_Preferences_Panel)
        return
    try:
        unregister_class(MP_TOOL_Addon_Preferences_Panel)
    except: pass
    ################
    # ADDON
    ################

    # register all
    for cls in init_classes:
        register_class(cls)
    
    # init point
    bpy.types.Scene.mp_csgo_addons_prefs = PointerProperty(type=MP_TOOL_Addon_Preferences_Property)

    ################
    # MODULES
    ################

    # register modules and points
    for module in init_modules:
        module.register_classes()
        module.register_point()

    
def unregister():
    ################
    # MODULES
    ################
    try:
        # unregister modules and points
        for module in reversed(init_modules):
            module.unregister_point()
            module.unregister_classes()

    except: pass
        
    ################
    # ADDON
    ################
    try:
        # remove point
        bpy.types.Scene.mp_csgo_addons_prefs = None
        del bpy.types.Scene.mp_csgo_addons_prefs

        # unregister all
        for cls in reversed(init_classes):
            unregister_class(cls)

    except: pass

if __name__ == '__main__':
    unregister()
    register()
