import bpy, mathutils
from bpy.types import (
    Panel,
    Operator
)
#################################################
RIG_NAME = ['RIG_NAME', 'CSGO NEW CHARACTER']
RIG_ARMATURE_INDIFICATOR = ['RIG_ARMATURE_INDIFICATOR', 'CSGO_NEW_CHARACTER_RIG']


ROOT_CONSTRAINT_BONE = [
    '["ROOT_by_BODY"]', # attribute
    'Root_grp', # bone name
    'ROOT CONSTRAINT LOCATION', # constraints names
    'ROOT CONSTRAINT ROTATION'
]

ARMS_ATTRIBUTES = [
    '["L_ARM_IK_SWITCH"]', # 0
    '["L_ARM_Hand_by_Secondary_Parent"]', # 1
    '["L_ARM_Pole_Body_space"]', # 2
    '["L_IK_Clavicle_space"]', # 3
    
    '["L_ARM_AUTO_TWIST"]', # 4

    '["R_ARM_IK_SWITCH"]', # 5
    '["R_ARM_Hand_by_Secondary_Parent"]', # 6
    '["R_ARM_Pole_Body_space"]', # 7
    '["R_IK_Clavicle_space"]', # 8
    
    '["R_ARM_AUTO_TWIST"]', # 9
]

LEGS_ATTRIBUTES = [
    '["L_FOOT_AUTO_straight_ball"]', # 0

    '["L_FOOT_AUTO_Ball_LIFT_MAX"]', # 1
    '["L_FOOT_AUTO_Toe_LIFT_MAX"]', # 2
    '["L_FOOT_AUTO_Heel_LIFT_MAX"]', # 3

    '["L_LEG_Pole_Body_space"]', # 4

    '["L_LEG_TWIST_AUTO"]', # 5


    '["R_FOOT_AUTO_straight_ball"]', # 6

    '["R_FOOT_AUTO_Ball_LIFT_MAX"]', # 7
    '["R_FOOT_AUTO_Toe_LIFT_MAX"]', # 8
    '["R_FOOT_AUTO_Heel_LIFT_MAX"]', # 9

    '["R_LEG_Pole_Body_space"]', # 10

    '["R_LEG_TWIST_AUTO"]', # 11
]

OTHER_ATTRIBUTES = [
    '["Head_Neck_Space"]',
]

L_ARM_IK_MATCH_BONES = [
    'L_Hand_CTRL_IK',
    'L_ARM_PoleVector',

    'L_Shoulder_FK',
    'L_Elbow_FK',
    'L_Hand_FK',

    'L_Hand_Secondary_PARENT_IK',
]


LAYERS = {      # layers name / layer[idx] # (data, 'layers', index=0, toggle=True, text='IK')
    'Main': 16,
    'L IK' : 17,
    'R IK' : 18,
    'L FK' : 1,
    'R FK' : 2,
    'L IK Secondary Parent': 19,
    'R IK Secondary Parent': 20,
    'L Fingers' : 5,
    'R Fingers' : 6,

    'L Arm Twists' : 8,
    'R Arm Twists' : 9,

    'L Leg Twists' : 24,
    'R Leg Twists' : 25,
    
    'L Foot' : 3,
    'R Foot' : 4,

}

