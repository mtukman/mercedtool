#Import System Modules

    
def DoInitial(procmask, cs, cd, devmask, c1,c14,c30,joins,nears,points, tempgdb, scratch, cm, conmask = 'None', treatmask = 'None'):
    """
    This function imports the primary tables, sets the dataframes used in the rest of the tool, and applies the conservation, developed, and treatment masks specificed in the tool inputs.
    ______________________________________________________________________________________________________________
    procmask: Custom processing mask, the function will use this if it exists, to decrease the size of the study area to the polygon's extent.
    cs: This is a custom processing flag.
    cd = This is a custom development mask flag. If it is 0, nothing happens. If it is 1, then a new development scenario is created (custom), where new 2030 development is replace by the development mask (devmask). If
    the flag is a 2, then new development is added to the BAU scenario in the treatment.
    devmask = The development polygon mask associated with cd.
    c1: Carbon look up table for 2001, defined in Generic Module
    c14: Carbon look up table for 2014 Generic Module
    c30: Carbon look up table for 2030 Generic Module
    joins: csv of points with attribute values
    nears: csv of points with near values (distance from nearest road, river etc.)
    points: Feature class with all the points converted from the landfire raster
    tempgdb: Temporary geodatabase where geoprocessing occurs
    scratch: Scratch folder
    cm: conservask flag, 0 is no mask, 1 is mask
    conmask: location of the conservation mask feature class
    treatmask: location of the treatmant mask is one is chosen
    
    
    """
    import pandas as pd
    import Helpers
    #Load Tables into Dataframes
    jointables = Helpers.LoadCSVs(joins)
    value_df = Helpers.MergeMultiDF('pointid', jointables)

    neartables = Helpers.LoadCSVs(nears)
    near_df = Helpers.MergeMultiDF('pointid', neartables)
    
    #Define the list of developed landcovers
    developed = ['Developed','Urban','Developed Roads']
    
    
    #Merge the near table and value table on pointid
    tabs_all_df = pd.merge(value_df,near_df, on = 'pointid')
    
    #Create landcover fields for the treatment scenarios and fill with baseline landcovers
    tabs_all_df['LC2030_trt_bau'] = tabs_all_df['LC2030_bau']
    tabs_all_df['LC2030_trt_med'] = tabs_all_df['LC2030_med']
    tabs_all_df['LC2030_trt_max'] = tabs_all_df['LC2030_max']


    #Create gridcode fields for the treatment scenarios and fill with baseline gridcodes
    tabs_all_df['gridcode30_trt_bau'] = tabs_all_df['gridcode30_bau']
    tabs_all_df['gridcode30_trt_med'] = tabs_all_df['gridcode30_med']
    tabs_all_df['gridcode30_trt_max'] = tabs_all_df['gridcode30_max']
    
    #Create modified dataframe using processing area mask if one is chosen
    if cs == 1:
        pts = Helpers.create_processing_table(points,procmask, tempgdb, scratch)
        tabs_all_df = pd.merge(pts,tabs_all_df, how = 'left', on = 'pointid')
    else:
        pass
    
    
    
    #Add User-defined additional urban areas using user-defined urban mask
    if cd == 1: #If cd is one, the developed polygons replace the 2030 bau scenario. New development in 2030 bau is reverted to 2014 landcover, and all pixels within the development mask will be changed to urban landcover.
        #Create a new landcover field for 2030 custom development scenario and make equal to the baseline landcover. Do the same for gridcode.
        tabs_all_df['LC2030_cust'] = tabs_all_df['LC2030_bau']
        tabs_all_df['gridcode30_cust'] = tabs_all_df['gridcode30_bau']
        
        #Create a list of points within the development mask
        pts = Helpers.create_processing_table(points,devmask, tempgdb, scratch)
        plist = pts['pointid'].tolist()
        Helpers.pmes('Creating User Defined BAU')
        
        #Where the 2030 bau landcover is different from the 2014 landcover, and the 2030 bau landcover is a developed landcover, change the landcover to the 2014 landcover (revert) 
        tabs_all_df.loc[((tabs_all_df['LC2030_cust'] != tabs_all_df['LC2014']) & (tabs_all_df['LC2030_cust'].isin(developed))),'LC2030_cust'] = tabs_all_df['LC2014']
        
        tabs_all_df['LC2030_trt_cust'] = tabs_all_df['LC2030_cust']
        
        tabs_all_df['gridcode30_trt_cust'] = tabs_all_df['gridcode30_cust']
        
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'gridcode30_cust'] = 13
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'gridcode30_trt_cust'] = 13

        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030_trt_cust'] = 'Urban'
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030_cust'] = 'Urban'
        tabs_all_df['dev_flag'] = 0
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'dev_flag'] = 1        
    # If a custom development area is specified, change pixels in the treatment landcover and treatment gridcodes to urban.
    elif cd == 2:
        pts = Helpers.create_processing_table(points,devmask, tempgdb, scratch)
        plist = pts['pointid'].tolist()
        Helpers.pmes('Creating User Defined Developent Polygons')
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'gridcode30_trt_bau'] = 13
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'gridcode30_trt_med'] = 13
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'gridcode30_trt_max'] = 13
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030_trt_bau'] = 'Urban'
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030_trt_med'] = 'Urban'
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030_trt_max'] = 'Urban'
        tabs_all_df['dev_flag'] = 0
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'dev_flag'] = 1
        
    else:
        pass

    #If a conservation mask was specified, change all pixels within the mask from treatment classes to 2014 landcover.
    if cm == 1:
        #Get list of points in mask
        pts = Helpers.create_processing_table(points,conmask, tempgdb, scratch)
        plist = pts['pointid'].tolist()
        Helpers.pmes('Creating User Defined Conservation Polygons')
        
        #Change treatment landcovers to 2014 landcovers
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030_trt_bau'] = tabs_all_df['LC2014']
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030_trt_med'] = tabs_all_df['LC2014']
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030_trt_max'] = tabs_all_df['LC2014']
        
        #IF there is a custom baseline development mask, also revert the landcovers in the LC2030_trt_cust field.
        if cd in [1]:
                  
            tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'LC2030_trt_cust'] = tabs_all_df['LC2014']  
        
        #Flag points that were conserved
        tabs_all_df['con_flag'] = 0
        tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'con_flag'] = 1
        
        #Change the development flag for pixels that were changed to 2014
        if cd == 1:
            tabs_all_df.loc[tabs_all_df['pointid'].isin(plist),'dev_flag'] = 0
            
    #Create a general gridcode look-up dictionary
    gcdict = {'Wetland':0, 'Water':1, 'Grassland':2,'Barren':4, 'Orchard':7,'Vineyard':8,'Annual Cropland':9,'Rice':10,'Irrigated Pasture':11,'Young Forest':14, 'Young Shrubland':15}
    
    
    devlist = ['bau','med','max']
    keylist = [*gcdict]
    
    #Make sure all gridcodes in treatment scenarios are correct
    for i in devlist:
        for x in keylist:
            tabs_all_df.loc[(tabs_all_df['LC2030_trt_'+i] ==  x),'gridcode30_trt_' + i] = gcdict[x]



    #If a treatment mask was specified, set a treatment flag so activities can only occur in these areas
    if treatmask != 'None':
        pts = Helpers.create_processing_table(points,treatmask, tempgdb, scratch)
        plist = pts['pointid'].tolist()
        Helpers.pmes('Flagging points for treatment')
        tabs_all_df['trt_flag'] = 0
        tabs_all_df.loc[(tabs_all_df['pointid'].isin(plist)) ,'trt_flag'] = 1

    else:
        tabs_all_df['trt_flag'] = 0
    
    #Load up the carbon look up tables
    carb01 = pd.read_csv(c1)
    carb14 = pd.read_csv(c14)
    carb30 = pd.read_csv(c30)
    Helpers.pmes('Tables Loaded')
    listofdfs = (tabs_all_df,carb01,carb14,carb30)
    return listofdfs




































