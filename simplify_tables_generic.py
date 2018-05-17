
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 12:10:25 2018

@author: Dylan
"""
runfolder = r"E:\Temp\20180515-110310\\"
mba_title_font = 18
plot_dict = {}
axis_lab_font = 16
import plotly.plotly as py

py.sign_in('mtukman', 'FbUYCv4tcjCPF2ZdfzKo')

def simp(afolder = ''):

    import os
    import pandas as pd
    import functools
    
    if not os.path.exists(afolder + 'plot_tables'):
        os.makedirs(afolder + 'plot_tables')
    if not os.path.exists(afolder + 'plots'):
        os.makedirs(afolder + 'plots')
    outfolder =     afolder + 'plot_tables/'
        
    def fmmp2014():
        df = pd.read_csv(afolder + r'\fmmp.csv')
        df = df[['fmmp_class','ha_2014']]
        df = df.loc[df['ha_2014'] > 0]
        df = df.rename(columns = {'fmmp_class': 'Farmland Class', 'ha_2014':'Hectares'})
        df.to_csv(outfolder+'2014 Ag Land Quality.csv', index = False)
        
        
    def fmmp2030():
        df = pd.read_csv(afolder + r'\fmmp.csv')
        df = df[['fmmp_class','ha_loss_trt_bau', 'ha_loss_trt_med', 'ha_loss_trt_max' ]]
        df = df.rename(columns = {'fmmp_class': 'Farmland Class', 'ha_loss_trt_bau':'Reference Scenario', 'ha_loss_trt_med':'Medium Infill Scenario', 'ha_loss_trt_max':'Max Infill Scenario'})
        df.set_index(['Farmland Class'], inplace = True)
        df = df[df.values.sum(axis=1) != 0]
        df.reset_index(inplace = True)
        
        df.to_csv(outfolder+'2030 Ag Land Quality.csv', index = False)
        
        
        
    def crop2014():
        df = pd.read_csv(afolder + r'\cropvalue.csv')
        df = df[['landcover','cropvalue_usd_2014']]
        df = df.rename(columns = {'landcover': 'Crop Type', 'cropvalue_usd_2014':'US Dollars'})
        df.to_csv(outfolder+'2014 Crop Value.csv', index = False)
    
    
    
    def crop2030():
        df2 = pd.read_csv(afolder + r'\cropvalue.csv')
        df2 = df2[['landcover','usd_change_trt_bau', 'usd_change_trt_med', 'usd_change_trt_max']]
        df2 = df2.rename(columns = {'landcover': 'Crop Type', 'usd_change_trt_bau':'Reference Scenario', 'usd_change_trt_med':'Medium Infill Scenario','usd_change_trt_max':'Max Infill Scenario'})
        df2.to_csv(outfolder+'2030 Crop Value.csv', index = False)
        
        
        
        
    def watcon2014():
        df = pd.read_csv(afolder + r'\watcon.csv')
        df = df[['landcover','ac_ft_2014']]
        df = df.loc[df['ac_ft_2014'] > 0]
        df = df.rename(columns = {'landcover': 'Landcover', 'ac_ft_2014':'Acre Feet Annual Water Demand'})
        df.to_csv(outfolder+'2014 Ag and Urban Water Conservation.csv', index = False)
    
    
    
    
    def watcon2030():
        df2 = pd.read_csv(afolder + r'\watcon.csv')
        df2 = df2[['landcover','ac_ft_change_trt_bau', 'ac_ft_change_trt_med', 'ac_ft_change_trt_max']]
        df2 = df2.rename(columns = {'landcover': 'Landcover', 'ac_ft_change_trt_bau':'Reference Scenario', 'ac_ft_change_trt_med':'Medium Infill Scenario','ac_ft_change_trt_max':'Max Infill Scenario'})
        df2 = df2[df2.values.sum(axis=1) != 0]
        df2.reset_index(inplace = True)
        df2.to_csv(outfolder+'2030 Ag and Urban Water Conservation.csv', index = False)

    def groundwater2030():
        df = pd.read_csv(afolder + r'\groundwater.csv')
        df = df[['landcover','ac_ft_rec_lst_trt_bau','ac_ft_rec_lst_trt_med','ac_ft_rec_lst_trt_max']]
        df.set_index(['landcover'], inplace = True)
        df = df[df.values.sum(axis=1) != 0]
        df.reset_index(inplace = True)
        df['landcover'] = 'Acre Feet of Annual Groundwater Recharge Lost'
        df = df.groupby(['landcover'], as_index = False).sum()
        test = df.transpose()
        test.columns = test.iloc[0]
        test = test[1:]
        test.reset_index(inplace = True)
        
        df = df.rename(columns = {'landcover': 'Landcover', 'ac_ft_rec_lst_trt_bau':'Reference Scenario', 'ac_ft_rec_lst_trt_med':'Medium Infill Scenario', 'ac_ft_rec_lst_trt_max':'Max Infill Scenario'})
        test = df.transpose()
        test.columns = test.iloc[0]
        test = test[1:]
        test.reset_index(inplace = True)
        test.rename(columns = {'index':'Development Scenario'}, inplace = True)
        print (test)
        test.to_csv(outfolder+'2030 Groundwater Recharge.csv', index = False)
    
    
    def watint2014():
        df = pd.read_csv(afolder + r'\watint.csv')
        df = df[['Integrity_Class','ha_2014']]
        df = df.rename(columns = {'Integrity_Class': 'Watershed Class', 'ha_2014':'Hectares'})
        df = df.loc[df['Watershed Class'] != 'na']
        
        df.to_csv(outfolder+'2014 Watershed Integrity.csv', index = False)
        
    def watint2030():
        df2 = pd.read_csv(afolder + r'\watint.csv')
        df = pd.read_csv(afolder + r'\watint.csv')
        df2 = df2[['Integrity_Class','ha_change_trt_bau']]
        df2 = df2.rename(columns = {'Integrity_Class': 'Watershed Class','ha_change_trt_bau':'Reference Scenario'})
        df = df[['Integrity_Class','ha_change_trt_med','ha_change_trt_max']]
        df = df.rename(columns = {'Integrity_Class': 'Watershed Class', 'ha_change_trt_med':'Medium Infill Scenario', 'ha_change_trt_max':'Max Infill Scenario'})
    
        temp = pd.merge(df2, df, on = 'Watershed Class', how = 'left')
        temp.set_index(['Watershed Class'], inplace = True)
        temp = temp[temp.values.sum(axis=1) != 0]
        temp.reset_index(inplace = True)
        
        temp.to_csv(outfolder+'2030 Watershed Integrity.csv', index = False)   
    
    
    def nitrun2014():
        df = pd.read_csv(afolder + r'\runoff_nitrates.csv')
        df = df[['landcover','tons_no3_14']]
        df = df.loc[df['tons_no3_14'] > 0]
        df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_14':'Annual Tons of Nitrate Runoff'})
        df.to_csv(outfolder+'2014 Water Quality - Nitrate Runoff.csv', index = False)
    
    def nitleach2014():
        df = pd.read_csv(afolder + r'\leach_nitrates.csv')
        df = df[['landcover','tons_no3_14']]
        df = df.loc[df['tons_no3_14'] > 0]
        df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_14':'Annual Tons of Nitrate Leaching'})
        df.to_csv(outfolder+'2014 Water Quality - Nitrate Leaching.csv', index = False)
        
        
    def nitrun2030():
        df2 = pd.read_csv(afolder + r'\runoff_nitrates.csv')
        df = pd.read_csv(afolder + r'\runoff_nitrates.csv')
        df2 = df2[['landcover','tons_no3_change_trt_bau']]
        df2 = df2.rename(columns = {'landcover': 'Landcover','tons_no3_change_trt_bau':'Reference Scenario'})
        df = df[['landcover','tons_no3_change_trt_med','tons_no3_change_trt_max']]
        df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_change_trt_med':'Medium Infill Scenario', 'tons_no3_change_trt_max':'Max Infill Scenario'})
        
        
        temp = pd.merge(df2, df, on = 'Landcover', how = 'left')
        temp['Landcover'] = 'Change in Annual Tons of Nitrate Runoff'
        temp = temp.groupby(['Landcover'], as_index = False).sum()
        test = temp.transpose()
        test.columns = test.iloc[0]
        test = test[1:]
        test.reset_index(inplace = True)
        test.rename(columns = {'index':'Scenario'}, inplace = True)
        test.to_csv(outfolder+'2030 Water Quality - Nitrate Runoff.csv', index = False)
        
    def nitleach2030():
        df2 = pd.read_csv(afolder + r'\leach_nitrates.csv')
        df = pd.read_csv(afolder + r'\leach_nitrates.csv')
        df2 = df2[['landcover','tons_no3_change_trt_bau']]
        df2 = df2.rename(columns = {'landcover': 'Landcover','tons_no3_change_trt_bau':'Reference Scenario'})
        df = df[['landcover','tons_no3_change_trt_med','tons_no3_change_trt_max']]
        df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_change_trt_med':'Medium Infill Scenario', 'tons_no3_change_trt_max':'Max Infill Scenario'})
        
        temp = pd.merge(df2, df, on = 'Landcover', how = 'left')
        temp['Landcover'] = 'Change in Annual Tons of Nitrate Leaching'
        temp = temp.groupby(['Landcover'], as_index = False).sum()
        test = temp.transpose()
        test.columns = test.iloc[0]
        test = test[1:]
        test.reset_index(inplace = True)
        test.rename(columns = {'index':'Scenario'}, inplace = True)
        test.to_csv(outfolder+'2030 Water Quality - Nitrate Leaching.csv', index = False)

    
    def flood2014():
        df = pd.read_csv(afolder + r'\flood100.csv')
        df = df[['gen_class','ha_2014']]
        df = df.loc[df['ha_2014'] > 0]
        df = df.rename(columns = {'gen_class': 'General Landcover', 'ha_2014':'Hectares'})
        df.to_csv(outfolder+'2014 Flood Risk Reduction.csv', index = False)
        
        
        
    
    def flood2030():
        df = pd.read_csv(afolder + r'\flood100.csv')
        df = df[['gen_class','ha_change_trt_bau', 'ha_change_trt_med', 'ha_change_trt_max' ]]
        df = df.rename(columns = {'gen_class': 'General Landcover', 'ha_change_trt_bau':'Reference Scenario', 'ha_change_trt_med':'Medium Infill Scenario', 'ha_change_trt_max':'Max Infill Scenario'})
        
        #Remove any rows with all 0s
        df.set_index(['General Landcover'], inplace = True)
        df = df[df.values.sum(axis=1) != 0]
        df.reset_index(inplace = True)

        df.to_csv(outfolder+'2030 Flood Risk Reduction.csv', index = False)
    
    
    def air2014():
        import functools as fc
        df1 = pd.read_csv(afolder + r'\co_val_airpollute.csv')
        df2 = pd.read_csv(afolder + r'\no2_val_airpollute.csv')
        df3 = pd.read_csv(afolder + r'\o3_val_airpollute.csv')
        df4 = pd.read_csv(afolder + r'\pm2_5_val_airpollute.csv')
        df5 = pd.read_csv(afolder + r'\pm10_val_airpollute.csv')
        df6 = pd.read_csv(afolder + r'\so2_val_airpollute.csv')
        
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
        df1 = pd.read_csv(afolder + r'\co_val_airpollute.csv')
        df2 = pd.read_csv(afolder + r'\no2_val_airpollute.csv')
        df3 = pd.read_csv(afolder + r'\o3_val_airpollute.csv')
        df4 = pd.read_csv(afolder + r'\pm2_5_val_airpollute.csv')
        df5 = pd.read_csv(afolder + r'\pm10_val_airpollute.csv')
        df6 = pd.read_csv(afolder + r'\so2_val_airpollute.csv')
        
        
        def cleanair(df, pollutant):
            df1 = df[['landcover','tons_change_trt_bau','tons_change_trt_med','tons_change_trt_max']]
            df1 = df1.rename(columns = {'landcover':'Landcover','tons_change_trt_bau': 'Reference Scenario','tons_change_trt_med':'Medium Infill Scenario','tons_change_trt_max':'Max Infill Scenario'})
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
    
    def scenic2014():
        df = pd.read_csv(afolder + r'\scenic.csv')
        df = df[['gen_class','ha_2014']]
        df = df.loc[df['ha_2014'] > 0]
        df = df.rename(columns = {'gen_class': 'General Landcover', 'ha_2014':'Hectares'})
        df.to_csv(outfolder+'2014 Scenic Value.csv', index = False)
    
    def scenic2030():
        df = pd.read_csv(afolder + r'\scenic.csv')
        df = df[['gen_class','ha_change_trt_bau', 'ha_change_trt_med', 'ha_change_trt_max' ]]
        df = df.rename(columns = {'gen_class': 'General Landcover', 'ha_change_trt_bau':'Reference Scenario', 'ha_change_trt_med':'Medium Infill Scenario', 'ha_change_trt_max':'Max Infill Scenario'})
        
        #Remove any rows with all 0s
        df.set_index(['General Landcover'], inplace = True)
        df = df[df.values.sum(axis=1) != 0]
        df.reset_index(inplace = True)

        
        df.to_csv(outfolder+'2030 Scenic Value.csv', index = False)
    
    
    def move2014():
        df = pd.read_csv(afolder + r'\countymovement.csv')
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
    
    def move2030():
        df2 = pd.read_csv(afolder + r'\countymovement.csv')
        df = pd.read_csv(afolder + r'\countymovement.csv')
        df2 = df2[['resistance_class','ha_change_trt_bau']]
        df2 = df2.rename(columns = {'resistance_class': 'Resistance to Movement','ha_change_trt_bau':'Reference Scenario'})
        df = df[['resistance_class','ha_change_trt_med','ha_change_trt_max']]
        df = df.rename(columns = {'resistance_class': 'Resistance to Movement', 'ha_change_trt_med':'Medium Infill Scenario', 'ha_change_trt_max':'Max Infill Scenario'})
        
        
        temp = pd.merge(df2, df, on = 'Resistance to Movement', how = 'left')
        
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
        df.to_csv(outfolder+'2030 Terrestrial Connectivity.csv', index = False)
    
    def move2014_eca():
        df = pd.read_csv(afolder + r'\ecamovement.csv')
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
    
    def move2030_eca():
        df2 = pd.read_csv(afolder + r'\ecamovement.csv')
        df = pd.read_csv(afolder + r'\ecamovement.csv')
        df2 = df2[['resistance_class','ha_change_trt_bau']]
        df2 = df2.rename(columns = {'resistance_class': 'Resistance to Movement','ha_change_trt_bau':'Reference Scenario'})
        df = df[['resistance_class','ha_change_trt_med','ha_change_trt_max']]
        df = df.rename(columns = {'resistance_class': 'Resistance to Movement', 'ha_change_trt_med':'Medium Infill Scenario', 'ha_change_trt_max':'Max Infill Scenario'})
        
        
        temp = pd.merge(df2, df, on = 'Resistance to Movement', how = 'left')
        
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
        df.to_csv(outfolder+'2030 ECA Terrestrial Connectivity.csv', index = False)

    
    def lcc2014():
        df = pd.read_csv(afolder + r'\lcchange.csv')
        df = df[['landcover','ha_2014']]
        df = df.loc[df['ha_2014'] > 0]
        df = df.rename(columns = {'landcover': 'Landcover', 'ha_2014':'Hectares'})
        df.to_csv(outfolder+'2014 Natural Habitat Area.csv', index = False)
    
    def lcc2030():
        df2 = pd.read_csv(afolder + r'\lcchange.csv')
        df = pd.read_csv(afolder + r'\lcchange.csv')
        df2 = df2[['landcover','ha_change_trt_bau']]
        df2 = df2.rename(columns = {'landcover': 'Landcover','ha_change_trt_bau':'Reference Scenario'})
        df = df[['landcover','ha_change_trt_med','ha_change_trt_max']]
        df = df.rename(columns = {'landcover': 'Landcover', 'ha_change_trt_med':'Medium Infill Scenario', 'ha_change_trt_max':'Max Infill Scenario'})
        
        
        temp = pd.merge(df2, df, on = 'Landcover', how = 'left')

        temp.to_csv(outfolder+'2030 Natural Habitat Area.csv', index = False)
          
        
        
    def pcalcc2014():
        df = pd.read_csv(afolder + r'\pca_cover_change.csv')
        df = df[['landcover','ha_2014']]
        df = df.loc[df['ha_2014'] > 0]
        df = df.rename(columns = {'landcover': 'Landcover', 'ha_2014':'Hectares'})
        df.to_csv(outfolder+'2014 Priority Conservation Areas.csv', index = False)
    
    def pcalcc2030():
        df2 = pd.read_csv(afolder + r'\pca_cover_change.csv')
        df = pd.read_csv(afolder + r'\pca_cover_change.csv')
        df2 = df2[['landcover','ha_change_trt_bau']]
        df2 = df2.rename(columns = {'landcover': 'Landcover','ha_change_trt_bau':'Reference Scenario'})
        df = df[['landcover','ha_change_trt_med','ha_change_trt_max']]
        df = df.rename(columns = {'landcover': 'Landcover', 'ha_change_trt_med':'Medium Infill Scenario', 'ha_change_trt_max':'Max Infill Scenario'})
        
        
        temp = pd.merge(df2, df, on = 'Landcover', how = 'left')
        
        temp.to_csv(outfolder+'2030 Priority Conservation Areas.csv', index = False)
          
        
    def terrhab2030():
        if os.path.exists(afolder + '/terrhab.csv'):
            df2 = pd.read_csv(afolder + r'\terrhab.csv')
            df = pd.read_csv(afolder + r'\terrhab.csv')
            df2 = df2[['guild','ha_trt_bau']]
            df2 = df2.rename(columns = {'guild': 'Guild','ha_trt_bau':'Reference Scenario'})
            df = df[['guild','ha_trt_med','ha_trt_max']]
            df = df.rename(columns = {'guild': 'Guild', 'ha_trt_med':'Medium Infill Scenario', 'ha_trt_max':'Max Infill Scenario'})
            
            
            temp = pd.merge(df2, df, on = 'Guild', how = 'left')
            
            
            temp.loc[temp['Guild'] == 'mammals_avg_deg_ha', 'Guild'] = 'Mammal Degraded'
            temp.loc[temp['Guild'] == 'mammals_avg_imp_ha', 'Guild'] = 'Mammal Improved'
            temp.loc[temp['Guild'] == 'birds_avg_deg_ha', 'Guild'] = 'Bird Degraded'
            temp.loc[temp['Guild'] == 'birds_avg_imp_ha', 'Guild'] = 'Bird Improves'
            temp.loc[temp['Guild'] == 'amphibians_avg_deg_ha', 'Guild'] = 'Amphibian Degraded'
            temp.loc[temp['Guild'] == 'amphibians_avg_imp_ha', 'Guild'] = 'Amphibian Improved'
            temp.loc[temp['Guild'] == 'tes_avg_deg_ha', 'Guild'] = 'Threatened and Endangered Degraded'
            temp.loc[temp['Guild'] == 'tes_avg_imp_ha', 'Guild'] = 'Treatened and Endangered Improved'
        
            
            temp.to_csv(outfolder+'2030 Terrestrial Habitat Value.csv', index = False)    
        
    def aqua2014():
        df = pd.read_csv(afolder + r'\aquatic.csv')
        df = df[['gen_class','ha_2014']]
        df = df.loc[df['ha_2014'] > 0]
        df = df.rename(columns = {'gen_class': 'Landcover', 'ha_2014':'Hectares'})
        df.to_csv(outfolder+'2014 Aquatic Biodiversity.csv', index = False)    
        
        
    def aqua2030():
        df2 = pd.read_csv(afolder + r'\aquatic.csv')
        df = pd.read_csv(afolder + r'\aquatic.csv')
        df2 = df2[['gen_class','ha_change_trt_bau']]
        df2 = df2.rename(columns = {'gen_class': 'Landcover','ha_change_trt_bau':'Reference Scenario'})
        df = df[['gen_class','ha_change_trt_med','ha_change_trt_max']]
        df = df.rename(columns = {'gen_class': 'Landcover', 'ha_change_trt_med':'Medium Infill Scenario', 'ha_change_trt_max':'Max Infill Scenario'})
        
        
        temp = pd.merge(df2, df, on = 'Landcover', how = 'left')
    
        
        temp.to_csv(outfolder+'2030 Aquatic Biodiversity.csv', index = False)   
    
    
    def eco_resi():
        df = pd.read_csv(afolder + r'\aquatic.csv')
        df = df[['gen_class','ha_change_trt_bau','ha_change_trt_med','ha_change_trt_max']]
        df = df.rename(columns = {'gen_class': 'Landcover', 'ha_change_trt_bau':'Reference Scenario', 'ha_change_trt_med':'Medium Infill Scenario','ha_change_trt_max':'Max Infill Scenario'})
        temp = df
        temp.set_index(['Landcover'], inplace = True)
        temp = temp[temp.values.sum(axis=1) != 0]
        temp.reset_index(inplace = True)
        
        temp.to_csv(outfolder+'2030 ecoresilience_table.csv', index = False)   
    def soc_resi():
        df = pd.read_csv(afolder + r'\aquatic.csv')
        df = df[['gen_class','ha_change_trt_bau','ha_change_trt_med','ha_change_trt_max']]
        df = df.rename(columns = {'gen_class': 'Landcover', 'ha_change_trt_bau':'Reference Scenario', 'ha_change_trt_med':'Medium Infill Scenario','ha_change_trt_max':'Max Infill Scenario'})
        temp = df
        temp.set_index(['Landcover'], inplace = True)
        temp = temp[temp.values.sum(axis=1) != 0]
        temp.reset_index(inplace = True)
        
        temp.to_csv(outfolder+'2030 socresilience_table.csv', index = False)   
           
        
    def soc_resi14():
        df = pd.read_csv(afolder + r'\aquatic.csv')
        df = df[['gen_class','ha_2014']]
        df = df.loc[df['ha_2014'] > 0]
        df = df.rename(columns = {'gen_class': 'Landcover', 'ha_2014':'Hectares'})
        df.to_csv(outfolder+'2014 Social Resilience.csv', index = False)        
        
    def eco_resi14():
        df = pd.read_csv(afolder + r'\aquatic.csv')
        df = df[['gen_class','ha_2014']]
        df = df.loc[df['ha_2014'] > 0]
        df = df.rename(columns = {'gen_class': 'Landcover', 'ha_2014':'Hectares'})
        df.to_csv(outfolder+'2014 Ecological Resilience.csv', index = False)        

    
    fmmp2014()
    fmmp2030()
    crop2014()
    crop2030()
    watcon2030()
    watcon2014()
    watint2014()
    watint2030()
    groundwater2030()
    nitrun2014()
    nitleach2014()
    nitrun2030()
    nitleach2030()
    flood2014()
    flood2030()
    air2014()
    air2030()
    scenic2014()
    scenic2030()
    move2014()
    move2030()
    move2014_eca()
    move2030_eca()
    lcc2014()
    lcc2030()
    pcalcc2014()
    pcalcc2030()
    terrhab2030()
    aqua2014()
    aqua2030()
    eco_resi()
    soc_resi()
    eco_resi14()
    soc_resi14()




def mba_threetrace(table, title = 'Nothing' , xax = 'holder', yax = 'holder', ytitle = 'None', x1 = 'None',  x2 = 'None', x3 = 'None',x4 = '', outfile = 'temp',y1 = 'none',y2 = 'none',y3 = 'none', xtit = '', x_font = 12):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    table = table.loc[:, ~table.columns.str.contains('^Unnamed')]

        

    trace1 = {
      "x": table[x1], 
      "y": table[x2], 
      "type":"bar",
      "name":y1
    }
    
    trace2 = {
      "x": table[x1], 
      "y": table[x3],  
      "type":"bar",
       "name":y2
    }
    trace3 = {
      "x": table[x1], 
      "y": table[x4], 
"type":"bar",
 "name":y3
    }


    data = go.Data([trace1, trace2, trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": title, 
      "titlefont": {
      "size": mba_title_font
          },
      "xaxis": {
        "autorange": True, 
        "type": "category",
        "title": xtit,
        "tickfont": {
      "size": x_font
          }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,1], 
        "title": ytitle, 
        "type": "linear",
        "titlefont": {
                "size": axis_lab_font
          }
      },
#        "annotations": [plot_dict[mba]['ann']
#      
#    ]
    }
   
    fig = go.Figure(data=data, layout=layout)
#    plot(fig, filename= plot_dict[mba]['title'] + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig

def mba_twotrace(table, title = 'Nothing' , xax = 'holder', yax = 'holder',  ytitle = 'None', x1 = 'None',  x2 = 'None', x3 = 'None', outfile = 'temp',y1 = 'none',y2 = 'none', xtit = '', a_font = 9):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    table = table.loc[:, ~table.columns.str.contains('^Unnamed')]

        

    trace1 = {
      "x": table[x1], 
      "y": table[x2], 
      "type":"bar",
      "name":y1
    }
    
    trace2 = {
      "x": table[x1], 
      "y": table[x3],  
      "type":"bar",
       "name":y2
    }


    data = go.Data([trace1, trace2])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": title, 
      "titlefont": {
      "size": mba_title_font
          },
      "xaxis": {
        "autorange": True, 
        "type": "category",
        "title": xtit,
        "tickfont": {
      "size": a_font
          }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,1], 
        "title": ytitle, 
        "type": "linear",
        "titlefont": {
                "size": axis_lab_font
          }
      },
#        "annotations": [plot_dict[mba]['ann']
#      
#    ]
    }
   
    fig = go.Figure(data=data, layout=layout)
#    plot(fig, filename= plot_dict[mba]['title'] + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig

def mba_chart_onetrace(table, xax = 'holder', yax = 'holder', x = 'None',y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, qu2 = 'None', outfile = 'temp', xtit = '', xfont = 12):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
    if qu != 'None':
        table = table.loc[table[qu] != qu2]
    if remzeros == 1:
        table.set_index(x, inplace = True)
        table = table[table.values.sum(axis=1) != 0]
        table.reset_index(inplace = True)       

    trace1 = {
      "x": table[x], 
      "y": table[y], 
      "type":"bar"
    }

    data = go.Data([trace1])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": False, 
      "title": xax, 
      "titlefont": {
      "size": mba_title_font
          },
      "xaxis": {
        "autorange": True, 
        "type": "category",
        "title": xtit,
        "tickfont": {
      "size": xfont
          }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": yrange, 
        "title": yax, 
        "type": "linear",
        "titlefont": {
                "size": axis_lab_font
          }
      }
    }
   
    fig = go.Figure(data=data, layout=layout)
#    plot(fig, filename= plot_dict[mba]['title'] + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig
    
    

def make_plots(afolder):
    tables = afolder + 'plot_tables'
    outpath = afolder + 'plots/'

    mba_chart_onetrace(tables + "/2014 Ag Land Quality.csv", xax = '2014 Farmland', yax = 'Hectares', x = 'Farmland Class',y = 'Hectares', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Farmland.png")
    
    mba_threetrace(tables + "/2030 Ag Land Quality.csv", '2014-2030 Farmland Loss', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Farmland Class', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Farmland Loss.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario')
    
    mba_chart_onetrace(tables + "/2014 Crop Value.csv", xax = '2014 Crop Value', yax = 'US Dollars', x = 'Crop Type',y = 'US Dollars', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Crop Value.png")
    
    mba_threetrace(tables + "/2030 Crop Value.csv", '2014-2030 Crop Value', xax = 'holder', yax = 'holder',   ytitle = 'US Dollars', x1 = 'Crop Type', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Crop Value.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario')

    mba_chart_onetrace(tables + "/2014 Ag and Urban Water Conservation.csv", xax = '2014 Water Demand', yax = 'Acre Ft/Year', x = 'Landcover',y = 'Acre Feet Annual Water Demand', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Ag and Urban Water Conservation.png")
    
    mba_threetrace(tables + "/2030 Ag and Urban Water Conservation.csv", '2014-2030 Water Demand', xax = 'holder', yax = 'holder',   ytitle = 'Acre Ft/Year', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Ag and Urban Water Conservation.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario')
    
    
    mba_chart_onetrace(tables + "/2030 Groundwater Recharge.csv", xax = '2030 Groundwater Recharge Loss', yax = 'Acre Ft/Year', x = 'Development Scenario',y = 'Acre Feet of Annual Groundwater Recharge Lost', yrange = [0,1], remzeros= 1, outfile = outpath + "2030 Groundwater Recharge.png")
    
    mba_chart_onetrace(tables + "/2014 Watershed Integrity.csv", xax = '2014 Watershed Integrity', yax = 'Hectares', x = 'Watershed Class',y = 'Hectares', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Watershed Integrity.png")
    
    mba_threetrace(tables + "/2030 Watershed Integrity.csv", '2014-2030 Change in Watershed Integrity', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Watershed Class', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Watershed Integrity Riparian.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario')
    
    mba_chart_onetrace(tables + "/2030 Water Quality - Nitrate Runoff.csv", xax = '2014-2030 Change in Nitrate Runoff', yax = 'Tons', x = 'Scenario',y = 'Change in Annual Tons of Nitrate Runoff', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Nitrate Runoff.png")
    
    mba_chart_onetrace(tables + "/2014 Water Quality - Nitrate Runoff.csv", xax = '2014 Nitrate Runoff', yax = 'Tons', x = 'Landcover',y = 'Annual Tons of Nitrate Runoff', yrange = [0,1], remzeros= 1, outfile = outpath + "2030 Nitrate Runoff.png")
    
    
    mba_chart_onetrace(tables + "/2014 Water Quality - Nitrate Leaching.csv", xax = '2014 Nitrate Leaching', yax = 'Tons', x = 'Landcover',y = 'Annual Tons of Nitrate Leaching', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Nitrate Leaching.png")
    
    mba_chart_onetrace(tables + "/2030 Water Quality - Nitrate Leaching.csv", xax = '2014-2030 Change in Nitrate Leaching', yax = 'Tons', x = 'Scenario',y = 'Change in Annual Tons of Nitrate Leaching', yrange = [0,1], remzeros= 1, outfile = outpath + "2030 Nitrate Leaching.png")

    mba_chart_onetrace(tables + "/2014 Flood Risk Reduction.csv", xax = '2014 Landcover in 100 Year Floodplain', yax = 'Hectares', x = 'General Landcover',y = 'Hectares', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Flood Risk Reduction.png")

    mba_threetrace(tables + "/2030 Flood Risk Reduction.csv", '2014-2030 Change in Landcover in 100 Year Floodplain', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'General Landcover', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Flood Risk Reduction.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario')
    
    
    mba_chart_onetrace(tables + "/2014 Air Quality.csv", xax = '2014 Air Pollutant Sequestration', yax = 'Tons of Pollutant Sequestered Annually', x = 'Air Pollutant',y = 'Tons of Pollutant Sequestered Annually', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Air Quality.png")
    
    mba_threetrace(tables + "/2030 Air Quality Change.csv", '2014-2030 Change in Air Pollutant Sequestration', xax = 'holder', yax = 'holder',   ytitle = 'Tons of Pollutant Sequestered', x1 = 'Air Pollutant', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Air Quality.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario', x_font = 10)
    
    
    mba_chart_onetrace(tables + "/2014 Scenic Value.csv", xax = '2014 Landcover in Highly Visible Areas', yax = 'Hectares', x = 'General Landcover',y = 'Hectares', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Scenic Value.png")

    mba_threetrace(tables + "/2030 Flood Risk Reduction.csv", '2014-2030 Change in Landcover in Highly Visible Areas', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'General Landcover', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Scenic Value.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario')
    
    mba_chart_onetrace(tables + "/2014 Terrestrial Connectivity.csv", xax = '2014 Resistance to Species Movement', yax = 'Hectares', x = 'Resistance to Movement',y = 'Hectares', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Terrestrial Connectivity.png")
    mba_chart_onetrace(tables + "/2014 ECA Terrestrial Connectivity.csv", xax = '2014 Resistance to Species Movement in Essential Connectivity Areas', yax = 'Hectares', x = 'Resistance to Movement',y = 'Hectares', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Terrestrial Connectivity ECA.png")
    

    mba_threetrace(tables + "/2030 ECA Terrestrial Connectivity.csv", '2014-2030 Change in Resistance to Species Movement<br>in Essential Connectivity Areas', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Resistance to Movement', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 ECA Terrestrial Connectivity.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario', xtit = 'Resistance to Movement')

    mba_threetrace(tables + "/2030 Terrestrial Connectivity.csv", '2014-2030 Change in Resistance to <br>Species Movement', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Resistance to Movement', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Terrestrial Connectivity.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario', xtit = 'Resistance to Movement')
    
    mba_chart_onetrace(tables + "/2014 Natural Habitat Area.csv", xax = '2014 Landcover', yax = 'Hectares', x = 'Landcover',y = 'Hectares', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Natural Habitat Area.png")
    mba_chart_onetrace(tables + "/2014 Priority Conservation Areas.csv", xax = '2014 Landcover in Priority Conservation Areas', yax = 'Hectares', x = 'Landcover',y = 'Hectares', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Priority Conservation Areas.png")
    
    mba_threetrace(tables + "/2030 Priority Conservation Areas.csv", '2014-2030 Change in Landcover in Priority Conservation Areas', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Priority Conservation Areas.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario')

    mba_threetrace(tables + "/2030 Natural Habitat Area.csv", '2014-2030 Change in Landcover for Conversion Scenario', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Natural Habitat Area.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario')

    mba_threetrace(tables + "/2030 Terrestrial Habitat Value.csv", '2014-2030 Change in Terrestrial Habitat Value', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Guild', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Terrestrial Habitat Value.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario')
    
    
    
    mba_chart_onetrace(tables + "/2014 Aquatic Biodiversity.csv", xax = '2014 Landcover in Watersheds with <br>Important Aquatic Habitat', yax = 'Hectares', x = 'Landcover',y = 'Hectares', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Aquatic Biodiversity.png")
    
    mba_threetrace(tables + "/2030 Aquatic Biodiversity.csv", '2014-2030 Landcover Change in Watersheds with <br>Important Aquatic Habitat', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Aquatic Biodiversity.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario')


    


    mba_threetrace(tables + "/2030 socresilience_table.csv", '2014-2030 Landcover Change in Areas Important <br>For Social Resilience', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Social Resilience.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario')


    mba_chart_onetrace(tables + "/2014 Social Resilience.csv", xax = '2014 Landcover in Areas Important <br>For Social Resilience', yax = 'Hectares', x = 'Landcover',y = 'Hectares', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Social Resilience.png")
    
    mba_chart_onetrace(tables + "/2014 Ecological Resilience.csv", xax = '2014 Landcover in Areas Important <br>For Natural Resilience', yax = 'Hectares', x = 'Landcover',y = 'Hectares', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Natural Resilience.png")


    mba_threetrace(tables + "/2030 ecoresilience_table.csv", '2014-2030 Landcover Change in Areas Important <br>For Social Resilience', xax = 'holder', yax = 'holder', ytitle = 'Hectares', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Medium Infill Scenario',x4 = 'Max Infill Scenario',outfile = outpath + "2030 Social Resilience.png", y1 = 'Reference Scenario', y2 = 'Medium Infill Scenario',y3 = 'Max Infill Scenario')



#simp(runfolder)
#make_plots(runfolder)





def  reductions_ALL(outfile):
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    folder = r"E:\Box\Box Sync\Merced Project\Tool\outputs\activities"
    table = 'carbon'
    
    
    
    cam25 = pd.read_csv(folder + '/compost_amendment_25/' + table + '.csv')
    cam100 = pd.read_csv(folder + '/compost_amendment_100/' + table + '.csv')
    ccr25 = pd.read_csv(folder + '/cover_cropping_25/' + table + '.csv')
    ccr100 = pd.read_csv(folder + '/cover_cropping_100/' + table + '.csv')
    cag25 = pd.read_csv(folder + '/grass_compost_amendment_25/' + table + '.csv')
    cag100 = pd.read_csv(folder + '/grass_compost_amendment_100/' + table + '.csv')
    gra25 = pd.read_csv(folder + '/grassland_resto_25/' + table + '.csv')
    gra100 = pd.read_csv(folder + '/grassland_resto_100/' + table + '.csv')
    hpl25 = pd.read_csv(folder + '/hedgerow_25/' + table + '.csv')
    hpl100 = pd.read_csv(folder + '/hedgerow_100/' + table + '.csv')
    mul25 = pd.read_csv(folder + '/mulching_25/' + table + '.csv')
    mul100 = pd.read_csv(folder + '/mulching_100/' + table + '.csv')
    nfm25 = pd.read_csv(folder + '/nfm_25/' + table + '.csv')
    nfm100 = pd.read_csv(folder + '/nfm_100/' + table + '.csv')
    rre25 = pd.read_csv(folder + '/RRE_COUNTY_25/' + table + '.csv')
    rre100 = pd.read_csv(folder + '/RRE_COUNTY_100/' + table + '.csv')

 
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    trace1 = {
      #"x": ["Riparian Restoration", 'Improved N Fertilizer Mngmt',"Compost Amendments to Croplands", 'Compost Amendments to Grasslands', #'Cover Cropping', 'Mulching', 'Hedgerow Planting', 'Oak Woodland Restoration', 'Urban Tree Planting']
      "x": [ 'Improved N<br> Fertilizer<br> Mngmt',"Compost<br>on<br>Croplands", 'Compost<br> on<br> Grasslands', 'Mulching','Cover<br>Cropping',  "Riparian<br>Restoration",  'Urban<br>Tree<br>Planting','Hedgerow<br>Planting', 'Oak<br> Woodland<br>Restoration'], 
      "y": [nfm25['carbon_nfm'].sum(), cam25['carbon_cam'].sum(), cag25['carbon_cag'].sum(), mul25['carbon_mul'].sum(), ccr25['carbon_ccr'].sum(), rre25['carbon_rre'].sum(),  urb25['carbon_urb'].sum(),  hpl25['carbon_hpl'].sum(), oak25['carbon_oak'].sum()],
      "type": "bar",
      "name":'25% Adoption'
      }
    trace2 = {
      "x": [ 'Improved N<br> Fertilizer<br> Mngmt',"Compost<br>on<br>Croplands", 'Compost<br> on<br> Grasslands', 'Mulching','Cover<br>Cropping',  "Riparian<br>Restoration",  'Urban<br>Tree<br>Planting','Hedgerow<br>Planting', 'Oak<br> Woodland<br>Restoration'], 
      "y": [nfm100['carbon_nfm'].sum(), cam100['carbon_cam'].sum(), cag100['carbon_cag'].sum(), mul100['carbon_mul'].sum(), ccr100['carbon_ccr'].sum(),  rre100['carbon_rre'].sum(),  urb100['carbon_urb'].sum(), hpl100['carbon_hpl'].sum(), oak100['carbon_oak'].sum()],
      "type": "bar",
      "name":'Full Adoption'
      }

    print (str(rre25['carbon_rre'].sum()))
    data = go.Data([trace1, trace2])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": "2014-2030 GHG Reductions from Countywide Activities", 
      "titlefont": {
      "size": titlefont
          },
      "xaxis": {
        "autorange": True, 
        "title": ['25% Adoption','Full Adoption'], 
        "type": "category",
        "tickangle":0,
        "tickfont":{
            "size":10,
            "color":'black'
        },
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0, 200000], 
        "type": 'linear',
        #"range": [min_y_range(table), max_y_range(table)], 
        "title": 'Tons CO<sub>2</sub> Equivalents', 
      "titlefont": {
      "size": 16
          },
        "tickfont":{
            "color":'black'
        }
      },

      }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'all_reductions' + '.html')
    py.image.save_as(fig, outfile, format='png')


def make_countywide_reductions_all_activities():
    import os
    import plotly.plotly as py

    py.sign_in('mtukman', 'FbUYCv4tcjCPF2ZdfzKo')

    boxpath = 'E:/Box/'
    reductions_ALL(os.path.join(boxpath, r'Box Sync/Merced Project/Report_How-To Guide/Tukman Working Material/Countywide GHG Reductions All Activities.png'))
    














































