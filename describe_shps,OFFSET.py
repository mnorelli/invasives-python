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
#
# MCN 9/9/15
# Python 2.7.5

import os, arcpy

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

def FindField(fc,myField):
    fieldList = arcpy.ListFields(fc)
    for field in fieldList:
        if str.lower(str(field.name)) == str.lower(myField):
            print "    " + fc + " contains fieldname: " + myField
            
myField = "offset"
 
for fc in inventory_data(searchpath, "FeatureClass"):
    desc = arcpy.Describe(fc)
    typ = desc.shapeType
    name = desc.baseName
    head, folder = os.path.split(desc.path)
    print folder.upper() + " " + name + " " + typ
    FindField(fc,myField)