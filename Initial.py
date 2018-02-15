#Import System Modules
import Generic
global pts
import pandas as pd
import Helpers
    
def DoInitial(procmask, cs, cd, devmask):
    #full set
    jointabs  = "E:/mercedtool/MASTER_DATA/Tables/ValueTables"
    neartabs  = "E:/mercedtool/MASTER_DATA/Tables/NearTables"
    
    
    jointables = Helpers.LoadCSVs(jointabs)
    value_df = Helpers.MergeMultiDF('pointid', jointables)
    #
    neartables = Helpers.LoadCSVs(neartabs)
    near_df = Helpers.MergeMultiDF('pointid', neartables)
    
    tabs_all_df = pd.merge(value_df,near_df, on = 'pointid')
    
    #Create modified dataframe using processing area mask is one is chosen
    if cs == 1:
        pts = Helpers.create_processing_table(Generic.Points,procmask)
        tabs_all_df = pd.merge(pts,tabs_all_df, how = 'left', on = 'pointid')
    else:
        pass
    
    #Add User-defined additional urban areas using user-defined urban mask
    if cd == 1:
        pts = Helpers.create_processing_table(Generic.Points,devmask)
        plist = pts['pointid'].tolist()
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),tabs_all_df['gridcode30']] = 13
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),tabs_all_df['LC2030']] = 'Urban'
        
        
        
    else:
        pass
        
    carb01 = pd.read_csv(Generic.Carbon2001)
    carb14 = pd.read_csv(Generic.Carbon2014)
    carb30 = pd.read_csv(Generic.Carbon2030)
    listofdfs = (tabs_all_df,carb01,carb14,carb30)
    return listofdfs