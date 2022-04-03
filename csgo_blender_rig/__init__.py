bl_info = {
    "name": "CSGO_RIG",
    "author": "Mpsterprod",
    "version": (1, 0),
    "blender": (2, 81, 0),
    "location": "View3D > Panel",
    "description": "Rigs for CSGO models",
    "warning": "",
    "wiki_url": "https://github.com/mpsterprod",
    "category": "Import-Export"
}

import math
import os


import bpy
from bpy.types import (
    Operator,
    Panel,
    PropertyGroup
)
from bpy.props import (
    StringProperty,
    BoolProperty,
    PointerProperty
)

from bpy.utils import register_class, unregister_class
from . import Rig_Connector


# OPERATOR
class CSGO_OP_SeriesCharacter_Rigging(Operator):
    bl_label = "CSGO_OP_SeriesCharacter_Rigging"
    bl_idname = "object.build_series_csgo_character_rig"
    bl_space_type = "VIEW_3D"

    # inputs
    op_prop_PLAYER_FOLDER = None
    op_prop_EXPORT_FOLDER = None

    op_prop_CUSTOM_RIG = None

    op_prop_CUSTOM_RIG_BLEND = None
    op_prop_COLLECTION = None
    op_prop_CUSTOM_CONNECTIONS = None


    def structure(self):
        props = bpy.context.scene.csgo_rigger_character
        self.op_prop_PLAYER_FOLDER = props.prop_import_folder
        self.op_prop_EXPORT_FOLDER = props.prop_export_folder

        self.op_prop_CUSTOM_RIG = props.prop_use_custom_rig

        self.op_prop_CUSTOM_RIG_BLEND = props.prop_custom_rig_blend
        self.op_prop_COLLECTION = props.prop_custom_collection_import
        self.op_prop_CUSTOM_CONNECTIONS = props.prop_custom_connections_file


    def execute(self, context):
        self.structure()
        print('-----> rigging start...')
        # input
        #PLAYERS_FOLDER = 'D:/DarkAssembler/Edits/Shadows/Content/csgo content/smd/models/player/custom_player/legacy'
        #EXPORT_FOLDER = 'D:/DarkAssembler/Edits/Shadows/scripts/csgo rig/csgo_blender_rig/export csgo players'
        PLAYERS_FOLDER = self.op_prop_PLAYER_FOLDER
        EXPORT_FOLDER = self.op_prop_EXPORT_FOLDER
        print(PLAYERS_FOLDER)
        print(EXPORT_FOLDER)
        print('read done')

        if PLAYERS_FOLDER == '' or PLAYERS_FOLDER == None:
            return {'FINISHED'}
        if EXPORT_FOLDER == '' or EXPORT_FOLDER == None:
            return {'FINISHED'}

        USED_CUSTOM_RIG = self.op_prop_CUSTOM_RIG

        CUSTOM_RIG_BLEND = self.op_prop_CUSTOM_RIG_BLEND
        CUSTOM_IMPORT_COLLECTION_NAME = self.op_prop_COLLECTION

        CUSTOM_CONNECTIONS_FILE = self.op_prop_CUSTOM_CONNECTIONS

        #CONST BY VERSION
        RIG_BLEND_FILE = 'mp_csgo_character_rig.blend'
        RIG_COLLECTION_IMPORT = 'CSGO_RIG'
        CONNECTION_FILE = 'mp_csgo_character_rig.connections'
        RIG_FOLDER = __file__.replace(os.path.basename(__file__), "")+'/rigs/'


        #CHARACTERS_QC = []

        # get files
        for player in next(os.walk(PLAYERS_FOLDER))[1]:
            # CHARACTER
            character_folder = PLAYERS_FOLDER + '/'+player
            # Clear BPY.DATA
            self.delete_from_bpy()

            if len(bpy.data.scenes) != 1:
                for i, s in bpy.data.scenes.items():
                    bpy.data.scenes.remove(s)

            scene = bpy.data.scenes[0]


            character_name = ''
            qc_file = ''

            # import smd
            for f in next(os.walk(PLAYERS_FOLDER+'/'+player))[2]:
                # this files in folder `player`
                if f[len(f)-3:] == '.qc':
                    character_name = f.replace('.qc','')
                    qc_file = character_folder + '/' + f
                if f[len(f)-4:] == '.smd':
                    bpy.ops.import_scene.smd(
                        filepath = character_folder+'/'+str(f),
                        doAnim = False,
                        createCollections=False,
                        makeCamera=False,
                        append='APPEND',
                        upAxis='Y',
                        rotMode='XYZ',
                        boneMode='NONE'
                    )
            if character_name == '':
                continue

            # rename scene
            scene.name = character_name

            # set 0.01 scale and freeze
            for name, obj, in scene.objects.items():
                if scene.objects[name].type == 'ARMATURE':
                    # set scale
                    scene.objects[name].scale = (0.01, 0.01, 0.01)
                    # set active object
                    self.select(scene, False)
                    scene.objects[name].select_set(True)
                    # frezee
                    bpy.ops.object.transform_apply()

                    scene.objects[name].select_set(False)
                    # extra
                    for i, a in bpy.data.armatures.items():
                        bpy.data.armatures[i].name = 'root'
                    # rename skeleton
                    scene.objects[name].name = 'root'
                    break

            # create collections
            rig_collections = [
                character_name,
                'Skeleton',
                'Mesh',
                #'Rig'
            ]
            # Create
            for coll in rig_collections:
                bpy.ops.collection.create(name=coll)
            # link Master Collection to scene Collections
            scene.collection.children.link(bpy.data.collections[rig_collections[0]])
            # parenting collections
            for name, collectinos in bpy.data.collections.items():
                if name != rig_collections[0]:
                    bpy.data.collections[rig_collections[0]].children.link(bpy.data.collections[name])

            # parenting objects
            for i, v in scene.objects.items():
                if v.type == 'MESH':
                    # set frezee
                    v.select_set(True)
                    bpy.ops.object.transform_apply()
                    v.select_set(False)
                   
                    bpy.data.collections[rig_collections[2]].objects.link(scene.objects[i])
                    scene.collection.objects.unlink(scene.objects[i])

            for i, v in scene.objects.items():
                if v.type == 'ARMATURE':
                    bpy.data.collections[rig_collections[1]].objects.link(scene.objects[i])
                    scene.collection.objects.unlink(scene.objects[i])

            # import rig
            #auto_blender_csgo_rig.build_rig("my_csgo_rig", rig_collections[0], 'root')
            #bpy.ops.view3d.toggle_xray()

            if USED_CUSTOM_RIG:
                bpy.ops.wm.append(
                    filepath=CUSTOM_RIG_BLEND,
                    directory=CUSTOM_RIG_BLEND+'/Collection/',
                    filename=CUSTOM_IMPORT_COLLECTION_NAME,
                    autoselect=False,
                    active_collection=False,
                    instance_collections=False,
                    instance_object_data=False,
                    set_fake=False,
                    use_recursive=False
                )
            else:
                bpy.ops.wm.append(
                    filepath=RIG_FOLDER+RIG_BLEND_FILE,
                    directory=RIG_FOLDER+RIG_BLEND_FILE+'/Collection/',
                    filename=RIG_COLLECTION_IMPORT,
                    autoselect=False,
                    active_collection=False,
                    instance_collections=False,
                    instance_object_data=False,
                    set_fake=False,
                    use_recursive=False
                )

            for name, collectinos in bpy.data.collections.items():
                if name == RIG_COLLECTION_IMPORT:
                    # link to character collection
                    bpy.data.collections[rig_collections[0]].children.link(bpy.data.collections[name])
                    # unlink from scene and `Appended Data`
                    for n, c in bpy.data.collections['Appended Data'].children.items():
                        bpy.data.collections['Appended Data'].children.unlink(bpy.data.collections[n])
                    # remove this collection
                    bpy.data.collections.remove(bpy.data.collections['Appended Data'])
                    break


            # create folder
            self.create_folder(EXPORT_FOLDER+'/'+character_name+'/')

            self.select(scene, False)

            # export SkeletalMesh .FBX - потому что полевектор может изменить позу(
            for name, obj in bpy.data.objects.items():
                if obj.type == 'MESH':
                    obj.select_set(True)
            
            bpy.data.objects['root'].select_set(True)

            print('EXPORT_PATH=  ', EXPORT_FOLDER+'/'+character_name+'/'+'SkeletalMesh_'+character_name+'.fbx')

            bpy.ops.export_scene.fbx(
                filepath=EXPORT_FOLDER+'/'+character_name+'/'+'SkeletalMesh_'+character_name+'.fbx',
                bake_anim=False,
                use_selection=True
            )

            self.select(scene, False)

            # connect skeleton to rig
            if USED_CUSTOM_RIG:
                Rig_Connector.Import_Connection_Dict(CUSTOM_CONNECTIONS_FILE)
            else:
                Rig_Connector.Import_Connection_Dict(RIG_FOLDER+CONNECTION_FILE)


            # add pole vector
            bpy.data.objects['my_csgo_rig'].pose.bones['L_Lower_IK'].constraints[0].pole_target = bpy.data.objects['my_csgo_rig']
            bpy.data.objects['my_csgo_rig'].pose.bones['L_Lower_IK'].constraints[0].pole_subtarget = 'L_ARM_POLEVECTOR'

            bpy.data.objects['my_csgo_rig'].pose.bones['R_Lower_IK'].constraints[0].pole_target = bpy.data.objects['my_csgo_rig']
            bpy.data.objects['my_csgo_rig'].pose.bones['R_Lower_IK'].constraints[0].pole_subtarget = 'R_ARM_POLEVECTOR'


            bpy.data.objects['my_csgo_rig'].pose.bones['L_leg_lower_IK'].constraints[0].pole_target = bpy.data.objects['my_csgo_rig']
            bpy.data.objects['my_csgo_rig'].pose.bones['L_leg_lower_IK'].constraints[0].pole_subtarget = 'L_LEG_POLEVECTOR'

            bpy.data.objects['my_csgo_rig'].pose.bones['R_leg_lower_IK'].constraints[0].pole_target = bpy.data.objects['my_csgo_rig']
            bpy.data.objects['my_csgo_rig'].pose.bones['R_leg_lower_IK'].constraints[0].pole_subtarget = 'R_LEG_POLEVECTOR'
                    
            for iname in ['L_Lower_IK', 'R_Lower_IK', 'L_leg_lower_IK', 'R_leg_lower_IK']:
                # set -90
                bpy.data.objects['my_csgo_rig'].pose.bones[iname].constraints[0].pole_angle = -(math.pi/2)

            # set visibility
            bpy.data.objects['root'].hide_viewport = True

            # export Rig Blender Project .BLEND
            bpy.ops.wm.save_as_mainfile(
                filepath=EXPORT_FOLDER+'/'+character_name+'/'+'Rig_'+character_name+'.blend'
            )
        
            break
    
        self.delete_from_bpy()
        print('------> Rigging done!')

        
        return {'FINISHED'}


    def select(self, scene, value):
        for i, x in scene.objects.items():
            scene.objects[i].select_set(value)
        
    
    def delete_from_bpy(self):
        # delete `COLLECTIONS`, `MESH`, `ARMATURES`, `CAMERA`, `LIGHT`, `MATERIAL`
        for data in [
            bpy.data.meshes,
            bpy.data.armatures,
            bpy.data.cameras,
            bpy.data.lights,
            bpy.data.objects,
            bpy.data.materials,
            bpy.data.collections
        ]:
            if data.items() == []: 
                continue
            for i, point in data.items():
                data.remove(point)

    def create_folder(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory


class CSGO_OP_SeriesWeapon_Riging(Operator):
    pass

class CSGO_OP_SeriesPov_Rigging(Operator):
    pass




# PROPERTY
class SeriesCharacter_PROP(PropertyGroup):
    prop_import_folder : StringProperty(
        subtype="FILE_PATH",
        name='Players .SMD Folder',
        default=''
    )
    prop_export_folder : StringProperty(
        subtype="FILE_PATH",
        name='Export Folder',
        default=''
    )

    prop_use_custom_rig : BoolProperty(
        name='Use Custom Rig',
        default=False
    )

    prop_custom_rig_blend : StringProperty(
        subtype="FILE_PATH",
        name='Custom Rig .blend',
        default=''
    )
    prop_custom_collection_import : StringProperty(
        name='Collection from Rig File',
        default=''
    )
    prop_custom_connections_file : StringProperty(
        subtype="FILE_PATH",
        name='Custom Connections Script',
        default=''
    )



class SeriesWeapon_PROP(PropertyGroup):
    pass

class SeriesPov_PROP(PropertyGroup):
    pass


# PANEL
class CSGO_PT_Character_Panel(Panel):
    bl_label = 'CSGO Character'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CSGO'

    def draw(self, context):
        layout = self.layout
        props = context.scene.csgo_rigger_character
        # input
        col_global = layout.column()
        col_global.prop(props, "prop_import_folder")
        col_global.prop(props, "prop_export_folder")
        col_global.label(text='Custom Rig')
        col_global.prop(props, 'prop_use_custom_rig')
        bx = col_global.box()
        bx.active = False
        # custom input
        bx.prop(props, 'prop_custom_rig_blend')
        bx.prop(props, 'prop_custom_collection_import')
        bx.prop(props, 'prop_custom_connections_file')

        # set operator
        col_global.operator(operator='object.build_series_csgo_character_rig', text='Start Rigging')




class CSGO_PT_Weapon_Panel(Panel):
    bl_label = 'CSGO Weapons'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CSGO'

class CSGO_PT_Pov_Panel(Panel):
    bl_label = 'CSGO Pov'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CSGO'

class CSGO_PT_Props_Panel(Panel):
    bl_label = 'CSGO Custom'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CSGO'



register_props = [
    SeriesCharacter_PROP
]

register_operator = [
    CSGO_OP_SeriesCharacter_Rigging#,
    #CSGO_OP_SeriesWeapon_Riging,
    #CSGO_OP_SeriesPov_Rigging,

    # panel
    #CSGO_PT_Addon_Panel
]

register_panel = [
    CSGO_PT_Character_Panel
]

def register():
    for cls in register_props, register_operator, register_panel:
        for i in cls:
            register_class(i)
    print('\n\n\n\nregister done\n\n\n\n')
    # register address
    bpy.types.Scene.csgo_rigger_character = PointerProperty(type=SeriesCharacter_PROP)

def unregister():
    for cls in register_panel, register_operator, register_props:
        for i in reversed(cls):
            unregister_class(i)


if __name__ == '__main__':
    unregister()
    register()