MAIN_CTRLS = [
    'Master_CTRL',
    'Root_CTRL',
    'Body_CTRL',
    'Hips_CTRL',
    'Spine_1',
    'Spine_2',
    'Spine_3',
    'Neck',
    'HEAD',
]
LEFT_ARM_CTRLS = [
    # leg
    'L_FOOT_CTRL',
    'L_LEG_PoleVector',
    'L_LEG_Twist_0',
    'L_LEG_Twist_1',
    'L_Ball',
    # foot
    'L_foot_Ball_LIFT_SWEEP',
    'L_foot_TOE_LIFT',
    'L_foot_HEEL_LIFT',
    'L_foot_TOE_SWEEP',
    'L_foot_HEEL_SWEEP',
    'L_FOOT_AUTO_ROLL',
    'L_foot_INSIDE_LIFT',
    'L_foot_OUTSIDE_LIFT',
    # arms
    'L_Clavicle',
    'L_Shoulder_FK',
    'L_Elbow_FK',
    'L_Hand_FK',
    'L_Shoulder_TWIST_0',
    'L_Shoulder_TWIST_1',
    'L_Elbow_TWIST_0',
    'L_Elbow_TWIST_1',
    'L_Hand_CTRL_IK',
    'L_ARM_PoleVector',
    'L_Hand_Secondary_PARENT_IK',
    # fingers
    'L_FINGER_Thumb_0',
    'L_FINGER_Thumb_1',
    'L_FINGER_Thumb_2',

    'L_FINGER_Index_META',
    'L_FINGER_Index_0',
    'L_FINGER_Index_1',
    'L_FINGER_Index_2',

    'L_FINGER_Middle_META',
    'L_FINGER_Middle_0',
    'L_FINGER_Middle_1',
    'L_FINGER_Middle_2',

    'L_FINGER_Ring_META',
    'L_FINGER_Ring_0',
    'L_FINGER_Ring_1',
    'L_FINGER_Ring_2',

    'L_FINGER_Pink_META',
    'L_FINGER_Pink_0',
    'L_FINGER_Pink_1',
    'L_FINGER_Pink_2',
]


#################################################
#################################################
                   # helps # 
#################################################
#################################################
def del_char(string, chars):
    str_new = string
    for char in chars:
        str_new = str_new.replace(char, '')
    return str_new

def attr_in_object(obj, attr_name):
    yes = False
    for n, v in obj.items():
        if n == attr_name:
            yes = True
            break
    return yes

#################################################
#################################################
                # operatora # 
#################################################
#################################################

class LEFT_CSGO_OP_MP_CHR_Math_FK_to_IK(Operator):
    bl_label = 'LEFT FK to IK'
    bl_idname = 'object.mpcsgo_ch_arm_l_fk_to_ik'
    bl_options = {'UNDO'}

    def execute(self, context):
        armature = bpy.context.active_object
        if not armature:
            return {'FINISHED'}

        # set object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        # switch to IK
        if not attr_in_object(armature, del_char(ARMS_ATTRIBUTES[0], ['"','[',']'])):
            print('not attr in object')
            return {'FINISHED'}
        
        armature[del_char(ARMS_ATTRIBUTES[0], ['"','[',']']) ] = 1.0

        # update matrix
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        # get from fk pose by ik influences
        matrix_data = []
        for bone in L_ARM_IK_MATCH_BONES[2:5]:
            a = mathutils.Matrix(armature.pose.bones[bone].matrix.copy())
            matrix_data.append(a)

        # set to fk
        for i in range(3):
            armature.pose.bones[L_ARM_IK_MATCH_BONES[2:5][i]].rotation_euler = (0, 0, 0)
            armature.pose.bones[L_ARM_IK_MATCH_BONES[2:5][i]].matrix = matrix_data[i]
            armature.pose.bones[L_ARM_IK_MATCH_BONES[2:5][i]].location = (0, 0, 0)
            armature.pose.bones[L_ARM_IK_MATCH_BONES[2:5][i]].scale = (1, 1, 1)

            # update
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.view_layer.update()
            bpy.ops.object.mode_set(mode='POSE')

        # go to FK MODE
        armature[del_char(ARMS_ATTRIBUTES[0], ['"','[',']']) ] = 0.0

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        del matrix_data

        return {'FINISHED'}

