# MCN 9/17/15
# Python 2.7.5

import os, arcpy

arcpy.env.overwriteOutput = True

searchpath = os.getcwd()
outFile = open("13_calc_CARRVOL_ME.txt", "w")
outFile.write(searchpath+"\n")
 
skipPaths = ["!workday","!points","!template","!testcode","!uniqvals","!points","!points_previous", "crosswalks","merge_poly","merge_point"]

# Folders that contain two feature classes
skipPaths.extend(["20150827_GTT_CR","PICO_COJU_8-24-2015","PICO_COJU_8-25-2015"])

skipData = ["Line_gen.shp","Point_ge.shp","PosnLine.shp","Workday.shp"]
fcType = "All"
#dropFields = ['SNAME_1', 'Recorder_1', 'Workgrou_1', 'Workgrou_2', 'SNAME_12', 'Work_Des_1', 'TREAT_TY_1', 'TRADE_NM_1', 'AGT_APP__1', 'ADJ_TRADE1', 'ADJ_AGT__1', 'Total_US_1', 'TREAT_1']

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
    
    sumDENSITY_dbf = desc.path+"\\sumDENSITY.dbf"    
    processCOJU_shp = desc.path+"\\processCOJU.shp"
    
    try:
        
        # Process: Select
        arcpy.Select_analysis(fc, processCOJU_shp, "\"TREAT\" = 'f' AND \"PCTTREATED\" = 100")
        outFile.write(line + "\tSelected fields...\n")
        print line + "\tSelected fields..."  
        
        # Process: Summary Statistics
        arcpy.Statistics_analysis(processCOJU_shp, sumDENSITY_dbf, "DENSITY SUM", "TREAT_PLAN")
        outFile.write(line + "\tSummarized...\n")
        print line + "\tSummarized..."  
        
        # Process: Join Field
        arcpy.JoinField_management(fc, "TREAT_PLAN", sumDENSITY_dbf, "TREAT_PLAN", "SUM_DENSIT")
        outFile.write(line + "\tJoined...\n")
        print line + "\tJoined..."   
        
        # Process: Calculate
        arcpy.CalculateField_management(fc, "SUMDENSITY", "[SUM_DENSIT]")
        outFile.write(line + "\tCalculated SUMDENSITY...\n")
        print line + "\tCalculated SUMDENSITY..."   
        
        # Process: Clean up
        arcpy.DeleteField_management(fc,["SUM_DENSIT","SUMDENSIT", "SUM_DENS_1"])    
        arcpy.Delete_management(sumDENSITY_dbf)
        arcpy.Delete_management(processCOJU_shp)
        outFile.write(line + "\tCleaned up...\n")
        print line + "\tCleaned up..."       
        
        # Process: CARRVOL_ME
        arcpy.CalculateField_management(fc, "CARRVOL_ME", "round([Total_USED]*( [DENSITY]/ [SUMDENSITY]),2)")
        outFile.write(line + "\tCARRVOL_ME...\n")
        print line + "\tCARRVOL_ME..."
        
    except:
        outFile.write(line + "\tSkipping...\n")
        print line + "\tSkipping..."         

    countLayers += 1
    stopAt = 999
    if countLayers == stopAt:
        print "Stopped at " + str(stopAt) + " layers processed."
        break
   
    last_folder = folder
    
     
outFile.write("Processed " + str(countLayers) + " layers.")
print "Processed " + str(countLayers) + " layers."
outFile.close()    # This closes the text file
