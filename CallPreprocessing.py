## -*- coding: utf-8 -*-
##"""
##Created on Thu Dec 14 10:44:39 2017
##
##@author: Dylan
##"""
import Generic
import arcpy
##
##Rasters to Raster Lookups - MakeMBARaster(Raster,LUT,OutputPath,JoinKey,TargetKey,Lfield)
Generic.set_paths_and_workspaces()
##
##Generic.MakeMBARaster('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Air_Pollution.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/ClippedRasters/New/O3.tif','EVT_Nick_2','Landcover','O3')
##
##Rasters to Look Up CSVs
##Rasters to Points - RastersToPoints(Raster,ValueField,OutputName):
##
##Generic.RastersToPoints(Generic.Root_Mid_Path + 'Rasters/'  + 'Subsidence.tif','Value','subsidence')
##
##FCs to CSVs
##Generic.FCtoCSV(Generic.tempgdb,Generic.MTABS)
##
##
##Clean Tables - (csv,idfield,valuefield,keepfields = [], renamefields = [])
##Generic.Clean_Table(Generic.MBTABS + 'subsidence.csv','pointid','Value',['pointid','Value'],[('Value','subsidence')])
##
##
##Make Near Tables
##arcpy.GenerateNearTable_analysis(Generic.Points,Generic.vects + 'huc12', Generic.neartabs + 'env_near_huc12.csv')
##arcpy.GenerateNearTable_analysis(Generic.Points,Generic.vects + 'Roads', Generic.neartabs + 'env_near_roads.csv')
##arcpy.GenerateNearTable_analysis(Generic.Points,Generic.vects + 'FEMA', Generic.neartabs + 'env_near_fema.csv')
##arcpy.GenerateNearTable_analysis(Generic.Points,Generic.vects + 'CPAD', Generic.neartabs + 'env_near_cpad.csv')

##
##
##Join Near Tables to Spatial Data Merge2csvs(inputcsv1,inputcsv2,mergefield,outputcsv,origcol = 'none',newcol = 'none')



##Write Vectors to Tables
##Generic.FCtoCSV_Single('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/CPAD_2017a/CPAD_2017a/CPAD_2017a_Holdings_Merced.shp','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/vector_tables/cpad.csv')
##Generic.FCtoCSV_Single('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/CV_Riparian/ds1000.gdb/Riparian_Clean_Merced','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/vector_tables/riparian.csv')
##Generic.FCtoCSV_Single('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/CV_Riparian/ds1000.gdb/WoodyRiparian','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/vector_tables/woodyriparian.csv')
##Generic.FCtoCSV_Single('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/NFHL/NFHL_20171004.gdb/Merced_Clean','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/vector_tables/fema.csv')
##Generic.FCtoCSV_Single('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/Wetlands/NWI.gdb/NWI_Merced','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/vector_tables/wetlands.csv')


