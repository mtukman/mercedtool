#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Dylan
#
# Created:     12/12/2017
# Copyright:   (c) Dylan 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import calculations, arcpy, os, zipfile, pandas
from arcpy import env
arcpy.CheckOutExtension("Spatial")
ws = "D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/Extractions.gdb"
arcpy.env.workspace = calculations.rev_slash(ws)
arcpy.env.overwriteOutput = 1

points = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/CellPoints.gdb/LFC_Points_Merged'
fc1 = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/FinalVectors/VectorFCs.gdb/FloodRisk'
fc2 = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/FinalVectors/VectorFCs.gdb/FMMP_2014'
fc3 = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/WBD/WBD_National_GDB/WBD/WBD.gdb/HUC12_Projected'
fc4 = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/CalEnviroscreen/CES3GDB.gdb/CES3ResultsGDB'
fc5 = 'D:/TGS/projects/64 - Merced Carbon/MBA/Deliverables from TNC/Urban Footprint/data/shapefile_zips/california_tnc_priority_areas.shp'
fc6 = 'D:/TGS/projects/64 - Merced Carbon/MBA/Deliverables from TNC/Urban Footprint/data/shapefile_zips/california_audubon_iba.shp'
fc7 = 'D:/TGS/projects/64 - Merced Carbon/MBA/Deliverables from TNC/Urban Footprint/data/shapefile_zips/california_ecoregions_l3.shp'


#arcpy.SpatialJoin_analysis ( points,fc1, 'Flood', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
#arcpy.SpatialJoin_analysis ( points,fc2, 'FMMP', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
#arcpy.SpatialJoin_analysis ( points,fc3, 'HUC12', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
arcpy.SpatialJoin_analysis ( points,fc4, 'CES3', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
arcpy.SpatialJoin_analysis ( points,fc5, 'TNC_PRIOR', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
arcpy.SpatialJoin_analysis ( points,fc6, 'IBA', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
arcpy.SpatialJoin_analysis ( points,fc7, 'ECO', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')