class RIGHT_CSGO_OP_MP_CHR_Math_FK_to_IK(Operator):
    bl_label = 'RIGHT FK to IK'
    bl_idname = 'object.mpcsgo_ch_arm_r_fk_to_ik'
    bl_options = {'UNDO'}

    def execute(self, context):
        armature = bpy.context.active_object
        if not armature:
            return {'FINISHED'}

        # set object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        # switch to IK
        if not attr_in_object(armature, del_char(ARMS_ATTRIBUTES[5], ['"','[',']'])):
            print('not attr in object')
            return {'FINISHED'}
        
        armature[del_char(ARMS_ATTRIBUTES[5], ['"','[',']']) ] = 1.0

        # update matrix
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        # get from fk pose by ik influences
        matrix_data = []
        for bone in L_ARM_IK_MATCH_BONES[2:5]:
            a = mathutils.Matrix(armature.pose.bones[
                'R'+bone[1:]
            ].matrix.copy())
            matrix_data.append(a)

        # set to fk
        for i in range(3):
            bone_name = 'R'+L_ARM_IK_MATCH_BONES[2:5][i][1:]
            armature.pose.bones[bone_name].rotation_euler = (0, 0, 0)
            armature.pose.bones[bone_name].matrix = matrix_data[i]
            armature.pose.bones[bone_name].location = (0, 0, 0)
            armature.pose.bones[bone_name].scale = (1, 1, 1)

            # update
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.view_layer.update()
            bpy.ops.object.mode_set(mode='POSE')

        # go to FK MODE
        armature[del_char(ARMS_ATTRIBUTES[5], ['"','[',']']) ] = 0.0

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        del matrix_data

        return {'FINISHED'}


class LEFT_CSGO_OP_MP_CHR_Math_IK_to_FK(Operator):
    bl_label = 'LEFT IK to FK'
    bl_idname = 'object.mpcsgo_ch_arm_l_ik_to_fk'
    bl_options = {'UNDO'}

    def execute(self, context):
        armature = bpy.context.active_object
        if not armature:
            return {'FINISHED'}

        # set object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        # switch to IK
        if not attr_in_object(armature, del_char(ARMS_ATTRIBUTES[0], ['"','[',']'])):
            print('not attr in object')
            return {'FINISHED'}
        
        armature[del_char(ARMS_ATTRIBUTES[0], ['"','[',']']) ] = 0.0

        # get FK Elbow and FK Hand Positions
        hand_fk_matrix = mathutils.Matrix(armature.pose.bones[L_ARM_IK_MATCH_BONES[4]].matrix.copy())
        elbow_fk_matrix = mathutils.Matrix(armature.pose.bones[L_ARM_IK_MATCH_BONES[3]].matrix.copy())
        
        # set to ik hand
        armature.pose.bones[L_ARM_IK_MATCH_BONES[0]].rotation_euler = (0, 0, 0)
        armature.pose.bones[L_ARM_IK_MATCH_BONES[0]].location = (0, 0, 0)
        armature.pose.bones[L_ARM_IK_MATCH_BONES[0]].matrix = hand_fk_matrix
        armature.pose.bones[L_ARM_IK_MATCH_BONES[0]].scale = (1, 1, 1)

        # update matrix
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        # set to ik pole vector
        armature.pose.bones[L_ARM_IK_MATCH_BONES[1]].rotation_euler = (0, 0, 0)
        armature.pose.bones[L_ARM_IK_MATCH_BONES[1]].location = (0, 0, 0)
        armature.pose.bones[L_ARM_IK_MATCH_BONES[1]].matrix = elbow_fk_matrix
        armature.pose.bones[L_ARM_IK_MATCH_BONES[1]].rotation_euler = (0, 0, 0)
        armature.pose.bones[L_ARM_IK_MATCH_BONES[1]].scale = (1, 1, 1)

        # update matrix
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        armature[del_char(ARMS_ATTRIBUTES[0], ['"','[',']']) ] = 1.0

        # update matrix
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        return {'FINISHED'}

