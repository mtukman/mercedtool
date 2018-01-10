#Import System Modules
''' This will be a funtion 
that takes the activity abbreviations and
the change flag (regular or mod)

It will assign new fields to tabs_all_df dataframe

it will be run from main_program.py first for the 
land cover changing activities and then for the 
non land cover changing ones
'''

import pandas as pd
import Helpers
dict_eligibility = {}
#Generic.tabs_all_df = pd.merge(value_df,near_df, on = 'pointid')

def CreateSuitFlags(activity):
    '''Tales an activity name (a key from dict_activity) and uses
    that to calculate a 1/0 suitability flag for the activity 
    in the tabs_all_df dataframe'''
    
    initflag = activity + '_conv_flag'
    Generic.tabs_all_df[initflag] = 0
    Generic.tabs_all_df.loc[Generic.dict_activity[activity]['query'], initflag] = 1
    
    
#first create change flag
Generic.ChangeFlag()

#Calculate Oak and Riparian Suitability Flags
rrequery = (Generic.tabs_all_df['LC2014'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren']) & (Generic.tabs_all_df['lcchange'] == 1) & ((Generic.tabs_all_df['near_rivers'] < 650) | (Generic.tabs_all_df['near_streams'] < 100)) & (Generic.tabs_all_df['near_woody'] != 0))
oakquery =(Generic.tabs_all_df['LC2014'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren']))

#Activity Dictionaries
Generic.dict_activity['oak']['query']= oakquery
Generic.dict_activity['rre']['query']= rrequery

#if parameter3 == 1:
CreateSuiteFlags('rre')
CreateSuitFlags('oak')

Helpers.CreateEligDict(Generic.tabs_all_df, 'rre', dict_activity,dict_eligibility)
Helpers.CreateEligDict(Generic.tabs_all_df, 'oak', dict_activity,dict_eligibility)

#Create Oak and Riparian Eligibility


#Create Oak and Riparian Selection


#Change Landcover Labels from Selection


#Update Change Flag List



#Calculate Agricultural Activity Suitability Flags


#Create Agricultural Activity Eligibility


#Create Agricultural Activity Selection


#Update Activity GHG values in Carbon Table







