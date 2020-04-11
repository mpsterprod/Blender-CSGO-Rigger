install addon in blender
open blender and go to preference/addons/install
select .zip and install/ activate in addons

Necessary:
######################################################################################################
################ for the script to work you need to install the "blender source tool" ################ 
######################################################################################################

###########
# create export:
create cube
select cube
go to "object" menu and click to "Exporter QC/SMD to FBX"


############
warning:       this tool does not import or export animation/ only for static models
############


if the folder where you specified no .smd and .qc, script stop or next find files in next folder!
- please make sure that each model is in its own folder! 
- since the script checks folders and files in them, 
- but does not check the files that are in the folder that you specified,
- only folders!

#############
minuses .qc imports:
-when importing fbx to some software - there may be errors or the file will not open at all in such as maya
-this happens because. when importing .qc- animations are imported together - this can cause buggies
###########
RECOMENDATION:

use decompile crowbar settings "sort in folders"
so that each model is in its own folder

###########################
set export path

# and$
rotation - for all imports obdate world rotate model (object mode)

prefix - prefix_  exports files : name.ModelFromBlender.fbx -------- prefix_name.ModelFromBlender.fbx

global scale - FBX world scale export

import qc? - import only qc from all folders

Use Suffix? - use name + .ModelFromBlender.fbx ? or not?

physics collision(only for smd method) - import collision model

max_files - maximum number of folders in a folder for importing and checking

go to export!


##############################
# script made by mp mpsterprod
# youtube: https://www.youtube.com/channel/UCXvI8JRMsskPQrpQoSLeeBA
# discord: MP#9395
# github https://github.com/mpsterprod
##############################








