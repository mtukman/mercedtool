#Import System Modules
''' This will be a funtion
that takes the activity abbreviations and
the change flag (regular or mod)

It will assign new fields to tabs_all_df dataframe

it will be run from main_program.py first for the
land cover changing activities and then for the
non land cover changing ones
'''
''' Activey abbreviations are
oak - OAK WOODLAND RESTORATION
rre - RIPARIAN RESTORATION
mul - MULCHING
nfm - NITROGEN FERTILIZER MANAGEMENT
ccr - COVER CROPS
aca - AVOIDED CONVERSION TO AG
acu - AVOIDED CONVERSION TO URBAN
hpl - HEDGEROW PLANTING
urb - URBAN FORESTRY
'''

import Helpers
global dict_eligibility


def DoActivities(df,activitylist, dictact,acdict, treatmask = 'None',customdev = 0, aca = 0, acu= 0):
    dict_eligibility = {}
    
    Helpers.ChangeFlag(df,'LC2014','LC2030_trt_bau') #Create a change flag where the landcover is the same between 2014 and 2030
    Helpers.pmes ('Entering the Activity Application Module')


    #Calculate Riparian Suitability and Selection
    Helpers.pmes (activitylist)
    if customdev == 1:
        if treatmask != 'None':
            queryadd = ((df['dcode_medinfill'] == 0) & (df['dcode_maxinfill'] == 0))&(df['trt_flag'] == 1) & (df['gridcode30_trt_cust'] != 13)
        else:
            queryadd = ((df['dcode_medinfill'] == 0) & (df['dcode_maxinfill'] == 0))&(df['gridcode30_trt_cust'] != 13)
        
    else:    
        if treatmask != 'None':
            queryadd = ((df['dcode_medinfill'] == 0) & (df['dcode_maxinfill'] == 0))& (df['trt_flag'] == 1)

        else:
            queryadd = ((df['dcode_medinfill'] == 0) & (df['dcode_maxinfill'] == 0))
            
    if 'rre' in activitylist:
        Helpers.pmes ('Applying Riparian Restoration')
        dictact['rre']['query'] = (df['LC2030_trt_bau'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren'])) & (df['lcchange'] == 1) & ((df['near_rivers'] < 650) | (df['near_streams'] < 100)) & (df['near_woody'] != 0) & ((df['dcode_medinfill'] == 0) & (df['dcode_maxinfill'] == 0))
        Helpers.CreateSuitFlags('rre',df,dictact)
        Helpers.CreateEligDict(df, 'rre', dictact,dict_eligibility)
        Helpers.selectionfunc (dict_eligibility,df, 'rre',dictact)

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
        dictact['oak']['query'] =(df['LC2030_trt_bau'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren'])) & (df['rreselected'] != 1) & (df['lcchange'] == 1) & (df['oakrange_flg'] == 1) & ((df['dcode_medinfill'] == 0) & (df['dcode_maxinfill'] == 0))
               
        Helpers.CreateSuitFlags('oak',df,dictact)
        Helpers.CreateEligDict(df, 'oak', dictact,dict_eligibility)
        Helpers.selectionfunc (dict_eligibility,df, 'oak',dictact)

        
    
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
        Helpers.CreateSuitFlags(activity,df,dictact)
        Helpers.CreateEligDict(df, activity, dictact,dict_eligibility)
        Helpers.selectionfunc (dict_eligibility,df,activity,dictact)

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
            
        Helpers.CreateSuitFlags('aco',df,dictact, i)
        Helpers.CreateEligDict(df, 'aco', dictact,dict_eligibility, i)
        Helpers.selectionfunc (dict_eligibility,df,'aco',dictact, i)
        Helpers.lc_mod(i+'selected',t, 'LC2030_trt_bau', df)

        Helpers.lc_mod(i+'selected',g, 'gridcode30_trt_bau', df)


    return df






























