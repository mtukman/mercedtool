# -*- coding: utf-8 -*-
#Import System Modules
''' 

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
import Helpers
global dict_eligibility
import csv

def ApplyGHG(df,carb01,carb14,carb30mod):
    tempdf = df
    tempdf = Helpers.MergeMultiDF('gridcode14',[tempdf,carb30mod])
    tempdf = tempdf.sort_values(['pointid'])
    
    trt = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/trt/trt_reductions.csv")    
    trt = trt.rename(columns={'Landcover':'LC2030MOD_y'})

                
    def UpdateValues (tempdf,activity):
        upact = activity.upper()
        temptrt = trt.loc[trt['Activity'] == upact]
        
        #Update GHG Values with the TRT Reductions Table
        for index, row in temptrt.iterrows():
            if row['Reductions_N2O'] != 0:
                tempdf.loc[(tempdf['LC2030MOD_y'] == row['LC2030MOD_y']) & (tempdf[activity + 'selected'] == 1), 'n20_em_mod'] = tempdf['n20_em_mod'] * row['Reductions_N2O']
#            if row['Reductions_CH4'] != 0:
#                tempdf.loc[(tempdf['LC2030MOD'] == row['LC2030MOD_y']) & (tempdf[activity + 'selected'] == 1), 'ch4_em_mod'] = tempdf['n20_em_mod'] * row['Reductions_CH4']

    UpdateValues(tempdf,'ccr')
    
    return tempdf