class RIGHT_CSGO_OP_MP_CHR_Math_IK_to_FK(Operator):
    bl_label = 'RIGHT IK to FK'
    bl_idname = 'object.mpcsgo_ch_arm_r_ik_to_fk'
    bl_options = {'UNDO'}

    def execute(self, context):
        armature = bpy.context.active_object
        if not armature:
            return {'FINISHED'}

        # set object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        # switch to IK
        if not attr_in_object(armature, del_char(ARMS_ATTRIBUTES[5], ['"','[',']'])):
            print('not attr in object')
            return {'FINISHED'}
        
        armature[del_char(ARMS_ATTRIBUTES[5], ['"','[',']']) ] = 0.0

        # get FK Elbow and FK Hand Positions
        hand_fk_matrix = mathutils.Matrix(armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[4][1:]].matrix.copy())
        elbow_fk_matrix = mathutils.Matrix(armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[3][1:]].matrix.copy())
        
        # set to ik hand
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[0][1:]].rotation_euler = (0, 0, 0)
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[0][1:]].location = (0, 0, 0)
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[0][1:]].matrix = hand_fk_matrix
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[0][1:]].scale = (1, 1, 1)

        # update matrix
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        # set to ik pole vector
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[1][1:]].rotation_euler = (0, 0, 0)
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[1][1:]].location = (0, 0, 0)
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[1][1:]].matrix = elbow_fk_matrix
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[1][1:]].rotation_euler = (0, 0, 0)
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[1][1:]].scale = (1, 1, 1)

        # update matrix
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        armature[del_char(ARMS_ATTRIBUTES[5], ['"','[',']']) ] = 1.0

        # update matrix
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        return {'FINISHED'}

class LEFT_CSGO_OP_MP_CHR_ik_secondary_parent_to_ik_ctrl(Operator):
    bl_label = 'LEFT ik_secondary_parent_to_ik_ctrl'
    bl_idname = 'object.mpcsgo_ch_arm_l_ik_secondary_parent_to_ik_hand'
    bl_options = {'UNDO'}

    def execute(self, context):
        armature = bpy.context.active_object
        if not armature:
            return {'FINISHED'}

        # set object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        # switch to IK
        if not attr_in_object(armature, del_char(ARMS_ATTRIBUTES[1], ['"','[',']'])):
            print('not attr in object')
            return {'FINISHED'}
        
        armature[del_char(ARMS_ATTRIBUTES[1], ['"','[',']']) ] = 0.0

        # get matrix from ik hand
        hand_matrix = mathutils.Matrix(armature.pose.bones[L_ARM_IK_MATCH_BONES[0]].matrix.copy())

        # set to iksp
        armature.pose.bones[L_ARM_IK_MATCH_BONES[5]].location = (0, 0, 0)
        armature.pose.bones[L_ARM_IK_MATCH_BONES[5]].rotation_euler = (0, 0, 0)
        armature.pose.bones[L_ARM_IK_MATCH_BONES[5]].scale = (1, 1, 1)
        armature.pose.bones[L_ARM_IK_MATCH_BONES[5]].matrix = hand_matrix
        armature.pose.bones[L_ARM_IK_MATCH_BONES[5]].scale = (1, 1, 1)

        # update matrix
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        return {'FINISHED'}

class RIGHT_CSGO_OP_MP_CHR_ik_secondary_parent_to_ik_ctrl(Operator):
    bl_label = 'RIGHT ik_secondary_parent_to_ik_ctrl'
    bl_idname = 'object.mpcsgo_ch_arm_r_ik_secondary_parent_to_ik_hand'
    bl_options = {'UNDO'}

    def execute(self, context):
        armature = bpy.context.active_object
        if not armature:
            return {'FINISHED'}

        # set object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        # switch to IK
        if not attr_in_object(armature, del_char(ARMS_ATTRIBUTES[1], ['"','[',']'])):
            print('not attr in object')
            return {'FINISHED'}
        
        armature[del_char(ARMS_ATTRIBUTES[6], ['"','[',']']) ] = 0.0

        # get matrix from ik hand
        hand_matrix = mathutils.Matrix(armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[0][1:]].matrix.copy())

        # set to iksp
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[5][1:]].location = (0, 0, 0)
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[5][1:]].rotation_euler = (0, 0, 0)
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[5][1:]].scale = (1, 1, 1)
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[5][1:]].matrix = hand_matrix
        armature.pose.bones['R'+L_ARM_IK_MATCH_BONES[5][1:]].scale = (1, 1, 1)

        # update matrix
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='POSE')

        return {'FINISHED'}

