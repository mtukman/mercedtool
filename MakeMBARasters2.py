#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Dylan
#
# Created:     21/12/2017
# Copyright:   (c) Dylan 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

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
    tempo = arcpy.sa.Lookup('temp2.tif',Lfield[:10])
    tempo.save(OutputPath)


#Crop Value
MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Crop_Value_LUT_New.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/Crop_Value.tif','EVT_Nick_2','Landcover','Value')

##Nitrate Leach
MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Nitrate_Final.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/Nitrate_Leach.tif','EVT_Nick_2','Landcover','Leach')

#Nitrate Runoff
MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Nitrate_Final.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/Nitrate_Runoff.tif','EVT_Nick_2','Landcover','Runoff')

#Nitrate Atmosphere
MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Nitrate_Final.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/Nitrate_Atmos.tif','EVT_Nick_2','Landcover','Atmospheric')

#Water Demand
MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/WaterUse.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/WaterCons.tif','EVT_Nick_2','Landcover','Value')

#Resistance Lookup
MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Crop_Value_LUT_New.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/Resistance.tif','EVT_Nick_2','Landcover','Value')

#Air pollutin
MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Air_Pollution_LUT.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/NO2.tif','EVT_Nick_2','Landcover','NO2')
MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Air_Pollution_LUT.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/SO2.tif','EVT_Nick_2','Landcover','SO2')
MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Air_Pollution_LUT.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/PM10.tif','EVT_Nick_2','Landcover','PM10')
MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Air_Pollution_LUT.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/PM2_5.tif','EVT_Nick_2','Landcover','PM2_5')
MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Air_Pollution_LUT.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/CO.tif','EVT_Nick_2','Landcover','CO')
MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/Landcover_2014.tif','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Air_Pollution_LUT.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/O3.tif','EVT_Nick_2','Landcover','O3')