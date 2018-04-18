#Import System Modules


import Helpers
global dict_eligibility


def DoActivities(df,activitylist, dictact,acdict,logfile, treatmask = 'None',customdev = 0, ug = 0, ucc = 0, sflag = 0):
    ''' This function takes the activities selected by the user, finds suitable pixels and randomly selects pixels for the activity based on spatial attributes until the desired amount of pixels have been selected.
    
    df: The dataframe fom the initial module
    activitylist: List of activities selected in the tool, from the main_program module
    dictact: Dictionary of values and queries that is housed in the Generic module
    acdict: Diction of avoided conversion activities, created in the main_program module
    treatmask: The treatment mask, if one has been specified in the tool.
    customdev: custom development mask, if one has been specified in the tool.
    
    
    Activity abbreviations are
    oak - OAK WOODLAND RESTORATION
    rre - RIPARIAN RESTORATION
    mul - MULCHING
    nfm - NITROGEN FERTILIZER MANAGEMENT
    ccr - COVER CROPS
    hpl - HEDGEROW PLANTING
    urb - URBAN FORESTRY
    '''
    #Create a dictionary of eligibility,this will inform the tool as to how many points need to be selected and will be populated as the tool progresses
    dict_eligibility = {}

    Helpers.ChangeFlag(df,'LC2014','LC2030_trt_bau') #Create a change flag where the landcover is the same between 2014 and 2030
    Helpers.pmes ('Entering the Activity Application Module')


    #Create an query addon that is based on whether a custom development or treatment mask has been provided by the user.
    queryadd =  ((df['pref_dev_flag'] == 0) & (df['dcode_maxinfill'] == 0))
    if customdev == 1:
        
        if treatmask != 'None':
            Helpers.pmes ('customdev = 1, treatmask')
            queryadd = queryadd & (df['trt_flag'] == 1) & (df['gridcode30_trt_cust'] != 13)
        else:
            Helpers.pmes ('customdev = 1, no treatmask')
            queryadd = queryadd &  (df['gridcode30_trt_cust'] != 13)
        
    else:    
        if treatmask != 'None':
            Helpers.pmes ('customdev != 1, treatmask')
            queryadd = queryadd &  (df['trt_flag'] == 1)
        
            
            
    # Start the activity applications. This first section creates suitability flags for the riparian activity.
    if 'rre' in activitylist:
        Helpers.pmes ('Applying Riparian Restoration')
        
        
        #Set the query that will define suitability
        dictact['rre']['query'] = (df['LC2030_trt_bau'].isin(['Grassland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren'])) & (df['lcchange'] == 1) & ((df['near_rivers'] < 304.8) | ((df['ripstr_dist'] < 30.48) & (df['ripstr_flag'] == 1))) & (df['near_woody'] != 0) & queryadd #Units are in meters for distance requirements (df['LC2030_trt_bau'].isin(['Grassland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren'])) & (df['lcchange'] == 1) & ((df['near_rivers'] < 304.8) | ((df['ripstr_dist'] < 30.48) & (df['ripstr_flag'] == 1))) & (df['near_woody'] != 0) & 
        Helpers.CreateSuitFlags('rre',df,dictact,'rre')
        Helpers.CreateEligDict(df, 'rre', dictact,dict_eligibility, 'rre')
        
        # Select points randomly that were flagged as suitable
        Helpers.selectionfunc (dict_eligibility,df, 'rre',dictact, 'rre', logfile)
        queryadd = queryadd & (df['rreselected'] != 1)
        df.loc[df['rreselected'] == 1, 'LC2030_trt_bau'] = 'Forest'
        df.loc[df['rreselected'] == 1, 'LC2030_trt_med'] = 'Forest'
        df.loc[df['rreselected'] == 1, 'LC2030_trt_max'] = 'Forest'
        df.loc[df['rreselected'] == 1, 'gridcode30_trt_bau'] = 3
        df.loc[df['rreselected'] == 1, 'gridcode30_trt_med'] = 3
        df.loc[df['rreselected'] == 1, 'gridcode30_trt_max'] = 3
        if customdev == 1:
            df.loc[df['rreselected'] == 1, 'LC2030_trt_cust'] = 'Forest'
            df.loc[df['rreselected'] == 1, 'gridcode30_trt_cust'] = 3
            
    #Create Oak Suitability and Selection
    if 'oak' in activitylist:
        dictact['oak']['query'] =(df['LC2030_trt_bau'].isin(['Grassland','Shrubland','Irrigated Pasture','Barren'])) & (df['lcchange'] == 1) & (df['oakrange_flg'] == 1) & queryadd
        #Create suitability flags for the oak conversion activity
        Helpers.CreateSuitFlags('oak',df,dictact, 'oak')
        Helpers.CreateEligDict(df, 'oak', dictact,dict_eligibility, 'oak')
        #Select points randomly for the oak conversion activity
        Helpers.selectionfunc (dict_eligibility,df, 'oak',dictact, 'oak', logfile)
        queryadd = queryadd & (df['oakselected'] != 1)
        df.loc[df['oakselected'] == 1, 'LC2030_trt_bau'] = 'Forest'
        df.loc[df['oakselected'] == 1, 'LC2030_trt_med'] = 'Forest'
        df.loc[df['oakselected'] == 1, 'LC2030_trt_max'] = 'Forest'
        df.loc[df['oakselected'] == 1, 'gridcode30_trt_bau'] = 11
        df.loc[df['oakselected'] == 1, 'gridcode30_trt_med'] = 11
        df.loc[df['oakselected'] == 1, 'gridcode30_trt_max'] = 11
        if customdev == 1:
            df.loc[df['oakselected'] == 1, 'LC2030_trt_cust'] = 'Forest'
            df.loc[df['oakselected'] == 1, 'gridcode30_trt_cust'] = 3
        #Change landcover and gridcode fields for points selected for the activity

    
    #Calculate 2030MOD values
    #Create GHG dictionary entries for suitability, these queries will be used for the ag activity suitability function
    df['lcchange'] = 0
    
    #This next line of code updates the land cover change flag, which removes pixels selected for those activities from consideration for ag activity suitability
    df.loc[(df['LC2030_trt_bau'] == df['LC2014']), 'lcchange'] = 1
    
    
    #Loop through the keys in the acdict dictionary, created in the main program. For each avoided conversion activity found, perform suitability, eligibility and selection functions.    
    keylist = [*acdict]
    for i in keylist:
        df.loc[(df['LC2030_trt_bau'] == df['LC2030_bau']), 'lcchange'] = 1   
        if i == 'ac_wet_arc':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland'])) & (df['LC2014'] == 'Wetland') & (df['LC2030_bau'].isin(['Annual Cropland']))
            t = 'Wetland'
            g = 0
        if i == 'ac_gra_arc':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland'])) & (df['LC2014'] == 'Grassland') & (df['LC2030_bau'].isin(['Annual Cropland']))
            t = 'Grassland'
            g = 2
        if i == 'ac_irr_arc':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland'])) & (df['LC2014'] == 'Irrigated Pasture') & (df['LC2030_bau'].isin(['Annual Cropland']))
            t = 'Irrigated Pasture'
            g = 11
        if i == 'ac_orc_arc':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland'])) & (df['LC2014'] == 'Orchard') & (df['LC2030_bau'].isin(['Annual Cropland']))
            t = 'Orchard'
            g = 9
        if i == 'ac_arc_urb':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Urban', 'Developed', 'Developed Roads'])) & (df['LC2014'] == 'Annual Cropland') & (df['LC2030_bau'].isin(['Urban', 'Developed', 'Developed Roads']))
            t = 'Annual Cropland'
            g = 7
        if i == 'ac_gra_urb':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Urban', 'Developed', 'Developed Roads'])) & (df['LC2014'] == 'Grassland') & (df['LC2030_bau'].isin(['Urban', 'Developed', 'Developed Roads']))
            t = 'Grassland'
            g = 2
        if i == 'ac_irr_urb':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Urban', 'Developed', 'Developed Roads'])) & (df['LC2014'] == 'Irrigated Pasture') & (df['LC2030_bau'].isin(['Urban', 'Developed', 'Developed Roads']))
            t = 'Irrigated Pasture'
            g = 11
        if i == 'ac_orc_urb':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Urban', 'Developed', 'Developed Roads'])) & (df['LC2014'] == 'Orchard') & (df['LC2030_bau'].isin(['Urban', 'Developed', 'Developed Roads']))
            t = 'Orchard'
            g = 9
        if i == 'ac_arc_orc':
            dictact['aco']['query'] = (df['LC2014'] == 'Annual Cropland') & (df['lcchange'] == 1) & (df['LC2030_trt_bau'].isin(['Orchard']))
            t = 'Annual Cropland'
            g = 7
        if i == 'ac_gra_orc':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Orchard'])) & (df['LC2014'] == 'Grassland') & (df['LC2030_bau'].isin(['Orchard']))
            t = 'Grassland'
            g = 2
        if i == 'ac_irr_orc':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Orchard'])) & (df['LC2014'] == 'Irrigated Pasture') & (df['LC2030_bau'].isin(['Orchard']))
            t = 'Irrigated Pasture'
            g = 11
        if i == 'ac_vin_orc':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Orchard'])) & (df['LC2014'] == 'Vineyard') & (df['LC2030_bau'].isin(['Orchard']))
            t = 'Orchard'
            g = 9
        if i == 'ac_arc_irr':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Irrigated Pasture'])) & (df['LC2014'] == 'Annual Cropland') & (df['LC2030_bau'].isin(['Irrigated Pasture']))
            t = 'Annual Cropland'
            g = 7
        if i == 'ac_orc_irr':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Irrigated Pasture'])) & (df['LC2014'] == 'Orchard') & (df['LC2030_bau'].isin(['Irrigated Pasture']))
            t = 'Orchard'
            g = 9
            #Do the suitability, eligibility and selection functions for an avoided conversion activity
        dictact['aco']['adoption'] = acdict[i]
        
        Helpers.CreateSuitFlags('aco',df,dictact, i)
        Helpers.CreateEligDict(df, 'aco', dictact,dict_eligibility, i)
        Helpers.selectionfunc (dict_eligibility,df,'aco',dictact, i, logfile)
    
        #Change the gridcode and landcover label in the treatment bau
        Helpers.lc_mod(i+'selected',t, 'LC2030_trt_bau', df)

        Helpers.lc_mod(i+'selected',g, 'gridcode30_trt_bau', df)
        
    #Create GHG dictionary entries for suitability, these queries will be used for the ag activity suitability function
    df['lcchange'] = 0
    
    #This next line of code updates the land cover change flag, which removes pixels selected for those activities from consideration for ag activity suitability
    df.loc[(df['LC2030_trt_bau'] == df['LC2014']), 'lcchange'] = 1        
        
    dictact['ccr']['query'] = queryadd #(df['LC2030_trt_bau'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & 
    dictact['mul']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland','Rice'])) & (df['lcchange'] == 1) & queryadd
    dictact['nfm']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland', 'Orchard', 'Vineyard', 'Rice'])) & (df['lcchange'] == 1) & queryadd
    dictact['hpl']['query'] = queryadd #(df['LC2030_trt_bau'].isin(['Orchard','Vineyard'])) & (df['lcchange'] == 1) & 
    dictact['cam']['query'] = (df['LC2030_trt_bau'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & queryadd
    dictact['urb']['query'] = (df['LC2030_trt_bau'].isin(['Urban', 'Developed', 'Developed Roads'])) & (df['lcchange'] == 1) & queryadd
    dictact['cag']['query'] = (df['LC2030_trt_bau'].isin(['Grassland'])) & (df['lcchange'] == 1) & (df['slope_val'] < 15) & ((df['near_rivers'] > 304.8) | (df['near_streams'] > 30.48)) & queryadd
    dictact['gra']['query'] = (df['LC2030_trt_bau'].isin(['Grassland'])) & (df['lcchange'] == 1) & queryadd #Units are in meters for distance requirements

    #Create green house gas function to run suitability, eligibility and selection functions from Helpers
    def ghg_selection (df,activity,dict_eligibility,dictact):
        Helpers.CreateSuitFlags(activity,df,dictact, activity)
        Helpers.CreateEligDict(df, activity, dictact,dict_eligibility, activity)
        Helpers.selectionfunc (dict_eligibility,df,activity,dictact, activity, logfile)
    #GHG Suitability Flag and Selection for CCR
    if 'ccr' in activitylist:
        ghg_selection (df,'ccr',dict_eligibility,dictact)
    if 'mul' in activitylist:
        ghg_selection (df,'mul',dict_eligibility,dictact)
    if 'nfm' in activitylist:
        ghg_selection (df,'nfm',dict_eligibility,dictact)
    if 'hpl' in activitylist:
        ghg_selection (df,'hpl',dict_eligibility,dictact)
    if 'cam' in activitylist:
        ghg_selection (df,'cam',dict_eligibility,dictact)
    if 'cag' in activitylist:
        ghg_selection (df,'cag',dict_eligibility,dictact)
    if 'gra' in activitylist:
        ghg_selection (df,'gra',dict_eligibility,dictact)
#    if ug != 0:
#        temp = df.loc[(df['LC2030_trt_bau'].isin(['Urban', 'Developed','Developed Roads'])) & (df['lcchange'] == 1) & queryadd]
#        numb = len(temp.index)
#        Helpers.pmes ('Suitable Pixels for Urban: ' + str(numb))
#        dictact['urb']['adoption'] = numb/4.49555
#        Helpers.pmes ('Suitable Acres for Urban: ' + str(dictact['urb2']['adoption']))
#        ghg_selection (df,'urb',dict_eligibility,dictact)
        
        
    if ug != 0:
        temp = df.loc[(df['LC2030_trt_bau'].isin(['Urban', 'Developed','Developed Roads'])) & (df['lcchange'] == 1) & queryadd]
        numb = len(temp.index)
        dictact['urb']['adoption'] = numb/4.49555
        dictact['urb']['adoption'] = dictact['urb']['adoption']*ug
        Helpers.pmes ('Adoption Goal Acres for Urban: ' + str(dictact['urb']['adoption']))
        
        ghg_selection (df,'urb',dict_eligibility,dictact)
        
    blist = ['ccrsuitflag','mulsuitflag','nfmsuitflag','hplsuitflag','camsuitflag','cagsuitflag','grasuitflag','urbsuitflag','urb2suitflag','oaksuitflag','rresuitflag','ac_wet_arc','ac_gra_arc','ac_irr_arc','ac_orc_arc','ac_arc_urb','ac_gra_urb','ac_irr_urb','ac_orc_urb','ac_arc_orc','ac_gra_orc','ac_irr_orc','ac_vin_orc','ac_arc_irr','ac_orc_irr','gp_code','LC2001','hydrovuln_flag','huc12_val','slope_val','medgroup_val','smallgroup_val','gridcode01','pref_dev_flag','near_nwi','near_roads','pref_dev_type','woodyrip_class','near_woody', 'biodiversity_rank','clim_rank','terrhabrank']
    
    clist = []
    for i in blist:
        if i in df.columns:
            clist.append(i)
#    df = df.drop(columns = clist)
    df.drop(clist, axis = 1, inplace = True)       
    
    
    
    
    return df






























