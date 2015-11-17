# MCN 9/16/15
# Python 2.7.5

import os, arcpy

arcpy.env.overwriteOutput = True

searchpath = os.getcwd()
outFile = open("09_fix_SQ_METERS_OUTPUT.txt", "w")
outFile.write(searchpath+"\n")
 
skipPaths = ["!workday","!points","!template","!testcode","!uniqvals","!points","!points_previous"]
skipData = ["Line_gen.shp","Point_ge.shp","PosnLine.shp","Workday.shp","OccurTre_new.shp","OccurTr4_new.shp"]

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

fcType = "Point"

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
    
    output = desc.path+"\\"+name+"_new.shp"
    if arcpy.Exists(output): 
        arcpy.DeleteFeatures_management(output)     
        
    line = folder.upper() + " " + name + " " + typ
    outFile.write(str(countLayers+1)+": Processing "+line + "\n")
    print str(countLayers+1)+": Processing "+line
    
    arcpy.MakeFeatureLayer_management(fc, "Layer", "", "", "")
    
    arcpy.SelectLayerByAttribute_management("Layer", "NEW_SELECTION", "\"SQ_METERS\" = 0 and \"LENGTH\" = 0 and \"WIDTH\" = 0")
    selected = int(arcpy.GetCount_management("Layer").getOutput(0)) 
    outFile.write("\tFound "+str(selected)+" records where SQM,L,W are zero"+ "\n")
    print "\tFound "+str(selected)+" records where SQM,L,W are zero"

    if selected > 0:
        arcpy.CalculateField_management("Layer", "SQ_METERS", "1")
        outFile.write("\tSet to SQM = 1..."+ "\n")
        print "\tSet to SQM = 1..."
    
    arcpy.SelectLayerByAttribute_management("Layer", "NEW_SELECTION",  "\"SQ_METERS\" = 0 and (\"LENGTH\" > 0 or \"WIDTH\" > 0 )")
    selected = int(arcpy.GetCount_management("Layer").getOutput(0)) 
    outFile.write("\tFound "+str(selected)+" records where SQM is 0 but L or W are nonzero"+ "\n")
    print "\tFound "+str(selected)+" records where SQM is 0 but L or W are nonzero"

    if selected > 0:
        arcpy.CalculateField_management("Layer", "SQ_METERS", "[LENGTH] * [WIDTH]")    
        outFile.write("\tSet to L*W..."+ "\n")
        print "\tSet to L*W..."    
   
    if selected > 0: 
        arcpy.SelectLayerByAttribute_management("Layer", "CLEAR_SELECTION")          
        arcpy.CopyFeatures_management("Layer", output)
        outFile.write("\tCreated "+line+"_new.shp"+ "\n")
        print "\tCreated "+line+"_new.shp" 
        
    
    arcpy.Delete_management("Layer")

    outFile.write("\n")
    print 
    
    #fieldList = arcpy.ListFields(fc)   
    #for field in fieldList:
        #if (str.lower(str(field.name)) == str.lower(findField)):
            
            #print "Changing "+folder+"\t"+name+"..."
            #outFile.write("Changing "+folder+"\t"+name+"...\n")
        
    countLayers += 1
    stopAt = 6999
    if countLayers == stopAt:
        print "Stopped at " + str(stopAt) + " layers processed."
        break
   
    last_folder = folder
    
     
outFile.write("Processed " + str(countLayers) + " layers.")
print "Processed " + str(countLayers) + " layers."
outFile.close()    # This closes the text file
