# -*- coding: utf-8 -*-
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
mma - REPLACING SYNTHETIC FERTILIZER WITH SOIL AMENDMENTS
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

def ApplyGHG(df,carb30,carb14,carb30mod):
    df = Helpers.MergeMultiDF('gridcode14',[df,carb30mod])
    