class CSGO_OP_MP_CHR_show_ctrls(Operator):
    bl_label = 'csgo character show all hide anim ctrls'
    bl_idname = 'object.csgo_mp_character_rig_panel_show_hides_ctrls'
    bl_options = {'UNDO'}

    def execute(self, context):
        armature_object = context.active_object

        for bone in MAIN_CTRLS:
            armature_object.data.bones[bone].hide = False

        for bone in self.create_list_r_from_l(lst=LEFT_ARM_CTRLS, char='R'):
            armature_object.data.bones[bone].hide = False
        
        return {'FINISHED'}

    def create_list_r_from_l(self, lst=[], char=''):
        new_list = []
        for i in lst:
            new_list.append(i)
            new_list.append(char+i[1:])
        return new_list

#################################################
#################################################
                    # UI #
#################################################
#################################################

# rig layers
class CSGO_PT_MP_CharacterRIG_Layers(Panel):
    bl_label = 'Layers'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'CSGO_PT_MP_Character_Rig_Panel'

    def draw(self, context):
        layout = self.layout
        main_col = layout.column()

        armature_object = context.active_object
        main_col.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['Main'],
            toggle=True, 
            text='Main'
        )

        # arms
        bx = main_col.box()
        coll_bx = bx.column()
        coll_bx.label(text='Arms Layers')
        row_l_r = coll_bx.row()
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['L IK'],
            toggle=True, 
            text='L Arms IK'
        )
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['R IK'],
            toggle=True, 
            text='R Arms IK'
        )

        row_l_r = coll_bx.row()
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['L FK'],
            toggle=True, 
            text='L Arms FK'
        )
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['R FK'],
            toggle=True, 
            text='R Arms FK'
        )

        row_l_r = coll_bx.row()
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['L IK Secondary Parent'],
            toggle=True, 
            text='L IK Secondary Parent'
        )
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['R IK Secondary Parent'],
            toggle=True, 
            text='R IK Secondary Parent'
        )

        coll_bx.label(text='Arm Twists')
        row_l_r = coll_bx.row()
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['L Arm Twists'],
            toggle=True, 
            text='L Arm Twists'
        )
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['R Arm Twists'],
            toggle=True, 
            text='R Arm Twists'
        )

        coll_bx.label(text='Arm Fingers')
        row_l_r = coll_bx.row()
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['L Fingers'],
            toggle=True, 
            text='L Fingers'
        )
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['R Fingers'],
            toggle=True, 
            text='R Fingers'
        )

        # legs
        bx = main_col.box()
        coll_bx = bx.column()
        coll_bx.label(text='Legs Layers')
        row_l_r = coll_bx.row()
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['L Foot'],
            toggle=True, 
            text='L Foot CTRLS'
        )
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['R Foot'],
            toggle=True, 
            text='R Foot CTRLS'
        )

        row_l_r = coll_bx.row()
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['L Leg Twists'],
            toggle=True, 
            text='L Leg Twists'
        )
        row_l_r.prop(data=armature_object.data, 
            property='layers',
            index=LAYERS['R Leg Twists'],
            toggle=True, 
            text='R Leg Twists'
        )

# main rig settings
class CSGO_PT_MP_CharacterRIG_MainSettings(Panel):
    bl_label = 'Settings'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'CSGO_PT_MP_Character_Rig_Panel'

    def draw(self, context):
        layout = self.layout
        armature_object = context.active_object
        col = layout.column()
        col.scale_x = 1.4
        col.scale_y = 1.4
        col.label(text='Head Rotation Space')
        col.prop(data=armature_object, property=OTHER_ATTRIBUTES[0], slider=True, text='Neck Rotate Space')

