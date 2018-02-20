#Import System Modules
''' This will be a funtion
that takes the activity abbreviations and
the change flag (regular or mod)

It will assign new fields to tabs_all_tempdf dataframe

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


def DoActivities(df,activitylist, scenario,customdev, dictact):
    tempdf = df
    dict_eligibility = {}
    Helpers.ChangeFlag(tempdf,'LC2014','LC2030') #Create a change flag where the landcover is the same between 2014 and 2030
    Helpers.pmes ('Entering the Activity Application Module')

    vlist = []
    #Calculate Riparian Suitability and Selection
    Helpers.pmes (activitylist)
    
    
    
    if 'rre' in activitylist:
        Helpers.pmes ('Applying Riparian Restoration')
        dictact['rre']['query'] = (tempdf['LC2030'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren']) & (tempdf['lcchange'] == 1) & ((tempdf['near_rivers'] < 650) | (tempdf['near_streams'] < 100)) & (tempdf['near_woody'] != 0))
        Helpers.CreateSuitFlags('rre',tempdf,dictact)
        Helpers.CreateEligDict(tempdf, 'rre', dictact,dict_eligibility)
        Helpers.selectionfunc (dict_eligibility,tempdf, 'rre',dictact)
        vlist.append('rre')

    #Create Oak Suitability and Selection
    if 'oak' in activitylist:
        dictact['oak']['query'] =(tempdf['LC2030'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren']) & tempdf['rreselected'] != 1 & (tempdf['lcchange'] == 1))
        Helpers.CreateSuitFlags('oak',tempdf,dictact)
        Helpers.CreateEligDict(tempdf, 'oak', dictact,dict_eligibility)
        Helpers.selectionfunc (dict_eligibility,tempdf, 'oak',dictact)
        vlist.append('oak')
        
    #Calculate 2030MOD values
    #Create GHG dictionary entries for suitability
    if 'rre' in activitylist and 'oak' in activitylist:
        dictact['ccr']['query'] = (df['LC2030'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & (df['rreselected'] == 0) & (df['oakselected'] == 0)
        dictact['mul']['query'] = (df['LC2030'].isin(['Annual Cropland', 'Irrigated Pasture','Rice'])) & (df['lcchange'] == 1) & (df['rreselected'] == 0) & (df['oakselected'] == 0)
        dictact['nfm']['query'] = (df['LC2030'].isin(['Annual Cropland'])) & (df['lcchange'] == 1) & (df['rreselected'] == 0) & (df['oakselected'] == 0)
        dictact['aca']['query'] = (df['LC2030'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & (df['rreselected'] == 0) & (df['oakselected'] == 0)
        dictact['acu']['query'] = (df['LC2030'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & (df['rreselected'] == 0) & (df['oakselected'] == 0)
        dictact['hpl']['query'] = (df['LC2030'].isin(['Orchard','Vineyard'])) & (df['lcchange'] == 1) & (df['rreselected'] == 0) & (df['oakselected'] == 0)
    
    if 'rre' in activitylist and 'oak' not in activitylist:
        dictact['ccr']['query'] = (df['LC2030'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & (df['rreselected'] == 0)
        dictact['mul']['query'] = (df['LC2030'].isin(['Annual Cropland', 'Irrigated Pasture','Rice'])) & (df['lcchange'] == 1) & (df['rreselected'] == 0)
        dictact['nfm']['query'] = (df['LC2030'].isin(['Annual Cropland'])) & (df['lcchange'] == 1) & (df['rreselected'] == 0)
        dictact['aca']['query'] = (df['LC2030'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & (df['rreselected'] == 0)
        dictact['acu']['query'] = (df['LC2030'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & (df['rreselected'] == 0)
        dictact['hpl']['query'] = (df['LC2030'].isin(['Orchard','Vineyard'])) & (df['lcchange'] == 1) & (df['rreselected'] == 0)
        
    if 'rre' not in activitylist and 'oak' in activitylist:
        dictact['ccr']['query'] = (df['LC2030'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & (df['oakselected'] == 0)
        dictact['mul']['query'] = (df['LC2030'].isin(['Annual Cropland', 'Irrigated Pasture','Rice'])) & (df['lcchange'] == 1) & (df['oakselected'] == 0)
        dictact['nfm']['query'] = (df['LC2030'].isin(['Annual Cropland'])) & (df['lcchange'] == 1) & (df['oakselected'] == 0)
        dictact['aca']['query'] = (df['LC2030'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & (df['oakselected'] == 0)
        dictact['acu']['query'] = (df['LC2030'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1) & (df['oakselected'] == 0)
        dictact['hpl']['query'] = (df['LC2030'].isin(['Orchard','Vineyard'])) & (df['lcchange'] == 1) & (df['oakselected'] == 0)
        
    if 'rre' not in activitylist and 'oak' not in activitylist:
        dictact['ccr']['query'] = (df['LC2030'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1)
        dictact['mul']['query'] = (df['LC2030'].isin(['Annual Cropland', 'Irrigated Pasture','Rice'])) & (df['lcchange'] == 1)
        dictact['nfm']['query'] = (df['LC2030'].isin(['Annual Cropland'])) & (df['lcchange'] == 1)
        dictact['aca']['query'] = (df['LC2030'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1)
        dictact['acu']['query'] = (df['LC2030'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1)
        dictact['hpl']['query'] = (df['LC2030'].isin(['Orchard','Vineyard'])) & (df['lcchange'] == 1)
        
    #Create green house gas function to run suitability, eligibility and selection functions from Helpers
    def ghg_selection (tempdf,activity,dict_eligibility,dictact):
        Helpers.CreateSuitFlags(activity,tempdf,dictact)
        Helpers.CreateEligDict(tempdf, activity, dictact,dict_eligibility)
        Helpers.selectionfunc (dict_eligibility,tempdf,activity,dictact)

    #GHG Suitability Flag and Selection for CCR
    if 'ccr' in activitylist:
        ghg_selection (tempdf,'ccr',dict_eligibility,dictact)
    if 'mul' in activitylist:
        ghg_selection (tempdf,'mul',dict_eligibility,dictact)
    if 'nfm' in activitylist:
        ghg_selection (tempdf,'nfm',dict_eligibility,dictact)
    if 'hpl' in activitylist:
        ghg_selection (tempdf,'hpl',dict_eligibility,dictact)


    return tempdf





