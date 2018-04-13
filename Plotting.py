
folder = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\\"
outpath2 = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\plotting_tables\\"
mba_title_font = 18
plot_dict = {}
axis_lab_font = 16

flist = ['_base_bau','_base_med','_base_max','_trt_bau','_trt_med','_trt_max']






















def mba_cropvalue_plot_tables(csv='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/cropvalue.csv', outpath='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/plot_tables/'):
    import os
    import pandas as pd 
    
    df =pd.read_csv(csv)
    df2 = df[df['landcover'].isin(['Annual Cropland', 'Orchard', 'Vineyard', 'Rice', 'Irrigated Pasture'])]
    df3 =df2.fillna(0)
    
    # Annual Croplands
    orchard = pd.DataFrame(columns=['Untreated', 'Treated'])
    orchard.loc[len(orchard)] = [float(df3.loc[df3['landcover']=='Orchard', 'usd_change_base_bau']), float(df3.loc[df3['landcover']=='Orchard', 'usd_change_trt_bau'])]
    orchard.loc[len(orchard)] = [float(df3.loc[df3['landcover']=='Orchard', 'usd_change_base_med']), float(df3.loc[df3['landcover']=='Orchard', 'usd_change_trt_med'])]
    orchard.loc[len(orchard)] = [float(df3.loc[df3['landcover']=='Orchard', 'usd_change_base_max']), float(df3.loc[df3['landcover']=='Orchard', 'usd_change_trt_max'])]
    orchard['scenario'] = ['ref', 'med', 'max']
    orchard.to_csv(os.path.join(outpath, 'plt_cropvalue_orchards.csv'))
    
    annual = pd.DataFrame(columns=['Untreated', 'Treated'])
    annual.loc[len(annual)] = [float(df3.loc[df3['landcover']=='Annual Cropland', 'usd_change_base_bau']), float(df3.loc[df3['landcover']=='Annual Cropland', 'usd_change_trt_bau'])]
    annual.loc[len(annual)] = [float(df3.loc[df3['landcover']=='Annual Cropland', 'usd_change_base_med']), float(df3.loc[df3['landcover']=='Annual Cropland', 'usd_change_trt_med'])]
    annual.loc[len(annual)] = [float(df3.loc[df3['landcover']=='Annual Cropland', 'usd_change_base_max']), float(df3.loc[df3['landcover']=='Annual Cropland', 'usd_change_trt_max'])]
    annual['scenario'] = ['ref', 'med', 'max']
    annual.to_csv(os.path.join(outpath, 'plt_cropvalue_annual.csv'))
    
    
    all_acts = pd.DataFrame(columns=['Untreated', 'Treated'])
    all_acts.loc[len(all_acts)] = [df3.sum(axis=0)['usd_change_base_bau'], df3.sum(axis=0)['usd_change_trt_bau']]
    all_acts.loc[len(all_acts)] = [df3.sum(axis=0)['usd_change_base_med'], df3.sum(axis=0)['usd_change_trt_med']]
    all_acts.loc[len(all_acts)] = [df3.sum(axis=0)['usd_change_base_max'], df3.sum(axis=0)['usd_change_trt_max']]
    all_acts['scenario'] = ['ref', 'med', 'max']
    all_acts.to_csv(os.path.join(outpath, 'plt_cropvalue_all.csv'))
    return [all_acts,annual,orchard]
    


    
def mba_plot_tables_sum(csv='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/groundwater.csv', outpath='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/plot_tables/', csvname = 'plt_groundwater.csv', changefield = 'blah'):
    """
    This function reports on summed fields for a table. Fields can be the change field (so total change), or total field (total values for a scenario)
    """
    import os
    import pandas as pd 
    
    df = pd.read_csv(csv)
    df3 =df.fillna(0)
    gwrc = pd.DataFrame(columns=['Untreated', 'Treated'])
    gwrc.loc[len(gwrc)] = [df3.sum(axis=0)[changefield + '_base_bau'], df3.sum(axis=0)[changefield + '_trt_bau']]
    gwrc.loc[len(gwrc)] = [df3.sum(axis=0)[changefield + '_base_med'], df3.sum(axis=0)[changefield + '_trt_med']]
    gwrc.loc[len(gwrc)] = [df3.sum(axis=0)[changefield + '_base_max'], df3.sum(axis=0)[changefield + '_trt_max']]

   
    gwrc['scenario'] = ['ref', 'med', 'max']
    
    gwrc.to_csv(os.path.join(outpath, csvname))


def carbon_plot_tables_sum(csv='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/groundwater.csv', outpath='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/plot_tables/', csvname = 'plt_groundwater.csv'):
    """
    This function reports on summed fields for a table. Fields can be the change field (so total change), or total field (total values for a scenario)
    """
    import os
    import pandas as pd 
    
    df = pd.read_csv(csv)
    df3 =df.fillna(0)
    gwrc = pd.DataFrame(columns=['Untreated', 'Treated'])
    gwrc.loc[len(gwrc)] = [df3.sum(axis=0)['carbon_base_bau'], df3.sum(axis=0)['trt_bau_total']]
    gwrc.loc[len(gwrc)] = [df3.sum(axis=0)['carbon_base_med'], df3.sum(axis=0)['trt_med_total']]
    gwrc.loc[len(gwrc)] = [df3.sum(axis=0)['carbon_base_max'], df3.sum(axis=0)['trt_max_total']]

   
    gwrc['scenario'] = ['ref', 'med', 'max']
    
    gwrc.to_csv(os.path.join(outpath, csvname))





