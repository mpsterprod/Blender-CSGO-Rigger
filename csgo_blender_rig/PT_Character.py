import bpy, os
from bpy.props import (
    PointerProperty,
    StringProperty,
    BoolProperty,
)
from bpy.types import (
    Panel,
    PropertyGroup,
    Operator
)

PARENT_CATEGORY = 'CSGO'
DEFAULT_RIG_FILE = 'mp_csgo_character_rig_v3.blend'
DEFAULT_RIG_COLLECTION = 'CSGO_RIG'
DEFAULT_RIG_ARMATURE = 'csgo_character_rig'
DEFAULT_BUILD_SCRIPT_IN_DEFAULT_RIG_FILE = 'CSGO_Character_Rig_Connector.py'

class CSGO_PG_CharacterProperty(PropertyGroup):
    main_root_qc_folder : StringProperty(
        subtype='FILE_PATH',
        name='Qc/Smd Folders',
        default=''
    )

    main_root_export_folder : StringProperty(
        subtype='FILE_PATH',
        name='Export Rigs Folder',
        default=''
    )

    # custom rig
    use_custom_rig : BoolProperty(
        name='Use Custom Rig File',
        default=False
    )

    custom_rig_file : StringProperty(
        subtype='FILE_PATH',
        name='Custom .BLEND rig file',
        default=''
    )
    collection_name : StringProperty(
        name='Rig Collection in file',
        default=''
    )
    armature_rig_name : StringProperty(
        name='Armature Object Rig Name',
        default=''
    )
    script_name : StringProperty(
        name='Build/Connection Script in file',
        default=''
    )


