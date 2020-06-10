# Source Blender Exporter
Tool created to convert models from qc/smd to fbx for Blender 2.8+

# Wont work without
Blender Source Tool https://developer.valvesoftware.com/wiki/Blender_Source_Tools

# Setup
* 1 Open Blender preferences/addons
* 2 Click install 
* 3 select script mpSourceExporter.zip/open and activate it

# How it works
* 1 Delete everything from the scene **except cube**
* 2 select cube and go to menu Object->Exporter->QC/SMD to FBX

# Main Settings
* 1 Path to qc smd folders (warning: your models should stay in their own folders like it is originally)
* 2 Path to export folder
* 3 Root Rotation Offset
* 4 Global Scale for FBX export
* 5 Custom prefix for files `modelname.fbx` or `prefix_modelname.fbx`
* 6 Import .qc? Import only qc files in folders
* 7 Use suffix? Suffix it's `.ModelFromBlender.fbx`: `modelname.fbx` or `modelname.ModelFromBlender.fbx`
* 8 Physics Collision - import collision model (`only for SMD method`)
* 9 Max Files Export - max folders in import path for export 
* 10 Start Export!

# Warning
This tool doesn't import or export animations. Its only for models!
