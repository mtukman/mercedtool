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

def ApplyGHG(df,activitylist, dictact):

    tempdf = df.sort_values(['pointid'])
    carb = {}
    carb2 = {}
    trt = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/trt/trt_reductions.csv")    
    def UpdateValues (tempdf,activity,carb,carb2, dictact):
        Helpers.pmes('Updating Carbon For: ' + activity)
        upact = activity.upper()
        
        #Create a dataframe from trt_reductions for the activity
        temptrt = trt.loc[trt['Activity'] == upact]
        actcount = tempdf.groupby('LC2030_trt_bau').sum()[activity+'selected']
        actcount2 = actcount.to_frame()
        #Convert Landcover and reduction rates to their own lists
        dfList = temptrt['Landcover'].tolist()
        dfList2 = temptrt['red_10'].tolist()
        counter1 = 0
        maxyrs = 2031 - dictact[activity]['adoptyear'] #Max number of years an activity can run between 2014 and 2030 (counting the year 2030)
        fulladoptyrs = (11-dictact[activity]['years']) #How many years an ag activity can run at full capativity between growth and decay
        # Loop through landcovers for the activity and calculate and sum up carbon
        tempix = 0
        for i in dfList:
        
            if i in actcount:
                carb1 = 0
                tempix = 0
                Helpers.pmes('Landcover is: ' + i +', AND Pixels: ' + str(actcount2.at[i,activity+'selected']))
                pixels = actcount2.at[i,activity+'selected'] #Get the number of selected pixers for the activity/landcover combination
                
                #If there are selected pixels, do the carbon reduction loop
                if pixels > 0:
                    anngrowth = pixels/dictact[activity]['years']
                    
                    redrate = dfList2[counter1] #Get the carbon reduction rate that corresponds to the activity/landcover
                    counter2 = 0
                    
                    #Do the first years of activity growth 
                    while counter2 < dictact[activity]['years'] and counter2<maxyrs:
                        
                        carb1 = carb1 + (((counter1 + 1)*anngrowth)*redrate)
            
                        counter2 = counter2 + 1
                    fullcount = 0
                    
                    #For oak and Riparian, carry through 2030 at full capacity
                    if activity == 'rre' or activity == 'oak':
                        while counter2<maxyrs:
                            carb1 = carb1 + (pixels*redrate)
                
                            counter2 = counter2 + 1
                                                    
                    else: #If not oak or riparian, do the middle years are full adoption
                        while counter2<maxyrs and fullcount < fulladoptyrs:
                            carb1 = carb1 + (pixels*redrate)
                
                            counter2 = counter2 + 1
                            fullcount = fullcount + 1
                    endcount = dictact[activity]['years']
                    
                    #Count down the tail end of the adoption period until it its 2030
                    while counter2<maxyrs and endcount>0:
                        carb1 = carb1 + (((endcount)*anngrowth)*redrate)
            
                        counter2 = counter2 + 1
                        endcount = endcount - 1       
                        
                    carb[activity+i+'_co2'] = carb1
                    tempix = tempix + pixels
                    
                    carb2[activity +i+ '_sel'] = tempix
            counter1 = counter1 + 1
            
            if tempix > 0:
                tempdf[activity +'_carbred'] = tempdf[activity+'selected']*(carb1/pixels)
                    
    # Run the above functionf or every activity selected
    for i in activitylist:
        UpdateValues(tempdf,i, carb, carb2, dictact)
        
        
    # Update gridcodes for treatment scenarios
    gcdict = {'Wetland':0, 'Water':1, 'Grassland':2,'Barren':4, 'Orchard':7,'Vineyard':8,'Annual Cropland':9,'Rice':10,'Irrigated Pasture':11,'Young Forest':14, 'Young Shrubland':15}
    devlist = ['bau','med','max']
    keylist = [*gcdict]
    
    for i in devlist:
        for x in keylist:
            tempdf.loc[(tempdf['LC2030_trt_'+i] ==  x),'gridcode30_trt_' + i] = gcdict[x]
            
    return (tempdf,carb,carb2)


