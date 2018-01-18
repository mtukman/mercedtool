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
import arcpy
import numpy as np

def DoActivities(df,activitylist, scenario,customdev):
    Generic.set_paths_and_workspaces()
    tempdf = df
    dict_eligibility = {}

    tempdf['LC2030MOD'] = tempdf['LC2014']
        
        
    Helpers.ChangeFlag(tempdf,'LC2014','LC2030MOD')
    

    if 'custom' == scenario:
        arcpy.MakeFeatureLayer_management(Generic.points,'temppts)
        arcpy.SelectLayerByLocation_management('temppts','INTERSECT',customdev)
        arcpy.Frequency_analysis('temppts', Generic.scratch + '/custompts.csv')
        custpts = pd.read_csv(Generic.scratch + '/custompts.csv',usecols = ['pointid'])
        plist = custpts['pointid'].tolist()
        df.loc[tmpdf['pointid'].isin(plist), 'LC2014'] = 'Urban'
        
    #Calculate Riparian Suitability and Selection        
    if 'rre' in activitylist:
        Generic.dict_activity['rre']['query'] = (tempdf['LC2014'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren']) & (tempdf['lcchange'] == 1) & ((tempdf['near_rivers'] < 650) | (tempdf['near_streams'] < 100)) & (tempdf['near_woody'] != 0))
        Helpers.CreateSuitFlags('rre',tempdf)
        Helpers.CreateEligDict(tempdf, 'rre', Generic.dict_activity,dict_eligibility)    
        Helpers.selectionfunc (dict_eligibility,tempdf, 'rre')
  
  
    #Create Oak Suitability and Selection
    if 'oak' in activitylist:
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
    def ghg_selection (tempdf,activity,dict_eligibility):
        Helpers.CreateSuitFlags(activity,tempdf)    
        Helpers.CreateEligDict(tempdf, activity, Generic.dict_activity,dict_eligibility)  
        Helpers.selectionfunc (dict_eligibility,tempdf,activity)
        
    #GHG Suitability Flag and Selection for CCR
    if 'ccr' in activitylist:
        ghg_selection (tempdf,'ccr',dict_eligibility)
    if 'mul' in activitylist:
        ghg_selection (tempdf,'mul',dict_eligibility)
    if 'nfm' in activitylist:
        ghg_selection (tempdf,'nfm',dict_eligibility)
    if 'aca' in activitylist:
        ghg_selection (tempdf,'aca',dict_eligibility)
    if 'acu' in activitylist:
        ghg_selection (tempdf,'acu',dict_eligibility)
    if 'hpl' in activitylist:
        ghg_selection (tempdf,'hpl',dict_eligibility)
    if 'urb' in activitylist:
        ghg_selection (tempdf,'urb',dict_eligibility)

    return tempdf





