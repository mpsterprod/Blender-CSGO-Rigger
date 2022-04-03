'''
    connection script

    syntax
    
    [
        object "parent", "children", "type_expression_connect"
    ]

    [
        bone "armature_parent" "bone_parent", "armature_children", "bone_children", "type_expression_connect"
    ]

    # OBLY "_NAMES_NAME______" != "SPACE SPACE SPACE"

'''
import bpy

CONNECT_DATA = [
    'COPY_TRANSFORMS',
    'COPY_SCALE',
    'COPY_LOCATION',
    'COPY_ROTATION',
    'DRIVER_AVERAGE',
    'DRIVER_EXPRESSION'
]



# methods
def add_bone_constraint(type_cnstr, arm_parent, bone_parent, arm_child, bone_child):
    constraint_point = None
    if bone_child == "":
        # to object
        constraint_point = bpy.data.objects[arm_child].constraints.new(type=type_cnstr)
    else:
        # to pose bone
        constraint_point = bpy.data.objects[arm_child].pose.bones[bone_child].constraints.new(type=type_cnstr)

    if arm_parent == "":
        # object - parent
        #temp_data = bpy.data.objects[arm_child].constraints.items()
        #i = 0 if len(temp_data) == 0 else len(temp_data)-1
        constraint_point.target = bpy.data.objects[arm_parent]
        #del temp_data
    else:
        #temp_data = bpy.data.objects[arm_child].pose.bones[bone_child].constraints.items()
        #i = 0 if len(temp_data) == 0 else len(temp_data)-1
        # bone - parent
        constraint_point.target = bpy.data.objects[arm_parent]

        constraint_point.subtarget = bone_parent
        #del temp_data



def Driver_Average(chld, channel, parent_type, parent, data_path_Channel, var_name):
    pass

def Driver_Expression(chld, channel, vars_list_data, expression, type_expression):
    pass



def Import_Connection_Dict(file_path=str):
    f = open(file_path, 'r')
    data = f.readlines()
    f.close()

    line = ''
    i = 0
    while line != 'end':
        line = data[i]
        if line[0] == '/' or line[0] == '*' or line[0] == ' ' or line[0] == '' or line == 'start_block':
            i+=1
            continue
        slt = line.split(' ')
        if slt[0] == 'bone':
            # read and create 
            armature_parent = slt[1].replace('"','')
            bone_parent = slt[2].replace('"','')
            if slt[3] == 'bone':
                armature_child = slt[4].replace('"','')
                bone_child = slt[5].replace('"','')

                last_item = slt[6].split('//')
                for cnstr in last_item:
                    if cnstr.replace('\n','') == CONNECT_DATA[0]:
                        add_bone_constraint(
                            CONNECT_DATA[0],
                            armature_parent,
                            bone_parent,
                            armature_child,
                            bone_child
                        )
                    elif cnstr.replace('\n','') == CONNECT_DATA[1]:
                        add_bone_constraint(
                            CONNECT_DATA[1],
                            armature_parent,
                            bone_parent,
                            armature_child,
                            bone_child
                        )
                    elif cnstr.replace('\n','') == CONNECT_DATA[2]:
                        add_bone_constraint(
                            CONNECT_DATA[2],
                            armature_parent,
                            bone_parent,
                            armature_child,
                            bone_child
                        )
                    elif cnstr.replace('\n','') == CONNECT_DATA[3]:
                        add_bone_constraint(
                            CONNECT_DATA[3],
                            armature_parent,
                            bone_parent,
                            armature_child,
                            bone_child
                        )
                    elif cnstr.replace('\n','') == CONNECT_DATA[4]:
                        pass
                    elif cnstr.replace('\n','') == CONNECT_DATA[5]:
                        pass
            else:
                # object
                object_child = slt[4].replace('"','')

                last_item = slt[5].split('//')
                for cnstr in last_item:
                    if cnstr.replace('\n','') == CONNECT_DATA[0]:
                        add_bone_constraint(
                            CONNECT_DATA[0],
                            armature_parent,
                            bone_parent,
                            object_child,
                            ""
                        )
                    elif cnstr.replace('\n','') == CONNECT_DATA[1]:
                        add_bone_constraint(
                            CONNECT_DATA[1],
                            armature_parent,
                            bone_parent,
                            object_child,
                            ""
                        )
                    elif cnstr.replace('\n','') == CONNECT_DATA[2]:
                        add_bone_constraint(
                            CONNECT_DATA[2],
                            armature_parent,
                            bone_parent,
                            object_child,
                            ""
                        )
                    elif cnstr.replace('\n','') == CONNECT_DATA[3]:
                        add_bone_constraint(
                            CONNECT_DATA[3],
                            armature_parent,
                            bone_parent,
                            object_child,
                            ""
                        )
                    elif cnstr.replace('\n','') == CONNECT_DATA[4]:
                        pass
                    elif cnstr.replace('\n','') == CONNECT_DATA[5]:
                        pass 
        i+=1
    
    data.clear()
    del data