'''
    /*
        main rig build 
    */
'''
class CSGO_OP_CharacterBuild(Operator):
    bl_label = 'create csgo characters'
    bl_idname = 'scene.csgo_rig_tool_character_rigging'

    def execute(self, context):
        props = context.scene.mp_csgo_rig_character_info

        CH_FOLDERS = self.fix_last_slash((props.main_root_qc_folder).replace("\\", '/'))
        EXPORT_FOLDER = self.fix_last_slash((props.main_root_export_folder).replace("\\", '/'))

        DEFAULT_RIGS = __file__.replace(os.path.basename(__file__), "")+'/rigs/'

        good_folders = []

        # read folders and validate
        for character_folder in next(os.walk(CH_FOLDERS))[1]:
            if self.validate_folders(CH_FOLDERS+'/'+character_folder):
                good_folders.append(CH_FOLDERS+'/'+character_folder)
     
        # clear blend file
        for character_path in good_folders:
            scene = context.scene
            character_name = self.get_from_split(string=character_path, char='/', pos=len(character_path.split('/'))-1)

            deform_armature_name = ''

            print('\n\ncreate for', character_name)
            # new scene
            #bpy.ops.wm.read_homefile(app_template='')
            # clear bpy
            self.clear_blend_data()
            # import smds
            for file in next(os.walk(character_path))[2]:
                if file[len(file)-4:] == '.smd':
                    bpy.ops.import_scene.smd(
                        filepath = character_path+'/'+file,
                        doAnim = False,
                        createCollections=False,
                        makeCamera=False,
                        append='APPEND',
                        upAxis='Y',
                        rotMode='XYZ',
                        boneMode='NONE'
                    )
            
            # set scale
            if not self.fix_skeletalMesh_Scale(scene):
                continue

            # create root bone
            for n, obj in scene.objects.items():
                if obj.type == 'ARMATURE':
                    obj.name = 'Armature'
                    break
            self.__create_root(armature_name='Armature')

            ##########################################
                    # EXPORT SKELETAL MESH #
            ##########################################
            meshes = []

            for n, obj in scene.objects.items():
                if obj.type == 'ARMATURE':
                    deform_armature_name = n
                    obj.select_set(True)
                elif obj.type == 'MESH':
                    meshes.append(n)
                    obj.select_set(True)
        
            # make folder 
            CHARACTER_FOLDER = self.make_folder(filepath=EXPORT_FOLDER+'/'+character_name+'/')

            # export in fbx
            bpy.ops.export_scene.fbx(
                filepath=CHARACTER_FOLDER+'/'+'SkeletalMesh_'+character_name+'.fbx',
                bake_anim=False,
                use_selection=True,
                use_armature_deform_only=True,
                add_leaf_bones=False,
                armature_nodetype='NULL'
            )

            self.select(scene, False)


            # append rig collection and build script
            if props.use_custom_rig:
                # import by path and check valide
                bpy.ops.wm.append(      # RIG COLLECTION
                    filepath=props.custom_rig_file,
                    directory=props.custom_rig_file+'/Collection/',
                    filename=props.collection_name,
                    autoselect=False,
                    active_collection=False,
                    instance_collections=False,
                    instance_object_data=False,
                    set_fake=False,
                    use_recursive=False
                )
                # remove `Append Data` Collection
                scene.collection.children.link(bpy.data.collections[props.collection_name])
                bpy.data.collections['Appended Data'].children.unlink(bpy.data.collections[props.collection_name])
                bpy.data.collections.remove(bpy.data.collections['Appended Data'])

                # append script
                bpy.ops.wm.append(      # BUILD SCRIPT
                    filepath=props.custom_rig_file,
                    directory=props.custom_rig_file+'/Text/',
                    filename=props.script_name,
                    autoselect=False,
                    active_collection=False,
                    instance_collections=False,
                    instance_object_data=False,
                    set_fake=False,
                    use_recursive=False
                )

                # remove librarie
                for f, rna in bpy.data.libraries.items():
                    bpy.data.libraries.remove(rna)

                # run script as module
                try:
                    script = bpy.data.texts[props.script_name].as_module()
                    script.csgo_rig_build(
                        character_name=character_name,
                        # rig
                        rig_collection_name=props.collection_name,
                        rig_armature_name=props.armature_rig_name,
                        # skeletal mesh
                        deform_armature_name=deform_armature_name,
                        meshes = meshes
                    )
                except Exception as error:
                    print(error)
                    break

            else:
                # default mp rig
                bpy.ops.wm.append(      # RIG COLLECTION
                    filepath=DEFAULT_RIGS+DEFAULT_RIG_FILE,
                    directory=DEFAULT_RIGS+DEFAULT_RIG_FILE+'/Collection/',
                    filename=DEFAULT_RIG_COLLECTION,
                    autoselect=False,
                    active_collection=False,
                    instance_collections=False,
                    instance_object_data=False,
                    set_fake=False,
                    use_recursive=False
                )
                # fix `Append Data`
                scene.collection.children.link(bpy.data.collections[DEFAULT_RIG_COLLECTION])

                for n, c in bpy.data.collections.items():
                    if n == 'Appended Data':
                        try:
                            bpy.data.collections['Appended Data'].children.unlink(bpy.data.collections[DEFAULT_RIG_COLLECTION])
                            bpy.data.collections.remove(bpy.data.collections['Appended Data'])
                        except KeyError as k:
                            print('not unlink and delete Appended Data', k)
                        break

                # append script
                bpy.ops.wm.append(      # BUILD SCRIPT
                    filepath=DEFAULT_RIGS+DEFAULT_RIG_FILE,
                    directory=DEFAULT_RIGS+DEFAULT_RIG_FILE+'/Text/',
                    filename=DEFAULT_BUILD_SCRIPT_IN_DEFAULT_RIG_FILE,
                    autoselect=False,
                    active_collection=False,
                    instance_collections=False,
                    instance_object_data=False,
                    set_fake=False,
                    use_recursive=False
                )

                # remove librarie
                for f, rna in bpy.data.libraries.items():
                    bpy.data.libraries.remove(rna)

                # run script as module
                try:
                    script = bpy.data.texts[DEFAULT_BUILD_SCRIPT_IN_DEFAULT_RIG_FILE].as_module()
                    script.csgo_rig_build(
                        character_name=character_name,
                        # rig
                        rig_collection_name=DEFAULT_RIG_COLLECTION,
                        rig_armature_name=DEFAULT_RIG_ARMATURE,
                        # skeletal mesh
                        deform_armature_name=deform_armature_name,
                        meshes = meshes
                    )
                except Exception as error:
                    print(error)
                    break

            # as script :
            '''##########################################################################
                --- > default name: csgo_mp_character_rig_create.py

                    def csgo_rig_build(character_name)
                        1) create collection rig struct and create links
                        2) add root bone to deforms bone
                        3) create constraint

                        ->> return True or False
            for i in bpy.context.selected_pose_bones_from_active_object: i.rotation_mode = 'XYZ'
            '''##########################################################################
            # delete script
            for n, t in bpy.data.texts.items():
                bpy.data.texts.remove(t)

            # save file
            bpy.ops.wm.save_as_mainfile(
                filepath=CHARACTER_FOLDER+'/'+'Rig_'+character_name+'.blend'
            )
        del good_folders

        self.clear_blend_data()

        return {'FINISHED'}

    def validate_folders(self, path):
        good = False
        for f in next(os.walk(path))[2]:
            if f[len(f)-4:] == '.smd':
                good = True
                break
        return good
    
    def fix_last_slash(self, string):
        return( string if string[len(string)-1:] != '/' else string[:len(string)-1]  )

    def clear_blend_data(self):
        for data in [
            bpy.data.actions,
            bpy.data.armatures,
            bpy.data.brushes,
            bpy.data.images,
            bpy.data.linestyles,
            bpy.data.materials,
            bpy.data.meshes,
            bpy.data.objects,
            bpy.data.palettes,
            bpy.data.collections,
            bpy.data.lights,
            bpy.data.cameras
        ]:
            for type_data in data.items():
                data.remove(data[type_data[0]])

    def get_from_split(self, string='', char='', pos=0):
        mass = string.split(char)
        return mass[pos]

    def select(self, scene, value):
        for i in scene.objects.items():
            i[1].select_set(value)

    def fix_skeletalMesh_Scale(self, scene):
        print('\n\n\n\nin fix_skeletalMesh_Scale()')
        deform_armature_name = ''
        # get armature
        for n, o in scene.objects.items():
            if o.type == 'ARMATURE':
                print('--- armature ', n)
                deform_armature_name = n
                break
        if deform_armature_name == '':
            # next model
            return False
        
        # for all meshes delete modificator
        for name, obj in scene.objects.items():
            if obj.type == 'MESH':
                print('-mesh--------- ', name)
                # remove
                for n, m in obj.modifiers.items():
                    obj.modifiers.remove(m)
                print('delete modificators')
                # set scale
                obj.scale = [0.01, 0.01, 0.01]
                obj.select_set(True)
                bpy.ops.object.transform_apply()
                obj.select_set(False)
                print('\nset and freeze scale')
                obj.parent = None

        # rescale armature
        bpy.context.view_layer.objects.active = None
        self.select(scene, False)
        scene.objects[deform_armature_name].scale = [0.01, 0.01, 0.01]

        bpy.context.view_layer.objects.active = scene.objects[deform_armature_name]
        scene.objects[deform_armature_name].select_set(True)
        bpy.ops.object.transform_apply()
        self.select(scene, False)
        bpy.context.view_layer.objects.active = None

        # back `armature` modificator
        for name, obj in scene.objects.items():
            if obj.type == 'MESH':
                obj.modifiers.new(name='csgo_skin_cluster',type='ARMATURE')
                obj.modifiers['csgo_skin_cluster'].object = scene.objects[deform_armature_name]
        
        # next methods
        return True

    def make_folder(self, filepath):
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def __create_root(self, armature_name):
        print('in create root')

        scene = bpy.context.scene
        
        self.__select(scene, False)
        bpy.context.view_layer.objects.active = None
        
        armature = scene.objects[armature_name]
        
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature
        bpy.context.view_layer.update()
        
        print('start edit armature')
        
        bpy.ops.object.mode_set(mode='EDIT')
    
        if not self.__key_in_dict(armature.data.edit_bones.items(), 'root'):
            #add bone
            bone = armature.data.edit_bones.new(name='root')
            bone.head = [0.0, 0.0, 0.0]
            bone.tail = [0.0, 0.0, 1.0]
            print('in edit mode and check root bone')
    
        # set parent to `root`
        for name, bone in armature.data.edit_bones.items():
            if name != 'root' and bone.parent==None:
                bone.parent = armature.data.edit_bones['root']
        print('set parent bones')
        
        # disconnect all bones!
        for n, bone in armature.data.edit_bones.items():
            bone.use_connect = False
        print('disconnect bones done!')
        
        bpy.context.view_layer.update()

        bpy.ops.object.mode_set(mode='OBJECT')

    def __select(self, scene, value):
        for i in scene.objects.items():
            i[1].select_set(value)
        
    def __key_in_dict(self, data, value):
        print('in find')
        yes = False
        for key, obj in data:
            if key == value:
                yes = True
                break
        return yes
        
    
    
