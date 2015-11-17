
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

skipPaths = ["!workday","!points","!template","!testcode","!uniqvals"]
skipData = ["Line_gen.shp","Point_ge.shp","PosnLine.shp","Workday.shp"]

print "Processing "+searchpath+"..."

last_folder = "" 

countLayers = 0            

for fc in inventory_data(searchpath, "FeatureClass"):
    desc = arcpy.Describe(fc)
    typ = desc.shapeType
    name = desc.baseName
    head, folder = os.path.split(desc.path)
    
    print "\t"+name.upper()
    for prop in ["baseName","catalogPath","dataElementType","dataType","extension","file","name","path"]:
        print "\t"+prop+": "+getattr(desc, prop)
    fields = desc.fields
    for field in fields:
        for fprop in ["Name","Length","Type","Scale"]:
            print "\t\t"+fprop+": "+str(getattr(field, fprop))
        print
    print
        
    if folder != last_folder:
        print
        print folder.upper()
    
    countLayers += 1
    stopAt = 4
    if countLayers == stopAt:
        print "Stopped at " + str(stopAt) + " layers processed."
        break
 
print "Processed " + str(countLayers) + " layers."
