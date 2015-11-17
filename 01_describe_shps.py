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

import os, arcpy

searchpath = os.getcwd()
outFile = open("01_describe_shps_OUTPUT.txt", "w")
outFile.write(searchpath+"\n")
 
skipPaths = ["!workday","!points","!template","!testcode","!uniqvals","!points","!points_previous", "crosswalks"]
skipData = ["Line_gen.shp","Point_ge.shp","PosnLine.shp","Workday.shp"]

def inventory_data(workspace, datatypes):  
    for path, path_names, data_names in arcpy.da.Walk(workspace, datatype=datatypes, type=fcType):
        
        for skipPath in skipPaths:
            if skipPath in path_names:
                path_names.remove(skipPath)

        for skipDatum in skipData:
            if skipDatum in data_names:
                data_names.remove(skipDatum)

        for data_name in data_names:
            yield os.path.join(path, data_name)
           
fcType = "All"
countLayers = 0  
last_folder = ""


for fc in inventory_data(searchpath, "FeatureClass"):
    desc = arcpy.Describe(fc)
    typ = desc.shapeType
    name = desc.baseName
    head, folder = os.path.split(desc.path)
    
    if folder != last_folder:
        print
        outFile.write("\n") 
        
    line = folder.upper() + " " + name + " " + typ

    outFile.write(line + "\n")
    print line
    
    #fieldList = arcpy.ListFields(fc)   
    #for field in fieldList:
        #if (str.lower(str(field.name)) == str.lower(findField)):
            #print line
            #outFile.write(line + "\n")

    countLayers += 1
    last_folder = folder
    
print 
print "Processed " + str(countLayers) + " layers."
outFile.write("\nProcessed " + str(countLayers) + " layers.")
outFile.close()    # This closes the text file
