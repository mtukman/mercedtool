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
import random 
dict_eligibility = {}

def CreateSelFlags(randnum,suitfield,flagfield):
    '''Takes an activity name (a key from dict_activity) and uses
    that to calculate a 1/0 suitability flag for the activity 
    in the tabs_all_df dataframe'''
    
    initflag = activity + '_conv_flag'
    Generic.tabs_all_df[initflag] = 0
    Generic.tabs_all_df.loc[Generic.dict_activity[activity]['query'], initflag] = 1

def selectionfunc (goal,flagfield, groupnumber):
    count = 0
    curgoal = goal    
    usednum = []
    while count < goal:
        for x in range(20000):
            c = random.randint(1,groupnumber)
            if c in usednum:
                pass
            else:
                tabs_all_df.loc
            