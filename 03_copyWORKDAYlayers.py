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
# Search for field: http://gis.stackexchange.com/questions/26892/search-if-field-exists-in-feature-class
# Adjust point: http://gis.stackexchange.com/questions/65959/how-to-move-offset-point-locations-using-modelbuilder-or-arcpy
# Math on OFFSET to XY:  
#
# MCN 9/9/15
# Python 2.7.5

import os, arcpy
from arcpy import env
from arcpy.sa import *

searchpath = os.getcwd()
outFile = open("03_copyWORKDAYlayers_RESULT.txt", "w")

def inventory_data(workspace, datatypes):  
    for path, path_names, data_names in arcpy.da.Walk(workspace, datatype=datatypes, type=fcType):
        
        for skipPath in skipPaths:
            if skipPath in path_names:
                path_names.remove(skipPath)

        for skipDatum in skipData:
            if skipDatum in data_names:
                data_names.remove(skipDatum)
                # print "removed "+ skipDatum

        for data_name in data_names:
            yield os.path.join(path, data_name)

skipPaths = ["!workday","!points","!template","!testcode","!uniqvals","!points","!points_previous", "crosswalks","merge_poly","merge_point"]
skipData = ["Line_gen.shp","Point_ge.shp","PosnLine.shp","processCOJU.shp","processCOJU1.shp"]


outpath = "!workday"
countLayers = 0 
fcType = "Point"

outFile.write(searchpath+"\n"+"\n")
print searchpath

for fc in inventory_data(searchpath, "FeatureClass"):
    desc = arcpy.Describe(fc)
    typ = desc.shapeType
    name = desc.baseName
    head, folder = os.path.split(desc.path)

    if name == "Workday":
        
        print folder.upper()
    
        fc2 = outpath + "\\" + folder.upper() + "_" + name
        fieldList = arcpy.ListFields(fc)
        
        # LABEL FCs WITH "AGT_APP_RT" THAT ARE string INSTEAD OF single
        for field in fieldList:
            if (str.lower(str(field.name)) == str.lower("AGT_APP_RT")) and field.type == "String":
                fc2 = outpath + "\\" + "STR_"+ folder.upper() + "_" + name
                
        if arcpy.Exists(fc2):
            arcpy.Delete_management(fc2)
        outFile.write("Copying "+fc+"\n")
        arcpy.Copy_management(fc,fc2)      
    
        countLayers += 1

 
outFile.write("\nCopied " + str(countLayers) + " layers.")
print "\nCopied " + str(countLayers) + " layers."
outFile.close()    # This closes the text file


