#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Dylan
#
# Created:     29/12/2017
# Copyright:   (c) Dylan 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import Generic
import arcpy

#Rasters to Raster Lookups - MakeMBARaster(Raster,LUT,OutputPath,JoinKey,TargetKey,Lfield)
Generic.set_paths_and_workspaces()

##arcpy.SpatialJoin_analysis (Generic.Points,Generic.vects + 'hydrovuln', Generic.tempgdb + 'hydrovuln', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
##arcpy.SpatialJoin_analysis (Generic.Points,Generic.vects + 'huc12', Generic.tempgdb + 'huc12', 'JOIN_ONE_TO_ONE', 'KEEP_ALL') # THIS ONE WAS HAVING AN UNEXPECTED ERROR
##arcpy.SpatialJoin_analysis (Generic.Points,Generic.vects + 'genplan', Generic.tempgdb + 'genplan', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
##arcpy.SpatialJoin_analysis (Generic.Points,Generic.vects + 'fmmp', Generic.tempgdb + 'fmmp', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
##arcpy.SpatialJoin_analysis (Generic.Points,Generic.vects + 'calenviro', Generic.tempgdb + 'calenviro', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
##
Generic.FCtoCSV(Generic.tempgdb,Generic.Root_Mid_Path + 'ValueTables/JoinTables/')

