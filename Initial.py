#Import System Modules
import arcpy
from arcpy import env
import Generic
global pts
import os
Generic.set_paths_and_workspaces()
arcpy.env.overwriteOutput = True
arcpy.env.extent = Generic.MASK


pts = Generic.create_processing_table(Generic.Points,Generic.MASK)
import gc
gc.collect()


jointables = Generic.LoadCSVs(os.path.join(Generic.valuetables,'JoinTables'))
value_df = Generic.MergeMultiDF('pointid', jointables)


neartables = Generic.LoadCSVs("E:/mercedtool/MASTER_DATA/ValueTables/NearTables")
near_df = Generic.MergeMultiDF('pointid', neartables)


carb01 = pd.read_csv(os.path.join(Generic.Root_Mid_Path, 'CarbonTables/Carb01.csv'))
carb14 = pd.read_csv(os.path.join(Generic.RDP, Generic.MP, 'CarbonTables/Carb14.csv'))
carb30 = pd.read_csv(os.path.join(Generic.RDP, Generic.MP, 'CarbonTables/Carb30.csv'))


