# Source Blender Exporter
Tool for export static qc/smd to fbx for Blender 2.8+

# Necessary
install Blender Source Tool https://developer.valvesoftware.com/wiki/Blender_Source_Tools

# Setup
* 1 Open Blender preferences/addons
* 2 click install 
* 3 select script .zip/open and activate
# How it works

* 1 delete everything from the scene, and leave only the cube
* 2 select cube and go to object/Exporter QC/SMD to FBX

# Main Settings

* 1 Path to import all models folders (warning: your models should be sorted into folders each!)
* 2 Path to export folder
* 3 New Rotate for root Armature
* 4 Global Scale for FBX export
* 5 Custom prefix for files `modelname.fbx` or `prefix_modelname.fbx`
* 6 Import .qc? Import only qc files in folders
* 7 Use suffix? Suffix it's `.ModelFromBlender.fbx`: `modelname.fbx` or `modelname.ModelFromBlender.fbx`
* 8 Physics Collision - import collision model (`only for SMD method`)
* 9 Max Files Export - max folders in import path for export 
* 10 Start Export!

# Warning
This tool does not import or export animation/ only for static models!
