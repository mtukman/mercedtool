# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 10:09:32 2017

@author: Dylan
"""

import arcpy
import csv


#ws = "E:/Temp/scratch.gdb"
#arcpy.env.workspace = ws
#arcpy.env.overwriteOutput = 1
#flist = arcpy.ListFeatureClasses()
#
#
#for i in flist():
table ='E:/Temp/scratch.gdb/Nitrate_2001'
outfile = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/MBTABLES/test.csv'

#--first lets make a list of all of the fields in the table
fields = arcpy.ListFields(table)
field_names = [field.name for field in fields]
print (fields)
print (field_names)

with open(outfile,'w') as f:
    dw = csv.DictWriter(f,field_names, lineterminator = '\n')
    #--write all field names to the output file
    dw.writeheader()

    #--now we make the search cursor that will iterate through the rows of the table
    with arcpy.da.SearchCursor(table,field_names) as cursor:
        for row in cursor:
            dw.writerow(dict(zip(field_names,row)))

