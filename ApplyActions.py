# -*- coding: utf-8 -*-
#Import System Modules

''' 
Activity abbreviations are:
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
global _eligibility

def ApplyGHG(df,carb14,carb30,activitylist, dictact):
#    tempdf = Helpers.MergeMultiDF('gridcode30',[df,carb30])
    tempdf = df.sort_values(['pointid'])
    carb = {}
    carb2 = {}
    trt = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/trt/trt_reductions.csv")    
    def UpdateValues (tempdf,activity,carb,carb2, dictact):
        Helpers.pmes('Updating Carbon For: ' + activity)
        upact = activity.upper()
        
        #Create a dataframe from trt_reductions for the activity
        temptrt = trt.loc[trt['Activity'] == upact]
        actcount = tempdf.groupby('LC2030').sum()[activity+'selected']
        actcount2 = actcount.to_frame()
        #Convert Landcover and reduction rates to their own lists
        dfList = temptrt['Landcover'].tolist()
        dfList2 = temptrt['red_10'].tolist()
        counter1 = 0
        maxyrs = 2030 - dictact[activity]['adoptyear']
        maxadopt = dictact[activity]['years'] + 10
        fulladoptyrs = maxadopt - 2*dictact[activity]['years']
        # Loop through landcovers for the activity and calculate and sum up carbon
        tempix = 0
        for i in dfList:
        
            if i in actcount:
                carb1 = 0
                tempix = 0
                Helpers.pmes('Landcover is: ' + i +', AND Pixels: ' + str(actcount2.at[i,activity+'selected']))
                pixels = actcount2.at[i,activity+'selected']
                if pixels > 0:
                    anngrowth = pixels/dictact[activity]['years']
                    
                    redrate = dfList2[counter1]
                    counter2 = 0
                    while counter2 < dictact[activity]['years'] and counter2<maxyrs:
                        
                        carb1 = carb1 + (((counter1 + 1)*anngrowth)*redrate)
            
                        counter2 = counter2 + 1
                    fullcount = 0
                    
                    if activity == 'rre' or activity == 'oak':
                        while counter2<maxyrs:
                            carb1 = carb1 + (pixels*redrate)
                
                            counter2 = counter2 + 1
                            fullcount = fullcount + 1
                        
                    else:
                        while counter2<maxyrs and fullcount < fulladoptyrs:
                            carb1 = carb1 + (pixels*redrate)
                
                            counter2 = counter2 + 1
                            fullcount = fullcount + 1
                    endcount = dictact[activity]['years']
                    while counter2<maxyrs and endcount>0:
                        carb1 = carb1 + (((endcount)*anngrowth)*redrate)
            
                        counter2 = counter2 + 1
                        endcount = endcount - 1       
                        
                    carb[activity+i+'_co2'] = carb1
                    tempix = tempix + pixels
                    
                    carb2[activity +i+ '_sel'] = tempix
            if tempix > 0:
                tempdf[activity +'_carbred'] = tempdf[activity+'selected']*(carb1/pixels)
                    
                    
    for i in activitylist:

        
        UpdateValues(tempdf,i, carb, carb2, dictact)
        

    return (tempdf,carb,carb2)


