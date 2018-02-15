#Import System Modules
import Generic
global pts
import pandas as pd
import Helpers
    
def DoInitial(procmask, cs):
#    Generic.set_paths_and_workspaces()
    
    
    pts = Helpers.create_processing_table(Generic.Points,procmask, cs)
    import gc
    gc.collect()
    
    #full set
    jointabs  = "E:/mercedtool/MASTER_DATA/Tables/ValueTables"
    neartabs  = "E:/mercedtool/MASTER_DATA/Tables/NearTables"
    
    
    jointables = Helpers.LoadCSVs(jointabs)
    value_df = Helpers.MergeMultiDF('pointid', jointables)
    #
    if cs == 1:
        
    else:
        
    
    
    
    neartables = Helpers.LoadCSVs(neartabs)
    near_df = Helpers.MergeMultiDF('pointid', neartables)
    
    tabs_all_df = pd.merge(value_df,near_df, on = 'pointid')
    
    carb01 = pd.read_csv(Generic.Carbon2001)
    carb14 = pd.read_csv(Generic.Carbon2014)
    carb30 = pd.read_csv(Generic.Carbon2030)
    listofdfs = (tabs_all_df,carb01,carb14,carb30)
    return listofdfs