# script made by mp mpsterprod
# youtube: https://www.youtube.com/channel/UCXvI8JRMsskPQrpQoSLeeBA
# discord: MP#9395
# github: https://github.com/mpsterprod

bl_info = {
    "name": "Source Static Exporter to FBX",
    "author": "mp mpsterprod",
    "version": (1, 0),
    "blender": (2, 81, 0),
    "location": "View3D > Object",
    "description": "For export qc/smd to FBX",
    "warning": "",
    "wiki_url": "",
    "category": "Object"
}


import bpy
from bpy.types import (
    AddonPreferences,
    Operator,
    Panel,
    PropertyGroup,
    StringProperty,
)
from bpy.props import (IntProperty)

import os
from pathlib import Path, PureWindowsPath


#def Create_FBX

import math
import pathlib


def Create_FBX_Export(folder_import=str,folder_export=str,update_rotation=[0,0,0],update_prefix='',max_files_folders=int, qc_only=bool, suffix_use=bool, import_physics_smd=bool, global_scale_root=float):
    # check folder import...
    if folder_import == '' or folder_export == '':
        return
    a_objects = os.listdir(folder_import+'/')
    folders_or_no = False
    smd_pathes=[]
    '''
    for ff in a_objects:
        suf = pathlib.Path(folder_import+'/'+ff).suffix
        if suf==".qc":
            folders_or_no = True
            # only one folder...
            break
    '''
    # create rotate
    update_r = True
    x = 0
    y = 0
    z = 0
    # check input data
    if update_rotation[0]==0 and update_rotation[1]==0 and update_rotation[2]==0:
        print('not data all zero')
        update_r=False
        del x,y,z
    else:
        update_r=True
        x = math.radians(update_rotation[0])  # angle to radians
        y = math.radians(update_rotation[1])
        z = math.radians(update_rotation[2])

    # for one folder 'folder_import'
    if folders_or_no: # qc_only   # old: folders_or_no
        # create list_qc
        #update_r = True
        qc=[]
        #x = 0
        #y = 0
        #z = 0

        # get all folders

        #                                  BREAK

        for all_files in a_objects:
            suf = pathlib.Path(folder_import+'/'+all_files).suffix
            if suf==".qc":
                qc.append(folder_import+'/'+all_files)
        use_qc=[]
        if qc!=[]:
            use_qc=qc[0:max_files_folders]
        else:
            return
        for i_path in use_qc: 
            character_name = i_path.replace('/',' ').split()
            CHARACTER_NAME = character_name[len(character_name)-1].replace('.qc','')
            del character_name
            bpy.ops.scene.new(type='NEW')                 # only for .qc files NOT .smd !
            bpy.ops.object.delete(use_global=True)
            bpy.ops.import_scene.smd(filepath = i_path, doAnim = False)
            if update_r:
                bpy.context.object.rotation_euler[0] = x
                bpy.context.object.rotation_euler[1] = y
                bpy.context.object.rotation_euler[2] = z
            if update_prefix!='':
                bpy.ops.export_scene.fbx(filepath = folder_export + '/'+ update_prefix +'_'+ CHARACTER_NAME + ".ModelFromBlender.fbx", bake_anim = False, global_scale = 0.01)
            else:
                bpy.ops.export_scene.fbx(filepath = folder_export + '/'+ CHARACTER_NAME + ".ModelFromBlender.fbx", bake_anim = False, global_scale = 0.01)
            bpy.ops.scene.new(type='NEW')
            bpy.ops.object.delete(use_global=True)
    else:
        # check folders
        # one level

        folders = []
        fast_f = []
        for w_o in a_objects:
            if os.path.isdir(folder_import+'/'+w_o):
                fast_f.append(folder_import+'/'+w_o)
        folders = fast_f[0:max_files_folders]
        for f_imp in folders:
            #check folder
            l_smd = []
            a_ff = os.listdir(f_imp+'/')
            if a_ff is None or a_ff==[]:
                continue
            if qc_only:
                for fffa in a_ff:
                    if pathlib.Path(f_imp+'/'+fffa).suffix==".qc":
                        l_smd.append(f_imp+'/'+fffa)
            else:
                for fffa in a_ff:
                    if pathlib.Path(f_imp+'/'+fffa).suffix==".smd":
                        # import physics?
                        if import_physics_smd:
                            l_smd.append(f_imp+'/'+fffa)
                        else:
                            if fffa.find("_physics")!=-1:
                                continue
                            else:
                                l_smd.append(f_imp+'/'+fffa)
            if l_smd is None or l_smd == []:
                continue
            bpy.ops.scene.new(type='NEW')                 # only for .smd !
            bpy.ops.object.delete(use_global=True)
            for imports_SMDS in l_smd:
                # import physics?
                    bpy.ops.import_scene.smd(filepath = imports_SMDS, doAnim = False)
                               
            # update rotation
            if update_r:
                bpy.context.object.rotation_euler[0] = x
                bpy.context.object.rotation_euler[1] = y
                bpy.context.object.rotation_euler[2] = z
            # get name
            # find qc file
            qc_name=''
            for qc_find in a_ff:
                if pathlib.Path(f_imp+'/'+qc_find).suffix==".qc":
                    qc_name = qc_find
                    break

            if qc_name !='':
                # export FBX
                if update_prefix!='':
                    if suffix_use:
                        bpy.ops.export_scene.fbx(filepath = folder_export + '/'+ update_prefix + '_'+ qc_name.replace('.qc','') + ".ModelFromBlender.fbx", bake_anim = False, global_scale = global_scale_root)
                    else:
                        bpy.ops.export_scene.fbx(filepath = folder_export + '/'+ update_prefix + '_'+ qc_name.replace('.qc','') + ".fbx", bake_anim = False, global_scale = global_scale_root)
                else:
                    if suffix_use:
                        bpy.ops.export_scene.fbx(filepath = folder_export + '/'+ qc_name.replace('.qc','') + ".ModelFromBlender.fbx", bake_anim = False, global_scale = global_scale_root)
                    else:
                        bpy.ops.export_scene.fbx(filepath = folder_export + '/'+ qc_name.replace('.qc','') + ".fbx", bake_anim = False, global_scale = global_scale_root)
            else:
                # get first file from import
                model_name = l_smd[0].replace('.smd','')
                if update_prefix!='':
                    if suffix_use:
                        bpy.ops.export_scene.fbx(filepath = folder_export + '/'+ update_prefix + '_'+ model_name + ".ModelFromBlender.fbx", bake_anim = False, global_scale = global_scale_root)
                    else:
                        bpy.ops.export_scene.fbx(filepath = folder_export + '/'+ update_prefix + '_'+ model_name + ".fbx", bake_anim = False, global_scale = global_scale_root)
                else:
                    if suffix_use:
                        bpy.ops.export_scene.fbx(filepath = folder_export + '/'+ model_name + ".ModelFromBlender.fbx", bake_anim = False, global_scale = global_scale_root)
                    else:
                        bpy.ops.export_scene.fbx(filepath = folder_export + '/'+ model_name + ".fbx", bake_anim = False, global_scale = global_scale_root)
            bpy.ops.scene.new(type='NEW')
            bpy.ops.object.delete(use_global=True)
                

