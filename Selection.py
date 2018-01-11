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


for x in range(10):
  print random.randint(1,101)