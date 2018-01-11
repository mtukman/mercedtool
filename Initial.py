#Import System Modules
import Generic
global pts
import pandas as pd
import Helpers
Helpers.set_paths_and_workspaces()


pts = Helpers.create_processing_table(Generic.Points,Generic.MASK)
import gc
gc.collect()

#full set
jointabs  = "E:/Temp/Tables/ValueTables"
neartabs  = "E:/Temp/Tables/NearTables"


jointables = Helpers.LoadCSVs(jointabs)
value_df = Helpers.MergeMultiDF('pointid', jointables)
#
neartables = Helpers.LoadCSVs(neartabs)
near_df = Helpers.MergeMultiDF('pointid', neartables)

#Sample set
#jointables = Generic.LoadCSVs(os.path.join(Generic.valuetables,'ValueTables'))
#value_df = Generic.MergeMultiDF('pointid', jointables)
#
#neartables = Generic.LoadCSVs("E:/mercedtool/MASTER_DATA/Tables/NearTables")
#near_df = Generic.MergeMultiDF('pointid', neartables)

Generic.tabs_all_df = pd.merge(value_df,near_df, on = 'pointid')

Generic.carb01 = pd.read_csv(Generic.Carbon2001)
Generic.carb14 = pd.read_csv(Generic.Carbon2014)
Generic.carb30 = pd.read_csv(Generic.Carbon2030)