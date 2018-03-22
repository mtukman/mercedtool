#Import System Modules


import Helpers
global dict_eligibility


def DoActivities(df,activitylist, dictact,acdict,logfile, treatmask = 'None',customdev = 0):
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
    Helpers.pmes (activitylist)
    queryadd =  ((df['dcode_medinfill'] == 0) & (df['dcode_maxinfill'] == 0))
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
        dictact['rre']['query'] = (df['LC2030_trt_bau'].isin(['Grassland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren'])) & (df['lcchange'] == 1) & ((df['near_rivers'] < 650) | (df['near_streams'] < 100)) & (df['near_woody'] != 0) & queryadd
        Helpers.CreateSuitFlags('rre',df,dictact,'rre')
        Helpers.CreateEligDict(df, 'rre', dictact,dict_eligibility, 'rre')
        
        # Select points randomly that were flagged as suitable
        Helpers.selectionfunc (dict_eligibility,df, 'rre',dictact, 'rre', logfile)
        
        #Update treatment scenario fields to reflect selections
        Helpers.lc_mod('rreselected','Woody Riparian', 'LC2030_trt_bau', df)
        Helpers.lc_mod('rreselected','Woody Riparian', 'LC2030_trt_med', df)
        Helpers.lc_mod('rreselected','Woody Riparian', 'LC2030_trt_max', df)
        Helpers.lc_mod('rreselected',16, 'gridcode30_trt_bau', df)
        Helpers.lc_mod('rreselected',16, 'gridcode30_trt_med', df)
        Helpers.lc_mod('rreselected',16, 'gridcode30_trt_max', df)
    
    #Create Oak Suitability and Selection
    if 'oak' in activitylist:
        dictact['oak']['query'] =((df['LC2030_trt_bau'].isin(['Grassland','Shrubland','Irrigated Pasture','Barren']))|((df['LC2030_trt_bau']== 'Urban') & df['nlcd_val'].isin([21,22,31]))) & (df['rreselected'] != 1) & (df['lcchange'] == 1) & (df['oakrange_flg'] == 1) & queryadd
        #Create suitability flags for the oak conversion activity
        Helpers.CreateSuitFlags('oak',df,dictact, 'oak')
        Helpers.CreateEligDict(df, 'oak', dictact,dict_eligibility, 'oak')
        #Select points randomly for the oak conversion activity
        Helpers.selectionfunc (dict_eligibility,df, 'oak',dictact, 'oak', logfile)

        
        #Change landcover and gridcode fields for points selected for the activity
        Helpers.lc_mod('oakselected','Oak Conversion', 'LC2030_trt_bau', df)
        Helpers.lc_mod('oakselected','Oak Conversion', 'LC2030_trt_med', df)  
        Helpers.lc_mod('oakselected','Oak Conversion', 'LC2030_trt_max', df)
        Helpers.lc_mod('oakselected',17, 'gridcode30_trt_bau', df)  
        Helpers.lc_mod('oakselected',17, 'gridcode30_trt_med', df) 
        Helpers.lc_mod('oakselected',17, 'gridcode30_trt_max', df) 

            
    if 'gra' in activitylist:
        dictact['gra']['query'] =(df['LC2030_trt_bau'].isin(['Grassland'])) & ((df['rreselected'] != 1)|(df['oakselected'] != 1)) & (df['lcchange'] == 1) & queryadd
        #Create suitability flags for the grassland restoration activity
        Helpers.CreateSuitFlags('gra',df,dictact, 'gra')
        Helpers.CreateEligDict(df, 'gra', dictact,dict_eligibility, 'gra')
        #Select points randomly for the grassland restoration activity
        Helpers.selectionfunc (dict_eligibility,df, 'gra',dictact, 'gra', logfile)

        
        #Change landcover and gridcode fields for points selected for the activity
        Helpers.lc_mod('graselected','Grassland', 'LC2030_trt_bau', df)
        Helpers.lc_mod('graselected','Grassland', 'LC2030_trt_med', df)  
        Helpers.lc_mod('graselected','Grassland', 'LC2030_trt_max', df)
        Helpers.lc_mod('graselected',2, 'gridcode30_trt_bau', df)  
        Helpers.lc_mod('graselected',2, 'gridcode30_trt_med', df) 
        Helpers.lc_mod('graselected',2, 'gridcode30_trt_max', df) 

    
    #Calculate 2030MOD values
    #Create GHG dictionary entries for suitability, these queries will be used for the ag activity suitability function
    df['lcchange'] = 0
    
    #This next line of code updates the land cover change flag, which removes pixels selected for those activities from consideration for ag activity suitability
    df.loc[(df['LC2030_trt_bau'] == df['LC2014']), 'lcchange'] = 1
    
    
    dictact['ccr']['query'] = (df['LC2030_trt_bau'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & queryadd
    dictact['mul']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland','Rice'])) & (df['lcchange'] == 1) & queryadd
    dictact['nfm']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland', 'Orchard', 'Vineyard', 'Rice'])) & (df['lcchange'] == 1) & queryadd
    dictact['hpl']['query'] = (df['LC2030_trt_bau'].isin(['Orchard','Vineyard'])) & (df['lcchange'] == 1) & queryadd
    dictact['cam']['query'] = (df['LC2030_trt_bau'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & queryadd
    dictact['cag']['query'] = (df['LC2030_trt_bau'].isin(['Grassland'])) & (df['lcchange'] == 1) & queryadd
    

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


    #Loop through the keys in the acdict dictionary, created in the main program. For each avoided conversion activity found, perform suitability, eligibility and selection functions.
    keylist = [*acdict]
    Helpers.pmes(keylist)
    for i in keylist:
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
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Orchard'])) & (df['LC2014'] == 'Annual Cropland') & (df['LC2030_bau'].isin(['Orchard']))
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
        Helpers.pmes(acdict[i])
        Helpers.pmes(i)
        dictact['aco']['adoption'] = acdict[i]
        
        Helpers.CreateSuitFlags('aco',df,dictact, i)
        Helpers.CreateEligDict(df, 'aco', dictact,dict_eligibility, i)
        Helpers.selectionfunc (dict_eligibility,df,'aco',dictact, i, logfile)
    
        #Change the gridcode and landcover label in the treatment bau
        Helpers.lc_mod(i+'selected',t, 'LC2030_trt_bau', df)

        Helpers.lc_mod(i+'selected',g, 'gridcode30_trt_bau', df)


    return df






























