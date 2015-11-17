# MCN 9/17/15
# Python 2.7.5

import os, arcpy, numpy

arcpy.env.overwriteOutput = True

# ***********  CONFIGURE YOUR FIELDS AND FEATURE CLASS TYPES  ***********

frequencyFields = ["TREAT_PLAN","PCTTREATED","COVERCLS","TREAT_TYPE","SNAME"]
fcType = "All"
# skipData = ["Line_gen.shp","Point_ge.shp","PosnLine.shp"]
skipData = ["Line_gen.shp","Point_ge.shp","PosnLine.shp","processCOJU.shp","processCOJU1.shp"]

# ***********  CONFIGURE YOUR FIELDS AND FEATURE CLASS TYPES  ***********

searchpath = os.getcwd()
fieldsOut = ','.join(frequencyFields)
outFile = open("10_FREQUENCY_folders_"+fieldsOut+"_OUTPUT.txt", "w")
outFile.write(searchpath+"\n")
print searchpath

skipPaths = ["!workday","!points","!template","!testcode","!uniqvals","!points","!points_previous", "crosswalks","merge_point","merge_poly"]


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

def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})
    
def unique_values_2(table, field):
    data = arcpy.da.TableToNumPyArray(table, [field])
    return numpy.unique(data[field])

def _print(l):
    outFile.write("".join(["{:>12}".format(i) for i in l]))
    outFile.write("\n")
    print("".join(["{:>12}".format(i) for i in l]))

#def pprint_fields(table):
    #""" pretty print table's fields and their properties """
    #def _print(l):
        #print("".join(["{:>12}".format(i) for i in l]))
    #atts = ['FREQUENCY','TREAT_TYPE','SNAME','Folder']
    #_print(atts)
    #for f in arcpy.ListFields(table):
        #_print(["{:>12}".format(getattr(f, i)) for i in atts])

countLayers = 0  
last_folder = ""

for fc in inventory_data(searchpath, "FeatureClass"):
    desc = arcpy.Describe(fc)
    typ = desc.shapeType
    name = desc.baseName
    head, folder = os.path.split(desc.path)
    full = desc.catalogPath
    fullNoExt = desc.path+"\\"+desc.baseName
      
    #if folder != last_folder:
        #print 
        #print folder.upper()
        #outFile.write("\n"+folder.upper()+"\n") 
        
    outFile.write(folder.upper()+"\t"+name+" "+typ+"\n") 
    print folder.upper()+"\t"+name+" "+typ   

    if name == "Workday":
        inTable = full    
        outTable = desc.path+"\\"+desc.baseName+"_FREQ.dbf"
        editfrequencyFields = frequencyFields
        editfrequencyFields.remove("PCTTREATED")
        editfrequencyFields.remove("COVERCLS")
        arcpy.Frequency_analysis(inTable, outTable, editfrequencyFields)
        
        rows = arcpy.SearchCursor(outTable,fields="FREQUENCY;SNAME;TREAT_TYPE;TREAT_PLAN",sort_fields="SNAME A")
        atts = ["FREQUENCY","SNAME","TREAT_TYPE","TREAT_PLAN"]
        _print(atts)    
        for row in rows:
            print("\t{0}\t{1}\t{2}\t{3}".format(row.getValue("FREQUENCY"),row.getValue("SNAME"),row.getValue("TREAT_TYPE"),row.getValue("TREAT_PLAN")))
            outFile.write("\t{0}\t{1}\t{2}\t{3}\n".format(row.getValue("FREQUENCY"),row.getValue("SNAME"),row.getValue("TREAT_TYPE"),row.getValue("TREAT_PLAN")))
        del row, rows
    else:
        frequencyFields = ["TREAT_PLAN","PCTTREATED","COVERCLS","TREAT_TYPE","SNAME"]
        inTable = full    
        outTable = desc.path+"\\"+desc.baseName+"_FREQ.dbf"     
        arcpy.Frequency_analysis(inTable, outTable, frequencyFields)

        rows = arcpy.SearchCursor(outTable,fields="FREQUENCY;SNAME;COVERCLS;TREAT_TYPE;TREAT_PLAN;PCTTREATED",sort_fields="SNAME A")
        atts = ["FREQUENCY","SNAME","COVERCLS","TREAT_TYPE","TREAT_PLAN","PCTTREATED"]
        _print(atts)    
        for row in rows:
            print("\t{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(row.getValue("FREQUENCY"),row.getValue("SNAME"),row.getValue("COVERCLS"),row.getValue("TREAT_TYPE"),row.getValue("TREAT_PLAN"),row.getValue("PCTTREATED")))
            outFile.write("\t{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(row.getValue("FREQUENCY"),row.getValue("SNAME"),row.getValue("COVERCLS"),row.getValue("TREAT_TYPE"),row.getValue("TREAT_PLAN"),row.getValue("PCTTREATED")))       
        del row, rows
        
    #for f in frequencyFields:
        #print "\t"+f
        #outFile.write("\t"+f+"\n") 
        #for val in unique_values_2(inTable, f):
            #print "\t\t"+val
            #outFile.write("\t\t"+val+"\n")
                    
    countLayers += 1
    stopAt = 6999
    if countLayers == stopAt:
        print "Stopped at " + str(stopAt) + " layers processed."
        break
   
    last_folder = folder
    
print 
print "Processed " + str(countLayers) + " layers."
outFile.write("\nProcessed " + str(countLayers) + " layers.")
outFile.close()    # This closes the text file
