def Plots(folder, aclist, actlist, thabflag,cproc, apikey, username, units = 'Acres'):
    """
    This function takes the reports from the Reporting module and creates siplified tables and plots using the Plotly website.
    
    folder - Folder that the tool outputs went into.
    aclist - List of activities chosen for the run of the tool
    actlist - List of avoided conversion activities chosen for the run of the tool
    thabflag - Flag for whether terrestrial habitat reporting was checked or not.
    cproc - flag for whether a custom processing mask was used in the run of the tool
    apikey - API Key from Plotly
    username - Username from Plotly
        
    """
    runfolder = folder
    mba_title_font = 20
    axis_lab_font = 16
import plotly.plotly as py
import Helpers
    py.sign_in(username, apikey)
    
    #This dictionary contains acronym to actual activity description lookups
    ludict = {'ac_wet_arc':'AC Wet. to Ann. Crop','ac_gra_arc':'AC Grass. to <br> Ann. Crop','ac_irr_arc':'AC Irr. Pas. to Ann. Crop','ac_orc_arc': 'AC Orc. to Ann. Crop','ac_arc_urb':'AC Ann. Crop to Urban','ac_gra_urb':'AC Grass. to Urban','ac_irr_urb':'AC Irr. Pas. <br> to Urban','ac_orc_urb':'AC Orc. to Urban','ac_arc_orc':'AC Ann. Crop to Orc.','ac_gra_orc':'AC Grass. to Orc.','ac_irr_orc':'AC Irr. Pas. to Orc.','ac_vin_orc':'AC Vin. to Orc.','ac_arc_irr':'AC Ann. Crop to Irr. Pas.','ac_orc_irr':'AC Or. to Irr. Pas.','rre':'Riparian Restoration','oak':'Oak Woodland<br>Restoration','ccr':'Cover Crops','mul':'Mulching','nfm':'Improved Nitrogen<br>Fertilizer Management','hpl':'Hedgerow Planting','urb':'Urban Tree<br>Planting','gra':'Native Grass<br>Restoration','cam':'Replacing Synthetic<br>Nitrogen Fertilizer<br>with Soil Amendments','cag':'Compost Application<br>to Non-irrigated<br> Grasslands'}
    if units == 'Acres':
        ubrv = 'ac'
    if units == 'Hectares':
        ubrv= 'ha'
    def simp(afolder = ''):
    
        import os
        import pandas as pd
        import functools
        
        #Create the folders if they do not exist
        if not os.path.exists(afolder + 'plot_tables'):
            os.makedirs(afolder + 'plot_tables')
        if not os.path.exists(afolder + 'plots'):
            os.makedirs(afolder + 'plots')
        outfolder =     afolder + 'plot_tables/'
        import os.path

        if os.path.exists(afolder + "/act_acres.csv"):
            df = pd.read_csv(afolder + 'act_acres.csv')
            test = df.transpose()
            test.reset_index(inplace = True)
            test.rename(columns = {'index': 'Activity',0:units}, inplace = True)
            test.to_csv(outfolder + 'act_acres.csv')
        
        
        #Create the function that create the simplified tables

        def fmmp2014():
            df = pd.read_csv(afolder + 'fmmp.csv')
            df = df[['fmmp_class',ubrv + '_2014']]
            df = df.loc[df[ubrv + '_2014'] > 0]
            df = df.rename(columns = {'fmmp_class': 'Farmland Class', ubrv + '_2014':units})
            df.to_csv(outfolder+'2014 Ag Land Quality.csv', index = False)
    
        def crop2014():
            df = pd.read_csv(afolder + 'cropvalue.csv')
            df = df[['landcover','cropvalue_usd_2014']]
            df = df.rename(columns = {'landcover': 'Crop Type', 'cropvalue_usd_2014':'US Dollars'})
            df.to_csv(outfolder+'2014 Crop Value.csv', index = False)
    
        def watcon2014():
            df = pd.read_csv(afolder + 'watcon.csv')
            df = df[['landcover','ac_ft_2014']]
            df = df.loc[df['ac_ft_2014'] > 0]
            df = df.rename(columns = {'landcover': 'Landcover', 'ac_ft_2014':'Acre Feet Annual Water Demand'})
            df.to_csv(outfolder+'2014 Ag and Urban Water Conservation.csv', index = False)

        def watint2014():
            df = pd.read_csv(afolder + 'watint.csv')
            df = df[['Integrity_Class',ubrv + '_2014']]
            df = df.rename(columns = {'Integrity_Class': 'Watershed Class', ubrv + '_2014':units})
            df = df.loc[df['Watershed Class'] != 'na']
            
            df.to_csv(outfolder+'2014 Watershed Integrity.csv', index = False)
    
        def nitrun2014():
            df = pd.read_csv(afolder + 'runoff_nitrates.csv')
            df = df[['landcover','tons_no3_14']]
            df = df.loc[df['tons_no3_14'] > 0]
            df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_14':'Annual Tons of Nitrate Runoff'})
            df.to_csv(outfolder+'2014 Water Quality - Nitrate Runoff.csv', index = False)
        
        def nitleach2014():
            df = pd.read_csv(afolder + 'leach_nitrates.csv')
            df = df[['landcover','tons_no3_14']]
            df = df.loc[df['tons_no3_14'] > 0]
            df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_14':'Annual Tons of Nitrate Leaching'})
            df.to_csv(outfolder+'2014 Water Quality - Nitrate Leaching.csv', index = False)
    
        def flood2014():
            df = pd.read_csv(afolder + 'flood100.csv')
            df = df[['gen_class',ubrv + '_2014']]
            df = df.loc[df[ubrv + '_2014'] > 0]
            df = df.rename(columns = {'gen_class': 'General Landcover', ubrv + '_2014':units})
            df.to_csv(outfolder+'2014 Flood Risk Reduction.csv', index = False)
    
        def air2014():
            import functools as fc
            df1 = pd.read_csv(afolder + 'co_val_airpollute.csv')
            df2 = pd.read_csv(afolder + 'no2_val_airpollute.csv')
            df3 = pd.read_csv(afolder + 'o3_val_airpollute.csv')
            df4 = pd.read_csv(afolder + 'pm2_5_val_airpollute.csv')
            df5 = pd.read_csv(afolder + 'pm10_val_airpollute.csv')
            df6 = pd.read_csv(afolder + 'so2_val_airpollute.csv')
            
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
    
        def scenic2014():
            df = pd.read_csv(afolder + 'scenic.csv')
            df = df[['gen_class',ubrv + '_2014']]
