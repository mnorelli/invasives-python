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
print searchpath
 
def inventory_data(workspace, datatypes):
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
    """
    for path, path_names, data_names in arcpy.da.Walk(
            workspace, datatype=datatypes):
        for data_name in data_names:
            yield os.path.join(path, data_name)


fc_copy_path = r"O:\gis_projects\_Marin\EPMT_2015 - Copy\xxOffset"
            
 
for fc in inventory_data(searchpath, "FeatureClass"):
    desc = arcpy.Describe(fc)
    typ = desc.shapeType
    name = desc.baseName
    head, folder = os.path.split(desc.path)
    print folder.upper() + " " + name + " " + typ
    
    # Check for OFFSET
    fieldList = arcpy.ListFields(fc)
    for field in fieldList:
        if str.lower(str(field.name)) == "offset":
            ## open cursor, search through values
            #arcpy.MakeFeatureLayer_management ("C:/data/data.mdb/states", "stateslyr")
            #arcpy.SelectLayerByAttribute_management ("stateslyr", "NEW_SELECTION", " [NAME] = 'California' ")
            ## get value of OFFSET_M and OFFSET_AZ
            #xOffset = 0.001
            #yOffset = 0.001            
            #u = x + r*sin(a) 
            #v = y + r*cos(a)
            
            # make a copy which will have its coordinates moved (and can be compared with original)
            fc2 = fc_copy_path + "\\" + folder.upper() + "_" + name
            if arcpy.Exists(fc2):
                arcpy.Delete_management(fc2)
            print "Copying "+fc2
            arcpy.Copy_management(fc,fc2)
            # select OFFSET_M > 0 
            # Perform the move
            #with arcpy.da.UpdateCursor(fc2, ["SHAPE@XY"]) as cursor:
                #for row in cursor:
                    #cursor.updateRow([[row[0][0] + xOffset,row[0][1] + yOffset]])            