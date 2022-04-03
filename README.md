# Blender CSGO Rigger tool
Blender Addon for Auto Create Rigs for CSGO Models!

# Wont work without
Blender Source Tool https://developer.valvesoftware.com/wiki/Blender_Source_Tools

# Setup
* 1 Open Blender preferences/addons
* 2 Click install 
* 3 select script `mp_csgo_rigging.zip`/open and activate it

# How it works
* 1 Goto to in the viewport, on the right side of the panel, the `CSGO` category
* 2 Set Player Folder your decompiled files `.smd` files`-->> \models\player\custom_player\legacy\`
* 3 Set Export folder
* 4 Click to `Start Rigging!`

![image](https://github.com/mpsterprod/Blender-CSGO-Rigger/blob/master/misc/panel_screenshot.png)

* -> the script creates a folder with the name of the character
* -> `SkeletalMesh_NameCharacter.fbx` - for import to Game Engine (Unreal Engine and other)
* -> `rig_NameCharacter.blend` - this blender rig file

# Export Animation
`DONT RENAME ARMATURE OBJECT` -> `root` <- only
* Select Armature Object `root`
* Export/FBX -> toggle `selected only` and `bake animation`

# Import to Game Engine
* Import this `SkeletalMesh` from Export Folder to Game Engine
* Import to Game Engine as Animation Asset - Not new Skeletal Mesh


# Main
* In future versions, it is planned to add the ability to use custom RIG and connections to the skeleton.
* And add Weapons and Pov rigs.

![image](https://github.com/mpsterprod/Blender-CSGO-Rigger/blob/master/misc/rig_character_screenshot.png)

# Warning
This tool VERSION support ONLY FOR CHARACTERS!
