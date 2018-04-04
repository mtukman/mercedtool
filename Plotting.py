
folder = "E:/Temp/tooloutputs/RRE_FULL/"

mba_title_font = 24
plot_dict = {}

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







def mba_chart_3scenario(table, plot_dict, xax = 'holder', yax = 'holder'):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    
    def max_y_range(table):
        c =table.max(axis=0, numeric_only = True)
        return round(max(c) +plot_dict[1], plot_dict[2])
        
    def min_y_range(table):
        c =table.min(axis=0, numeric_only = True)
        return round(min(c) -plot_dict[1], plot_dict[2])        

    trace1 = {
      "x": table['scenario'], 
      "y": table['Untreated'], 
      "name": "Untreated", 
      "type": "bar"
    }
    trace2 = {
      "x": table['scenario'], 
      "y": table['Treated'], 
      "name": "Treated", 
      "type": "bar"
    }

    data = go.Data([trace1, trace2])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": plot_dict[0], 
      "titlefont": {
      "size": mba_title_font
          },
      "xaxis": {
        "autorange": True, 
        "range": [-0.5, 2.5], 
        "title": "Scenario", 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": False, 
        "range": [min_y_range(table), max_y_range(table)], 
        "title": plot_dict[3], 
        "type": "linear"
      }
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= plot_dict[0] + '.html')





def mb_panel ():
    import plotly
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    
    from plotly import tools
    import plotly.graph_objs as go
    scenarios = ['High Intensity', 'Medium Intensity', 'Low Intensity']
    terrhab = ['Bird',  'Mammal', 'Reptile', 'T&E']
    marker=dict( color='rgb(158,202,225)', line=dict( color='rgb(8,48,107)', width=1.5))
    trace1 = go.Bar(x=scenarios, y=[4, 5, 6], marker = marker)
    trace2 = go.Bar(x=scenarios, y=[50, 60, 70], marker = marker)
    trace3 = go.Bar(x=scenarios, y=[600, 700, 800], marker = marker)
    trace4 = go.Bar(x=scenarios, y=[7000, 8000, 9000], marker = marker)
    trace5 = go.Bar(x=scenarios, y=[7000, 8000, 9000], marker = marker)
    trace6 = go.Bar(x =terrhab, y=[15, 56, 10, 2], marker = marker)
    
    
    fig = tools.make_subplots(rows=2, cols=3, subplot_titles=('Groundwater Recharge', 'Ag Land Quality',
                                                              'Air Quality', 'Scenic Value', 'Scenic Value','Acres Degraded Terrestrial Habitat' ))
    
    fig.layout.titlefont.size= 22
    fig.layout.title = 'Avoided Conversion Benefits - Flying M Ranch'
    fig.layout.showlegend=False
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 1, 3)
    fig.append_trace(trace4, 2, 1)
    fig.append_trace(trace5, 2, 2)
    fig.append_trace(trace6, 2, 3)
    layout =go.Layout(showlegend=False)
    #fig = go.Figure(data=data, layout=layout)
    plot(fig, filename='multiple-subplots2.html')
    




#Dictionary entries
plot_dict['groundwater'] ={'title':"2014-2030 Projected Loss of Groundwater Recharge",'max': 1,'min' :-1,'ytitle': "Loss of Recharge (Acre Feet per Year)", 'changefield':'ac_ft_rec_lst', 'totfield':  'None','rfield' : 'landcover', 'sum': 1}

plot_dict['cropvalue'] ={'title':"2014-2030 Projected Change in Crop Value by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Crop Value (Millions of Dollars)", 'changefield':'usd_change', 'totfield':  'usd', 'rfield' : 'landcover', 'sum': 1}

plot_dict['aquatic'] ={'title':"2014-2030 Projected Change in Landcover in Watersheds With High Aquatic Habitat Value by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Hectares of Landcover", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0}

plot_dict['co_val_airpollute'] ={'title':"2014-2030 Projected Change in Carbon Monoxide Sequestration by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Tons of CO", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1}

