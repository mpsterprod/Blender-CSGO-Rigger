# Blender CSGO Rigger tool
Blender Addon for Auto Create Rigs for CSGO Models!

# Wont work without
Blender Source Tool https://developer.valvesoftware.com/wiki/Blender_Source_Tools

# Setup
* 1 Open Blender preferences/addons
* 2 Click install 
* 3 select script `mp_csgo_rigging.zip`/open and activate it

# How it works

# * Default MP RIG

* 1 Goto to in the viewport, on the right side of the panel, the `CSGO` category
* 2 Set Player Folder your decompiled files `.smd` files`-->> \models\player\custom_player\legacy\`
* 3 Set Export folder
* 4 Click to `Start Rigging!`

![image](https://github.com/mpsterprod/Blender-CSGO-Rigger/blob/master/misc/newwwwwwwwww.png)

* -> the script creates a folder with the name of the character
* -> `SkeletalMesh_NameCharacter.fbx` - for import to Game Engine (Unreal Engine and other)
* -> `rig_NameCharacter.blend` - this blender rig file

![image](https://github.com/mpsterprod/Blender-CSGO-Rigger/blob/master/misc/skeletal_mesh.png)

# * CUSTOM USER RIG
* 1 specify names
* 2 specify Python Connection script in your USER_RIG.blend

# Rules Python Script
* main function name and arguments
```py
'''
    /*
        MAIN FUNC IN MODULE
    */
'''
def csgo_rig_build(
        character_name='',
        # rig
        rig_collection_name='',
        rig_armature_name='',
        # skeletal mesh
        deform_armature_name='',
        meshes = []
    ):
    '''
    1) create collections and link's
        `character name`
        
        - Mesh -- all objects meshes
        
        - Skeleton -- deform armature
        
        - `Rig` # from append collection
    
    2) create constraints in `deform_armature`
    
    3) return True in not error
    
    '''
```

# * how it works from the inside.
* 1 the model is imported, the root bone is edited - SkeletalMesh is exported as FBX,
* 2 then your rig with USER_Rig is added from USER_Rig.blend/Collections/my_new_csgo_rig
* 3 also adds the python script that you specified
-- the function is being called!
```py
csgo_rig_build(character_name='', rig_collection_name='', rig_armature_name='', deform_armature_name='', meshes = [])
```
--- the appropriate arguments are submitted so that they can be used!!
* 4 Save Rig as .blend and next iterate...

![image](https://github.com/mpsterprod/Blender-CSGO-Rigger/blob/master/misc/custom_rig.png)

# Export Animation
# * 1 BAKE ANIMATION
* Go to deform Armature as POSE MODE
* Select all Bones
* Set KeyFrame in Fisrt and Last frame
* Click F3 and find ```Bake Action```
* Use only for selected bones
* Go to OBJECT MODE
# * 2 EXPORT
* Select deform Armature
* Set Settings:
```
Selected Objects = True
Armature/ ONLY DEFORM BONES = True
Armature/ Add Leaf Bones - FALSE !!!!!!!!!!!!!!!

bake animation - True
NLA strips - FALSE
All Actions - FALSE
```
* Export/FBX...

# Import to Game Engine
* Import this `SkeletalMesh` from Export Folder to Game Engine
* Import to Game Engine as Animation Asset - Not new Skeletal Mesh


# Main
* In future versions, it is planned to add add Weapons and Pov rigs.

![image](https://github.com/mpsterprod/Blender-CSGO-Rigger/blob/master/misc/unknown.png)

# Warning
Character rig only for `\models\player\custom_player\legacy\` MODELS! // old models not support this version!

This tool VERSION support ONLY FOR CHARACTERS!
