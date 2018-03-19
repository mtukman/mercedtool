#Import System Modules


import Helpers
global dict_eligibility


def DoActivities(df,activitylist, dictact,acdict, treatmask = 'None',customdev = 0):
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
            
            

    Helpers.pmes (str(queryadd))
    if 'rre' in activitylist:
        Helpers.pmes ('Applying Riparian Restoration')
        Helpers.pmes (queryadd)
        dictact['rre']['query'] = (df['LC2030_trt_bau'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren'])) & (df['lcchange'] == 1) & ((df['near_rivers'] < 650) | (df['near_streams'] < 100)) & (df['near_woody'] != 0) & queryadd
        Helpers.pmes (str(dictact['rre']['query']))
        Helpers.CreateSuitFlags('rre',df,dictact,'rre')
        Helpers.CreateEligDict(df, 'rre', dictact,dict_eligibility, 'rre')
        Helpers.selectionfunc (dict_eligibility,df, 'rre',dictact, 'rre')

        Helpers.lc_mod('rreselected','Woody Riparian', 'LC2030_trt_bau', df)
        Helpers.lc_mod('rreselected','Woody Riparian', 'LC2030_trt_med', df)
        Helpers.lc_mod('rreselected','Woody Riparian', 'LC2030_trt_max', df)
        Helpers.lc_mod('rreselected',16, 'gridcode30_trt_bau', df)
        Helpers.lc_mod('rreselected',16, 'gridcode30_trt_med', df)
        Helpers.lc_mod('rreselected',16, 'gridcode30_trt_max', df)
        if customdev == 1:
            Helpers.lc_mod('rreselected','Woody Riparian', 'LC2030_trt_cust', df)        
        if customdev == 1:
            Helpers.lc_mod('rreselected',16, 'gridcode30_trt_cust', df)
    
    #Create Oak Suitability and Selection
    if 'oak' in activitylist:
        dictact['oak']['query'] =(df['LC2030_trt_bau'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren'])) & (df['rreselected'] != 1) & (df['lcchange'] == 1) & (df['oakrange_flg'] == 1) & queryadd
               
        Helpers.CreateSuitFlags('oak',df,dictact, 'oak')
        Helpers.CreateEligDict(df, 'oak', dictact,dict_eligibility, 'oak')
        Helpers.selectionfunc (dict_eligibility,df, 'oak',dictact, 'oak')

        
    
        Helpers.lc_mod('oakselected','Oak Conversion', 'LC2030_trt_bau', df)
        Helpers.lc_mod('oakselected','Oak Conversion', 'LC2030_trt_med', df)  
        Helpers.lc_mod('oakselected','Oak Conversion', 'LC2030_trt_max', df)
        
        if customdev == 1:
            Helpers.lc_mod('rreselected','Oak Conversion', 'LC2030_trt_cust', df)
        

        Helpers.lc_mod('oakselected',17, 'gridcode30_trt_bau', df)  
        
        Helpers.lc_mod('oakselected',17, 'gridcode30_trt_med', df) 
        
        Helpers.lc_mod('oakselected',17, 'gridcode30_trt_max', df) 
        if customdev == 1:
            Helpers.lc_mod('oakselected',17, 'gridcode30_trt_cust', df)
    
    #Calculate 2030MOD values
    #Create GHG dictionary entries for suitability
    
    df['lcchange'] = 0
    df.loc[(df['LC2030_trt_bau'] == df['LC2014']), 'lcchange'] = 1
    
    dictact['ccr']['query'] = (df['LC2030_trt_bau'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & queryadd
    dictact['mul']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland', 'Irrigated Pasture','Rice'])) & (df['lcchange'] == 1) & queryadd
    dictact['nfm']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland'])) & (df['lcchange'] == 1) & queryadd
    dictact['hpl']['query'] = (df['LC2030_trt_bau'].isin(['Orchard','Vineyard'])) & (df['lcchange'] == 1) & queryadd
    
    
    
    
    #Create green house gas function to run suitability, eligibility and selection functions from Helpers
    def ghg_selection (df,activity,dict_eligibility,dictact):
        Helpers.CreateSuitFlags(activity,df,dictact, activity)
        Helpers.CreateEligDict(df, activity, dictact,dict_eligibility, activity)
        Helpers.selectionfunc (dict_eligibility,df,activity,dictact, activity)

    #GHG Suitability Flag and Selection for CCR
    if 'ccr' in activitylist:
        ghg_selection (df,'ccr',dict_eligibility,dictact)
    if 'mul' in activitylist:
        ghg_selection (df,'mul',dict_eligibility,dictact)
    if 'nfm' in activitylist:
        ghg_selection (df,'nfm',dict_eligibility,dictact)
    if 'hpl' in activitylist:
        ghg_selection (df,'hpl',dict_eligibility,dictact)



    keylist = [*acdict]
    Helpers.pmes(keylist)
    for i in keylist:
        if i == 'ac_for_urb':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Urban', 'Developed', 'Developed Roads'])) & (df['LC2014'] == 'Forest')
            t = 'Forest'
            g = 3
        if i == 'ac_for_arc':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland'])) & (df['LC2014'] == 'Forest')
            t = 'Forest'
            g = 3
        if i == 'ac_gra_arc':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland'])) & (df['LC2014'] == 'Grassland')
            t = 'Grassland'
            g = 2
        if i == 'ac_irr_arc':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland'])) & (df['LC2014'] == 'Irrigated Pasture')
            t = 'Irrigated Pasture'
            g = 11
        if i == 'ac_orc_arc':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland'])) & (df['LC2014'] == 'Orchard')
            t = 'Orchard'
            g = 7
        if i == 'ac_shr_arc':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland'])) & (df['LC2014'] == 'Shrubland')
            t = 'Shrubland'
            g = 5
        if i == 'ac_vin_arc':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Annual Cropland'])) & (df['LC2014'] == 'Vineyard')
            t = 'Vineyard'
            g = 8
        if i == 'ac_shr_urb':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Urban', 'Developed', 'Developed Roads'])) & (df['LC2014'] == 'Forest')
            t = 'Forest'
            g = 3
        if i == 'ac_orc_urb':
            dictact['aco']['query'] = (df['LC2030_trt_bau'].isin(['Urban', 'Developed', 'Developed Roads'])) & (df['LC2014'] == 'Orchard')
            t = 'Orchard'
            g = 7
            
        Helpers.pmes(acdict[i])
        Helpers.pmes(i)
        dictact['aco']['adoption'] = acdict[i]
        
        Helpers.CreateSuitFlags('aco',df,dictact, i)
        Helpers.CreateEligDict(df, 'aco', dictact,dict_eligibility, i)
        Helpers.selectionfunc (dict_eligibility,df,'aco',dictact, i)
    
    
        Helpers.lc_mod(i+'selected',t, 'LC2030_trt_bau', df)

        Helpers.lc_mod(i+'selected',g, 'gridcode30_trt_bau', df)


    return df






