plot_dict['county_movement'] ={'title':"2014-2030 Projected Countywide Change in Terrestrial Movement Resistance by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'movement_potential', 'sum': 0}

plot_dict['ecamovement'] ={'title':"2014-2030 Projected Change in Terrestrial Movement Resistance by Development Scenario in Essential Connectivity Areas",'max': 5000000,'min' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'movement_potential', 'sum': 0}

plot_dict['flood100'] ={'title':"2014-2030 Projected Change in 100 Year Floodplain Landcover by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0}

plot_dict['flood500'] ={'title':"2014-2030 Projected Change in 500 Year Floodplain Landcover by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0}

plot_dict['lcchange'] ={'title':"2014-2030 Projected Change in Landcover by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'landcover', 'sum': 0}

plot_dict['fmmp'] ={'title':"2014-2030 Projected Impact to Farmland by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Hectares", 'changefield':'ha_loss', 'totfield':  'None', 'rfield' : 'fmmp_class', 'sum': 0}

plot_dict['leach_nitrates'] ={'title':"2014-2030 Projected Change in Nitrate Leaching by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Tons of Nitrate", 'changefield':'kgs_no3_change', 'totfield':  'kgs_no3', 'rfield' : 'landcover', 'sum': 1}

plot_dict['no2_val_airpollute'] ={'title':"2014-2030 Projected Change in NO2 Sequestration by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1}

plot_dict['o3_val_airpollute'] ={'title':"2014-2030 Projected Change in O3 Sequestration by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1}

plot_dict['pca_cover_change'] ={'title':"2014-2030 Projected Change in Priority Conservation Area Landcover by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Hectares",'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'landcover', 'sum': 1}

plot_dict['pm2_5_val_airpollute'] ={'title':"2014-2030 Projected Change in PM 2.5 Sequestration by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1}

plot_dict['pm10_val_airpollute'] ={'title':"2014-2030 Projected Change in PM 10 Sequestration by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1}

plot_dict['runoff_nitrates'] ={'title':"2014-2030 Projected Change in Nitrate Runoff by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Tons of Nitrate", 'changefield':'kgs_no3_change', 'totfield':  'kgs_no3', 'rfield' : 'landcover', 'sum': 1}

plot_dict['scenic'] ={'title':"2014-2030 Projected Change in Highly Visible Landcover by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Hectares",'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0}

plot_dict['so2_val_airpollute'] ={'title':"2014-2030 Projected Change in SO2 Sequestration by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1}

plot_dict['terrhab'] ={'title':"2014-2030 Projected Change in Terrestrial Habitat Quality by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Acres", 'changefield':'acres', 'totfield':  'None', 'rfield' : 'guild', 'sum': 0}

plot_dict['watcon'] ={'title':"2014-2030 Projected Change in Water Usage by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Acre Feet of Water (Per Year)", 'changefield':'ac_ft_change', 'totfield':  'ac_ft', 'rfield' : 'landcover', 'sum': 1}

plot_dict['watint'] ={'title':"2014-2030 Projected Change of Watershed Integrity by Development Scenario",'max': 5000000,'min' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'Integrity_Class', 'sum': 0}


flist = ['_base_bau','_base_med','_base_max','_trt_bau','_trt_med','_trt_max']




mbalist = ['aquatic','co_val_airpollute','county_movement','ecamovement','flood100','flood500','fmmp','groundwater','lcchange','leach_nitrates','no2_val_airpollute','o3_val_airpollute','pca_cover_change','pm2_5_val_airpollute','pm10_val_airpollute','runoff_nitrates','scenic','so2_val_airpollute','terrhab','watcon','watint','cropvalue'] #,'cropvalue'

import glob

csvlist = glob.glob(folder + '*.csv')
combined = '\t'.join(csvlist)

print (mbalist)
print (combined)
for i in mbalist:
    if i in combined:
        print (folder + '/' + i + '.csv')
        if plot_dict[i]['sum'] == 1:
            print ('Doing sum for ' + i)
            dftest = mba_plot_tables_sum(folder + '/' + i + '.csv', outpath='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/plot_tables/', csvname = i + '_' + 'sum' + '.csv', changefield = plot_dict[i]['changefield'])
        if plot_dict[i]['totfield'] != 'None':
            print ('Doing tot for ' + i)
            dftest = mba_plot_tables_rows(folder + '/' + i + '.csv', outpath='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/plot_tables/',csvname = i + '_' + 'total' + '.csv', fieldname = plot_dict[i]['totfield'],  rfield = plot_dict[i]['rfield'])
            
        if plot_dict[i]['changefield'] != 'None':
            print ('Doing change for ' + i)
            dftest = mba_plot_tables_rows(folder + '/' + i + '.csv', outpath='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/plot_tables/',csvname = i + '_' + 'change' + '.csv', fieldname = plot_dict[i]['changefield'],  rfield = plot_dict[i]['rfield'])













































































