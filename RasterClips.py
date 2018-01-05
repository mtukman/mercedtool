#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      dylan
#
# Created:     10/11/2017
# Copyright:   (c) dylan 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import calculations, arcpy, os, zipfile, pandas, MercedRasterProcessing
from arcpy import env
arcpy.CheckOutExtension("Spatial")
ws = "P:/Temp/Temp.gdb"
arcpy.env.workspace = calculations.rev_slash(ws)
arcpy.env.overwriteOutput = 1

def ProcessRasters (InputRaster, SnapRaster, OutputRaster):
    arcpy.env.mask = SnapRaster
    arcpy.env.cellSize = SnapRaster
    arcpy.env.snapRaster = SnapRaster
    temp = arcpy.sa.ExtractByMask(InputRaster,SnapRaster)
    temp.save(OutputRaster)

MasterRaster = 'U:/Merced Project/GIS Data/CombinedRasters/Combined.gdb/LF2001_Combined'

t = "D:/TGS/projects/64 - Merced Carbon/MBA/Deliverables from TNC/Urban Footprint/data/rasters"
outpath = "D:/TGS/projects/64 - Merced Carbon/MBA/Deliverables from TNC/Urban Footprint/data/rasters/Clipped/"
arcpy.env.workspace = calculations.rev_slash(t)
arcpy.env.overwriteOutput = 1
list = arcpy.ListRasters()
print list

for i in list:
    ProcessRasters(i,MasterRaster,outpath + i)