#            df = df.loc[df[ubrv + '_2014'] > 0]
            df = df.rename(columns = {'gen_class': 'General Landcover', ubrv + '_2014':units})
            df.to_csv(outfolder+'2014 Scenic Value.csv', index = False)
    
        def move2014():
            df = pd.read_csv(afolder + 'countymovement.csv')
            df = df[['resistance_class',ubrv + '_2014']]
#            df = df.loc[df[ubrv + '_2014'] > 0]
            df = df.rename(columns = {'resistance_class': 'Resistance to Movement', ubrv + '_2014':units})
            
            
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
    
        def move2014_eca():
            df = pd.read_csv(afolder + 'ecamovement.csv')
            df = df[['resistance_class',ubrv + '_2014']]
#            df = df.loc[df[ubrv + '_2014'] > 0]
            df = df.rename(columns = {'resistance_class': 'Resistance to Movement', ubrv + '_2014':units})
            
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
    
        def lcc2014():
            df = pd.read_csv(afolder + 'lcchange.csv')
            df = df[['landcover',ubrv + '_2014']]
            df = df.loc[df[ubrv + '_2014'] > 0]
            df = df.rename(columns = {'landcover': 'Landcover', ubrv + '_2014':units})
            df.to_csv(outfolder+'2014 Natural Habitat Area.csv', index = False)
    
        def pcalcc2014():
            df = pd.read_csv(afolder + 'pca_cover_change.csv')
            df = df[['landcover',ubrv + '_2014']]
            df = df.loc[df[ubrv + '_2014'] > 0]
            df = df.rename(columns = {'landcover': 'Landcover', ubrv + '_2014':units})
            df.to_csv(outfolder+'2014 Priority Conservation Areas.csv', index = False)
    
        def aqua2014():
            df = pd.read_csv(afolder + 'aquatic.csv')
            df = df[['gen_class',ubrv + '_2014']]
            df = df.loc[df[ubrv + '_2014'] > 0]
            df = df.rename(columns = {'gen_class': 'Landcover', ubrv + '_2014':units})
            df.to_csv(outfolder+'2014 Aquatic Biodiversity.csv', index = False)     
    
        def soc_resi14():
            df = pd.read_csv(afolder + 'aquatic.csv')
            df = df[['gen_class',ubrv + '_2014']]
            df = df.loc[df[ubrv + '_2014'] > 0]
            df = df.rename(columns = {'gen_class': 'Landcover', ubrv + '_2014':units})
            df.to_csv(outfolder+'2014 Social Resilience.csv', index = False)        
        def eco_resi14():
            df = pd.read_csv(afolder + 'aquatic.csv')
            df = df[['gen_class',ubrv + '_2014']]
            df = df.loc[df[ubrv + '_2014'] > 0]
            df = df.rename(columns = {'gen_class': 'Landcover', ubrv + '_2014':units})
            df.to_csv(outfolder+'2014 Natural Resilience.csv', index = False)        
    
        #Create the 2014 simplified tables
        fmmp2014()
        crop2014()
        watcon2014()
        if cproc == 0:
            watint2014()
        nitrun2014()
        nitleach2014()
        flood2014()
        air2014()
        scenic2014()
        move2014()
        move2014_eca()
        lcc2014()
        pcalcc2014()
        aqua2014()
        eco_resi14()
        soc_resi14()
        
        
        def fmmp2030():
            df = pd.read_csv(afolder + 'fmmp.csv')
            df = df[['fmmp_class',ubrv + '_loss_base_bau', ubrv + '_loss_trt_bau' ]]
            df = df.rename(columns = {'fmmp_class': 'Farmland Class', ubrv + '_loss_base_bau':'Reference Scenario', ubrv + '_loss_trt_bau':'Treatment Scenario'})
            df.set_index(['Farmland Class'], inplace = True)
            df = df[df.values.sum(axis=1) != 0]
            df.reset_index(inplace = True)
            
            df.to_csv(outfolder+'2030 Ag Land Quality.csv', index = False)
            
    
        
        def crop2030():
            df = pd.read_csv(afolder + 'cropvalue.csv')
            df = df[['landcover','usd_change_base_bau', 'usd_change_trt_bau']]
            df = df.rename(columns = {'landcover': 'Crop Type', 'usd_change_base_bau':'Reference Scenario', 'usd_change_trt_bau':'Treatment Scenario'})
            df.set_index(['Crop Type'], inplace = True)
            df = df[df.values.sum(axis=1) != 0]
            df.reset_index(inplace = True)
            df['Crop Type'] = 'Crop Value'
            df = df.groupby(['Crop Type'], as_index = False).sum()
            
            df.to_csv(outfolder+'2030 Crop Value.csv', index = False)
            
            
            
        
        
        def watcon2030():
            df = pd.read_csv(afolder + 'watcon.csv')
            df = df[['landcover','ac_ft_change_base_bau', 'ac_ft_change_trt_bau']]
            df = df.rename(columns = {'landcover': 'Landcover', 'ac_ft_change_base_bau':'Reference Scenario', 'ac_ft_change_trt_bau':'Treatment Scenario'})
    #        df2 = df2[df2.values.sum(axis=1) != 0]
            df.set_index(['Landcover'], inplace = True)
            df = df[df.values.sum(axis=1) != 0]
            df.reset_index(inplace = True)
            df['Landcover'] = 'Water Demand'
            df = df.groupby(['Landcover'], as_index = False).sum()
    
            df.to_csv(outfolder+'2030 Ag and Urban Water Conservation.csv', index = False)
    
        def groundwater2030():
            df = pd.read_csv(afolder + 'groundwater.csv')
            df = df[['landcover','ac_ft_rec_lst_base_bau','ac_ft_rec_lst_trt_bau']]
            df.set_index(['landcover'], inplace = True)
            df = df[df.values.sum(axis=1) != 0]
            df.reset_index(inplace = True)
            df['landcover'] = 'Acre Feet of Annual Groundwater Recharge Lost'
            df = df.groupby(['landcover'], as_index = False).sum()
            df = df.rename(columns = {'landcover': 'Landcover', 'ac_ft_rec_lst_base_bau':'Reference Scenario', 'ac_ft_rec_lst_trt_bau':'Treatment Scenario'})
            print (df)
            df.to_csv(outfolder+'2030 Groundwater Recharge.csv', index = False)
        

        def watint2030():
            df2 = pd.read_csv(afolder + 'watint.csv')
            df = pd.read_csv(afolder + 'watint.csv')
            df2 = df2[['Integrity_Class',ubrv + '_change_base_bau']]
            df2 = df2.rename(columns = {'Integrity_Class': 'Watershed Class',ubrv + '_change_base_bau':'Reference Scenario'})
            df = df[['Integrity_Class',ubrv + '_change_trt_bau']]
            df = df.rename(columns = {'Integrity_Class': 'Watershed Class', ubrv + '_change_trt_bau':'Treatment Scenario'})
        
            temp = pd.merge(df2, df, on = 'Watershed Class', how = 'left')
            temp.set_index(['Watershed Class'], inplace = True)
            temp = temp[temp.values.sum(axis=1) != 0]
            temp.reset_index(inplace = True)
            
            temp.to_csv(outfolder+'2030 Watershed Integrity.csv', index = False)   
            
    
        def nitrun2030():
            df2 = pd.read_csv(afolder + 'runoff_nitrates.csv')
            df = pd.read_csv(afolder + 'runoff_nitrates.csv')
            df2 = df2[['landcover','tons_no3_change_base_bau']]
            df2 = df2.rename(columns = {'landcover': 'Landcover','tons_no3_change_base_bau':'Reference Scenario'})
            df = df[['landcover','tons_no3_change_trt_bau']]
            df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_change_trt_bau':'Treatment Scenario'})
            
            
            temp = pd.merge(df2, df, on = 'Landcover', how = 'left')
            temp['Landcover'] = 'Nitrate Runoff'
            temp = temp.groupby(['Landcover'], as_index = False).sum()
    
            temp.rename(columns = {'Landcover':'Scenario'}, inplace = True)
            temp.to_csv(outfolder+'2030 Water Quality - Nitrate Runoff.csv', index = False)
            
        def nitleach2030():
            df2 = pd.read_csv(afolder + 'leach_nitrates.csv')
            df = pd.read_csv(afolder + 'leach_nitrates.csv')
            df2 = df2[['landcover','tons_no3_change_base_bau']]
            df2 = df2.rename(columns = {'landcover': 'Landcover','tons_no3_change_base_bau':'Reference Scenario'})
            df = df[['landcover','tons_no3_change_trt_bau']]
            df = df.rename(columns = {'landcover': 'Landcover', 'tons_no3_change_trt_bau':'Treatment Scenario'})
            
            temp = pd.merge(df2, df, on = 'Landcover', how = 'left')
            temp['Landcover'] = 'Nitrate Leaching'
            temp = temp.groupby(['Landcover'], as_index = False).sum()
    
            temp.rename(columns = {'Landcover':'Scenario'}, inplace = True)
            temp.to_csv(outfolder+'2030 Water Quality - Nitrate Leaching.csv', index = False)
    
            
        
        def flood2030():
            df = pd.read_csv(afolder + 'flood100.csv')
            df = df[['gen_class',ubrv + '_change_base_bau', ubrv + '_change_trt_bau' ]]
            df = df.rename(columns = {'gen_class': 'General Landcover', ubrv + '_change_base_bau':'Reference Scenario', ubrv + '_change_trt_bau':'Treatment Scenario'})
            
            #Remove any rows with all 0s
            df.set_index(['General Landcover'], inplace = True)
            df = df[df.values.sum(axis=1) != 0]
            df.reset_index(inplace = True)
    
            df.to_csv(outfolder+'2030 Flood Risk Reduction.csv', index = False)
        
    
        def air2030():
            import functools as fc
            df1 = pd.read_csv(afolder + 'co_val_airpollute.csv')
            df2 = pd.read_csv(afolder + 'no2_val_airpollute.csv')
            df3 = pd.read_csv(afolder + 'o3_val_airpollute.csv')
            df4 = pd.read_csv(afolder + 'pm2_5_val_airpollute.csv')
            df5 = pd.read_csv(afolder + 'pm10_val_airpollute.csv')
            df6 = pd.read_csv(afolder + 'so2_val_airpollute.csv')
            
            
            def cleanair(df, pollutant):
                df1 = df[['landcover','tons_change_base_bau','tons_change_trt_bau']]
                df1 = df1.rename(columns = {'landcover':'Landcover','tons_change_base_bau': 'Reference Scenario','tons_change_trt_bau':'Treatment Scenario'})
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
            plist = ['CO','NO2','O3','PM 2.5','PM 10', 'SO2']
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
    
        def scenic2030():
            df = pd.read_csv(afolder + 'scenic.csv')
            df = df[['gen_class',ubrv + '_change_base_bau', ubrv + '_change_trt_bau' ]]
            df = df.rename(columns = {'gen_class': 'General Landcover', ubrv + '_change_base_bau':'Reference Scenario', ubrv + '_change_trt_bau':'Treatment Scenario'})
            
            #Remove any rows with all 0s
            df.set_index(['General Landcover'], inplace = True)
            df = df[df.values.sum(axis=1) != 0]
            df.reset_index(inplace = True)
    
            
            df.to_csv(outfolder+'2030 Scenic Value.csv', index = False)
    
        def move2030():
            df2 = pd.read_csv(afolder + 'countymovement.csv')
            df = pd.read_csv(afolder + 'countymovement.csv')
            df2 = df2[['resistance_class',ubrv + '_change_base_bau']]
            df2 = df2.rename(columns = {'resistance_class': 'Resistance to Movement',ubrv + '_change_base_bau':'Reference Scenario'})
            df = df[['resistance_class',ubrv + '_change_trt_bau']]
            df = df.rename(columns = {'resistance_class': 'Resistance to Movement', ubrv + '_change_trt_bau':'Treatment Scenario'})
            
            
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
        
    
        def move2030_eca():
            df2 = pd.read_csv(afolder + 'ecamovement.csv')
            df = pd.read_csv(afolder + 'ecamovement.csv')
            df2 = df2[['resistance_class',ubrv + '_change_base_bau']]
            df2 = df2.rename(columns = {'resistance_class': 'Resistance to Movement',ubrv + '_change_base_bau':'Reference Scenario'})
            df = df[['resistance_class',ubrv + '_change_trt_bau']]
            df = df.rename(columns = {'resistance_class': 'Resistance to Movement', ubrv + '_change_trt_bau':'Treatment Scenario'})
            
            
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
    
    
        def lcc2030():
            df2 = pd.read_csv(afolder + 'lcchange.csv')
            df = pd.read_csv(afolder + 'lcchange.csv')
            df2 = df2[['landcover',ubrv + '_change_base_bau']]
            df2 = df2.rename(columns = {'landcover': 'Landcover',ubrv + '_change_base_bau':'Reference Scenario'})
            df = df[['landcover',ubrv + '_change_trt_bau']]
            df = df.rename(columns = {'landcover': 'Landcover', ubrv + '_change_trt_bau':'Treatment Scenario'})
            
            
            temp = pd.merge(df2, df, on = 'Landcover', how = 'left')
    
            temp.to_csv(outfolder+'2030 Natural Habitat Area.csv', index = False)
    
        def pcalcc2030():
            df2 = pd.read_csv(afolder + 'pca_cover_change.csv')
            df = pd.read_csv(afolder + 'pca_cover_change.csv')
            df2 = df2[['landcover',ubrv + '_change_base_bau']]
            df2 = df2.rename(columns = {'landcover': 'Landcover',ubrv + '_change_base_bau':'Reference Scenario'})
            df = df[['landcover',ubrv + '_change_trt_bau']]
            df = df.rename(columns = {'landcover': 'Landcover', ubrv + '_change_trt_bau':'Treatment Scenario'})
            
            
            temp = pd.merge(df2, df, on = 'Landcover', how = 'left')
            
            temp.to_csv(outfolder+'2030 Priority Conservation Areas.csv', index = False)
              
        if thabflag == 1:
            def terrhab2030():
                if os.path.exists(afolder + '/terrhab.csv'):
                    df2 = pd.read_csv(afolder + 'terrhab.csv')
                    df = pd.read_csv(afolder + 'terrhab.csv')
                    df2 = df2[['guild',ubrv + '_base_bau']]
                    df2 = df2.rename(columns = {'guild': 'Guild',ubrv + '_base_bau':'Reference Scenario'})
                    df = df[['guild',ubrv + '_trt_bau']]
                    df = df.rename(columns = {'guild': 'Guild', ubrv + '_trt_bau':'Treatment Scenario'})
                    
                    
                    temp = pd.merge(df2, df, on = 'Guild', how = 'left')
                    
                    
                    temp.loc[temp['Guild'] == 'mammals_avg_deg_ha', 'Guild'] = 'Mammal Degraded'
                    temp.loc[temp['Guild'] == 'mammals_avg_imp_ha', 'Guild'] = 'Mammal Improved'
                    temp.loc[temp['Guild'] == 'birds_avg_deg_ha', 'Guild'] = 'Bird Degraded'
                    temp.loc[temp['Guild'] == 'birds_avg_imp_ha', 'Guild'] = 'Bird Improves'
                    temp.loc[temp['Guild'] == 'amphibians_avg_deg_ha', 'Guild'] = 'Amphibian Degraded'
                    temp.loc[temp['Guild'] == 'amphibians_avg_imp_ha', 'Guild'] = 'Amphibian Improved'
                    temp.loc[temp['Guild'] == 'tes_avg_deg_ha', 'Guild'] = 'T and E Degraded'
                    temp.loc[temp['Guild'] == 'tes_avg_imp_ha', 'Guild'] = 'T and E Improved'
                
                    
                    temp.to_csv(outfolder+'2030 Terrestrial Habitat Value.csv', index = False)    
            
        def aqua2030():
            df2 = pd.read_csv(afolder + 'aquatic.csv')
            df = pd.read_csv(afolder + 'aquatic.csv')
            df2 = df2[['gen_class',ubrv + '_change_base_bau']]
            df2 = df2.rename(columns = {'gen_class': 'Landcover',ubrv + '_change_base_bau':'Reference Scenario'})
            df = df[['gen_class',ubrv + '_change_trt_bau']]
            df = df.rename(columns = {'gen_class': 'Landcover', ubrv + '_change_trt_bau':'Treatment Scenario'})
            
            
            temp = pd.merge(df2, df, on = 'Landcover', how = 'left')
        
            
            temp.to_csv(outfolder+'2030 Aquatic Biodiversity.csv', index = False)   
        
        
        def eco_resi():
            df = pd.read_csv(afolder + 'eco_resil.csv')
            df = df[['gen_class',ubrv + '_change_base_bau',ubrv + '_change_trt_bau']]
            df = df.rename(columns = {'gen_class': 'Landcover', ubrv + '_change_base_bau':'Reference Scenario', ubrv + '_change_trt_bau':'Treatment Scenario'})
            temp = df
            temp.set_index(['Landcover'], inplace = True)
            temp = temp[temp.values.sum(axis=1) != 0]
            temp.reset_index(inplace = True)
            
            temp.to_csv(outfolder+'2030 ecoresilience_table.csv', index = False)
            
        def soc_resi():
            df = pd.read_csv(afolder + 'soc_res.csv')
            df = df[['gen_class',ubrv + '_change_base_bau',ubrv + '_change_trt_bau']]
            df = df.rename(columns = {'gen_class': 'Landcover', ubrv + '_change_base_bau':'Reference Scenario', ubrv + '_change_trt_bau':'Treatment Scenario'})
            temp = df
            temp.set_index(['Landcover'], inplace = True)
            temp = temp[temp.values.sum(axis=1) != 0]
            temp.reset_index(inplace = True)
            
            temp.to_csv(outfolder+'2030 socresilience_table.csv', index = False)   
               
        def carbon():
            df = pd.read_csv(afolder + 'carbon.csv')
            alist2 = []
            aclist2 = []
            alist = ['carbon_' + i for i in actlist]
            for i in alist:
                if i in df.columns:
                    alist2.append(i)
            aclist1 = ['carbon_' + i for i in aclist]
            for i in aclist1:
                if i in df.columns:
                    aclist2.append(i)
            plist = ['landcover']
            
            plist.extend(alist2)
            plist.extend(aclist2)
            df = df[plist]
            df.set_index(['landcover'], inplace = True)
            df = df[df.values.sum(axis=1) != 0]
            df.reset_index(inplace = True)
            df['landcover'] = 'Tons of CO2e Reduced'
            df = df.groupby(['landcover'], as_index = False).sum()
            test = df.transpose()
            test.columns = test.iloc[0]
            test = test[1:]
            test.reset_index(inplace = True)
            
            df = df.rename(columns = {'landcover': 'Landcover'})
            for i in aclist:
                df.rename(columns = {i:ludict[i]})
            for i in actlist:
                df.rename(columns = {i:ludict[i]})
            test = df.transpose()
            test.columns = test.iloc[0]
            test = test[1:]
            test.reset_index(inplace = True)
            test.rename(columns = {'index':'Activity'}, inplace = True)
            print (test)
            test.sort_values(by='Tons of CO2e Reduced', ascending=1)
            test.to_csv(outfolder+'Carbon Reductions.csv', index = False)
            
            
            
            
            
        
        def carbon2():
            df = pd.read_csv(afolder + 'carbon.csv')
            df = df[['landcover','carbon_base_bau','trt_bau_total', 'carbon2014']]
            c14 = df['carbon2014'].sum()
            df.set_index(['landcover'], inplace = True)
            df = df[df.values.sum(axis=1) != 0]
            df.reset_index(inplace = True)
            df['landcover'] = 'Tons of CO2e'
            df = df.groupby(['landcover'], as_index = False).sum()
            test = df.transpose()
            test.columns = test.iloc[0]
            test = test[1:]
            test.reset_index(inplace = True)
            
            df = df.rename(columns = {'landcover': 'Landcover', 'carbon_base_bau':'Reference Scenario','trt_bau_total':'Treatment Scenario'})
            df = df[['Landcover','Reference Scenario','Treatment Scenario']]
            test = df.transpose()
            test.columns = test.iloc[0]
            test = test[1:]
            test.reset_index(inplace = True)
            test.rename(columns = {'index':'Scenario'}, inplace = True)
            test['Tons of CO2e'] = test['Tons of CO2e'] - c14
            
            test.to_csv(outfolder+'Carbon Reductions Compare.csv', index = False)
    
        
    
    #Create the 2014-2030 simplified tables
        fmmp2030()
        crop2030()
        watcon2030()
        if cproc == 0:
            watint2030()
        groundwater2030()
        nitrun2030()
        nitleach2030()
        flood2030()
        air2030()
        scenic2030()
        move2030()
        move2030_eca()
        lcc2030()
        pcalcc2030()
        if thabflag == 1:
            terrhab2030()
        aqua2030()
        eco_resi()
        soc_resi()
        carbon()
        carbon2()
    
    
    
    def mba_threetrace(table, title = 'Nothing' , xax = 'holder', yax = 'holder',  ytitle = 'None', x1 = 'None',  x2 = 'None', x3 = 'None', outfile = 'temp',y1 = 'none',y2 = 'none',y3 = 'none', xtit = '', a_font = 14, barmode = 'group'):
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
          "y": table[y1], 
          "type":"bar",
          "name":y1
        }
        
        trace2 = {
          "x": table[x2], 
          "y": table[y2],  
          "type":"bar",
           "name":y2
        }
        trace3 = {
          "x": table[x3], 
          "y": table[y3],  
          "type":"bar",
           "name":y3
        }
    
    
        data = go.Data([trace1, trace2,trace3])
        layout = {
          "autosize": False, 
          "hovermode": "closest", 
          "showlegend": True,
          "legend": {"font": {"size": 14}},
          "height": 1024,
          "width": 1280,  
          "title": title,
          "barmode": barmode,
          "bargap": 0.6599999999999999,
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
                    "size": 17
              }
          },
        }
       
        fig = go.Figure(data=data, layout=layout)
    #    plot(fig, filename= plot_dict[mba]['title'] + '.html')
        py.image.save_as(fig, outfile, format='png')
        return fig
    
    #Define the plotting functions
    def mba_twotrace(table, title = 'Nothing' , xax = 'holder', yax = 'holder',  ytitle = 'None', x1 = 'None',  x2 = 'None', x3 = 'None', outfile = 'temp',y1 = 'none',y2 = 'none', xtit = '', a_font = 14):
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
          "autosize": False, 
          "hovermode": "closest", 
          "showlegend": True,
          "legend": {"font": {"size": 14}},
          "height": 1024,
          "width": 1280,  
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
                    "size": 17
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

    def mba_chart_onetrace(table, xax = 'holder', yax = 'holder', x = 'None',y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, qu2 = 'None', outfile = 'temp', xtit = '', xfont = 14):
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
          "autosize": False, 
          "hovermode": "closest", 
          "showlegend": False,
          "title": xax,
          "width": 1280,
          "height": 1024,
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
    
    #Create a function to make the plots
    def custom_plots(afolder):
        #Set the folder variables
        tables = afolder + 'plot_tables'
        outpath = afolder + 'plots/'


   
        #Call the plotting functions for each plot
        mba_twotrace(tables + "/2030 Ag Land Quality.csv", '2014-2030 Farmland Loss', xax = 'holder', yax = 'holder',   ytitle = units, x1 = 'Farmland Class', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Farmland Loss.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario', a_font = 14)
        
        mba_twotrace(tables + "/2030 Groundwater Recharge.csv", '2014-2030 Groundwater Recharge Loss', xax = 'holder', yax = 'holder',   ytitle = 'Acre Feet per Year', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Groundwater Recharge.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario', a_font = 14)
    
        mba_twotrace(tables + "/2030 Crop Value.csv", '2014-2030 Change in Crop Value', xax = 'holder', yax = 'holder',   ytitle = 'US Dollars', x1 = 'Crop Type', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Crop Value.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
     
        mba_twotrace(tables + "/2030 Ag and Urban Water Conservation.csv", '2014-2030 Change in Water Demand', xax = 'holder', yax = 'holder',   ytitle = 'Acre Ft/Year', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Ag and Urban Water Conservation.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
        
        
        if cproc == 0:
            mba_twotrace(tables + "/2030 Watershed Integrity.csv", '2014-2030 Change in Watershed Integrity', xax = 'holder', yax = 'holder',   ytitle = units, x1 = 'Watershed Class', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Watershed Integrity Riparian.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
    
        
        mba_twotrace(tables + "/2030 Flood Risk Reduction.csv", '2014-2030 Change in Landcover in 100 Year Floodplain', xax = 'holder', yax = 'holder',   ytitle = units, x1 = 'General Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Flood Risk Reduction.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
        
    
        mba_twotrace(tables + "/2030 Air Quality Change.csv", '2014-2030 Change in Air Pollutant Sequestration', xax = 'holder', yax = 'holder',   ytitle = 'Tons of Pollutant Sequestered', x1 = 'Air Pollutant', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Air Quality.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
        
        
    
        mba_twotrace(tables + "/2030 Flood Risk Reduction.csv", '2014-2030 Change in Landcover in Highly Visible Areas', xax = 'holder', yax = 'holder',   ytitle = units, x1 = 'General Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Scenic Value.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
    
    
        mba_twotrace(tables + "/2030 ECA Terrestrial Connectivity.csv", '2014-2030 Change in Resistance to Species Movement<br>in Essential Connectivity Areas', xax = 'holder', yax = 'holder',   ytitle = units, x1 = 'Resistance to Movement', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 ECA Terrestrial Connectivity.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario', xtit = 'Resistance to Movement',a_font = 14)
    
        mba_twotrace(tables + "/2030 Terrestrial Connectivity.csv", '2014-2030 Change in Resistance to <br>Species Movement', xax = 'holder', yax = 'holder',   ytitle = units, x1 = 'Resistance to Movement', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Terrestrial Connectivity.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario', xtit = 'Resistance to Movement', a_font = 14)
        
    
        mba_twotrace(tables + "/2030 Priority Conservation Areas.csv", '2014-2030 Change in Landcover in Priority Conservation Areas', xax = 'holder', yax = 'holder',   ytitle = units, x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Priority Conservation Areas.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
    
        mba_twotrace(tables + "/2030 Natural Habitat Area.csv", '2014-2030 Change in Landcover', xax = 'holder', yax = 'holder',   ytitle = units, x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Natural Habitat Area.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
        if thabflag == 1:
            mba_twotrace(tables + "/2030 Terrestrial Habitat Value.csv", '2014-2030 Change in Terrestrial Habitat Value', xax = 'holder', yax = 'holder',   ytitle = units, x1 = 'Guild', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Terrestrial Habitat Value.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario', a_font = 13)
        
    
        mba_twotrace(tables + "/2030 Aquatic Biodiversity.csv", '2014-2030 Landcover Change in Watersheds with <br>Important Aquatic Habitat', xax = 'holder', yax = 'holder',   ytitle = units, x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Aquatic Biodiversity.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
    
        mba_twotrace(tables + "/2030 socresilience_table.csv", '2014-2030 Landcover Change in Areas Important <br>For Social Resilience', xax = 'holder', yax = 'holder',   ytitle = units, x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Social Resilience.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
    
    
        mba_twotrace(tables + "/2030 ecoresilience_table.csv", '2014-2030 Landcover Change in Areas Important <br>For Natural Resilience', xax = 'holder', yax = 'holder', ytitle = units, x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Natural Resilience.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario', a_font = 13)
        
        import pandas as pd
        
        df = pd.read_csv(tables + "/Carbon Reductions.csv")
        for key in ludict:
            df.loc[df['Activity'] ==  'carbon_' + key, 'Activity'] = ludict[key]
        df.to_csv(tables + "/Carbon Reductions.csv")
        
        mba_chart_onetrace(tables + "/Carbon Reductions.csv", '2030 Carbon Reductions from Activities', yax = 'Tons of CO2e', x = 'Activity',y = 'Tons of CO2e Reduced', yrange = [0,1], qu = 'None', remzeros = 0, qu2 = 'None', outfile = outpath + "2030 Carbon Reductions.png", xtit = '', xfont = 12)
        
        mba_chart_onetrace(tables + "/Carbon Reductions Compare.csv", '2014-2030 Carbon Reduction Change', yax = 'Tons of CO2e', x = 'Scenario',y = 'Tons of CO2e', yrange = [0,1], qu = 'None', remzeros = 0, qu2 = 'None', outfile = outpath + "2030 Carbon Reductions Compare.png", xtit = '', xfont = 12)
        
        import os.path

        if os.path.exists(tables + "/act_acres.csv"):
            df = pd.read_csv(tables + "/act_acres.csv")
            for key in ludict:
                df.loc[df['Activity'] == key + '_acres','Activity'] = ludict[key]
            df.to_csv(tables + "/act_acres.csv")
        
        
            mba_chart_onetrace(tables + "/act_acres.csv", 'Activities and Acres', yax = 'Acres Selected', x = 'Activity',y = units, yrange = [0,1], qu = 'None', remzeros = 0, qu2 = 'None', outfile = outpath + "Activity Acres Selected.png", xtit = '', xfont = 11)
        
        mba_twotrace(tables + "/2030 Water Quality - Nitrate Runoff.csv", '2014-2030 Change in Nitrate Runoff', xax = 'holder', yax = 'holder',   ytitle = 'Tons of Nitrate', x1 = 'Scenario', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Water Quality - Nitrate Runoff.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
        
        mba_twotrace(tables + "/2030 Water Quality - Nitrate Leaching.csv", '2014-2030 Change in Nitrate Leaching', xax = 'holder', yax = 'holder',   ytitle = 'Tons of Nitrate', x1 = 'Scenario', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Water Quality - Nitrate Leaching.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario', a_font = 14)

                                                    
        mba_chart_onetrace(tables + "/2014 Ag Land Quality.csv", xax = '2014 Farmland', yax = units, x = 'Farmland Class',y = units, yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Farmland.png")

        mba_chart_onetrace(tables + "/2014 Crop Value.csv", xax = '2014 Crop Value', yax = 'US Dollars', x = 'Crop Type',y = 'US Dollars', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Crop Value.png")

        mba_chart_onetrace(tables + "/2014 Ag and Urban Water Conservation.csv", xax = '2014 Water Demand', yax = 'Acre Ft/Year', x = 'Landcover',y = 'Acre Feet Annual Water Demand', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Ag and Urban Water Conservation.png")

        if cproc == 0:
            mba_chart_onetrace(tables + "/2014 Watershed Integrity.csv", xax = '2014 Watershed Integrity', yax = units, x = 'Watershed Class',y = units, yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Watershed Integrity.png")
        
        mba_chart_onetrace(tables + "/2014 Water Quality - Nitrate Runoff.csv", xax = '2014 Nitrate Runoff', yax = 'Tons', x = 'Landcover',y = 'Annual Tons of Nitrate Runoff', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Nitrate Runoff.png")
        
        mba_chart_onetrace(tables + "/2014 Water Quality - Nitrate Leaching.csv", xax = '2014 Nitrate Leaching', yax = 'Tons', x = 'Landcover',y = 'Annual Tons of Nitrate Leaching', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Nitrate Leaching.png")

        mba_chart_onetrace(tables + "/2014 Flood Risk Reduction.csv", xax = '2014 Landcover in 100 Year Floodplain', yax = units, x = 'General Landcover',y = units, yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Flood Risk Reduction.png")

        mba_chart_onetrace(tables + "/2014 Air Quality.csv", xax = '2014 Air Pollutant Sequestration', yax = 'Tons of Pollutant Sequestered Annually', x = 'Air Pollutant',y = 'Tons of Pollutant Sequestered Annually', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Air Quality.png")

        mba_chart_onetrace(tables + "/2014 Scenic Value.csv", xax = '2014 Landcover in Highly Visible Areas', yax = units, x = 'General Landcover',y = units, yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Scenic Value.png")

        mba_chart_onetrace(tables + "/2014 Terrestrial Connectivity.csv", xax = '2014 Resistance to Species Movement', yax = units, x = 'Resistance to Movement',y = units, yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Terrestrial Connectivity.png")
        
        mba_chart_onetrace(tables + "/2014 ECA Terrestrial Connectivity.csv", xax = '2014 Resistance to Species Movement in Essential Connectivity Areas', yax = units, x = 'Resistance to Movement',y = units, yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Terrestrial Connectivity ECA.png")

        mba_chart_onetrace(tables + "/2014 Natural Habitat Area.csv", xax = '2014 Landcover', yax = units, x = 'Landcover',y = units, yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Natural Habitat Area.png")
        
        mba_chart_onetrace(tables + "/2014 Priority Conservation Areas.csv", xax = '2014 Landcover in Priority Conservation Areas', yax = units, x = 'Landcover',y = units, yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Priority Conservation Areas.png")

        
        mba_chart_onetrace(tables + "/2014 Aquatic Biodiversity.csv", xax = '2014 Landcover in Watersheds with <br>Important Aquatic Habitat', yax = units, x = 'Landcover',y = units, yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Aquatic Biodiversity.png")

    
        mba_chart_onetrace(tables + "/2014 Social Resilience.csv", xax = '2014 Landcover in Areas Important <br>For Social Resilience', yax = units, x = 'Landcover',y = units, yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Social Resilience.png")
        
        mba_chart_onetrace(tables + "/2014 Natural Resilience.csv", xax = '2014 Landcover in Areas Important <br>For Natural Resilience', yax = units, x = 'Landcover',y = units, yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Natural Resilience.png")

        mba_threetrace(tables + "/total_reductions.csv", 'Total Emission Reductions and CO2 Removals<br>Achieved at 2030 from Planned Activities', xax = 'holder', yax = 'Tonnes CO2e', x1 = 'Carbon', x3 = 'CH4', x2 = 'N2O',outfile = outpath + "Total Reductions.png", y1 = 'CO2e Reductions', y3 = 'CH4 Reductions',y2 = 'N2O Reductions', a_font = 13, barmode = 'stack', ytitle = 'Tonnes CO2e')

        mba_twotrace(tables + "/annual_emissions.csv", 'A Comparison of 2030 N2O, CH4 Emissions<br>and CO2 Removal Flux (Baseline and Treatment) ', xax = 'holder', yax = 'holder', ytitle = 'Tonnes CO2e', x1 = 'Source', x2 = '2030 Baseline', x3 = '2030 Treatment',outfile = outpath + "Annual Flux.png", y1 = '2030<br>Baseline', y2 = '2030<br>Treatment', a_font = 13)

        mba_twotrace(tables + "/annual_emissions_aggregate.csv", 'A Comparison of 2030 N2O and CH4 Emissions<br>Net of CO2 Removals (Baseline and Treatment) ', xax = 'holder', yax = 'holder', ytitle = 'Tonnes CO2e', x1 = 'Source', x2 = '2030 Baseline', x3 = '2030 Treatment',outfile = outpath + "Aggregate Flux.png", y1 = '2030<br>Baseline', y2 = '2030<br>Treatment', a_font = 13)


    simp(runfolder)
    custom_plots(runfolder)











