class OBJECT_OT_customsmdqcexport(Operator):
    bl_label = "Exporter QC/SMD to FBX"
    bl_idname = "object.customsmdqcexport"
    bl_description = "Exporting static qc/smd to fbx"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_option = {'REGISTER', 'UNDO'}

    globalFPath: bpy.props.StringProperty(
        subtype="FILE_PATH",
        name = "Folder QC/SMD files",
        description = "Folder for import",
    )

    globalExportPath: bpy.props.StringProperty(
        subtype="FILE_PATH",
        name = "Folder Export",
        description = "Folder for Export",
    )

    new_Rotation: bpy.props.FloatVectorProperty(
        name = "New Rotate",
        subtype = "XYZ",
    )


    '''
    AreYourFoldes: bpy.props.BoolProperty(
        name="Models Sorted by Folder?",
        subtype ="FACTOR",
    )
    '''

    globalScale_Input: bpy.props.FloatProperty(
        name = "Global Scale",
        default = 1,
        min = 0.01,
        max = 1,
        description = "Global Scale Value",
    )





    Custom_Prefix: bpy.props.StringProperty(
        subtype="NONE",
        name = "Custom Prefix Files",
        description = "Folder for import",
    )
    

    '''
    globalExportPath: bpy.props.StringProperty(
        subtype="FILE_PATH",
        name = "Folder Export",
        description = "Folder for Export",
    )
    '''

    qc_import_bool: bpy.props.BoolProperty(
        name = "Import .qc ?",
        default = 0,
        #min = 0,
        #max = 1,
        description = "import qc only/no smd import",
    )


    suffixUse: bpy.props.BoolProperty(
        name = "Use Suffix ?",
        default = 1,
        #min = 0,
        #max = 1,
        description = "Use suffix .ModelFromBlender.fbx ?",
    )



    importPhysicsModels: bpy.props.BoolProperty(
        #name = "Import Physics Collision",
        name = "Physics Collision",
        default = 1,
        description = "Import Physics Collision .smd",
    )



    numberMassiveFiles: bpy.props.IntProperty(
        name = "Max Files Export",
        default = 1,
        min = 1,
        max = 10000,
        description = "Max Min exportins numbers",
    )

    

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    '''
    def execute(self, context):
        scanFile(self.globalFPath)
        return {'FINISHED'}
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    '''

    #start export func
    def execute(self, context):
        # start...
        FPath = self.globalFPath.replace('\\', '/')
        ExportPath = self.globalExportPath.replace('\\', '/')
        # fix prefix
        input_prefix = ''
        if self.Custom_Prefix!="":
            if self.Custom_Prefix[len(self.Custom_Prefix)-1]=="_":
                input_prefix = self.Custom_Prefix[0:len(self.Custom_Prefix)-1]
            else:
                input_prefix = self.Custom_Prefix

        Create_FBX_Export(folder_import=FPath,
            folder_export=ExportPath,
            update_rotation=self.new_Rotation,
            update_prefix=input_prefix,
            max_files_folders=self.numberMassiveFiles,
            qc_only=self.qc_import_bool,
            suffix_use=self.suffixUse,
            import_physics_smd=self.importPhysicsModels,
            global_scale_root=self.globalScale_Input,
        )
        # FINISHED...
        return {'FINISHED'}



def menu_func(self, context):
    self.layout.operator(OBJECT_OT_customsmdqcexport.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_customsmdqcexport)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_customsmdqcexport)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
