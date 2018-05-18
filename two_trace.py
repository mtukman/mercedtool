
runfolder = r"E:\Temp\20180515-110310\\"
mba_title_font = 20
plot_dict = {}
axis_lab_font = 16
import plotly.plotly as py

py.sign_in('mtukman', 'FbUYCv4tcjCPF2ZdfzKo')

def simp(afolder = ''):

    import os
    import pandas as pd
    import functools
    
    if not os.path.exists(afolder + 'plot_tables_twotrace'):
        os.makedirs(afolder + 'plot_tables_twotrace')
    if not os.path.exists(afolder + 'plots_twotrace'):
        os.makedirs(afolder + 'plots_twotrace')
    outfolder =     afolder + 'plot_tables_twotrace/'
        
    def fmmp2030():
        df = pd.read_csv(afolder + r'\fmmp.csv')
        df = df[['fmmp_class','ha_loss_base_bau', 'ha_loss_trt_bau' ]]
        df = df.rename(columns = {'fmmp_class': 'Farmland Class', 'ha_loss_base_bau':'Reference Scenario', 'ha_loss_trt_bau':'Treatment Scenario'})
        df.set_index(['Farmland Class'], inplace = True)
        df = df[df.values.sum(axis=1) != 0]
        df.reset_index(inplace = True)
        
        df.to_csv(outfolder+'2030 Ag Land Quality.csv', index = False)
        

    
    def crop2030():
        df = pd.read_csv(afolder + r'\cropvalue.csv')
        df = df[['landcover','usd_change_base_bau', 'usd_change_trt_bau']]
        df = df.rename(columns = {'landcover': 'Crop Type', 'usd_change_base_bau':'Reference Scenario', 'usd_change_trt_bau':'Treatment Scenario'})
        df.set_index(['Crop Type'], inplace = True)
        df = df[df.values.sum(axis=1) != 0]
        df.reset_index(inplace = True)
        df['Crop Type'] = 'Crop Value'
        df = df.groupby(['Crop Type'], as_index = False).sum()
        
        df.to_csv(outfolder+'2030 Crop Value.csv', index = False)
        
        
        
    
    
    def watcon2030():
        df = pd.read_csv(afolder + r'\watcon.csv')
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
        df = pd.read_csv(afolder + r'\groundwater.csv')
        df = df[['landcover','ac_ft_rec_lst_base_bau','ac_ft_rec_lst_trt_bau']]
        df.set_index(['landcover'], inplace = True)
        df = df[df.values.sum(axis=1) != 0]
        df.reset_index(inplace = True)
        df['landcover'] = 'Acre Feet of Annual Groundwater Recharge Lost'
        df = df.groupby(['landcover'], as_index = False).sum()
        test = df.transpose()
        test.columns = test.iloc[0]
        test = test[1:]
        test.reset_index(inplace = True)
        
        df = df.rename(columns = {'landcover': 'Landcover', 'ac_ft_rec_lst_base_bau':'Reference Scenario', 'ac_ft_rec_lst_trt_bau':'Treatment Scenario'})
        test = df.transpose()
        test.columns = test.iloc[0]
        test = test[1:]
        test.reset_index(inplace = True)
        test.rename(columns = {'index':'Development Scenario'}, inplace = True)
        print (test)
        test.to_csv(outfolder+'2030 Groundwater Recharge.csv', index = False)
    

        
    def watint2030():
        df2 = pd.read_csv(afolder + r'\watint.csv')
        df = pd.read_csv(afolder + r'\watint.csv')
        df2 = df2[['Integrity_Class','ha_change_base_bau']]
        df2 = df2.rename(columns = {'Integrity_Class': 'Watershed Class','ha_change_base_bau':'Reference Scenario'})
        df = df[['Integrity_Class','ha_change_trt_bau']]
        df = df.rename(columns = {'Integrity_Class': 'Watershed Class', 'ha_change_trt_bau':'Treatment Scenario'})
    
        temp = pd.merge(df2, df, on = 'Watershed Class', how = 'left')
        temp.set_index(['Watershed Class'], inplace = True)
        temp = temp[temp.values.sum(axis=1) != 0]
        temp.reset_index(inplace = True)
        
        temp.to_csv(outfolder+'2030 Watershed Integrity.csv', index = False)   
    

    def nitrun2030():
        df2 = pd.read_csv(afolder + r'\runoff_nitrates.csv')
        df = pd.read_csv(afolder + r'\runoff_nitrates.csv')
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
        df2 = pd.read_csv(afolder + r'\leach_nitrates.csv')
        df = pd.read_csv(afolder + r'\leach_nitrates.csv')
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
        df = pd.read_csv(afolder + r'\flood100.csv')
        df = df[['gen_class','ha_change_base_bau', 'ha_change_trt_bau' ]]
        df = df.rename(columns = {'gen_class': 'General Landcover', 'ha_change_base_bau':'Reference Scenario', 'ha_change_trt_bau':'Treatment Scenario'})
        
        #Remove any rows with all 0s
        df.set_index(['General Landcover'], inplace = True)
        df = df[df.values.sum(axis=1) != 0]
        df.reset_index(inplace = True)

        df.to_csv(outfolder+'2030 Flood Risk Reduction.csv', index = False)
    

    def air2030():
        import functools as fc
        df1 = pd.read_csv(afolder + r'\co_val_airpollute.csv')
        df2 = pd.read_csv(afolder + r'\no2_val_airpollute.csv')
        df3 = pd.read_csv(afolder + r'\o3_val_airpollute.csv')
        df4 = pd.read_csv(afolder + r'\pm2_5_val_airpollute.csv')
        df5 = pd.read_csv(afolder + r'\pm10_val_airpollute.csv')
        df6 = pd.read_csv(afolder + r'\so2_val_airpollute.csv')
        
        
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
        df = pd.read_csv(afolder + r'\scenic.csv')
        df = df[['gen_class','ha_change_base_bau', 'ha_change_trt_bau' ]]
        df = df.rename(columns = {'gen_class': 'General Landcover', 'ha_change_base_bau':'Reference Scenario', 'ha_change_trt_bau':'Treatment Scenario'})
        
        #Remove any rows with all 0s
        df.set_index(['General Landcover'], inplace = True)
        df = df[df.values.sum(axis=1) != 0]
        df.reset_index(inplace = True)

        
        df.to_csv(outfolder+'2030 Scenic Value.csv', index = False)

    def move2030():
        df2 = pd.read_csv(afolder + r'\countymovement.csv')
        df = pd.read_csv(afolder + r'\countymovement.csv')
        df2 = df2[['resistance_class','ha_change_base_bau']]
        df2 = df2.rename(columns = {'resistance_class': 'Resistance to Movement','ha_change_base_bau':'Reference Scenario'})
        df = df[['resistance_class','ha_change_trt_bau']]
        df = df.rename(columns = {'resistance_class': 'Resistance to Movement', 'ha_change_trt_bau':'Treatment Scenario'})
        
        
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
        df2 = pd.read_csv(afolder + r'\ecamovement.csv')
        df = pd.read_csv(afolder + r'\ecamovement.csv')
        df2 = df2[['resistance_class','ha_change_base_bau']]
        df2 = df2.rename(columns = {'resistance_class': 'Resistance to Movement','ha_change_base_bau':'Reference Scenario'})
        df = df[['resistance_class','ha_change_trt_bau']]
        df = df.rename(columns = {'resistance_class': 'Resistance to Movement', 'ha_change_trt_bau':'Treatment Scenario'})
        
        
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
        df2 = pd.read_csv(afolder + r'\lcchange.csv')
        df = pd.read_csv(afolder + r'\lcchange.csv')
        df2 = df2[['landcover','ha_change_base_bau']]
        df2 = df2.rename(columns = {'landcover': 'Landcover','ha_change_base_bau':'Reference Scenario'})
        df = df[['landcover','ha_change_trt_bau']]
        df = df.rename(columns = {'landcover': 'Landcover', 'ha_change_trt_bau':'Treatment Scenario'})
        
        
        temp = pd.merge(df2, df, on = 'Landcover', how = 'left')

        temp.to_csv(outfolder+'2030 Natural Habitat Area.csv', index = False)

    def pcalcc2030():
        df2 = pd.read_csv(afolder + r'\pca_cover_change.csv')
        df = pd.read_csv(afolder + r'\pca_cover_change.csv')
        df2 = df2[['landcover','ha_change_base_bau']]
        df2 = df2.rename(columns = {'landcover': 'Landcover','ha_change_base_bau':'Reference Scenario'})
        df = df[['landcover','ha_change_trt_bau']]
        df = df.rename(columns = {'landcover': 'Landcover', 'ha_change_trt_bau':'Treatment Scenario'})
        
        
        temp = pd.merge(df2, df, on = 'Landcover', how = 'left')
        
        temp.to_csv(outfolder+'2030 Priority Conservation Areas.csv', index = False)
          
        
    def terrhab2030():
        if os.path.exists(afolder + '/terrhab.csv'):
            df2 = pd.read_csv(afolder + r'\terrhab.csv')
            df = pd.read_csv(afolder + r'\terrhab.csv')
            df2 = df2[['guild','ha_base_bau']]
            df2 = df2.rename(columns = {'guild': 'Guild','ha_base_bau':'Reference Scenario'})
            df = df[['guild','ha_trt_bau']]
            df = df.rename(columns = {'guild': 'Guild', 'ha_trt_bau':'Treatment Scenario'})
            
            
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
        df2 = pd.read_csv(afolder + r'\aquatic.csv')
        df = pd.read_csv(afolder + r'\aquatic.csv')
        df2 = df2[['gen_class','ha_change_base_bau']]
        df2 = df2.rename(columns = {'gen_class': 'Landcover','ha_change_base_bau':'Reference Scenario'})
        df = df[['gen_class','ha_change_trt_bau']]
        df = df.rename(columns = {'gen_class': 'Landcover', 'ha_change_trt_bau':'Treatment Scenario'})
        
        
        temp = pd.merge(df2, df, on = 'Landcover', how = 'left')
    
        
        temp.to_csv(outfolder+'2030 Aquatic Biodiversity.csv', index = False)   
    
    
    def eco_resi():
        df = pd.read_csv(afolder + r'\eco_resil.csv')
        df = df[['gen_class','ha_change_base_bau','ha_change_trt_bau']]
        df = df.rename(columns = {'gen_class': 'Landcover', 'ha_change_base_bau':'Reference Scenario', 'ha_change_trt_bau':'Treatment Scenario'})
        temp = df
        temp.set_index(['Landcover'], inplace = True)
        temp = temp[temp.values.sum(axis=1) != 0]
        temp.reset_index(inplace = True)
        
        temp.to_csv(outfolder+'2030 ecoresilience_table.csv', index = False)   
    def soc_resi():
        df = pd.read_csv(afolder + r'\soc_res.csv')
        df = df[['gen_class','ha_change_base_bau','ha_change_trt_bau']]
        df = df.rename(columns = {'gen_class': 'Landcover', 'ha_change_base_bau':'Reference Scenario', 'ha_change_trt_bau':'Treatment Scenario'})
        temp = df
        temp.set_index(['Landcover'], inplace = True)
        temp = temp[temp.values.sum(axis=1) != 0]
        temp.reset_index(inplace = True)
        
        temp.to_csv(outfolder+'2030 socresilience_table.csv', index = False)   
           
    def carbon():
        df = pd.read_csv(afolder + r'\carbon.csv')
        df = df[['landcover','carbon_rre'	,'carbon_ccr','carbon_nfm','carbon_avoided_ac_orc_urb']]
        df.set_index(['landcover'], inplace = True)
        df = df[df.values.sum(axis=1) != 0]
        df.reset_index(inplace = True)
        df['landcover'] = 'Tons of CO2e Reduced'
        df = df.groupby(['landcover'], as_index = False).sum()
        test = df.transpose()
        test.columns = test.iloc[0]
        test = test[1:]
        test.reset_index(inplace = True)
        
        df = df.rename(columns = {'landcover': 'Landcover', 'carbon_rre':	'Riparian Restoration','carbon_ccr':'Cover Cropping','carbon_nfm': 'N Fertilizer Management','carbon_avoided_ac_orc_urb':'AC Orchard to Urban'})
        test = df.transpose()
        test.columns = test.iloc[0]
        test = test[1:]
        test.reset_index(inplace = True)
        test.rename(columns = {'index':'Activity'}, inplace = True)
        print (test)
        test.sort_values(by='Tons of CO2e Reduced', ascending=1)
        test.to_csv(outfolder+'Carbon Reductions.csv', index = False)
    def carbon2():
        df = pd.read_csv(afolder + r'\carbon.csv')
        df = df[['landcover','carbon_base_bau','trt_bau_total']]
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
        test = df.transpose()
        test.columns = test.iloc[0]
        test = test[1:]
        test.reset_index(inplace = True)
        test.rename(columns = {'index':'Scenario'}, inplace = True)
        test['Tons of CO2e'] = test['Tons of CO2e'] - 52331726
        test.to_csv(outfolder+'Carbon Reductions Compare.csv', index = False)

    


    fmmp2030()

    crop2030()
    watcon2030()

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
    terrhab2030()

    aqua2030()
    eco_resi()
    soc_resi()
    carbon()
    carbon2()

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
def custom_plots(afolder):

    tables = afolder + 'plot_tables_twotrace'
    outpath = afolder + 'plots_twotrace/'


    mba_twotrace(tables + "/2030 Ag Land Quality.csv", '2014-2030 Farmland Loss', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Farmland Class', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Farmland Loss.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario', a_font = 14)
    

    mba_twotrace(tables + "/2030 Crop Value.csv", '2014-2030 Change in Crop Value', xax = 'holder', yax = 'holder',   ytitle = 'US Dollars', x1 = 'Crop Type', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Crop Value.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
 
    mba_twotrace(tables + "/2030 Ag and Urban Water Conservation.csv", '2014-2030 Change in Water Demand', xax = 'holder', yax = 'holder',   ytitle = 'Acre Ft/Year', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Ag and Urban Water Conservation.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
    
    

    mba_twotrace(tables + "/2030 Watershed Integrity.csv", '2014-2030 Change in Watershed Integrity', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Watershed Class', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Watershed Integrity Riparian.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')

    
    mba_twotrace(tables + "/2030 Flood Risk Reduction.csv", '2014-2030 Change in Landcover in 100 Year Floodplain', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'General Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Flood Risk Reduction.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
    

    mba_twotrace(tables + "/2030 Air Quality Change.csv", '2014-2030 Change in Air Pollutant Sequestration', xax = 'holder', yax = 'holder',   ytitle = 'Tons of Pollutant Sequestered', x1 = 'Air Pollutant', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Air Quality.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
    
    

    mba_twotrace(tables + "/2030 Flood Risk Reduction.csv", '2014-2030 Change in Landcover in Highly Visible Areas', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'General Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Scenic Value.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')


    mba_twotrace(tables + "/2030 ECA Terrestrial Connectivity.csv", '2014-2030 Change in Resistance to Species Movement<br>in Essential Connectivity Areas', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Resistance to Movement', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 ECA Terrestrial Connectivity.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario', xtit = 'Resistance to Movement',a_font = 14)

    mba_twotrace(tables + "/2030 Terrestrial Connectivity.csv", '2014-2030 Change in Resistance to <br>Species Movement', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Resistance to Movement', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Terrestrial Connectivity.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario', xtit = 'Resistance to Movement', a_font = 14)
    

    mba_twotrace(tables + "/2030 Priority Conservation Areas.csv", '2014-2030 Change in Landcover in Priority Conservation Areas', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Priority Conservation Areas.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')

    mba_twotrace(tables + "/2030 Natural Habitat Area.csv", '2014-2030 Change in Landcover', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Natural Habitat Area.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')

    mba_twotrace(tables + "/2030 Terrestrial Habitat Value.csv", '2014-2030 Change in Terrestrial Habitat Value', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Guild', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Terrestrial Habitat Value.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario', a_font = 13)
    

    mba_twotrace(tables + "/2030 Aquatic Biodiversity.csv", '2014-2030 Landcover Change in Watersheds with <br>Important Aquatic Habitat', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Aquatic Biodiversity.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')

    mba_twotrace(tables + "/2030 socresilience_table.csv", '2014-2030 Landcover Change in Areas Important <br>For Social Resilience', xax = 'holder', yax = 'holder',   ytitle = 'Hectares', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Social Resilience.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')


    mba_twotrace(tables + "/2030 ecoresilience_table.csv", '2014-2030 Landcover Change in Areas Important <br>For Social Resilience', xax = 'holder', yax = 'holder', ytitle = 'Hectares', x1 = 'Landcover', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Social Resilience.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')

    mba_chart_onetrace(tables + "/Carbon Reductions.csv", '2030 Carbon Reductions from Activities', yax = 'Tons of CO2e', x = 'Activity',y = 'Tons of CO2e Reduced', yrange = [0,1], qu = 'None', remzeros = 0, qu2 = 'None', outfile = outpath + "2030 Carbon Reductions.png", xtit = '', xfont = 14)
    
    mba_chart_onetrace(tables + "/Carbon Reductions Compare.csv", '2014-2030 Carbon Reduction Change', yax = 'Tons of CO2e', x = 'Scenario',y = 'Tons of CO2e', yrange = [0,1], qu = 'None', remzeros = 0, qu2 = 'None', outfile = outpath + "2030 Carbon Reductions Compare.png", xtit = '', xfont = 14)
    
    mba_chart_onetrace(tables + "/act_acres.csv", 'Activities and Acres', yax = 'Acres Selected', x = 'Activity',y = 'Acres', yrange = [0,1], qu = 'None', remzeros = 0, qu2 = 'None', outfile = outpath + "Activity Acres Selected.png", xtit = '', xfont = 14)
    
    mba_twotrace(tables + "/2030 Water Quality - Nitrate Runoff.csv", '2014-2030 Change in Nitrate Runoff', xax = 'holder', yax = 'holder',   ytitle = 'Tons of Nitrate', x1 = 'Scenario', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Water Quality - Nitrate Runoff.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario')
    
    mba_twotrace(tables + "/2030 Water Quality - Nitrate Leaching.csv", '2014-2030 Change in Nitrate Leaching', xax = 'holder', yax = 'holder',   ytitle = 'Tons of Nitrate', x1 = 'Scenario', x2 = 'Reference Scenario', x3 = 'Treatment Scenario',outfile = outpath + "2030 Water Quality - Nitrate Leaching.png", y1 = 'Reference<br>Scenario', y2 = 'Treatment<br>Scenario', a_font = 14)

simp(runfolder)
custom_plots(runfolder)










