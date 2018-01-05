#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Dylan
#
# Created:     27/11/2017
# Copyright:   (c) Dylan 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import calculations, arcpy, os, zipfile, pandas, MercedRasterProcessing
from arcpy import env
arcpy.CheckOutExtension("Spatial")
ws = "P:/Temp/Temp.gdb"
arcpy.env.workspace = calculations.rev_slash(ws)
arcpy.env.overwriteOutput = 1

CPAD ="D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/FinalVectors/VectorFCs.gdb/CPAD_2017a_Holdings_Merced"
Wetland ="D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/FinalVectors/VectorFCs.gdb/NWI_Merced"
Riparian = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/FinalVectors/VectorFCs.gdb/ds1000_Merced'
##StreamCL =
##ARA =
##GreenInfo =
Recreation ="D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/FinalVectors/VectorFCs.gdb/Parks_Projected"
Points = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/CellPoints.gdb/LFC_Points_Test'

def FlagCalc (InputPoints,InputFlagLayer,OutputCSV,fieldname):
    arcpy.MakeFeatureLayer_management(InputPoints,'temp')
    arcpy.SelectLayerByLocation_management('temp','INTERSECT',InputFlagLayer,"",'NEW_SELECTION')
    arcpy.MakeTableView_management(in_table="temp", out_view="temp_table", where_clause="", workspace="", field_info="OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;pointid pointid VISIBLE NONE;gridcode01 gridcode01 HIDDEN NONE;gridcode14 gridcode14 HIDDEN NONE")
    arcpy.CopyRows_management('temp_table',OutputCSV)


##FlagCalc(Points,CPAD,'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/CPADFlag.csv','CPAD')
##print 'done1'
FlagCalc(Points,Wetland,'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/WetlandFlag.csv','Wetland')
print 'done2'
FlagCalc(Points,Riparian,'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/RiparianFlag.csv','Riparian')
FlagCalc(Points,Recreation,'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/RecreationFlag.csv','Recreation')
