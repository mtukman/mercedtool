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
import pandas as pd
import Generic
import Helpers
global dict_eligibility

def DoActivities(df):
    tempdf = df
    dict_eligibility = {}
    
    smallgroup = 20000
    mediumgroup = 16000
    tempdf['LC2030MOD'] = tempdf['LC2014']
        
        
    Helpers.ChangeFlag(tempdf,'LC2014','LC2030MOD')
    
    #Calculate Riparian Suitability and Selection
    if blahblah == 'rre':
        Generic.dict_activity['rre']['query'] = (tempdf['LC2014'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren']) & (tempdf['lcchange'] == 1) & ((tempdf['near_rivers'] < 650) | (tempdf['near_streams'] < 100)) & (tempdf['near_woody'] != 0))
        Helpers.CreateSuitFlags('rre',tempdf)
        Helpers.CreateEligDict(tempdf, 'rre', Generic.dict_activity,dict_eligibility)    
        Helpers.selectionfunc (dict_eligibility,tempdf, 'rre')
  
  
    #Create Oak Suitability and Selection
    if blahblah == 'oak':
        Generic.dict_activity['oak']['query'] =(tempdf['LC2014'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren']))    
        Helpers.CreateSuitFlags('oak',tempdf)
        Helpers.CreateEligDict(tempdf, 'oak', Generic.dict_activity,dict_eligibility)
        Helpers.selectionfunc (dict_eligibility,tempdf, 'oak')

    #Calculate 2030MOD values
    tempdf['LC2030MOD'] = tempdf['LC2014']
    
    #Set GHG dictionary entries for suitability
    Generic.dict_activity['ccr']['query'] = (df['LC2030MOD'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1)
    Generic.dict_activity['mul']['query'] = (df['LC2030MOD'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1)
    Generic.dict_activity['nfm']['query'] = (df['LC2030MOD'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1)
    Generic.dict_activity['aca']['query'] = (df['LC2030MOD'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1)
    Generic.dict_activity['acu']['query'] = (df['LC2030MOD'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1)
    Generic.dict_activity['hpl']['query'] = (df['LC2030MOD'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1)
    Generic.dict_activity['urb']['query'] = (df['LC2030MOD'].isin(['Orchard','Annual Cropland'])) & (df['lcchange'] == 1)

    #Create green house gas function to run suitability, eligibility and selection functions from Helpers
    def ghg_selection (activity,adoption = .02):
        Helpers.CreateSuitFlags(activity,tempdf)    
        Helpers.CreateEligDict(tempdf, activity, Generic.dict_activity,dict_eligibility)  
        Helpers.selectionfunc (dict_eligibility,tempdf,activity)
        
    #GHG Suitability Flag and Selection for CCR
    if blahblah == 'ccr':
        ghg_selection ('ccr', ccradoption)
    if blahblah == 'mul':
        ghg_selection ('mul')
    if blahblah == 'nfm':
        ghg_selection ('nfm')
    if blahblah == 'aca':
        ghg_selection ('aca')
    if blahblah == 'acu':
        ghg_selection ('acu')
    if blahblah == 'hpl':
        ghg_selection ('hpl')
    if blahblah == 'urb':
        ghg_selection ('urb')

    return tempdf





