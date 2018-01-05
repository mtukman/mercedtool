

import calculations, arcpy, os, zipfile, pandas, MercedRasterProcessing
from arcpy import env
arcpy.CheckOutExtension("Spatial")
ws = "D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters"
arcpy.env.workspace = calculations.rev_slash(ws)
arcpy.env.overwriteOutput = 1

folder = "D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters"
list = arcpy.ListRasters()
outpath = "D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/"
lfc = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/CellPoints.gdb/LFC_Points_Merged'


def ExtractRasterValues (InputRaster,PointsLayer,OutputTable):
    arcpy.sa.ExtractValuesToPoints(PointsLayer,InputRaster,InputRaster[:-4],'NONE','ALL')
    arcpy.MakeTableView_management('TempPoints','TempView')
    arcpy.CopyRows_management("TempView", OutputTable)
ws = "E:/Temp/scratch.gdb"
arcpy.env.workspace = calculations.rev_slash(ws)
arcpy.env.overwriteOutput = 1

for i in list:
    ExtractRasterValues(folder + '/' + i,lfc,outpath + i[:-4] + '.csv')
