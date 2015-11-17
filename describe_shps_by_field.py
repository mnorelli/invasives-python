import os, arcpy, numpy

searchpath = os.getcwd()
#outFile = open("01_describe_shps_OUTPUT.txt", "w")
#outFile.write(searchpath+"\n")
 
skipPaths = ["!workday","!points","!template","!testcode","!uniqvals","!points","!points_previous","!frequencies"]
skipData = ["Line_gen.shp","Point_ge.shp","PosnLine.shp","Workday.shp"]
           
fcType = "All"
myField = "TREAT_TYPE" 



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
            

def FindField(fc,myField):
    fieldList = arcpy.ListFields(fc)
    for field in fieldList:
        if str.lower(str(field.name)) == str.lower(myField):
            # print "    " + fc + " contains fieldname: " + myField + " of type: " + field.type
            print field.type + "," + fc  
            
def unique_values_2(table, field):
    data = arcpy.da.TableToNumPyArray(table, [field])
    return numpy.unique(data[field])
                  
last_folder = ""
resultList = []
countLayers = 0  

 
for fc in inventory_data(searchpath, "FeatureClass"):
    desc = arcpy.Describe(fc)
    typ = desc.shapeType
    name = desc.baseName
    head, folder = os.path.split(desc.path)
    print folder.upper() + " " + name + " " + typ
    
    resultList += unique_values_2(desc.catalogPath, myField)
    
myList = sorted(set(resultList))

for f in myList:
    print f
        
    
    
    