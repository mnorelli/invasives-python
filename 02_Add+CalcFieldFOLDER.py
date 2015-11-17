# COPIED FROM
# Describe_shps.py
#
# Get descriptions of all shapefiles in a directory structure. 
# Uses current diretory, or change searchpath to match directory to search.
# Returns a text list of the parent directory, the folders inside, and the name
# and shapefile type of each shapefile found.
#
# Edited from Stackexchange
# https://arcpy.wordpress.com/2012/12/10/inventorying-data-a-new-approach/
# 
# MCN 9/3/15
# Python 2.7.5
#
#  Edit 9/11/15:  Add field FOLDER and populate with name of source folder

import os, arcpy, re
from arcpy import env
from arcpy.sa import *

def inventory_data(workspace, datatypes,skips):
    """
    Generates full path names under a catalog tree for all requested
    datatype(s).
 
    Parameters:
    workspace: string
        The top-level workspace that will be used.
    datatypes: string | list | tuple
        Keyword(s) representing the desired datatypes. A single
        datatype can be expressed as a string, otherwise use
        a list or tuple. See arcpy.da.Walk documentation 
        for a full list.
    skips: list
        List of folders to ignore when processing
    """    
    for path, path_names, data_names in arcpy.da.Walk(
            workspace, datatype=datatypes):
        for skip in skips:
            if skip in path_names:
                path_names.remove(skip)
        for data_name in data_names:
            yield os.path.join(path, data_name)

ignoreFolders = ["work"]
 
searchpath = os.getcwd()
print "Processing " + searchpath + "..."

outFile = open("02_Add+CalcFieldFOLDER_RESULT.txt", "w")
countLayers = 0  

outFile.write(searchpath + "\n")

for fc in inventory_data(searchpath, "FeatureClass",ignoreFolders):
    desc = arcpy.Describe(fc)
    typ = desc.shapeType
    name = desc.baseName
    head, folder = os.path.split(desc.path)
    folder_cap = folder.upper()
    outFile.write(folder_cap + " " + name + " " + typ + "\n")
    
    fields = arcpy.ListFields(fc)
    for f in fields:
        if f.name == "Folder":
            arcpy.DeleteField_management(fc, ["Folder"])
            outFile.write("Deleted FOLDER from " + folder_cap + "\\" + name + "..." + "\n")
    
    arcpy.AddField_management(fc, "Folder", "TEXT", "", "" , 50)
    outFile.write("Added FOLDER to " + folder_cap + "\\" + name + "..." + "\n")
    
    #scrubbedfolder = ''.join(e for e in folder_cap if (e.isalnum() or e == " " or e == "_"))
    #scrubbedfolder = scrubbedfolder.replace("'", "_")
    scrubbedfolder = folder_cap.replace("@", "at")
    scrubbedfolder = scrubbedfolder.replace("'", "-")
    print scrubbedfolder
    arcpy.CalculateField_management(fc, "Folder", "".join(("'",scrubbedfolder,"'")), "PYTHON_9.3", "")
    outFile.write("Calculated FOLDER for " + folder_cap + "\\" + name + "..." + "\n\n")
    
    countLayers += 1
    stopAt = 1000
    if countLayers == stopAt:
        outFile.write("Stopped at " + str(stopAt) + " layers processed." + "\n")
        break
  
outFile.write("Processed " + str(countLayers) + " layers." + "\n")

outFile.close()    # This closes the text file