class CSGO_PT_Character_Panel(Panel):
    bl_label = 'CSGO Character Rig'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PARENT_CATEGORY


    def draw(self, context):
        layout = self.layout
        props = context.scene.mp_csgo_rig_character_info

        bx = layout.box()
        col = bx.column()
        col.label(text='Tool Version 1.0')
        if props.use_custom_rig:
            col.label(text='STATUS: "CUSTOM USER RIG"')
        else:
            col.label(text='STATUS: "MP Default RIG"')

        col_main = layout.column()
        col_main.prop( data=props, property='main_root_qc_folder')
        col_main.prop(data=props, property='main_root_export_folder')

        col_main.label(text='Custom Rig:')
        col_main.prop(data=props, property='use_custom_rig')

        bx = col_main.box()
        bx.enabled = props.use_custom_rig

        col = bx.column()
        col.prop(data=props, property='custom_rig_file', icon='BLENDER')
        col.prop(data=props, property='collection_name', icon='COLLECTION_COLOR_04')
        col.prop(data=props, property='armature_rig_name', icon='OUTLINER_OB_ARMATURE')
        col.prop(data=props, property='script_name', icon='FILE_SCRIPT')
       
        op_col = col_main.column()

        op_col.operator(
            operator=CSGO_OP_CharacterBuild.bl_idname,
            text='Create Rigs!',
            icon='ARMATURE_DATA'
        )
        
        if props.main_root_qc_folder != '' and props.main_root_export_folder != '':
            if props.use_custom_rig:
                if props.custom_rig_file != '' and props.collection_name != '' and props.script_name != '' and props.armature_rig_name != '':
                    op_col.enabled = True
                else:
                    op_col.enabled = False
            else:
                op_col.enabled = True
        else:
            op_col.enabled = False


    @classmethod # from AddonPrefs
    def poll(self, context):
        if bpy.context.mode == 'OBJECT':
            return context.scene.mp_csgo_addons_prefs.mptool_csgo_panel_vis
        else:
            return False

classes = [
    CSGO_PG_CharacterProperty,
    CSGO_OP_CharacterBuild,

    CSGO_PT_Character_Panel
]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register_point():
    bpy.types.Scene.mp_csgo_rig_character_info = PointerProperty(type=CSGO_PG_CharacterProperty)

def unregister_point():
    try:
        bpy.types.Scene.mp_csgo_rig_character_info = None
        del bpy.types.Scene.mp_csgo_rig_character_info
    except: pass