##
##def Merge2csvs(inputcsv1,origcol,newcol,inputcsv2,mergefield,outputcsv)
##Generic.Merge2csvs('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/vector_tables/cpad.csv','OBJECTID','NEAR_FID','D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_cpad.csv','NEAR_FID','D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_cpad_full.csv')
##Generic.Merge2csvs('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/vector_tables/fema.csv','OBJECTID','NEAR_FID','D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_fema.csv','NEAR_FID','D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_fema_full.csv')
##Generic.Merge2csvs('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/vector_tables/riparian.csv','OBJECTID','NEAR_FID','D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_riparian.csv','NEAR_FID','D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_riparian_full.csv')
##Generic.Merge2csvs('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/vector_tables/woodyriparian.csv','OBJECTID','NEAR_FID','D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_woodyrip.csv','NEAR_FID','D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_wooodyrip_full.csv')
##Generic.Merge2csvs('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/vector_tables/wetlands.csv','OBJECTID','NEAR_FID','D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_wetlands.csv','NEAR_FID','D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_wetlands_full.csv')
Generic.Merge2csvs('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/vector_tables/fema.csv','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/env_near_fema.csv','NEAR_FID','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/env_near_fema_merged.csv','OBJECTID','NEAR_FID')
##
##Clean Near Tables Clean_Table (csv,idfield,valuefield = 'TEST',keepfields = [], renamefields = [],length)
##Generic.Clean_Table(Generic.Neartabs + 'NearTable_Wet.csv','pointid','Value',['pointid','Value'],[('Value','crop_value')])
##Generic.Clean_Table(Generic.Neartabs + 'NearTable_Rivers.csv','pointid','Value',['pointid','Value'],[('Value','crop_value')])
##Generic.Clean_Table(Generic.Neartabs + 'NearTable_Rip.csv','pointid','Value',['pointid','Value'],[('Value','crop_value')])
##Generic.Clean_Table(Generic.Neartabs + 'NearTable_Creeks.csv','pointid','Value',['pointid','Value'],[('Value','crop_value')])
##Generic.Clean_Table(Generic.Neartabs + 'NearTable_Roads.csv','pointid','Value',['pointid','Value'],[('Value','crop_value')])
##Generic.Clean_Table(Generic.Neartabs + 'NearTable_WoodyRip.csv','pointid','Value',['pointid','Value'],[('Value','crop_value')])
##Generic.Clean_Table(Generic.Neartabs + 'NearTable_WoodyCrop.csv','pointid','Value',['pointid','Value'],[('Value','crop_value')])
##Generic.Clean_Table(Generic.Neartabs + 'NearTable_CPAD.csv','pointid','Value',['pointid','Value'],[('Value','crop_value')])
##Generic.Clean_Table(Generic.Neartabs + 'NearTable_FEMA.csv','pointid','Value',['pointid','Value'],[('Value','crop_value')])
##Generic.Clean_Table("E:/mercedtool/MASTER_DATA/ValueTables/NearTables/env_near_parks.csv",'IN_FID',20000,keepfields = ['IN_FID','NEAR_DIST'],renamefields = [('IN_FID','pointid'),('NEAR_DIST','near_parks')])
##
##
##Create Spatial Join Lookups
##Spatial Join
##arcpy.SpatialJoin_analysis (Generic.Points,Generic.vects + 'hydrovuln', Generic.tempgdb + 'hydrovuln', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
##arcpy.SpatialJoin_analysis (Generic.Points,Generic.vects + 'huc12', Generic.tempgdb + 'huc12', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
##arcpy.SpatialJoin_analysis (Generic.Points,Generic.vects + 'genplan', Generic.tempgdb + 'genplan', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
##arcpy.SpatialJoin_analysis (Generic.Points,Generic.vects + 'fmmp', Generic.tempgdb + 'fmmp', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
##arcpy.SpatialJoin_analysis (Generic.Points,Generic.vects + 'calenviro', Generic.tempgdb + 'calenviro', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
##arcpy.SpatialJoin_analysis (Generic.Points,Generic.vects + 'sagbi_mod', Generic.tempgdb + 'sagbi_mod', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')
#arcpy.SpatialJoin_analysis (Generic.Points,'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/New File Geodatabase (2).gdb/SeciesRangeLU_Full', Generic.tempgdb + 'terhab', 'JOIN_ONE_TO_ONE', 'KEEP_ALL')

##
##FCs to CSVs
##Generic.FCstoCSVs(Generic.tempgdb,Generic.Root_Mid_Path + 'ValueTables/JoinTables/)

#Generic.FCtoCSV('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/Extractions.gdb/HUC12','D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/JoinTables/huc12.csv')
#Generic.FCtoCSV('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/temppts.gdb/terhab','D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/JoinTables/terhab.csv')

##
##Clean Tables
##Generic.Clean_Table(Generic.Root_Mid_Path + 'ValueTables/JoinTables/' + '','pointid','Value',['pointid','Value'],[('Value','crop_value')])
##
##
##
##
##
##
##
##
##
##Clean Memory
##import gc
##gc.collect()
##
##Merge Look-Up MBAs
##global temp
##temp =[]
##Generic.LoadMBAs(Generic.Root_Mid_Path + 'Flags/')
##Generic.LoadMBAs(Generic.Neartabs)
##Generic.LoadMBAs(Fulltables)
##Generic.LoadMBAs(Fulltables)
##Generic.MergeMultiDF('pointid','D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/MBAComplete')
##
##
##
##Landcover Rasters to points, to csv, then combined into a single CSV with pointid, LC2001 and LC2014
##def RastersToPoints(Raster,ValueField,OutputName):
##    import arcpy
##    arcpy.env.overwriteOutput = True
##    arcpy.RasterToPoint_conversion(Raster,OutputName,ValueField)
##
##RastersToPoints('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Landcover_Rasters/Landcover_2001.tif','EVT_Nick_1','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/RasterEctractions.gdb/LF2001_LUT')
##RastersToPoints('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Landcover_Rasters/Landcover_2014.tif','EVT_Nick_2','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/RasterEctractions.gdb/LF2014_LUT')
##
##import Generic
##Generic.FCtoCSV('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/RasterEctractions.gdb/','D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/')
##
##import pandas as pd
##import functools
##d1 = pd.read_csv('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/LF2001_LUT.csv', usecols = ['pointid','EVT_Nick_1'])
##d2 = pd.read_csv('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/LF2014_LUT.csv', usecols = ['pointid','EVT_Nick_2'])
##
##d1 = d1.rename(columns={'EVT_Nick_1':'LC2001'})
##d2 = d2.rename(columns={'EVT_Nick_2':'LC2014'})
##list1 = [d1,d2]
##mba= functools.reduce(lambda left,right: pd.merge(left,right,on='pointid'), list1)
##OutputDF = mba.loc[:, ~mba.columns.str.contains('^Unnamed')]
##OutputDF.to_csv('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/LookUpTables/Landcovers.csv')
##
##
