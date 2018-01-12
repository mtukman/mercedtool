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
import Generic
import Helpers
global dict_eligibility

def DoActivities(df):
    dict_eligibility = {}
    
    smallgroup = 20000
    mediumgroup = 16000
    
    
        
        
    #first create change flag
    Helpers.ChangeFlag(df)
    
    #Calculate Oak and Riparian Suitability Flags
    rrequery = (df['LC2014'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren']) & (df['lcchange'] == 1) & ((df['near_rivers'] < 650) | (df['near_streams'] < 100)) & (df['near_woody'] != 0))
    oakquery =(df['LC2014'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren']))
    
    
    
    
    #Activity Dictionaries
    Generic.dict_activity['oak']['query']= oakquery
    Generic.dict_activity['rre']['query']= rrequery
    
    #if parameter3 == 1:
    Helpers.CreateSuitFlags('rre',df)
    Helpers.CreateSuitFlags('oak',df)
    

    print (dict_eligibility)
    #selectionfunc (dict_eligibility,df, activity)
    Helpers.selectionfunc (dict_eligibility,df, 'rre')
#Create Oak and Riparian Eligibility
    Helpers.CreateEligDict(df, 'rre', Generic.dict_activity,dict_eligibility)
    Helpers.CreateEligDict(df, 'oak', Generic.dict_activity,dict_eligibility)
    print (dict_eligibility)
#Create Oak and Riparian Selection

    Helpers.selectionfunc (dict_eligibility,df, 'rre')

    
#Update Change Flag List



#Calculate Agricultural Activity Suitability Flags


#Create Agricultural Activity Eligibility


#Create Agricultural Activity Selection


#Update Activity GHG values in Carbon Table

    return df





