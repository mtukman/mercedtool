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

Generic.MergeLCValues()
temp = pts


#create a dataframe with 

