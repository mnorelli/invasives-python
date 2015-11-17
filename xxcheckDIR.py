import os, arcpy

searchpath = os.getcwd()

dirlist = []
for dirname, dirnames, filenames in os.walk(searchpath):
    dirlist.append(dirnames)
    
print dirlist