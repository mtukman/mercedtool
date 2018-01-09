#Import System Modules
import arcpy
from arcpy import env
import Generic
global pts
import os
import pandas as pd
Generic.set_paths_and_workspaces()
arcpy.env.overwriteOutput = True
arcpy.env.extent = Generic.MASK


pts = Generic.create_processing_table(Generic.Points,Generic.MASK)
import gc
gc.collect()

#full set
jointabs  = "D:\\TGS\\projects\\64 - Merced Carbon\\Python\\MercedTool\\Deliverables\\MASTER_DATA\\ValueTables\\JoinTables"
neartabs  = "D:\\TGS\\projects\\64 - Merced Carbon\\Python\\MercedTool\\Deliverables\\MASTER_DATA\\ValueTables\\NearTables"

jointables = Generic.LoadCSVs(jointabs)
value_df = Generic.MergeMultiDF('pointid', jointables)

neartables = Generic.LoadCSVs(neartabs)
near_df = Generic.MergeMultiDF('pointid', neartables)

#Sample set
#jointables = Generic.LoadCSVs(os.path.join(Generic.valuetables,'ValueTables'))
#value_df = Generic.MergeMultiDF('pointid', jointables)
#
#neartables = Generic.LoadCSVs("E:/mercedtool/MASTER_DATA/Tables/NearTables")
#near_df = Generic.MergeMultiDF('pointid', neartables)

Generic.tabs_all_df = pd.merge(value_df,near_df, on = 'pointid',axis = 1)

Generic.carb01 = pd.read_csv(Generic.Carbon2001)
Generic.carb14 = pd.read_csv(Generic.Carbon2014)
Generic.carb30 = pd.read_csv(Generic.Carbon2030)


