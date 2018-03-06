#Import System Modules
import pandas as pd
import Helpers
    
def DoInitial(procmask, cs, cd, devmask, c1,c14,c30,joins,nears,points, tempgdb, scratch, cm, conmask = 'None', acumask = 'None', acamask = 'None', acu = 0, aca = 0):
    #full set
#    temppath = "E:/mercedtool/MASTER_DATA/Tables/ValueTables"
    jointables = Helpers.LoadCSVs(joins)
    value_df = Helpers.MergeMultiDF('pointid', jointables)
    #
    neartables = Helpers.LoadCSVs(nears)
    near_df = Helpers.MergeMultiDF('pointid', neartables)
    aglist = ['Orchard','Annual Cropland','Vineyard', 'Rice', 'Irrigated Pasture']
    developed = ['Developed','Urban','Developed Roads']
    natlist = ['Forest', 'Shrubland', 'Wetland', 'Grassland','Barren']
    tabs_all_df = pd.merge(value_df,near_df, on = 'pointid')
    tabs_all_df['LC2030_trt'] = tabs_all_df['LC2030']
    tabs_all_df['LC2030_ac'] = tabs_all_df['LC2030']
    tabs_all_df['gridcode30_trt'] = tabs_all_df['gridcode30']
    
    #Create modified dataframe using processing area mask if one is chosen
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
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'gridcode30_trt'] = 13
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030_trt'] = 'Urban'
        tabs_all_df['dev_flag'] = 0
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'dev_flag'] = 1
        
    else:
        pass

    
    if cm == 1:
        pts = Helpers.create_processing_table(points,conmask, tempgdb, scratch)
        plist = pts['pointid'].tolist()
        Helpers.pmes('Creating User Defined Conservation Polygons')
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'gridcode30_trt'] = tabs_all_df['gridcode14'] + 100
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030_trt'] = tabs_all_df['LC2014']
        tabs_all_df['con_flag'] = 0
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'con_flag'] = 1        
    else:
        pass
    
    
    if acu == 1:
        pts = Helpers.create_processing_table(points,acumask, tempgdb, scratch)
        plist = pts['pointid'].tolist()
        Helpers.pmes('Flagging points for avoid conversion to urban')
        tabs_all_df['acu_flag'] = 0
        tabs_all_df.loc[((tabs_all_df['pointid'].isin(plist)) & ((tabs_all_df['LC2014'].isin(aglist)) |(tabs_all_df['LC2014'].isin(natlist))) & (tabs_all_df['LC2030_trt'].isin(developed))) ,'acu_flag'] = 1
#        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030_trt'] = tabs_all_df['LC2014']
#        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'gridcode30_trt'] = tabs_all_df['gridcode14'] + 100
    else:
        pass
    if aca == 1:
        pts = Helpers.create_processing_table(points,acumask, tempgdb, scratch)
        plist = pts['pointid'].tolist()
        Helpers.pmes('Flagging points for avoid conversion to agriculture')
        tabs_all_df['aca_flag'] = 0
        tabs_all_df.loc[((tabs_all_df['pointid'].isin(plist)) & (tabs_all_df['LC2014'].isin(natlist)) & (tabs_all_df['LC2030_trt'].isin(aglist))) ,'aca_flag'] = 1
#        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030_trt'] = tabs_all_df['LC2014']
#        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'gridcode30_trt'] = tabs_all_df['gridcode14'] + 100
        
        
    else:
        pass
    
    carb01 = pd.read_csv(c1)
    carb14 = pd.read_csv(c14)
    carb30 = pd.read_csv(c30)
    Helpers.pmes('Tables Loaded')
    listofdfs = (tabs_all_df,carb01,carb14,carb30)
#    tabs_all_df.to_csv('P:/Temp/initial.csv')
    return listofdfs


