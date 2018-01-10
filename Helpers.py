# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 10:23:24 2018

@author: mtukman
"""

def CreateEligDict(df, activity, dict_activity, dict_eligibility):
    import Generic
    import sys
    initflag = activity + '_conv_flag'
    if activity in dict_eligibility.keys():
        print('The activity is already in the dict_eligibility dictionary')
        sys.exit('***The activity is already in the dict_eligibility dictionary***')
    eli = df.groupby('LC2014').sum()[initflag]
    eli.loc['Annual Cropland'] = eli.loc['Annual Cropland'] * dict_activity[activity]['ag_modifier']
    #Need to add modifier for adoption accross the board from user input
    
    eli_dict_element = eli.to_dict()
    dict_eligibility[activity] = eli_dict_element