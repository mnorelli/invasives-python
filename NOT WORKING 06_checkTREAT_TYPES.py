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
outFile = open("NOT WORKING 06_checkTREAT_TYPES.txt", "w")
outFile.write(searchpath+"\n")

skipPaths = ["!workday","!points","!template","!testcode","!uniqvals"]
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

            
last_folder = ""   
countLayers = 0   

fcType = "All"

findField = "TREAT_TY_1"

# Create in memory container for all records across the file system processed below
arcpy.CreateTable_management('in_memory','stored_records')
arcpy.AddField_management(r"in_memory\stored_records", "REC", "TEXT")
         
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
    
    print "   " + name + " " + typ
    outFile.write("   " + name + " " + typ + "\n")    


    # Check that fields exist   
    
    process = 0
    fieldList = arcpy.ListFields(fc)
    for field in fieldList:
        if str.lower(str(field.name)) == str.lower(findField):
            process += 1

  
    if process == 0:
        print "Couldn't find "+ findField
        outFile.write("Couldn't find "+findField+"\n")
        
    else:        
        # Set local variables
        inTable = desc.catalogPath
        outTable = r'in_memory\name_FREQ'
        frequencyFields = [findField]
        summaryFields = []
         
        # Execute Frequency
        arcpy.Frequency_analysis(inTable, outTable, frequencyFields, summaryFields)
        
        # Print 
        rows = arcpy.SearchCursor(outTable)      
        for row in rows:    
            rVal = row.getValue(findField)
            arcpy.CalculateField_management(r'in_memory\stored_records', "REC", 
                                            """!{}!""".format(findField), "PYTHON_9.3")            
            print str(rVal)
            outFile.write(str(rVal))
        
        arcpy.management.Delete(r'in_memory\name_FREQ') 
        
        # Next...
        # select only foliar treatments
  
            
    countLayers += 1
    stopAt = 1
    if countLayers == stopAt:
        print "Stopped at " + str(stopAt) + " layers processed."
        outFile.write("Stopped at " + str(stopAt) + " layers processed." + "\n")
        break
    
    last_folder = folder

print
print "Summary..."
outFile.write("\nSummary...\n")

sum_rows = arcpy.SearchCursor(r'in_memory\stored_records')
for sum_row in sum_rows:    
    rVal2 = row.getValue('REC')          
    print str(rVal2)
    outFile.write(str(rVal2))    
        
arcpy.management.Delete(r'in_memory\stored_records') 

outFile.close()    # This closes the text file