class CSGO_PT_MP_CharacterRIG_ROOT(Panel):
    bl_label = 'Root Settings'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'CSGO_PT_MP_CharacterRIG_MainSettings'

    def draw(self, context):
        armature_object = context.active_object

        bx = self.layout.box()
        bx.label(text='Root Motion Space')

        col = bx.column()

        rw = col.row()
        rw.label(text='Location')
        for i in range(3):
            rw.prop(
                data=armature_object.pose.bones[ROOT_CONSTRAINT_BONE[1]].constraints[ROOT_CONSTRAINT_BONE[2]],
                property=['use_x', 'use_y', 'use_z'][i],
                toggle=True,
                text=['X', 'Y', 'Z'][i]
            )
        rw = col.row()
        rw.label(text='Rotation')
        for i in range(3):
            rw.prop(
                data=armature_object.pose.bones[ROOT_CONSTRAINT_BONE[1]].constraints[ROOT_CONSTRAINT_BONE[3]],
                property=['use_x', 'use_y', 'use_z'][i],
                toggle=True,
                text=['X', 'Y', 'Z'][i]
            )

        col.label(text='Influence by Body')
        grp = col.box()
        grp.scale_x = 1.2
        grp.scale_y = 1.2
        grp.alignment 
        grp.prop(data=armature_object, property=ROOT_CONSTRAINT_BONE[0], slider=True, text='ROOT By Body')

class CSGO_PT_MP_CharacterRIG_ARMS(Panel):
    bl_label = 'Arms'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'CSGO_PT_MP_CharacterRIG_MainSettings'

    def draw(self, context):
        layout = self.layout
        armature_object = context.active_object

        # ik switchs
        main_box = layout.box()
        main_coll = main_box.column()
        main_coll.label(text='FK/IK Switch')
        ikbx = main_coll.box()

        ikcoll = ikbx.column()

        row = ikcoll.row()
        row.scale_x = row.scale_y = 1.4

        row.prop(data=armature_object, property=ARMS_ATTRIBUTES[0], slider=True, text='L Arm IK/FK Switch')
        row.prop(data=armature_object, property=ARMS_ATTRIBUTES[5], slider=True, text='R Arm IK/FK Switch')
        # match operators
        ikcoll.label(text='Match FK to IK and IK to FK', icon='BRUSHES_ALL')
        
        bx = ikcoll.box()
        coll = bx.column()
        coll.scale_x = coll.scale_y = 1.4

        row = coll.row()
        row.label(text='LEFT ARM')
        row.label(text='RIGHT ARM')

        row = coll.row()
        row.operator(operator=LEFT_CSGO_OP_MP_CHR_Math_FK_to_IK.bl_idname, text='FK to IK', icon='MOD_PARTICLE_INSTANCE')
        row.operator(operator=RIGHT_CSGO_OP_MP_CHR_Math_FK_to_IK.bl_idname, text='FK to IK', icon='MOD_PARTICLE_INSTANCE')

        row = coll.row()
        row.operator(operator=LEFT_CSGO_OP_MP_CHR_Math_IK_to_FK.bl_idname, text='IK to FK', icon='MOD_PARTICLE_INSTANCE')
        row.operator(operator=RIGHT_CSGO_OP_MP_CHR_Math_IK_to_FK.bl_idname, text='IK to FK', icon='MOD_PARTICLE_INSTANCE')


        # IK Secondary Parent
        ikcoll.label(text='HAND_IK to IK Secondart Parent')
        bx = ikcoll.row()
        bx.scale_x = bx.scale_y = 1.2

        bx.prop(data=armature_object, property=ARMS_ATTRIBUTES[1], slider=True, text='L IK CTRL by Secondary')
        bx.prop(data=armature_object, property=ARMS_ATTRIBUTES[6], slider=True, text='R IK CTRL by Secondary')
        # match operators
        ikcoll.label(text='Match IK Secondary Parent to HAND_IK', icon='POSE_HLT')
        bx = ikcoll.box()
        coll = bx.column()

        row = coll.row()
        row.label(text='LEFT ARM')
        row.label(text='RIGHT ARM')

        row = coll.row()
        row.scale_x = row.scale_y = 1.4
        row.operator(operator=LEFT_CSGO_OP_MP_CHR_ik_secondary_parent_to_ik_ctrl.bl_idname, text='L IKSP to Hand', icon='OUTLINER_DATA_GREASEPENCIL')
        row.operator(operator=RIGHT_CSGO_OP_MP_CHR_ik_secondary_parent_to_ik_ctrl.bl_idname, text='R IKSP to Hand', icon='OUTLINER_DATA_GREASEPENCIL')


        # poleVectors
        main_coll.label(text='PoleVectors Translate in BODY Space')
        bx = main_coll.box()

        row = bx.row()
        row.scale_x = row.scale_y = 1.3

        row.prop(data=armature_object, property=ARMS_ATTRIBUTES[2], slider=True, text='L Pole by BODY')
        row.prop(data=armature_object, property=ARMS_ATTRIBUTES[7], slider=True, text='R Pole by BODY')

        # clavicle space
        main_coll.label(text='Arm IK in Clavicle Space')
        bx = main_coll.box()

        row = bx.row()
        row.scale_x = row.scale_y = 1.3
        row.prop(data=armature_object, property=ARMS_ATTRIBUTES[3], slider=True, text='L ARM IK by Clavicle')
        row.prop(data=armature_object, property=ARMS_ATTRIBUTES[8], slider=True, text='R ARM IK by Clavicle')


        # TWISTS
        main_coll.label(text='AUTO Arms Twists')
        bx = main_coll.box()
        bx.scale_x = bx.scale_y = 1.2
        row = bx.row()
        row.prop(data=armature_object, property=ARMS_ATTRIBUTES[4], slider=True, text='L AUTO TWIST')
        row.prop(data=armature_object, property=ARMS_ATTRIBUTES[9], slider=True, text='R AUTO TWIST')

