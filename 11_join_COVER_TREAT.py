# MCN 9/17/15
# Python 2.7.5

import os, arcpy

arcpy.env.overwriteOutput = True

searchpath = os.getcwd()
outFile = open("11_join_COVER_TREAT_OUTPUT.txt", "w")
outFile.write(searchpath+"\n")
 
skipPaths = ["!workday","!points","!template","!testcode","!uniqvals","!points","!points_previous", "crosswalks"]
skipData = ["Line_gen.shp","Point_ge.shp","PosnLine.shp","Workday.shp"]
fcType = "All"
dropFields = ['SNAME_1', 'Recorder_1', 'Workgrou_1', 'Workgrou_2', 'SNAME_12', 'Work_Des_1', 'TREAT_TY_1', 'TRADE_NM_1', 'AGT_APP__1', 'ADJ_TRADE1', 'ADJ_AGT__1', 'Total_US_1', 'TREAT_1']

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
    outFile.write("Processing "+line + "\n")
    print "Processing "+line    
        
    # JOIN TABLES
    inFeatures = fc
    joinField = "TREAT_TYPE"
    joinTable = "O:\gis_projects\_Marin\EPMT_2015_Process20150916\crosswalks\TREAT_TYPE.dbf"
    fieldList = ["TREAT"]
    arcpy.JoinField_management (inFeatures, joinField, joinTable, joinField, fieldList)    
    
    # JOIN TABLES
    inFeatures = fc
    joinField = "COVERCLS"
    joinTable = "O:\gis_projects\_Marin\EPMT_2015_Process20150916\crosswalks\COVERCLS.dbf"
    fieldList = ["COVERCALC"]
    arcpy.JoinField_management (inFeatures, joinField, joinTable, joinField, fieldList)     
        
    outFile.write("Deleting fields..." + "\n")
    print "Deleting fields..."
    arcpy.DeleteField_management(fc, dropFields)         
    
    arcpy.Delete_management("Layer")

    outFile.write("\n")
    print 

    countLayers += 1
    stopAt = 999
    if countLayers == stopAt:
        print "Stopped at " + str(stopAt) + " layers processed."
        break
   
    last_folder = folder
    
     
outFile.write("Processed " + str(countLayers) + " layers.")
print "Processed " + str(countLayers) + " layers."
outFile.close()    # This closes the text file
