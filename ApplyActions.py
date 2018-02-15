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

adoptrre = 5
yearrre = 2020

def ApplyGHG(df,carb14,carb30,activitylist):
#    tempdf = Helpers.MergeMultiDF('gridcode30',[df,carb30])
    tempdf = df.sort_values(['pointid'])
    carb = {}
    carb2 = {}
    trt = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/trt/trt_reductions.csv")    
    def UpdateValues (tempdf,activity):
        Helpers.pmes('Updating Carbon For: ' + activity)
        upact = activity.upper()
        
        #Create a dataframe from trt_reductions for the activity
        temptrt = trt.loc[trt['Activity'] == upact]
        actcount = tempdf.groupby('LC2014').sum()[activity+'selected']
        actcount2 = actcount.to_frame()
        #Convert Landcover and reduction rates to their own lists
        dfList = temptrt['Landcover'].tolist()
        dfList2 = temptrt['red_10'].tolist()
        counter1 = 0
        maxyrs = 2030 - yearrre
        maxadopt = adoptrre + 10
        fulladoptyrs = maxadopt - 2*adoptrre
        # Loop through landcovers for the activity and calculate and sum up carbon
        tempix = 0
        for i in dfList:
        
            if i in actcount:
                tempix = 0
                Helpers.pmes('Landcover is: ' + i +', AND Pixels: ' + str(actcount2.at[i,activity+'selected']))
                pixels = actcount2.at[i,activity+'selected']
                if pixels > 0:
                    anngrowth = pixels/adoptrre
                    carb1 = 0
                    redrate = dfList2[counter1]
                    counter2 = 0
                    while counter2 < adoptrre and counter2<maxyrs:
                        
                        carb1 = carb1 + (((counter1 + 1)*anngrowth)*redrate)
            
                        counter2 = counter2 + 1
                    fullcount = 0
                    while counter2<maxyrs and fullcount < fulladoptyrs:
                        carb1 = carb1 + (pixels*redrate)
            
                        counter2 = counter2 + 1
                        fullcount = fullcount + 1
                    endcount = adoptrre
                    while counter2<maxyrs and endcount>0:
                        carb1 = carb1 + (((endcount)*anngrowth)*redrate)
            
                        counter2 = counter2 + 1
                        endcount = endcount - 1       
                        
                    carb[activity+i+'_co2'] = carb1
                    tempix = tempix + pixels
                    
                    carb2[activity +i+ '_sel'] = tempix
                    tempdf[activity +i + '_carbred'] = tempdf[activity+'selected']*(carb1/tempix)
                    
                    
    for i in activitylist:

        
        UpdateValues(tempdf,i)
        

    return (tempdf,carb,carb2)


