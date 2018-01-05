#Import System Modules
import arcpy
from arcpy import env
import Generic
global pts
Generic.set_paths_and_workspaces()
arcpy.env.overwriteOutput = True
arcpy.env.extent = Generic.MASK


Generic.create_processing_table(Generic.Points,Generic.MASK)
import gc
gc.collect()


Generic.LoadCSVs(folder)
Generic.MergeMultiDF(JoinField,OutputDF, dflist)

Generic.LoadCSVs(folder)
Generic.MergeMultiDF(JoinField,OutputDF, dflist)

Generic.LoadCSVs(folder)
Generic.MergeMultiDF(JoinField,OutputDF, dflist)

Generic.LoadCSVs(folder)
Generic.MergeMultiDF(JoinField,OutputDF, dflist)

carb01 = pd.read_csv()
carb14 = pd.read_csv()
carb30 = pd.read_csv()
#create a dataframe with

