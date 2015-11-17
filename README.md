# invasives-python
A collection of Python scripts for processing invasive plant GPS data collection for the benefit of the Golden Gate National Parks Conservancy and the National Park Service

01_describe_shps.py
A general tool to list the name and feature class of each shapefile in each folder in the directory

01a_describe_shps_by_field.py
A general tool to list the name, feature class, and attributes of each shapefile in each folder in the directory

01b_drop_fields.py
Repeated runs of the 05_joinWorkday.py script added multiple sets of Workday fields.  List script removes them, essentially returning the OccurTreat shapefiles to their original state.

02_Add+CalcFieldFOLDER.py
It became very useful to track in the data the source folder of the record, so that if an error was found, it could be traced back to its source and corrected there for later processing.  This script adds a FOLDER field and calculates it to the folder name where the data is found, for each folder.

03_copyWORKDAYlayers.py
The problem of data dictionary edits during collection necessitated this script, which looks at the AGT_APP_RT field of each Workday shapefile and copies each to a new directory based on whether this field is defines as a string or a numeric field, for further processing.

04_locateOldWORKDAY.py
Again required by the different generations of data dictionaries, this script looks in the Workday shapefiles for the field Total_Mix_ which was replaced later by Total_USED to hold the amount of herbicide used for the day.  It adds a Total_USED field where it is missing and calculates the proper value for this field where needed.  It further lists the results for checking where there are differences when summing Total_Mix_ versus Total_USED, so those records can be corrected.  It also creates a Frequency table for those values
  
05_joinWorkday.py
This script joins the Workday table to the OccurTreat shapefile for each day’s folder in the directory.

06_fixWorkday.py
This script fixes each Workday table to conform to the standard, using Total_USED instead of Total_Mix_, AGT_APP_RT as a number instead of an alphanumeric field including a percent sign, and the list of fields common to each folder’s Workday table.  It calculates the correct values for these changed fields and deletes the previous uncorrected versions.

07_copyALLPOINTS.py
This script copied all point occurrence data to a single folder for checking results of earlier processing prior to merging into a single shapefile and to test using the OFFSET_AZ and OFFSET_M values to derive the correct target locations recorded from adjusting the source location coordinates.


09_fix_SQ_METERS.py
This script added a value for SQ_METERS where it was recorded as the default 0 but where LENGTH and WIDTH were greater than 0.  

10_FREQUENCY_all_folders.py
To help with error checking, this script was used to generate a frequency table on various attributes.  This script requires the most hand-editing, writing in the field names needed multiple times, since the author’s skills did not allow for a more elegant application of multiple processes for a single set of specified field names.

10a_FREQUENCY_all_folders.py
To check that all TREAT_PLAN values specified in Workday tables were applied to all occurrence records, this script was used to generate a list of both for all folders of data.  It is the output of this script, converted to a Word document, that was shared with field staff so that remaining occurrence records that had a TREAT_PLAN not specified could be corrected.  Since TREAT_PLAN is used to link Workday and occurrences, if there is an error here, many key values, including RECORDER and Total_USED, that come from Workday would not be filled in.

11_join_COVER_TREAT.py
This script joins a crosswalk table of COVERCALC values to the COVERCLS field in each occurrence table to facilitate the density calculation to follow.

12_add_DENSITY.py
This script calculates DENSITY as shown above, SQ_METERS times COVERCALC, and adds, but doesn’t calculate SUMDENSITY.

13_calc_CARRVOL_ME.py
This script creates a frequency table for each occurrence, summing the DENSITY field, joining the table to the occurrence data, and populating the SUMDENSITY field for each occurrence to the sum derived in the frequency.  It adds the CARRVOL_ME field and calculates it thusly:
Total_USED * (DENSITY/SUMDENSITY)
meaning, the amount of herbicide used on each occurrence should be based on the proportion of that record’s density among the total density of all occurrences

14_copyPreFinal.py
This script moved all point occurrences to a summary point folder prior to being merged into a final, single summary point shapefile for further processing.

Other scripts in the directory were created to be or attempt one-off solutions to a particular problem or a general query utility.  These include:
CalcCARRVOL_ME.py
copyOFFSETlayers.py
describe_shps_by_field.py
describe_shps,OFFSET.py
NOT WORKING 01b_fix_PCTTREATED.py
NOT WORKING 06_checkTREAT_TYPES.py
sel_calc2_export_lyr.py
xxcheckDIR.py
xxlist_all_folders.py
xxtestDesc.py
