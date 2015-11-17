# MCN 9/15/15
# Python 2.7.5

import os, arcpy
from arcpy import env
from arcpy.sa import *

searchpath = os.getcwd()
outFile = open("07_copyALLPOINTS.txt", "w")
outFile.write(searchpath+"\n")

skipPaths = ["!workday","!points","!template","!testcode","!uniqvals","!points","!points_previous"]
skipData = ["Line_gen.shp","Point_ge.shp","PosnLine.shp","Workday.shp"]


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

countLayers = 0            
last_folder = "" 
outpath = "!points"

try:  
    os.makedirs(outpath)  
except OSError:  
    if os.path.exists(outpath):   
        pass  
    else:  
        raise 

fcType = "Point"

for fc in inventory_data(searchpath, "FeatureClass"):
    desc = arcpy.Describe(fc)
    typ = desc.shapeType
    name = desc.baseName
    head, folder = os.path.split(desc.path)

    #if folder != last_folder:
        #print
        #print folder.upper()
        #outFile.write("\n")
        #outFile.write(folder.upper() + "\n") 

    fc2 = outpath + "\\" + folder.upper() + "_" + name

    if arcpy.Exists(fc2):
        arcpy.Delete_management(fc2)
    print "Copying "+folder.upper() + "_" + name
    outFile.write("Copying "+folder.upper() + "_" + name+"\n")
    arcpy.Copy_management(fc,fc2)      

    countLayers += 1
    #last_folder = folder
 
print "\nCopied " + str(countLayers) + " layers."
outFile.write("\nCopied " + str(countLayers) + " layers.")
outFile.close()  


