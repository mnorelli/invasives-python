# MCN 9/16/15
# Python 2.7.5

import os, arcpy

searchpath = os.getcwd()
outFile = open("01a_describe_shps_by_field_OUTPUT.txt", "w")
outFile.write(searchpath+"\n")
 
skipPaths = ["!workday","!points","!template","!testcode","!uniqvals","!points","!points_previous", "crosswalks","merge_point","merge_poly"]
skipData = ["Line_gen.shp","Point_ge.shp","PosnLine.shp","processCOJU.shp","processCOJU1.shp"]

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
findField = "Total_USED"

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
    
    fieldList = arcpy.ListFields(fc)   
    for field in fieldList:
        if (str.lower(str(field.name)) == str.lower(findField)):
            print line + "\t"+findField+"\tType: "+field.type
            outFile.write(line + "\t"+findField+"\tType: "+field.type+"\n")

   
    last_folder = folder
    
outFile.close()    # This closes the text file