def mba_plot_tables_rows(csv=r"E:\Temp\tooloutputs\RRE_FULL\cropvalue.csv", outpath='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/plot_tables/', csvname = 'plt_groundwater.csv', fieldname = 'usd',  rfield = 'landcover'):
    """
    This function reports on all of the rows by development scenarios. So for land cover change, it would report on the either the land cover change or total landcover by land cover class for each scenario. Pretty much a cleaned up version of the reporting csv.
    
    """
    import os
    import pandas as pd 

    df = pd.read_csv(csv)
    df3 =df.fillna(0)
    df3 = df

    flist2 = [rfield]
    for i in flist:
        flist2.append(fieldname + i)
    df3 = df3[flist2]
    
    df3.to_csv(os.path.join(outpath, csvname))







def mba_chart_onetrace(table, xax = 'holder', yax = 'holder', mba = 'temp', x = 'None',y = 'None', yrange = [0,1], qu = 'None', remzeros = 0):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    
    if qu != 'None':
        qu
    if remzeros == 1:
        table.loc[~(table==0).all(axis=1)]
    
    
    
    def max_y_range(table):
        c =table.max(axis=0, numeric_only = True)
        print ('maxy' + str(round(max(c) +plot_dict[mba]['changemax'], plot_dict[mba]['changemin'])))
        #print ('maxy' + str(max(c) +plot_dict[mba]['changemax']))
        return round(max(c) +plot_dict[mba]['changemax'], plot_dict[mba]['changemin'])
        
        
    def min_y_range(table):
        c =table.min(axis=0, numeric_only = True)
        print ('minc' + str(min(c)))
        print ('miny' + str(round(min(c) -plot_dict[mba]['changemax'], plot_dict[mba]['changemin'])))   
        return round(min(c) -plot_dict[mba]['changemax'], plot_dict[mba]['changemin'])        

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
        "tickfont": {
      "size": axis_lab_font
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
    plot(fig, filename= plot_dict[mba]['title'] + '.html')
    
    

def mba_chart_threetrace(table, plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    
    if qu != 'None':
        qu
    if remzeros == 1:
        table.loc[~(table==0).all(axis=1)]
    
    def max_y_range(table):
        c =table.max(axis=0, numeric_only = True)
        print ('maxy' + str(round(max(c) +plot_dict[mba]['changemax'], plot_dict[mba]['changemin'])))
        #print ('maxy' + str(max(c) +plot_dict[mba]['changemax']))
        return round(max(c) +plot_dict[mba]['changemax'], plot_dict[mba]['changemin'])
        
        
    def min_y_range(table):
        c =table.min(axis=0, numeric_only = True)
        print ('minc' + str(min(c)))
        print ('miny' + str(round(min(c) -plot_dict[mba]['changemax'], plot_dict[mba]['changemin'])))   
        return round(min(c) -plot_dict[mba]['changemax'], plot_dict[mba]['changemin'])        

    trace1 = {
      "x": table[plot_dict[mba]['rfield']], 
      "y": table[pre + '_base_bau'], 
      "type":"bar",
      "name":"Reference<br>Scenario"
    }
    
    trace2 = {
      "x": table[plot_dict[mba]['rfield']], 
      "y": table[pre + '_base_med'], 
      "type":"bar",
       "name":"Medium<br>Infill"
    }
    trace3 = {
      "x": table[plot_dict[mba]['rfield']], 
      "y": table[pre + '_base_max'], 
"type":"bar",
 "name":"Max<br>Infill"
    }


    data = go.Data([trace1, trace2, trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": plot_dict[mba]['title'], 
      "titlefont": {
      "size": mba_title_font
          },
      "xaxis": {
        "autorange": True, 
        "type": "category",
        "tickfont": {
      "size": axis_lab_font
          }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [min_y_range(table), max_y_range(table)], 
        "title": plot_dict[mba]['ytitle'], 
        "type": "linear",
        "titlefont": {
                "size": axis_lab_font
          }
      },
        "annotations": [plot_dict[mba]['ann']
      
    ]
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= plot_dict[mba]['title'] + '.html')





#Dictionary entries
plot_dict['cropvalue'] ={'title':"2030 Projected Crop Value by Development Scenario",'changemax': 10000000,'changemin' :-7,'ytitle': "Crop Value (Millions of Dollars)", 'changefield':'usd_change', 'totfield':  'usd', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{
        "xref": "x",
        "yref": "y",
        "text":  'Reference Scenario Total Value: ' + 'holder' +'<br>Medium Infill Total Value: ' + 'holder',
        "y": 200000000,
        "x": 'Annual Cropland',
        "font": {
          "color": "rgb(0, 0, 0)",
          "size": 12
        },
        "showarrow": False
      }}

plot_dict['county_movement'] ={'title':"2014-2030 Projected Countywide Change in Terrestrial Movement Resistance by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'movement_potential', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['ecamovement'] ={'title':"2014-2030 Projected Change in Terrestrial Movement Resistance by Development Scenario in Essential Connectivity Areas",'changemax': 500,'changemin' :-3,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'movement_potential', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['flood100'] ={'title':"2014-2030 Projected Change in 100 Year Floodplain Landcover by Development Scenario",'changemax': 200,'changemin' :-3,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}



plot_dict['aquatic'] ={'title':"2014-2030 Projected Change in Landcover in Watersheds With High Aquatic Habitat Value by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares of Landcover", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['groundwater'] ={'title':"2014-2030 Projected Loss of Groundwater Recharge",'changemax': 1,'changemin' :-1,'ytitle': "Loss of Recharge (Acre Feet per Year)", 'changefield':'ac_ft_rec_lst', 'totfield':  'None','rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}





plot_dict['co_val_airpollute'] ={'title':"2014-2030 Projected Change in Carbon Monoxide Sequestration by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of CO", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}






plot_dict['flood500'] ={'title':"2014-2030 Projected Change in 500 Year Floodplain Landcover by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['lcchange'] ={'title':"2014-2030 Projected Change in Landcover by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'landcover', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['fmmp'] ={'title':"2014-2030 Projected Impact to Farmland by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares", 'changefield':'ha_loss', 'totfield':  'None', 'rfield' : 'fmmp_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['leach_nitrates'] ={'title':"2014-2030 Projected Change in Nitrate Leaching by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Nitrate", 'changefield':'tons_no3_change', 'totfield':  'tons_no3', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['no2_val_airpollute'] ={'title':"2014-2030 Projected Change in NO2 Sequestration by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['o3_val_airpollute'] ={'title':"2014-2030 Projected Change in O3 Sequestration by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['pca_cover_change'] ={'title':"2014-2030 Projected Change in Priority Conservation Area Landcover by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares",'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['pm2_5_val_airpollute'] ={'title':"2014-2030 Projected Change in PM 2.5 Sequestration by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['pm10_val_airpollute'] ={'title':"2014-2030 Projected Change in PM 10 Sequestration by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['runoff_nitrates'] ={'title':"2014-2030 Projected Change in Nitrate Runoff by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Nitrate", 'changefield':'tons_no3_change', 'totfield':  'tons_no3', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['scenic'] ={'title':"2014-2030 Projected Change in Highly Visible Landcover by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares",'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['so2_val_airpollute'] ={'title':"2014-2030 Projected Change in SO2 Sequestration by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['terrhab'] ={'title':"2014-2030 Projected Change in Terrestrial Habitat Quality by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Acres", 'changefield':'acres', 'totfield':  'None', 'rfield' : 'guild', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['watcon'] ={'title':"2014-2030 Projected Change in Water Usage by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Acre Feet of Water (Per Year)", 'changefield':'ac_ft_change', 'totfield':  'ac_ft', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['watint'] ={'title':"2014-2030 Projected Change of Watershed Integrity by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'Integrity_Class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}


#flist = ['_base_bau','_base_med','_base_max','_trt_bau','_trt_med','_trt_max']
#
#
#
#
#mbalist = ['aquatic','co_val_airpollute','county_movement','ecamovement','flood100','flood500','fmmp','groundwater','lcchange','leach_nitrates','no2_val_airpollute','o3_val_airpollute','pca_cover_change','pm2_5_val_airpollute','pm10_val_airpollute','runoff_nitrates','scenic','so2_val_airpollute','terrhab','watcon','watint','cropvalue'] #,'cropvalue'
#
#import glob
#
#csvlist = glob.glob(folder + '*.csv')
#combined = '\t'.join(csvlist)
#
#print (mbalist)
#print (combined)
#
#for i in mbalist:
#    if i in combined:
#        print (folder + '/' + i + '.csv')
#        if plot_dict[i]['sum'] == 1:
#            print ('Doing sum for ' + i)
#            dftest = mba_plot_tables_sum(folder + '/' + i + '.csv', outpath = outpath2, csvname = i + '_' + 'sum' + '.csv', changefield = plot_dict[i]['changefield'])
#        if plot_dict[i]['totfield'] != 'None':
#            print ('Doing tot for ' + i)
#            dftest = mba_plot_tables_rows(folder + '/' + i + '.csv', outpath=outpath2,csvname = i + '_' + 'total' + '.csv', fieldname = plot_dict[i]['totfield'],  rfield = plot_dict[i]['rfield'])
#            
#        if plot_dict[i]['changefield'] != 'None':
#            print ('Doing change for ' + i)
#            dftest = mba_plot_tables_rows(folder + '/' + i + '.csv', outpath=outpath2,csvname = i + '_' + 'change' + '.csv', fieldname = plot_dict[i]['changefield'],  rfield = plot_dict[i]['rfield'])
        













































































