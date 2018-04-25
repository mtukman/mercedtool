# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 12:10:25 2018

@author: Dylan
"""


afolder = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\\"
outfolder = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\simp_tables\\"
import pandas as pd




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
    df = df.rename(columns = {'landcover': 'Crop Type', 'cropvalue_usd_2014':'Dollar Value'})
    df.to_csv(outfolder+'2014 Crop Value.csv', index = False)



def crop2030():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\cropvalue.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\cropvalue.csv')
    df2 = df2[['landcover','usd_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'Crop Type','usd_change_trt_bau':'100% Riparian Adoption'})
    df = df[['landcover','usd_change_base_bau','usd_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'Crop Type', 'usd_change_base_bau':'Reference', 'usd_change_trt_bau':'25% Riparian Adoption'})
    
    temp = pd.merge(df, df2, on = 'Crop Type', how = 'left')
    temp.set_index(['Crop Type'], inplace = True)
    temp = temp[temp.values.sum(axis=1) != 0]
    temp.reset_index(inplace = True)
    
    temp.to_csv(outfolder+'2030 Crop Value.csv', index = False)
    
    
    
    
def watcon2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\watcon.csv')
    df = df[['landcover','ac_ft_2014']]
    df = df.loc[df['ac_ft_2014'] > 0]
    df = df.rename(columns = {'landcover': 'Farmland Class', 'ac_ft_2014':'2014 Acre Feet Water Demand'})
    df.to_csv(outfolder+'2014 Ag and Urban Water Conservation.csv', index = False)




def watcon2030():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\watcon.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\watcon.csv')
    df2 = df2[['landcover','ac_ft_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'Landcover','ac_ft_change_trt_bau':'Acre Feet Change 100% Riparian'})
    df = df[['landcover','ac_ft_change_base_bau','ac_ft_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'Landcover', 'ac_ft_change_base_bau':'Acre Feet Change Reference', 'ac_ft_change_trt_bau':'Acre Feet Change 25% Riparian'})

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
    df['landcover'] = 'Acre Feet Lost (Annually)'
    df = df.groupby(['landcover'], as_index = False).sum()
    
    
    df = df.rename(columns = {'landcover': 'y_axis', 'ac_ft_rec_lst_base_bau':'Reference Scenario', 'ac_ft_rec_lst_base_med':'Medium Infill Scenario', 'ac_ft_rec_lst_base_max':'Max Infill Scenario'})
    df.to_csv(outfolder+'2030 Groundwater Recharge.csv', index = False)


def watint2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\watint.csv')
    df = df[['Integrity_Class','ha_2014']]
    df = df.rename(columns = {'Integrity_Class': 'Watershed Class', 'ha_2014':'2014 Hectares'})
    df.to_csv(outfolder+'2014 Watershed Integrity.csv', index = False)
    
def watint2030_rre():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\watint.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\watint.csv')
    df2 = df2[['Integrity_Class','ha_change_trt_bau']]
    df2 = df2.rename(columns = {'Integrity_Class': 'Watershed Class','ha_change_trt_bau':'Hectares Change 100% Riparian'})
    df = df[['Integrity_Class','ha_change_base_bau','ha_change_trt_bau']]
    df = df.rename(columns = {'Integrity_Class': 'Watershed Class', 'ha_change_base_bau':'Hectares Change Reference', 'ha_change_trt_bau':'Hectares Change 25% Riparian'})

    temp = pd.merge(df, df2, on = 'Watershed Class', how = 'left')
    temp.set_index(['Watershed Class'], inplace = True)
    temp = temp[temp.values.sum(axis=1) != 0]
    temp.reset_index(inplace = True)
    
    temp.to_csv(outfolder+'2030 Watershed Integrity Riparian.csv', index = False)   


def nitrun2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\runoff_nitrates.csv')
    df = df[['landcover','tons_no3_14']]
    df = df.loc[df['tons_no3_14'] > 0]
    df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_14':'2014 Tons of Nitrate Runoff'})
    df.to_csv(outfolder+'2014 Water Quality - Nitrate Runoff.csv', index = False)

def nitleach2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\leach_nitrates.csv')
    df = df[['landcover','tons_no3_14']]
    df = df.loc[df['tons_no3_14'] > 0]
    df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_14':'2014 Tons of Nitrate Leaching'})
    df.to_csv(outfolder+'2014 Water Quality - Nitrate Leaching.csv', index = False)
    
    
def nitrun2030_rre():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\runoff_nitrates.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\runoff_nitrates.csv')
    df2 = df2[['landcover','tons_no3_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'y_axis','tons_no3_change_trt_bau':'100% Riparian'})
    df = df[['landcover','tons_no3_change_base_bau','tons_no3_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'y_axis', 'tons_no3_change_base_bau':'Reference', 'tons_no3_change_trt_bau':'25% Riparian'})
    
    
    temp = pd.merge(df, df2, on = 'y_axis', how = 'left')
    temp['y_axis'] = 'Change in Tons of Runoff (Annually)'
    temp = temp.groupby(['y_axis'], as_index = False).sum()
    
    temp.to_csv(outfolder+'2030 Water Quality - Nitrate Runoff RRE.csv', index = False)
    

def nitrun2030_nfm():
    df2 = pd.read_csv(afolder + r'\nfm_100\runoff_nitrates.csv')
    df = pd.read_csv(afolder + r'\nfm_25\runoff_nitrates.csv')
    df2 = df2[['landcover','tons_no3_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'y_axis','tons_no3_change_trt_bau':'100% N Fertilizer Management'})
    df = df[['landcover','tons_no3_change_base_bau','tons_no3_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'y_axis', 'tons_no3_change_base_bau':'Reference', 'tons_no3_change_trt_bau':'25% N Fertilizer Management'})
    
    
    temp = pd.merge(df, df2, on = 'y_axis', how = 'left')
    temp['y_axis'] = 'Change in Tons of Runoff (Annually)'
    temp = temp.groupby(['y_axis'], as_index = False).sum()
    
    temp.to_csv(outfolder+'2030 Water Quality - Nitrate Runoff NFM.csv', index = False)
    
def nitleach2030_rre():
    df2 = pd.read_csv(afolder + r'\RRE_COUNTY_100\leach_nitrates.csv')
    df = pd.read_csv(afolder + r'\RRE_COUNTY_25\leach_nitrates.csv')
    df2 = df2[['landcover','tons_no3_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'y_axis','tons_no3_change_trt_bau':'100% Riparian'})
    df = df[['landcover','tons_no3_change_base_bau','tons_no3_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'y_axis', 'tons_no3_change_base_bau':'Reference', 'tons_no3_change_trt_bau':'25% Riparian'})
    
    
    temp = pd.merge(df, df2, on = 'y_axis', how = 'left')
    temp['y_axis'] = 'Change in Tons of Leaching (Annually)'
    temp = temp.groupby(['y_axis'], as_index = False).sum()
    
    temp.to_csv(outfolder+'2030 Water Quality - Nitrate Leaching RRE.csv', index = False)
def nitleach2030_nfm():
    df2 = pd.read_csv(afolder + r'\nfm_100\leach_nitrates.csv')
    df = pd.read_csv(afolder + r'\nfm_25\leach_nitrates.csv')
    df2 = df2[['landcover','tons_no3_change_trt_bau']]
    df2 = df2.rename(columns = {'landcover': 'y_axis','tons_no3_change_trt_bau':'100% N Fertilizer Management'})
    df = df[['landcover','tons_no3_change_base_bau','tons_no3_change_trt_bau']]
    df = df.rename(columns = {'landcover': 'y_axis', 'tons_no3_change_base_bau':'Reference', 'tons_no3_change_trt_bau':'25% N Fertilizer Management'})
    
    
    temp = pd.merge(df, df2, on = 'y_axis', how = 'left')
    temp['y_axis'] = 'Change in Tons of Leaching (Annually)'
    temp = temp.groupby(['y_axis'], as_index = False).sum()
    
    temp.to_csv(outfolder+'2030 Water Quality - Nitrate Leaching NFM.csv', index = False)

def flood2014():
    df = pd.read_csv(afolder + r'\RRE_COUNTY_100\leach_nitrates.csv')
    df = df[['gen_class','ha_2014']]
    df = df.loc[df['ha_2014'] > 0]
    df = df.rename(columns = {'gen_class': 'General Landcover', 'ha_2014':'Hectares of General Landcover in 2014'})
    df.to_csv(outfolder+'2014 Flood Risk Reduction.csv', index = False)
    
    
    















fmmp2014()
fmmp2030()
crop2014()
crop2030()
watcon2030()
watcon2014()
watint2014()
watint2030_rre()
groundwater2014()
nitrun2014()
nitleach2014()
nitrun2030_rre()
nitrun2030_nfm()
nitleach2030_rre()
nitleach2030_nfm()





