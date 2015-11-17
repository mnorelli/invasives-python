# MCN 9/14/15
# Python 2.7.5

import os, arcpy

searchpath = os.getcwd()
outFile = open("04_locateOldWORKDAY_OUTPUT.txt", "w")
outFile.write(searchpath)
 
skipPaths = ["!workday","!points","!template","!testcode","!uniqvals","!points","!points_previous"]
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

for fc in inventory_data(searchpath,"FeatureClass"):
    desc = arcpy.Describe(fc)
    typ = desc.shapeType
    name = desc.baseName
    head, folder = os.path.split(desc.path)
    
    
    if folder != last_folder:
        print
        print folder.upper()
        outFile.write("\n"+folder.upper() + "\n") 
        
    print "\t" + name + typ
    outFile.write("\t" + name + "\t"+typ+"\n") 
    
    if name == "Workday":
        process = 0
        fieldList = arcpy.ListFields(fc)
        for field in fieldList:
            if str.lower(str(field.name)) == str.lower("Total_Mix_"):
                process += 1
            if str.lower(str(field.name)) == str.lower("Total_USED"):
                process += 2
                Totused_total=0
                Totmix_total = 0
        
        if process == 3:
            arcpy.CalculateField_management(fc,"Total_USED", """!{}!""".format("Total_Mix_"), "PYTHON_9.3")
            Totused_total=0
            Totmix_total = 0
            with arcpy.da.SearchCursor(fc, "Total_USED") as cursor:
                for row in cursor:
                    Totused_total = Totused_total + row[0]
            with arcpy.da.SearchCursor(fc, "Total_Mix_") as cursor:
                for row in cursor:
                    Totmix_total = Totmix_total + row[0]            
            print "Sum Total_USED: "+ str(Totused_total) + "Sum Total_Mix_: "+str(Totmix_total)
            outFile.write("Sum Total_USED: "+ str(Totused_total) + "Sum Total_Mix_: "+str(Totmix_total) + "\n")             
        
        elif process == 1:    
            arcpy.AddField_management(fc, "Total_USED", "FLOAT", 7, 2)
            arcpy.CalculateField_management(fc,"Total_USED", """!{}!""".format("Total_Mix_"), "PYTHON_9.3")
            Totused_total, Totmix_total = 0
            with arcpy.da.SearchCursor(fc, "Total_USED") as cursor:
                for row in cursor:
                    Totused_total = Totused_total + row[0]
            with arcpy.da.SearchCursor(fc, "Total_Mix_") as cursor:
                for row in cursor:
                    Totmix_total = Totmix_total + row[0]                     
            print "Total_USED added.  Sum: "+ str(Totused_total) + "Sum Total_Mix_: "+str(Totmix_total)
            outFile.write("Total_USED added.  Sum: "+ str(Totused_total) + "Sum Total_Mix_: "+str(Totmix_total) + "\n")
            
        elif process == 2:
            Totused_total = 0
            with arcpy.da.SearchCursor(fc, "Total_USED") as cursor:
                for row in cursor:
                    Totused_total = Totused_total + row[0]
            print "Sum Total_USED: "+ str(Totused_total)
            outFile.write("Sum Total_USED: "+ str(Totused_total) + "\n")
            
            # FREQUENCY
            # Set local variables
            inTable = desc.catalogPath
            outTable = r'in_memory\name_FREQ'
            frequencyFields = ["TREAT_TYPE"]
            summaryFields = ["Total_USED"]
             
            # Execute Frequency
            arcpy.Frequency_analysis(inTable, outTable, frequencyFields, summaryFields)
            
            # Print 
            fields = ["TREAT_TYPE","Total_USED"]     
            with arcpy.da.SearchCursor(outTable, fields) as cursor:
                for row in cursor:
                    print('{0}, {1}'.format(row[0], row[1]))
                    outFile.write('{0}, {1}'.format(row[0], row[1])+"\n")
            
            arcpy.management.Delete(outTable) 
            
    

    last_folder = folder
    
outFile.close() 