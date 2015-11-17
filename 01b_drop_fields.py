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
outFile = open("01b_drop_fields_OUTPUT.txt", "w")
outFile.write(searchpath+"\n")
 
#skipPaths = ['!points', '!template', '!testcode', '!uniqvals', '!workday', '!^_^_^_^_^_ COPIED ON 20150916', '20150820-GTT-CR', '20150821-GTT-CR', '20150827_GTT_CR', '20150828-GTT-CR', '20150903-GTT-CR', '20150904-GTT_CR', '20150911_GTT_CR_GEOX7', 'DIAS-PANO_COJU_8-28-15', 'DIAS_HEPE_COJU_8-10-15', 'DIAS_HEPE_COJU_8-11-2015', 'DIAS_HEPE_COJU_8-17-2015', 'DIAS_HEPE_COJU_8-18-2015', 'DIAS_HEPE_COJU_8-19-2015', 'DIAS_HEPE_COJU_8-28-2015', 'PICO_COJU_8-24-2015', 'PICO_COJU_8-24-2015_Hand_Mapped', 'PICO_COJU_8-25-2015', 'PICO_COJU_8-25-2015_Hand_Mapped', 'RESTECH_COJU_081315', 'RESTECH_COJU_081415_A', 'RESTECH_COJU_081415_B', 'RESTECH_COJU_083115', 'RESTECH_COJU_090815', 'RESTECH_COJU_090915', 'SOMAHE_COJU_7-14-2015', 'SOMAHE_COJU_7-15-2015', 'SOMAHE_COJU_8-12-15', 'SOMAHE_COJU_8-13-2015', 'SOMAHE_COJU_8-14-15', 'SOMAHE_COJU_8-3-2015', 'SOMAHE_COJU_8-4-2015', 'SOMAHE_COJU_8-5-2015', 'SOMAHE_Rope_Access_COJU_8-11-2015', 'SOMAHE_Rope_Access_COJU_8-12-2015', 'TEVA_COJU_8-25-2015', 'TEVA_COJU_9-10-15', 'TEVA_COJU_9-2-2015', 'TEVA_COJU_9-8-15']

skipPaths = ['!points', '!template', '!testcode', '!uniqvals', '!workday', '!^_^_^_^_^_ COPIED ON 20150916', '20150820-GTT-CR', '20150821-GTT-CR', '20150827_GTT_CR', '20150828-GTT-CR', '20150903-GTT-CR', '20150904-GTT_CR', '20150911_GTT_CR_GEOX7', 'DIAS-PANO_COJU_8-28-15', 'DIAS_HEPE_COJU_8-10-15', 'DIAS_HEPE_COJU_8-11-2015', 'DIAS_HEPE_COJU_8-17-2015', 'DIAS_HEPE_COJU_8-18-2015', 'DIAS_HEPE_COJU_8-19-2015', 'DIAS_HEPE_COJU_8-28-2015', 'RESTECH_COJU_081315', 'RESTECH_COJU_081415_A', 'RESTECH_COJU_081415_B', 'RESTECH_COJU_083115', 'RESTECH_COJU_090815', 'RESTECH_COJU_090915', 'SOMAHE_COJU_7-14-2015', 'SOMAHE_COJU_7-15-2015', 'SOMAHE_COJU_8-12-15', 'SOMAHE_COJU_8-13-2015', 'SOMAHE_COJU_8-14-15', 'SOMAHE_COJU_8-3-2015', 'SOMAHE_COJU_8-4-2015', 'SOMAHE_COJU_8-5-2015', 'SOMAHE_Rope_Access_COJU_8-11-2015', 'SOMAHE_Rope_Access_COJU_8-12-2015', 'TEVA_COJU_8-25-2015', 'TEVA_COJU_9-10-15', 'TEVA_COJU_9-2-2015', 'TEVA_COJU_9-8-15']

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
           
fcType = "All"
countLayers = 0  
last_folder = ""

dropFields = ['Recorder', 'Workgroup', 'Workgroup2', 'SNAME_1', 'Work_Desc', 'TREAT_TYPE', 'TRADE_NM', 'AGT_APP_RT', 'ADJ_TRADE_', 'ADJ_AGT_AP', 'Total_USED', 'Recorder_1', 'Workgrou_1', 'Workgrou_2', 'SNAME_12', 'Work_Des_1', 'TREAT_TY_1', 'TRADE_NM_1', 'AGT_APP__1', 'ADJ_TRADE1', 'ADJ_AGT__1', 'Total_US_1']

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
    
    outFile.write("Deleteing fields..." + "\n")
    print "Deleteing fields..."
    arcpy.DeleteField_management(fc, dropFields)    

    fieldnames = [f.name for f in arcpy.ListFields(fc)]
    print str(fieldnames)
    outFile.write(str(fieldnames) + "\n")

   
    last_folder = folder
    
outFile.close()    # This closes the text file
