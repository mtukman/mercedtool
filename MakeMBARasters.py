# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 11:02:39 2017

@author: Dylan
"""

#Make MBA Raster
def MakeMBARaster(Raster,LUT,OutputPath,JoinKey,TargetKey,Lfield):
    import arcpy
    from arcpy import env
    arcpy.CheckOutExtension("Spatial")
    #Set the Variables
    ws = 'E:/Temp'
    arcpy.env.workspace = ws
    arcpy.env.overwriteOutput = 1
    
    arcpy.MakeRasterLayer_management(Raster,'temp')
    arcpy.AddJoin_management('temp',JoinKey,LUT,TargetKey)
    arcpy.CopyRaster_management('temp','temp2.tif')
    tempo = arcpy.sa.Lookup('temp2.csv',Lfield)
    tempo.save(OutputPath)
    
    
##Crop Value
#MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Crop_Value_LUT_New.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/Crop_Value.tif','EVT_Nick_2','Landcover','Value')
#
##Nitrate Leach
#MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Nitrate_LUT_New.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/Nitrate_Leach.tif','EVT_Nick_2','Landcover','Leach(kg/ha)')
#
##Nitrate Runoff
#MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Nitrate_LUT_New.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/Nitrate_Runoff.tif','EVT_Nick_2','Landcover','Runoff(kg/ha)')
#
##Nitrate Atmosphere
#MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Nitrate_LUT_New.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/Nitrate_Atmos.tif','EVT_Nick_2','Landcover','Atmospheric(kg/ha)')
#
##Water Demand
#MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/WaterUse.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/WaterCons.tif','EVT_Nick_2','Landcover','Value')
#
##Resistance Lookup
#MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Crop_Value_LUT_New.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/Resistance.tif','EVT_Nick_2','Landcover','Value')
#
##Air pollutin
#MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Air_Pollution.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/NO2.tif','EVT_Nick_2','Landcover_Class','NO2 (g/900m2)')
#MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Air_Pollution.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/SO2.tif','EVT_Nick_2','Landcover_Class','SO2 (g/900m2)')
#MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Air_Pollution.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/PM10.tif','EVT_Nick_2','Landcover_Class','PM10 (g/900m2)')
#MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Air_Pollution.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/PM2_5.tif','EVT_Nick_2','Landcover_Class','PM2.5 (g/900m2)')
#MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Air_Pollution.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/CO.tif','EVT_Nick_2','Landcover_Class','CO (g/900m2)')
MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Air_Pollution.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/O3.tif','EVT_Nick_2','Landcover_Class','O3 (g/900m2)')