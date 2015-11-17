# MCN 9/16/15
# Python 2.7.5

import os, arcpy

import gc
gc.collect()

# Load required toolboxes
#arcpy.ImportToolbox("C:/Program Files (x86)/ET SpatialTechniques/ET GeoWizards 11.1 for ArcGIS 10.2/ET GeoWizards.tbx")

searchpath = os.getcwd()
outFile = open("01b_fix_PCTTREATED_OUTPUT.txt", "w")
outFile.write(searchpath+"\n")
 
skipPaths = ["!workday","!points","!template","!testcode","!uniqvals"]
skipData = ["Line_gen.shp","Point_ge.shp","PosnLine.shp"]

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

## USES ETGEOWIZ TOOLBOX to CHANGE STRUCTURE OF FIELD
#findField = "PCTTREATED"
#findFieldTyp = "String"
#findFieldLen = "60"
#findFieldScal = "0"
#newTyp = "SHORT"
#newLen = "3"
#newScal = "0"

for fc in inventory_data(searchpath, "FeatureClass"):
    desc = arcpy.Describe(fc)
    typ = desc.shapeType
    name = desc.baseName
    head, folder = os.path.split(desc.path)
    
    if arcpy.Exists(desc.path+"\OccurFix1.shp"):       
        arcpy.Delete_management(desc.path+"\OccurFix1.shp")
        print "Temporary file removed.  Restart process"
        break
    
    if folder != last_folder:
        print
        outFile.write("\n") 
        
    line = folder.upper() + " " + name + " " + typ

    outFile.write(line + "\n")
    print line
    
    fieldList = arcpy.ListFields(fc)   
    for field in fieldList:
        if (str.lower(str(field.name)) == str.lower(findField)):

            
            print "Changing "+folder+"\t"+name+"..."
            outFile.write("Changing "+folder+"\t"+name+"...\n")
            
            
            ## USES ETGEOWIZ TOOLBOX to CHANGE STRUCTURE OF FIELD
            ## Local variables: 
            #outfile1 = desc.path+"\OccurFix1.shp"
            #outfile2 = desc.path+"\\" + name + "_new.shp"
            
            ## Process: Rename Total_Mix_ to Total_USED
            #arcpy.gp.toolbox = "C:/Program Files (x86)/ET SpatialTechniques/ET GeoWizards 11.1 for ArcGIS 10.2/ET GeoWizards.tbx";
            #arcpy.gp.ET_GPRedefineFields(fc, outfile1, findField+" x "+findFieldLen+" "+findFieldScal)  ## change existing field name to X
            
            ## Process: Add Field AGT_APP_RT as Float
            #arcpy.AddField_management(outfile1, findField, newTyp, newLen, newScal, "", "", "NULLABLE", "NON_REQUIRED", "")  ## re-add field correctly        
            
            ## Process: Calculate Field
            #arcpy.CalculateField_management(outfile1, findField, "int(str(!x!).split(\"%\")[0])", "PYTHON_9.3", "")   ## make the new field equal to the old field 
            ### HARDCODED TO CONVERT STRING TO NUMBER
            
            ## Process: Order Fields
            #arcpy.gp.toolbox = "C:/Program Files (x86)/ET SpatialTechniques/ET GeoWizards 11.1 for ArcGIS 10.2/ET GeoWizards.tbx";
            #arcpy.gp.ET_GPOrderFields(outfile1, outfile2, "SNAME","EARLY_DETE","OLDNEW","PHENO","OFFSET","OFFSET_M","OFFSET_AZ","SQ_METERS","LENGTH","WIDTH","COVERCLS","PCTTREATED","PLANTSA","COUNTPLANT","TREAT_PLAN","NOTES","Rcvr_Type","GPS_Date","Feat_Name","Datafile","Data_Dicti","Northing","Easting","Point_ID","Folder","Recorder","Workgroup","Workgroup2","SNAME_1","Work_Desc","TREAT_TYPE","TRADE_NM","AGT_APP_RT","ADJ_TRADE_","ADJ_AGT_AP","Total_USED")
            
         
            
            if arcpy.Exists(desc.path+"\OccurFix1.shp"):       
                arcpy.Delete_management(desc.path+"\OccurFix1.shp")
           
            
            print line + "\t"+findField+"\tType: "+field.type
            outFile.write(line + "\t"+findField+"\tType: "+field.type+"\n")

    countLayers += 1
    stopAt = 1
    if countLayers == stopAt:
        print "Stopped at " + str(stopAt) + " layers processed."
        break
   
    last_folder = folder
    
outFile.close()    # This closes the text file