class CSGO_PT_MP_CharacterRIG_LEGS(Panel):
    bl_label = 'Legs'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'CSGO_PT_MP_CharacterRIG_MainSettings'

    def draw(self, context):
        layout = self.layout
        main_coll = layout.column()

        armature_object = context.active_object

        main_coll.label(text='Foot Roll Settings')
        bx = main_coll.box()
        bx.scale_x = bx.scale_y = 1.4
        coll = bx.column()

        
        coll.label(text='AUTO Roll Settings')
        row = coll.row()
        row.label(text='LEFT LEG')
        row.label(text='RIGHT LEG')

        row = coll.row()
        row.prop(data=armature_object, property=LEGS_ATTRIBUTES[1], slider=True, text='L Max Ball Angle')
        row.prop(data=armature_object, property=LEGS_ATTRIBUTES[7], slider=True, text='R Max Ball Angle')

        row = coll.row()
        row.prop(data=armature_object, property=LEGS_ATTRIBUTES[2], slider=True, text='L Max Toe Angle')
        row.prop(data=armature_object, property=LEGS_ATTRIBUTES[8], slider=True, text='R Max Toe Angle')

        row = coll.row()
        row.prop(data=armature_object, property=LEGS_ATTRIBUTES[3], slider=True, text='L Max Heel Angle')
        row.prop(data=armature_object, property=LEGS_ATTRIBUTES[9], slider=True, text='R Max Heel Angle')

        row = coll.row()
        row.prop(data=armature_object, property=LEGS_ATTRIBUTES[0], slider=True, text='L Straight Ball')
        row.prop(data=armature_object, property=LEGS_ATTRIBUTES[6], slider=True, text='R Straight Ball')


        main_coll.label(text='PoleVectors by BDDY Space')
        bx = main_coll.box()
        coll = bx.column()

        row = coll.row()
        row.label(text='LEFT LEG')
        row.label(text='RIGHT LEG')

        row = coll.row()
        row.prop(data=armature_object, property=LEGS_ATTRIBUTES[4], slider=True, text='L Pole by BODY')
        row.prop(data=armature_object, property=LEGS_ATTRIBUTES[10], slider=True, text='R Pole by BODY')

        main_coll.label(text='AUTO Twists')
        bx = main_coll.box()
        coll = bx.column()

        row = coll.row()
        row.label(text='LEFT LEG')
        row.label(text='RIGHT LEG')

        row = coll.row()
        row.prop(data=armature_object, property=LEGS_ATTRIBUTES[5], slider=True, text='L Leg Twist')
        row.prop(data=armature_object, property=LEGS_ATTRIBUTES[11], slider=True, text='R Leg Twist')

