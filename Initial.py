#Import System Modules
import pandas as pd
import Helpers
    
def DoInitial(procmask, cs, cd, devmask, c1,c14,c30,joins,nears,points, tempgdb, scratch, cm, conmask):
    #full set
#    temppath = "E:/mercedtool/MASTER_DATA/Tables/ValueTables"
    jointables = Helpers.LoadCSVs(joins)
    value_df = Helpers.MergeMultiDF('pointid', jointables)
    #
    neartables = Helpers.LoadCSVs(nears)
    near_df = Helpers.MergeMultiDF('pointid', neartables)
    
    tabs_all_df = pd.merge(value_df,near_df, on = 'pointid')
    
    #Create modified dataframe using processing area mask is one is chosen
    if cs == 1:
        pts = Helpers.create_processing_table(points,procmask, tempgdb, scratch)
        tabs_all_df = pd.merge(pts,tabs_all_df, how = 'left', on = 'pointid')
    else:
        pass
    
    #Add User-defined additional urban areas using user-defined urban mask
    if cd == 1:
        pts = Helpers.create_processing_table(points,devmask, tempgdb, scratch)
        plist = pts['pointid'].tolist()
        Helpers.pmes('Creating User Defined Developent Polygons')
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'gridcode30'] = 13
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030'] = 'Urban'
    else:
        pass
    
    if cm == 1:
        pts = Helpers.create_processing_table(points,conmask, tempgdb, scratch)
        plist = pts['pointid'].tolist()
        Helpers.pmes('Creating User Defined Conservation Polygons')
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'gridcode30'] = tabs_all_df['gridcode14']
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030'] = tabs_all_df['LC2014']
    else:
        pass
    
#    tabs_all_df.to_csv("P:/Temp/process.csv")        
    carb01 = pd.read_csv(c1)
    carb14 = pd.read_csv(c14)
    carb30 = pd.read_csv(c30)
    Helpers.pmes('Tables Loaded')
    listofdfs = (tabs_all_df,carb01,carb14,carb30)
    return listofdfs