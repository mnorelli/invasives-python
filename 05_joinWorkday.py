# MCN 9/14/15
# Python 2.7.5

import os, arcpy
from arcpy import env
from arcpy.sa import *

def inventory_data(workspace, datatypes):  
    for path, path_names, data_names in arcpy.da.Walk(
            workspace, datatype=datatypes):
        
        for skipPath in skipPaths:
            if skipPath in path_names:
                path_names.remove(skipPath)

        for skipDatum in skipData:
            if skipDatum in data_names:
                data_names.remove(skipDatum)
                # print "removed "+ skipDatum

        for data_name in data_names:
            yield os.path.join(path, data_name)
            
searchpath = os.getcwd()
outFile = open("05_joinWORKDAY_OUTPUT.txt", "w")

skipPaths = ["!workday","!points","!template","!testcode","!uniqvals","!points","!points_previous"]
skipData = ["Line_gen.shp","Point_ge.shp","PosnLine.shp","Workday.shp"]

print "Processing "+searchpath+"..."
outFile.write("Processing "+searchpath+"...\n")

last_folder = "" 

countLayers = 0            

for fc in inventory_data(searchpath, "FeatureClass"):
    desc = arcpy.Describe(fc)
    typ = desc.shapeType
    name = desc.baseName
    head, folder = os.path.split(desc.path)
        
    if folder != last_folder:
        print
        print folder.upper()
        outFile.write("\n")
        outFile.write(folder.upper() + "\n") 

    inFeatures = desc.catalogPath
    joinField = "TREAT_PLAN"
    joinTable = desc.path+"\Workday.shp"
    fieldList = ["Recorder","Workgroup","Workgroup2","SNAME","Work_Desc","TREAT_TYPE","TRADE_NM","AGT_APP_RT","ADJ_TRADE_","ADJ_AGT_AP","Total_USED"]
    
    print "Joining Workday to "+name
    outFile.write("Joining Workday to "+name+"\n")
    arcpy.JoinField_management (inFeatures, joinField, joinTable, joinField, fieldList)        
    
    
    countLayers += 1
    stopAt = 1000
    if countLayers == stopAt:
        print "Stopped at " + str(stopAt) + " layers processed."
        outFile.write("Stopped at " + str(stopAt) + " layers processed." + "\n")
        break
 
outFile.write("\Processed " + str(countLayers) + " layers.")
print "Processed " + str(countLayers) + " layers."
outFile.close()    # This closes the text file