# main parent panel
class CSGO_PT_MP_Character_Rig_Panel(Panel):
    bl_label = 'CSGO Character Rig'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'

    def draw(self, context):
        layout = self.layout
        armature_object = context.active_object
        main_column = layout.column()
        bx = main_column.box()
        bx.label(text='Active Armature: '+armature_object.name)

        # draw hide/show button
        HIDE_CTRL = False
        for bone in MAIN_CTRLS:
            if armature_object.data.bones[bone].hide:
                HIDE_CTRL = True
                break
        if HIDE_CTRL:
            # draw
            self.hide_button_create(layout=main_column)
            return
        for bone in self.create_list_r_from_l(lst=LEFT_ARM_CTRLS, char='R'):
            if armature_object.data.bones[bone].hide:
                HIDE_CTRL = True
                break

        if HIDE_CTRL:
            # draw
            self.hide_button_create(layout=main_column)
            return
        

    @classmethod # from AddonPrefs and Avtive
    def poll(self, context):
        if context.mode == 'POSE' and context.active_object.type == 'ARMATURE':
            yes_rig_name = False
            yes_rig_indificator = False
    
            for n, v in context.active_object.items():
                if n == RIG_NAME[0] and v == RIG_NAME[1]:
                    yes_rig_name = True
                elif n == RIG_ARMATURE_INDIFICATOR[0] and v == RIG_ARMATURE_INDIFICATOR[1]:
                    yes_rig_indificator = True
            
            if yes_rig_name and yes_rig_indificator:
                return True
            else:
                return False
        else:
            return False

    def hide_button_create(self, layout):
        bx = layout.box()
        bx.scale_x = 2.0
        bx.scale_y = 2.0
        bx.operator(
            operator=CSGO_OP_MP_CHR_show_ctrls.bl_idname, 
            text='The controllers are hidden! Show it back on?',
            icon='OUTLINER_OB_LIGHT'
        )

    def create_list_r_from_l(self, lst=[], char=''):
        new_list = []
        for i in lst:
            new_list.append(i)
            new_list.append(char+i[1:])
        return new_list


classes = [
    # operators
    CSGO_OP_MP_CHR_show_ctrls,

    LEFT_CSGO_OP_MP_CHR_Math_FK_to_IK,
    RIGHT_CSGO_OP_MP_CHR_Math_FK_to_IK,

    LEFT_CSGO_OP_MP_CHR_Math_IK_to_FK,
    RIGHT_CSGO_OP_MP_CHR_Math_IK_to_FK,

    LEFT_CSGO_OP_MP_CHR_ik_secondary_parent_to_ik_ctrl,
    RIGHT_CSGO_OP_MP_CHR_ik_secondary_parent_to_ik_ctrl,

    # panels
    CSGO_PT_MP_Character_Rig_Panel,

    CSGO_PT_MP_CharacterRIG_Layers,
    CSGO_PT_MP_CharacterRIG_MainSettings,
        CSGO_PT_MP_CharacterRIG_ROOT,
        CSGO_PT_MP_CharacterRIG_ARMS,
        CSGO_PT_MP_CharacterRIG_LEGS,
]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register_point():
    pass

def unregister_point():
    pass