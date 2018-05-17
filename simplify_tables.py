
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 12:10:25 2018

@author: Dylan
"""


afolder = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\\"
outfolder = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\simp_tables\\"
import pandas as pd
import functools
import plotly.plotly as py

py.sign_in('mtukman', 'FbUYCv4tcjCPF2ZdfzKo')


def fmmp2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\fmmp.csv')
    df = df[['fmmp_class','ha_2014']]
    df = df.loc[df['ha_2014'] > 0]
    df = df.rename(columns = {'fmmp_class': 'Farmland Class', 'ha_2014':'Hectares'})
    df.to_csv(outfolder+'2014 Ag Land Quality.csv', index = False)
    
    
def fmmp2030():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\fmmp.csv')
    df = df[['fmmp_class','ha_loss_base_bau', 'ha_loss_base_med', 'ha_loss_base_max' ]]
    df = df.rename(columns = {'fmmp_class': 'Farmland Class', 'ha_loss_base_bau':'Reference Scenario', 'ha_loss_base_med':'Medium Infill Scenario', 'ha_loss_base_max':'Max Infill Scenario'})
    df.set_index(['Farmland Class'], inplace = True)
    df = df[df.values.sum(axis=1) != 0]
    df.reset_index(inplace = True)
    
    df.to_csv(outfolder+'2030 Ag Land Quality.csv', index = False)
    
    
    
def crop2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\cropvalue.csv')
    df = df[['landcover','cropvalue_usd_2014']]
    df = df.rename(columns = {'landcover': 'Crop Type', 'cropvalue_usd_2014':'US Dollars'})
    df.to_csv(outfolder+'2014 Crop Value.csv', index = False)



def crop2030():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\cropvalue.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\cropvalue.csv')
    df2 = df2[['landcover','usd_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'Crop Type','usd_change_trt_bau':'100% Riparian Restoration Adoption'})
    df = df[['landcover','usd_change_base_bau','usd_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'Crop Type', 'usd_change_base_bau':'No Activity Applied', 'usd_change_trt_bau':'25% Riparian Restoration Adoption'})
    
    temp = pd.merge(df, df2, on = 'Crop Type', how = 'left')
    temp.set_index(['Crop Type'], inplace = True)
    temp = temp[temp.values.sum(axis=1) != 0]
    temp.reset_index(inplace = True)
    temp.to_csv(outfolder+'2030 Crop Value.csv', index = False)
    
    
    
    
def watcon2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\watcon.csv')
    df = df[['landcover','ac_ft_2014']]
    df = df.loc[df['ac_ft_2014'] > 0]
    df = df.rename(columns = {'landcover': 'Landcover', 'ac_ft_2014':'Acre Feet Annual Water Demand'})
    df.to_csv(outfolder+'2014 Ag and Urban Water Conservation.csv', index = False)




def watcon2030():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\watcon.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\watcon.csv')
    df2 = df2[['landcover','ac_ft_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'Landcover','ac_ft_change_trt_bau':'100% Riparian Restoration Adoption'})
    df = df[['landcover','ac_ft_change_base_bau','ac_ft_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'Landcover', 'ac_ft_change_base_bau':'No Activity Applied', 'ac_ft_change_trt_bau':'25% Riparian Restoration Adoption'})

    temp = pd.merge(df, df2, on = 'Landcover', how = 'left')
    temp.set_index(['Landcover'], inplace = True)
    temp = temp[temp.values.sum(axis=1) != 0]
    temp.reset_index(inplace = True)
    
    
    temp.to_csv(outfolder+'2030 Ag and Urban Water Conservation.csv', index = False)



def groundwater2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\groundwater.csv')
    df = df[['landcover','ac_ft_rec_lst_base_bau','ac_ft_rec_lst_base_med','ac_ft_rec_lst_base_max']]
    df.set_index(['landcover'], inplace = True)
    df = df[df.values.sum(axis=1) != 0]
    df.reset_index(inplace = True)
    df['landcover'] = 'Acre Feet of Annual Groundwater Recharge Lost'
    df = df.groupby(['landcover'], as_index = False).sum()
    test = df.transpose()
    test.columns = test.iloc[0]
    test = test[1:]
    test.reset_index(inplace = True)
    
    df = df.rename(columns = {'landcover': 'Landcover', 'ac_ft_rec_lst_base_bau':'Reference Scenario', 'ac_ft_rec_lst_base_med':'Medium Infill Scenario', 'ac_ft_rec_lst_base_max':'Max Infill Scenario'})
    test = df.transpose()
    test.columns = test.iloc[0]
    test = test[1:]
    test.reset_index(inplace = True)
    test.rename(columns = {'index':'Development Scenario'}, inplace = True)
    print (test)
    test.to_csv(outfolder+'2030 Groundwater Recharge.csv', index = False)


def watint2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\watint.csv')
    df = df[['Integrity_Class','ha_2014']]
    df = df.rename(columns = {'Integrity_Class': 'Watershed Class', 'ha_2014':'Hectares'})
    df = df.loc[df['Watershed Class'] != 'na']
    
    df.to_csv(outfolder+'2014 Watershed Integrity.csv', index = False)
    
def watint2030_rre():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\watint.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\watint.csv')
    df2 = df2[['Integrity_Class','ha_change_trt_bau']]
    df2 = df2.rename(columns = {'Integrity_Class': 'Watershed Class','ha_change_trt_bau':'100% Riparian Restoration Adoption'})
    df = df[['Integrity_Class','ha_change_base_bau','ha_change_trt_bau']]
    df = df.rename(columns = {'Integrity_Class': 'Watershed Class', 'ha_change_base_bau':'No Activity Applied', 'ha_change_trt_bau':'25% Riparian Restoration Adoption'})

    temp = pd.merge(df, df2, on = 'Watershed Class', how = 'left')
    temp.set_index(['Watershed Class'], inplace = True)
    temp = temp[temp.values.sum(axis=1) != 0]
    temp.reset_index(inplace = True)
    
    temp.to_csv(outfolder+'2030 Watershed Integrity Riparian.csv', index = False)   


def nitrun2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\runoff_nitrates.csv')
    df = df[['landcover','tons_no3_14']]
    df = df.loc[df['tons_no3_14'] > 0]
    df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_14':'Annual Tons of Nitrate Runoff'})
    df.to_csv(outfolder+'2014 Water Quality - Nitrate Runoff.csv', index = False)

def nitleach2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\leach_nitrates.csv')
    df = df[['landcover','tons_no3_14']]
    df = df.loc[df['tons_no3_14'] > 0]
    df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_14':'Annual Tons of Nitrate Leaching'})
    df.to_csv(outfolder+'2014 Water Quality - Nitrate Leaching.csv', index = False)
    
    
def nitrun2030_rre():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\runoff_nitrates.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\runoff_nitrates.csv')
    df2 = df2[['landcover','tons_no3_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'Landcover','tons_no3_change_trt_bau':'100% Riparian Restoration Adoption'})
    df = df[['landcover','tons_no3_change_base_bau','tons_no3_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_change_base_bau':'No Activity Applied', 'tons_no3_change_trt_bau':'25% Riparian Restoration Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Landcover', how = 'left')
    temp['Landcover'] = 'Change in Annual Tons of Nitrate Runoff'
    temp = temp.groupby(['Landcover'], as_index = False).sum()
    test = temp.transpose()
    test.columns = test.iloc[0]
    test = test[1:]
    test.reset_index(inplace = True)
    test.rename(columns = {'index':'Scenario'}, inplace = True)
    test.to_csv(outfolder+'2030 Water Quality - Nitrate Runoff RRE.csv', index = False)
    

def nitrun2030_nfm():
    df2 = pd.read_csv(afolder + r'\nfm_100\runoff_nitrates.csv')
    df = pd.read_csv(afolder + r'\nfm_25\runoff_nitrates.csv')
    df2 = df2[['landcover','tons_no3_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'Landcover','tons_no3_change_trt_bau':'100% N Fertilizer Management Adoption'})
    df = df[['landcover','tons_no3_change_base_bau','tons_no3_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_change_base_bau':'No Activity Applied', 'tons_no3_change_trt_bau':'25% N Fertilizer Management Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Landcover', how = 'left')
    temp['Landcover'] = 'Change in Annual Tons of Nitrate Runoff'
    temp = temp.groupby(['Landcover'], as_index = False).sum()
    test = temp.transpose()
    test.columns = test.iloc[0]
    test = test[1:]
    test.reset_index(inplace = True)
    test.rename(columns = {'index':'Scenario'}, inplace = True)
    test.to_csv(outfolder+'2030 Water Quality - Nitrate Runoff NFM.csv', index = False)
    
def nitleach2030_rre():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\leach_nitrates.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\leach_nitrates.csv')
    df2 = df2[['landcover','tons_no3_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'Landcover','tons_no3_change_trt_bau':'100% Riparian Restoration Adoption'})
    df = df[['landcover','tons_no3_change_base_bau','tons_no3_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_change_base_bau':'No Activity Applied', 'tons_no3_change_trt_bau':'25% Riparian Restoration Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Landcover', how = 'left')
    temp['Landcover'] = 'Change in Annual Tons of Nitrate Leaching'
    temp = temp.groupby(['Landcover'], as_index = False).sum()
    test = temp.transpose()
    test.columns = test.iloc[0]
    test = test[1:]
    test.reset_index(inplace = True)
    test.rename(columns = {'index':'Scenario'}, inplace = True)
    test.to_csv(outfolder+'2030 Water Quality - Nitrate Leaching RRE.csv', index = False)
def nitleach2030_nfm():
    df2 = pd.read_csv(afolder + r'\nfm_100\leach_nitrates.csv')
    df = pd.read_csv(afolder + r'\nfm_25\leach_nitrates.csv')
    df2 = df2[['landcover','tons_no3_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'Landcover','tons_no3_change_trt_bau':'100% N Fertilizer Management Adoption'})
    df = df[['landcover','tons_no3_change_base_bau','tons_no3_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_change_base_bau':'No Activity Applied', 'tons_no3_change_trt_bau':'25% N Fertilizer Management Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Landcover', how = 'left')
    temp['Landcover'] = 'Change in Annual Tons of Nitrate Leaching'
    temp = temp.groupby(['Landcover'], as_index = False).sum()
    test = temp.transpose()
    test.columns = test.iloc[0]
    test = test[1:]
    test.reset_index(inplace = True)
    test.rename(columns = {'index':'Scenario'}, inplace = True)
    test.to_csv(outfolder+'2030 Water Quality - Nitrate Leaching NFM.csv', index = False)

def flood2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\flood100.csv')
    df = df[['gen_class','ha_2014']]
    df = df.loc[df['ha_2014'] > 0]
    df = df.rename(columns = {'gen_class': 'General Landcover', 'ha_2014':'Hectares'})
    df.to_csv(outfolder+'2014 Flood Risk Reduction.csv', index = False)
    
    
    

def flood2030():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\flood100.csv')
    df = df[['gen_class','ha_change_base_bau', 'ha_change_base_med', 'ha_change_base_max' ]]
    df = df.rename(columns = {'gen_class': 'General Landcover', 'ha_change_base_bau':'Reference Scenario', 'ha_change_base_med':'Medium Infill Scenario', 'ha_change_base_max':'Max Infill Scenario'})
    
    #Remove any rows with all 0s
    df.set_index(['General Landcover'], inplace = True)
    df = df[df.values.sum(axis=1) != 0]
    df.reset_index(inplace = True)
    
#    #Transpose columns and rows
#    test = df.transpose()
#    test.columns = test.iloc[0]
#    test = test[1:]
    
    df.to_csv(outfolder+'2030 Flood Risk Reduction.csv', index = False)


def air2014():
    import functools as fc
    df1 = pd.read_csv(afolder + r'\RRE_COUNTY_100\co_val_airpollute.csv')
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\no2_val_airpollute.csv')
    df3 = pd.read_csv(afolder + r'\RRE_COUNTY_100\o3_val_airpollute.csv')
    df4 = pd.read_csv(afolder + r'\RRE_COUNTY_100\pm2_5_val_airpollute.csv')
    df5 = pd.read_csv(afolder + r'\RRE_COUNTY_100\pm10_val_airpollute.csv')
    df6 = pd.read_csv(afolder + r'\RRE_COUNTY_100\so2_val_airpollute.csv')
    
    df1 = df1[['landcover','tons_14']]
    df1 = df1.rename(columns = {'landcover':'Landcover','tons_14':'CO2'})
    df2 = df2[['landcover','tons_14']]
    df2 = df2.rename(columns = {'landcover':'Landcover','tons_14':'NO2'})
    df3 = df3[['landcover','tons_14']]
    df3 = df3.rename(columns = {'landcover':'Landcover','tons_14':'O3'})
    df4 = df4[['landcover','tons_14']]
    df4 = df4.rename(columns = {'landcover':'Landcover','tons_14':'PM 2.5'})
    df5 = df5[['landcover','tons_14']]
    df5 = df5.rename(columns = {'landcover':'Landcover','tons_14':'PM 10'})
    df6 = df6[['landcover','tons_14']]
    df6 = df6.rename(columns = {'landcover':'Landcover','tons_14':'SO2'})
    dfs = [df1,df2,df3,df4,df5,df6]
    
    df_final = fc.reduce(lambda left,right: pd.merge(left,right,on='Landcover'), dfs)
    
    df_final = df_final.groupby(['Landcover'], as_index = False).sum()

    #Transpose columns and rows
    test = df_final.transpose()
    test.columns = test.iloc[0]
    test = test[1:]
    test['Tons of Pollutant Sequestered Annually'] = test.sum(axis=1)
    test.reset_index(inplace = True)
    test = test.rename(columns = {'index':'Air Pollutant'})
    test = test[['Air Pollutant','Tons of Pollutant Sequestered Annually']]
    test.to_csv(outfolder+'2014 Air Quality.csv', index = False)
    return test

def air2030():
    import functools as fc
    df1 = pd.read_csv(afolder + r'\RRE_COUNTY_100\co_val_airpollute.csv')
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\no2_val_airpollute.csv')
    df3 = pd.read_csv(afolder + r'\RRE_COUNTY_100\o3_val_airpollute.csv')
    df4 = pd.read_csv(afolder + r'\RRE_COUNTY_100\pm2_5_val_airpollute.csv')
    df5 = pd.read_csv(afolder + r'\RRE_COUNTY_100\pm10_val_airpollute.csv')
    df6 = pd.read_csv(afolder + r'\RRE_COUNTY_100\so2_val_airpollute.csv')
    
    
    def cleanair(df, pollutant):
        df1 = df[['landcover','tons_change_base_bau','tons_change_base_med','tons_change_base_max']]
        df1 = df1.rename(columns = {'landcover':'Landcover','tons_change_base_bau': 'Reference Scenario','tons_change_base_med':'Medium Infill Scenario','tons_change_base_max':'Max Infill Scenario'})
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1[pollutant] = df1.sum(axis=1)
        df1.reset_index(inplace = True)
        df1 = df1[['index', pollutant]]
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1.reset_index(inplace = True)
        df1 = df1.rename(columns = {'Landcover':'Air Pollutant'})
        return df1

    dlist = [df1,df2,df3,df4,df5,df6]
    plist = ['CO2','NO2','O3','PM 2.5','PM 10', 'SO2']
    pcadict = {}
    counter = 0
    
    for i in dlist:
        temp = cleanair(i,plist[counter])
        pcadict[plist[counter]] = temp
        counter = counter + 1

    tlist = list(pcadict.values())

    df = pd.concat(tlist)


    df.to_csv(outfolder+'2030 Air Quality Change.csv', index = False)
    return df

def air2030_rre():
    df1 = pd.read_csv(afolder + r'\RRE_COUNTY_25\co_val_airpollute.csv')
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_25\no2_val_airpollute.csv')
    df3 = pd.read_csv(afolder + r'\RRE_COUNTY_25\o3_val_airpollute.csv')
    df4 = pd.read_csv(afolder + r'\RRE_COUNTY_25\pm2_5_val_airpollute.csv')
    df5 = pd.read_csv(afolder + r'\RRE_COUNTY_25\pm10_val_airpollute.csv')
    df6 = pd.read_csv(afolder + r'\RRE_COUNTY_25\so2_val_airpollute.csv')
    
    df7 = pd.read_csv(afolder + r'\RRE_COUNTY_100\co_val_airpollute.csv')
    df8 = pd.read_csv(afolder + r'\RRE_COUNTY_100\no2_val_airpollute.csv')
    df9 = pd.read_csv(afolder + r'\RRE_COUNTY_100\o3_val_airpollute.csv')
    df10 = pd.read_csv(afolder + r'\RRE_COUNTY_100\pm2_5_val_airpollute.csv')
    df11 = pd.read_csv(afolder + r'\RRE_COUNTY_100\pm10_val_airpollute.csv')
    df12 = pd.read_csv(afolder + r'\RRE_COUNTY_100\so2_val_airpollute.csv')
    
    def cleanair(df, pollutant):
        df1 = df[['landcover','tons_change_base_bau','tons_change_trt_bau']]
        df1 = df1.rename(columns = {'landcover':'Landcover','tons_change_base_bau': 'No Activity Applied','tons_change_trt_bau':'25% Riparian Restoration Adoption'})
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1[pollutant] = df1.sum(axis=1)
        df1.reset_index(inplace = True)
        df1 = df1[['index', pollutant]]
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1.reset_index(inplace = True)
        df1 = df1.rename(columns = {'Landcover':'Air Pollutant'})
        return df1

    dlist = [df1,df2,df3,df4,df5,df6]
    plist = ['CO2','NO2','O3','PM 2.5','PM 10', 'SO2']
    pcadict = {}
    counter = 0
    for i in dlist:
        temp = cleanair(i,plist[counter])
        pcadict[plist[counter]] = temp
        counter = counter + 1
    tlist = list(pcadict.values())
    df25 = pd.concat(tlist)

    def cleanair(df, pollutant):
        df1 = df[['landcover','tons_change_trt_bau']]
        df1 = df1.rename(columns = {'landcover':'Landcover','tons_change_trt_bau': '100% Riparian Restoration Adoption'})
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1[pollutant] = df1.sum(axis=1)
        df1.reset_index(inplace = True)
        df1 = df1[['index', pollutant]]
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1.reset_index(inplace = True)
        df1 = df1.rename(columns = {'Landcover':'Air Pollutant'})
        return df1

    dlist = [df7,df8,df9,df10,df11,df12]
    plist = ['CO2','NO2','O3','PM 2.5','PM 10', 'SO2']
    pcadict = {}
    counter = 0
    for i in dlist:
        temp = cleanair(i,plist[counter])
        pcadict[plist[counter]] = temp
        counter = counter + 1
    tlist = list(pcadict.values())
    df100 = pd.concat(tlist)
    
    test = pd.merge(df25,df100, how = 'left', on = 'Air Pollutant')
    test.to_csv(outfolder+'2030 Air Quality Change RRE.csv', index = False)
    return test
def air2030_HPL():
    df1 = pd.read_csv(afolder + r'\hedgerow_25\co_val_airpollute.csv')
    df2 = pd.read_csv(afolder + r'\hedgerow_25\no2_val_airpollute.csv')
    df3 = pd.read_csv(afolder + r'\hedgerow_25\o3_val_airpollute.csv')
    df4 = pd.read_csv(afolder + r'\hedgerow_25\pm2_5_val_airpollute.csv')
    df5 = pd.read_csv(afolder + r'\hedgerow_25\pm10_val_airpollute.csv')
    df6 = pd.read_csv(afolder + r'\hedgerow_25\so2_val_airpollute.csv')
    
    df7 = pd.read_csv(afolder + r'\hedgerow_100\co_val_airpollute.csv')
    df8 = pd.read_csv(afolder + r'\hedgerow_100\no2_val_airpollute.csv')
    df9 = pd.read_csv(afolder + r'\hedgerow_100\o3_val_airpollute.csv')
    df10 = pd.read_csv(afolder + r'\hedgerow_100\pm2_5_val_airpollute.csv')
    df11 = pd.read_csv(afolder + r'\hedgerow_100\pm10_val_airpollute.csv')
    df12 = pd.read_csv(afolder + r'\hedgerow_100\so2_val_airpollute.csv')
    
    def cleanair(df, pollutant):
        df1 = df[['landcover','tons_change_base_bau','tons_change_trt_bau']]
        df1 = df1.rename(columns = {'landcover':'Landcover','tons_change_base_bau': 'No Activity Applied','tons_change_trt_bau':'25% Hedgerow Planting Adoption'})
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1[pollutant] = df1.sum(axis=1)
        df1.reset_index(inplace = True)
        df1 = df1[['index', pollutant]]
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1.reset_index(inplace = True)
        df1 = df1.rename(columns = {'Landcover':'Air Pollutant'})
        return df1

    dlist = [df1,df2,df3,df4,df5,df6]
    plist = ['CO2','NO2','O3','PM 2.5','PM 10', 'SO2']
    pcadict = {}
    counter = 0
    for i in dlist:
        temp = cleanair(i,plist[counter])
        pcadict[plist[counter]] = temp
        counter = counter + 1
    tlist = list(pcadict.values())
    df25 = pd.concat(tlist)

    def cleanair(df, pollutant):
        df1 = df[['landcover','tons_change_trt_bau']]
        df1 = df1.rename(columns = {'landcover':'Landcover','tons_change_trt_bau': '100% Hedgerow Planting Adoption'})
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1[pollutant] = df1.sum(axis=1)
        df1.reset_index(inplace = True)
        df1 = df1[['index', pollutant]]
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1.reset_index(inplace = True)
        df1 = df1.rename(columns = {'Landcover':'Air Pollutant'})
        return df1

    dlist = [df7,df8,df9,df10,df11,df12]
    plist = ['CO2','NO2','O3','PM 2.5','PM 10', 'SO2']
    pcadict = {}
    counter = 0
    for i in dlist:
        temp = cleanair(i,plist[counter])
        pcadict[plist[counter]] = temp
        counter = counter + 1
    tlist = list(pcadict.values())
    df100 = pd.concat(tlist)
    
    test = pd.merge(df25,df100, how = 'left', on = 'Air Pollutant')
    test.to_csv(outfolder+'2030 Air Quality Change HPL.csv', index = False)
    return test

def air2030_URB():
    df1 = pd.read_csv(afolder + r'\urb_25\co_val_airpollute.csv')
    df2 = pd.read_csv(afolder + r'\urb_25\no2_val_airpollute.csv')
    df3 = pd.read_csv(afolder + r'\urb_25\o3_val_airpollute.csv')
    df4 = pd.read_csv(afolder + r'\urb_25\pm2_5_val_airpollute.csv')
    df5 = pd.read_csv(afolder + r'\urb_25\pm10_val_airpollute.csv')
    df6 = pd.read_csv(afolder + r'\urb_25\so2_val_airpollute.csv')
    
    df7 = pd.read_csv(afolder + r'\urb_100\co_val_airpollute.csv')
    df8 = pd.read_csv(afolder + r'\urb_100\no2_val_airpollute.csv')
    df9 = pd.read_csv(afolder + r'\urb_100\o3_val_airpollute.csv')
    df10 = pd.read_csv(afolder + r'\urb_100\pm2_5_val_airpollute.csv')
    df11 = pd.read_csv(afolder + r'\urb_100\pm10_val_airpollute.csv')
    df12 = pd.read_csv(afolder + r'\urb_100\so2_val_airpollute.csv')
    
    def cleanair(df, pollutant):
        df1 = df[['landcover','tons_change_base_bau','tons_change_trt_bau']]
        df1 = df1.rename(columns = {'landcover':'Landcover','tons_change_base_bau': 'No Activity Applied','tons_change_trt_bau':'25% Urban Tree Planting Adoption'})
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1[pollutant] = df1.sum(axis=1)
        df1.reset_index(inplace = True)
        df1 = df1[['index', pollutant]]
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1.reset_index(inplace = True)
        df1 = df1.rename(columns = {'Landcover':'Air Pollutant'})
        return df1

    dlist = [df1,df2,df3,df4,df5,df6]
    plist = ['CO2','NO2','O3','PM 2.5','PM 10', 'SO2']
    pcadict = {}
    counter = 0
    for i in dlist:
        temp = cleanair(i,plist[counter])
        pcadict[plist[counter]] = temp
        counter = counter + 1
    tlist = list(pcadict.values())
    df25 = pd.concat(tlist)

    def cleanair(df, pollutant):
        df1 = df[['landcover','tons_change_trt_bau']]
        df1 = df1.rename(columns = {'landcover':'Landcover','tons_change_trt_bau': '100% Urban Tree Planting Adoption'})
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1[pollutant] = df1.sum(axis=1)
        df1.reset_index(inplace = True)
        df1 = df1[['index', pollutant]]
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1.reset_index(inplace = True)
        df1 = df1.rename(columns = {'Landcover':'Air Pollutant'})
        return df1

    dlist = [df7,df8,df9,df10,df11,df12]
    plist = ['CO2','NO2','O3','PM 2.5','PM 10', 'SO2']
    pcadict = {}
    counter = 0
    for i in dlist:
        temp = cleanair(i,plist[counter])
        pcadict[plist[counter]] = temp
        counter = counter + 1
    tlist = list(pcadict.values())
    df100 = pd.concat(tlist)
    
    test = pd.merge(df25,df100, how = 'left', on = 'Air Pollutant')
    test.to_csv(outfolder+'2030 Air Quality Change URB.csv', index = False)
    return test
def air2030_OAK():
    df1 = pd.read_csv(afolder + r'\oak_25\co_val_airpollute.csv')
    df2 = pd.read_csv(afolder + r'\oak_25\no2_val_airpollute.csv')
    df3 = pd.read_csv(afolder + r'\oak_25\o3_val_airpollute.csv')
    df4 = pd.read_csv(afolder + r'\oak_25\pm2_5_val_airpollute.csv')
    df5 = pd.read_csv(afolder + r'\oak_25\pm10_val_airpollute.csv')
    df6 = pd.read_csv(afolder + r'\oak_25\so2_val_airpollute.csv')
    
    df7 = pd.read_csv(afolder + r'\oak_100\co_val_airpollute.csv')
    df8 = pd.read_csv(afolder + r'\oak_100\no2_val_airpollute.csv')
    df9 = pd.read_csv(afolder + r'\oak_100\o3_val_airpollute.csv')
    df10 = pd.read_csv(afolder + r'\oak_100\pm2_5_val_airpollute.csv')
    df11 = pd.read_csv(afolder + r'\oak_100\pm10_val_airpollute.csv')
    df12 = pd.read_csv(afolder + r'\oak_100\so2_val_airpollute.csv')
    
    def cleanair(df, pollutant):
        df1 = df[['landcover','tons_change_base_bau','tons_change_trt_bau']]
        df1 = df1.rename(columns = {'landcover':'Landcover','tons_change_base_bau': 'No Activity Applied','tons_change_trt_bau':'25% Oak Woodland Conversion Adoption'})
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1[pollutant] = df1.sum(axis=1)
        df1.reset_index(inplace = True)
        df1 = df1[['index', pollutant]]
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1.reset_index(inplace = True)
        df1 = df1.rename(columns = {'Landcover':'Air Pollutant'})
        return df1

    dlist = [df1,df2,df3,df4,df5,df6]
    plist = ['CO2','NO2','O3','PM 2.5','PM 10', 'SO2']
    pcadict = {}
    counter = 0
    for i in dlist:
        temp = cleanair(i,plist[counter])
        pcadict[plist[counter]] = temp
        counter = counter + 1
    tlist = list(pcadict.values())
    df25 = pd.concat(tlist)

    def cleanair(df, pollutant):
        df1 = df[['landcover','tons_change_trt_bau']]
        df1 = df1.rename(columns = {'landcover':'Landcover','tons_change_trt_bau': '100% Oak Woodland Conversion Adoption'})
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1[pollutant] = df1.sum(axis=1)
        df1.reset_index(inplace = True)
        df1 = df1[['index', pollutant]]
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        df1.reset_index(inplace = True)
        df1 = df1.rename(columns = {'Landcover':'Air Pollutant'})
        return df1

    dlist = [df7,df8,df9,df10,df11,df12]
    plist = ['CO2','NO2','O3','PM 2.5','PM 10', 'SO2']
    pcadict = {}
    counter = 0
    for i in dlist:
        temp = cleanair(i,plist[counter])
        pcadict[plist[counter]] = temp
        counter = counter + 1
    tlist = list(pcadict.values())
    df100 = pd.concat(tlist)
    
    test = pd.merge(df25,df100, how = 'left', on = 'Air Pollutant')
    test.to_csv(outfolder+'2030 Air Quality Change OAK.csv', index = False)
    return test

def scenic2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\scenic.csv')
    df = df[['gen_class','ha_2014']]
    df = df.loc[df['ha_2014'] > 0]
    df = df.rename(columns = {'gen_class': 'General Landcover', 'ha_2014':'Hectares'})
    df.to_csv(outfolder+'2014 Scenic Value.csv', index = False)

def scenic2030():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\scenic.csv')
    df = df[['gen_class','ha_change_base_bau', 'ha_change_base_med', 'ha_change_base_max' ]]
    df = df.rename(columns = {'gen_class': 'General Landcover', 'ha_change_base_bau':'No Activity Applied', 'ha_change_base_med':'Medium Infill Scenario', 'ha_change_base_max':'Max Infill Scenario'})
    
    #Remove any rows with all 0s
    df.set_index(['General Landcover'], inplace = True)
    df = df[df.values.sum(axis=1) != 0]
    df.reset_index(inplace = True)
    
#    #Transpose columns and rows
#    test = df.transpose()
#    test.columns = test.iloc[0]
#    test = test[1:]
    
    df.to_csv(outfolder+'2030 Scenic Value.csv', index = False)


def move2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\countymovement.csv')
    df = df[['resistance_class','ha_2014']]
    df = df.loc[df['ha_2014'] > 0]
    df = df.rename(columns = {'resistance_class': 'Resistance to Movement', 'ha_2014':'Hectares'})
    
    
    a = df
    b, c = a.iloc[0], a.iloc[1]
    temp = a.iloc[0].copy()
    a.iloc[0] = c
    a.iloc[1] = temp
    
    b, c = a.iloc[1], a.iloc[2]
    temp = a.iloc[1].copy()
    a.iloc[1] = c
    a.iloc[2] = temp
    df = a
    
    df.to_csv(outfolder+'2014 Terrestrial Connectivity.csv', index = False)

def move2030_rre():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\countymovement.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\countymovement.csv')
    df2 = df2[['resistance_class','ha_change_trt_bau']]
    df2 = df2.rename(columns = {'resistance_class': 'Resistance to Movement','ha_change_trt_bau':'100% Riparian Restoration Adoption'})
    df = df[['resistance_class','ha_change_base_bau','ha_change_trt_bau']]
    df = df.rename(columns = {'resistance_class': 'Resistance to Movement', 'ha_change_base_bau':'No Activity Applied', 'ha_change_trt_bau':'25% Riparian Restoration Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Resistance to Movement', how = 'left')
    
    a = temp
    c =a.iloc[1]
    temp = a.iloc[0].copy()
    a.iloc[0] = c
    a.iloc[1] = temp
        
    c = a.iloc[2]
    temp = a.iloc[1].copy()
    a.iloc[1] = c
    a.iloc[2] = temp
    df = a
    df.to_csv(outfolder+'2030 Terrestrial Connectivity RRE.csv', index = False)

def move2030_hpl():
    df2 = pd.read_csv(afolder + r'\hedgerow_100\countymovement.csv')
    df = pd.read_csv(afolder + r'\hedgerow_25\countymovement.csv')
    df2 = df2[['resistance_class','ha_change_trt_bau']]
    df2 = df2.rename(columns = {'resistance_class': 'Resistance to Movement','ha_change_trt_bau':'100% Hedgerow Planting Adoption'})
    df = df[['resistance_class','ha_change_base_bau','ha_change_trt_bau']]
    df = df.rename(columns = {'resistance_class': 'Resistance to Movement', 'ha_change_base_bau':'No Activity Applied', 'ha_change_trt_bau':'25% Hedgerow Planting Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Resistance to Movement', how = 'left')

    a = temp
    c =a.iloc[1]
    temp = a.iloc[0].copy()
    a.iloc[0] = c
    a.iloc[1] = temp
        
    c = a.iloc[2]
    temp = a.iloc[1].copy()
    a.iloc[1] = c
    a.iloc[2] = temp
    df = a
    df.to_csv(outfolder+'2030 Terrestrial Connectivity HPL.csv', index = False)

def move2014_eca():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\ecamovement.csv')
    df = df[['resistance_class','ha_2014']]
    df = df.loc[df['ha_2014'] > 0]
    df = df.rename(columns = {'resistance_class': 'Resistance to Movement', 'ha_2014':'Hectares'})
    
    a = df
    c =a.iloc[1]
    temp = a.iloc[0].copy()
    a.iloc[0] = c
    a.iloc[1] = temp
        
    c = a.iloc[2]
    temp = a.iloc[1].copy()
    a.iloc[1] = c
    a.iloc[2] = temp
    df = a
    df.to_csv(outfolder+'2014 ECA Terrestrial Connectivity.csv', index = False)

def move2030_rre_eca():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\ecamovement.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\ecamovement.csv')
    df2 = df2[['resistance_class','ha_change_trt_bau']]
    df2 = df2.rename(columns = {'resistance_class': 'Resistance to Movement','ha_change_trt_bau':'100% Riparian Restoration Adoption'})
    df = df[['resistance_class','ha_change_base_bau','ha_change_trt_bau']]
    df = df.rename(columns = {'resistance_class': 'Resistance to Movement', 'ha_change_base_bau':'No Activity Applied', 'ha_change_trt_bau':'25% Riparian Restoration Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Resistance to Movement', how = 'left')
    
    a = temp
    c =a.iloc[1]
    temp = a.iloc[0].copy()
    a.iloc[0] = c
    a.iloc[1] = temp
        
    c = a.iloc[2]
    temp = a.iloc[1].copy()
    a.iloc[1] = c
    a.iloc[2] = temp
    df = a
    df.to_csv(outfolder+'2030 ECA Terrestrial Connectivity RRE.csv', index = False)

def move2030_hpl_eca():
    df2 = pd.read_csv(afolder + r'\hedgerow_100\ecamovement.csv')
    df = pd.read_csv(afolder + r'\hedgerow_25\ecamovement.csv')
    df2 = df2[['resistance_class','ha_change_trt_bau']]
    df2 = df2.rename(columns = {'resistance_class': 'Resistance to Movement','ha_change_trt_bau':'100% Hedgerow Planting Adoption'})
    df = df[['resistance_class','ha_change_base_bau','ha_change_trt_bau']]
    df = df.rename(columns = {'resistance_class': 'Resistance to Movement', 'ha_change_base_bau':'No Activity Applied', 'ha_change_trt_bau':'25% Hedgerow Planting Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Resistance to Movement', how = 'left')
    a = temp
    c =a.iloc[1]
    temp = a.iloc[0].copy()
    a.iloc[0] = c
    a.iloc[1] = temp
        
    c = a.iloc[2]
    temp = a.iloc[1].copy()
    a.iloc[1] = c
    a.iloc[2] = temp
    df = a
    
    df.to_csv(outfolder+'2030 ECA Terrestrial Connectivity HPL.csv', index = False)

def lcc2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\lcchange.csv')
    df = df[['landcover','ha_2014']]
    df = df.loc[df['ha_2014'] > 0]
    df = df.rename(columns = {'landcover': 'Landcover', 'ha_2014':'Hectares'})
    df.to_csv(outfolder+'2014 Natural Habitat Area.csv', index = False)

def lcc2030_rre():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\lcchange.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\lcchange.csv')
    df2 = df2[['landcover','ha_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'Landcover','ha_change_trt_bau':'100% Riparian Restoration Adoption'})
    df = df[['landcover','ha_change_base_bau','ha_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'Landcover', 'ha_change_base_bau':'No Activity Applied', 'ha_change_trt_bau':'25% Riparian Restoration Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Landcover', how = 'left')

    temp = temp[['Landcover','25% Riparian Restoration Adoption','100% Riparian Restoration Adoption']]
    temp.to_csv(outfolder+'2030 Natural Habitat Area RRE.csv', index = False)
    
def lcc2030_oak():
    df2 = pd.read_csv(afolder + r'\oak_100\lcchange.csv')
    df = pd.read_csv(afolder + r'\oak_25\lcchange.csv')
    df2 = df2[['landcover','ha_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'Landcover','ha_change_trt_bau':'100% Oak Woodland Conversion Adoption'})
    df = df[['landcover','ha_change_base_bau','ha_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'Landcover', 'ha_change_base_bau':'No Activity Applied', 'ha_change_trt_bau':'25% Oak Woodland Conversion Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Landcover', how = 'left')
    temp = temp.loc[temp['Landcover'].isin(['Forest','Grassland'])]
    
    temp.to_csv(outfolder+'2030 Natural Habitat Area OAK.csv', index = False)    
    
    
def pcalcc2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\pca_cover_change.csv')
    df = df[['landcover','ha_2014']]
    df = df.loc[df['ha_2014'] > 0]
    df = df.rename(columns = {'landcover': 'Landcover', 'ha_2014':'Hectares'})
    df.to_csv(outfolder+'2014 Priority Conservation Areas.csv', index = False)

def pcalcc2030_rre():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\pca_cover_change.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\pca_cover_change.csv')
    df2 = df2[['landcover','ha_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'Landcover','ha_change_trt_bau':'100% Riparian Restoration Adoption'})
    df = df[['landcover','ha_change_base_bau','ha_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'Landcover', 'ha_change_base_bau':'No Activity Applied', 'ha_change_trt_bau':'25% Riparian Restoration Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Landcover', how = 'left')
    temp = temp[['Landcover','25% Riparian Restoration Adoption','100% Riparian Restoration Adoption']]
    
    temp.to_csv(outfolder+'2030 Priority Conservation Areas RRE.csv', index = False)
    
def pcalcc2030_oak():
    df2 = pd.read_csv(afolder + r'\oak_100\pca_cover_change.csv')
    df = pd.read_csv(afolder + r'\oak_25\pca_cover_change.csv')
    df2 = df2[['landcover','ha_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'Landcover','ha_change_trt_bau':'100% Oak Woodland Conversion Adoption'})
    df = df[['landcover','ha_change_base_bau','ha_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'Landcover', 'ha_change_base_bau':'No Activity Applied', 'ha_change_trt_bau':'25% Oak Woodland Conversion Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Landcover', how = 'left')

    temp = temp.loc[temp['Landcover'].isin(['Forest','Grassland'])]
    temp.to_csv(outfolder+'2030 Priority Conservation Areas OAK.csv', index = False)      
    
def terrhab2030_rre():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\terrhab.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\terrhab.csv')
    df2 = df2[['guild','ha_trt_bau']]
    df2 = df2.rename(columns = {'guild': 'Guild','ha_trt_bau':'100% Oak Woodland Conversion Adoption'})
    df = df[['guild','ha_base_bau','ha_trt_bau']]
    df = df.rename(columns = {'guild': 'Guild', 'ha_base_bau':'No Activity Applied', 'ha_trt_bau':'25% Oak Woodland Conversion Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Guild', how = 'left')
    
    
    temp.loc[temp['Guild'] == 'mammals_avg_deg_ha', 'Guild'] = 'Mammal Degraded'
    temp.loc[temp['Guild'] == 'mammals_avg_imp_ha', 'Guild'] = 'Mammal Improved'
    temp.loc[temp['Guild'] == 'birds_avg_deg_ha', 'Guild'] = 'Bird Degraded'
    temp.loc[temp['Guild'] == 'birds_avg_imp_ha', 'Guild'] = 'Bird Improves'
    temp.loc[temp['Guild'] == 'amphibians_avg_deg_ha', 'Guild'] = 'Amphibian Degraded'
    temp.loc[temp['Guild'] == 'amphibians_avg_imp_ha', 'Guild'] = 'Amphibian Improved'
    temp.loc[temp['Guild'] == 'tes_avg_deg_ha', 'Guild'] = 'Threatened and Endangered Degraded'
    temp.loc[temp['Guild'] == 'tes_avg_imp_ha', 'Guild'] = 'Treatened and Endangered Improved'

    
    temp.to_csv(outfolder+'2030 Terrestrial Habitat Value RRE.csv', index = False)    
    
def terrhab2030_oak():
    df2 = pd.read_csv(afolder + r'\oak_100\terrhab.csv')
    df = pd.read_csv(afolder + r'\oak_25\terrhab.csv')
    df2 = df2[['guild','ha_trt_bau']]
    df2 = df2.rename(columns = {'guild': 'Guild','ha_trt_bau':'100% Oak Woodland Conversion Adoption'})
    df = df[['guild','ha_base_bau','ha_trt_bau']]
    df = df.rename(columns = {'guild': 'Guild', 'ha_base_bau':'No Activity Applied', 'ha_trt_bau':'25% Oak Woodland Conversion Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Guild', how = 'left')
    temp.loc[temp['Guild'] == 'mammals_avg_deg_ha', 'Guild'] = 'Mammal Degraded'
    temp.loc[temp['Guild'] == 'mammals_avg_imp_ha', 'Guild'] = 'Mammal Improved'
    temp.loc[temp['Guild'] == 'birds_avg_deg_ha', 'Guild'] = 'Bird Degraded'
    temp.loc[temp['Guild'] == 'birds_avg_imp_ha', 'Guild'] = 'Bird Improves'
    temp.loc[temp['Guild'] == 'amphibians_avg_deg_ha', 'Guild'] = 'Amphibian Degraded'
    temp.loc[temp['Guild'] == 'amphibians_avg_imp_ha', 'Guild'] = 'Amphibian Improved'
    temp.loc[temp['Guild'] == 'tes_avg_deg_ha', 'Guild'] = 'Threatened and Endangered Degraded'
    temp.loc[temp['Guild'] == 'tes_avg_imp_ha', 'Guild'] = 'Treatened and Endangered Improved'
    
    temp.to_csv(outfolder+'2030 Terrestrial Habitat Value OAK.csv', index = False)        
    
def aqua2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\aquatic.csv')
    df = df[['gen_class','ha_2014']]
    df = df.loc[df['ha_2014'] > 0]
    df = df.rename(columns = {'gen_class': 'Landcover', 'ha_2014':'Hectares'})
    df.to_csv(outfolder+'2014 Aquatic Biodiversity.csv', index = False)    
    
    
def aqua2030_rre():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\aquatic.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\aquatic.csv')
    df2 = df2[['gen_class','ha_change_trt_bau']]
    df2 = df2.rename(columns = {'gen_class': 'Landcover','ha_change_trt_bau':'100% Riparian Restoration Adoption'})
    df = df[['gen_class','ha_change_base_bau','ha_change_trt_bau']]
    df = df.rename(columns = {'gen_class': 'Landcover', 'ha_change_base_bau':'No Activity Applied', 'ha_change_trt_bau':'25% Riparian Restoration Adoption'})
    
    
    temp = pd.merge(df, df2, on = 'Landcover', how = 'left')

    
    temp.to_csv(outfolder+'2030 Aquatic Biodiversity RRE.csv', index = False)   


def eco_resi():
    df = pd.read_csv(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\urb_25\eco_resil.csv")
    df = df[['gen_class','ha_change_base_bau','ha_change_base_med','ha_change_base_max']]
    df = df.rename(columns = {'gen_class': 'Landcover', 'ha_change_base_bau':'Reference', 'ha_change_base_med':'Medium Infill','ha_change_base_max':'Max Infill'})
    temp = df
    temp.set_index(['Landcover'], inplace = True)
    temp = temp[temp.values.sum(axis=1) != 0]
    temp.reset_index(inplace = True)
    
    temp.to_csv(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\simp_tables\ecoresilience_table.csv", index = False)   
def soc_resi():
    df = pd.read_csv(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\urb_25\soc_res.csv")
    df = df[['gen_class','ha_change_base_bau','ha_change_base_med','ha_change_base_max']]
    df = df.rename(columns = {'gen_class': 'Landcover', 'ha_change_base_bau':'Reference', 'ha_change_base_med':'Medium Infill','ha_change_base_max':'Max Infill'})
    temp = df
    temp.set_index(['Landcover'], inplace = True)
    temp = temp[temp.values.sum(axis=1) != 0]
    temp.reset_index(inplace = True)
    
    temp.to_csv(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\simp_tables\socresilience_table.csv", index = False)   
       
    
def soc_resi14():
    df = pd.read_csv(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\urb_25\soc_res.csv")
    df = df[['gen_class','ha_2014']]
    df = df.loc[df['ha_2014'] > 0]
    df = df.rename(columns = {'gen_class': 'Landcover', 'ha_2014':'Hectares'})
    df.to_csv(outfolder+'2014 Social Resilience.csv', index = False)        
    
def eco_resi14():
    df = pd.read_csv(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\urb_25\eco_resil.csv")
    df = df[['gen_class','ha_2014']]
    df = df.loc[df['ha_2014'] > 0]
    df = df.rename(columns = {'gen_class': 'Landcover', 'ha_2014':'Hectares'})
    df.to_csv(outfolder+'2014 Ecological Resilience.csv', index = False)        

    
#fmmp2014()
#fmmp2030()
#crop2014()
#crop2030()
#watcon2030()
#watcon2014()
#watint2014()
#watint2030_rre()
#groundwater2014()
#nitrun2014()
#nitleach2014()
#nitrun2030_rre()
#nitrun2030_nfm()
#nitleach2030_rre()
#nitleach2030_nfm()
#flood2014()
#flood2030()
#test = air2014()
#test = air2030()
#test = air2030_rre()
#test = air2030_HPL()
#test = air2030_URB()
#test = air2030_OAK()
#scenic2014()
#scenic2030()
#move2014()
#move2030_rre()
#move2030_hpl()
#move2014_eca()
#move2030_rre_eca()
#move2030_hpl_eca()
#lcc2014()
#lcc2030_rre()
#lcc2030_oak()
#pcalcc2014()
#pcalcc2030_rre()
#pcalcc2030_oak()
#terrhab2030_rre()
#terrhab2030_oak()
#aqua2014()
#aqua2030_rre()
eco_resi()
soc_resi()
eco_resi14()
soc_resi14()























