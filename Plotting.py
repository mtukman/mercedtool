mba_title_font = 24

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
    return all_acts

def mba_chart_cropvalue(table, title = "2014-2030 Projected Loss of Groundwater Recharge"):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    
    def max_y_range(table):
        c =table.max(axis=0, numeric_only = True)
        return round(max(c) +5, -1)
        
    def min_y_range(table):
        c =table.min(axis=0, numeric_only = True)
        return round(min(c) -5, -1)        

    trace1 = {
      "x": table['Scenario'], 
      "y": table['Untreated'], 
      "name": "Untreated", 
      "type": "bar"
    }
    trace2 = {
      "x": table['Scenario'], 
      "y": table['Treated'], 
      "name": "Treated", 
      "type": "bar"
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
        "range": [-0.5, 2.5], 
        "title": "Scenario", 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": False, 
        "range": [min_y_range(table), max_y_range(table)], 
        "title": "Loss of Recharge (Acre Feet per Year)", 
        "type": "linear"
      }
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= title + '.html')




def mba_gwater_plot_tables(csv='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/groundwater.csv', outpath='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/plot_tables/'):
    import os
    import pandas as pd 
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    
    df = pd.read_csv(csv)
    df3 =df.fillna(0)
    gwrc = pd.DataFrame(columns=['Untreated', 'Treated'])
    gwrc.loc[len(gwrc)] = [df3.sum(axis=0)['ac_ft_rec_lst_base_bau'], df3.sum(axis=0)['ac_ft_rec_lst_trt_bau']]
    gwrc.loc[len(gwrc)] = [df3.sum(axis=0)['ac_ft_rec_lst_base_med'], df3.sum(axis=0)['ac_ft_rec_lst_trt_med']]
    gwrc.loc[len(gwrc)] = [df3.sum(axis=0)['ac_ft_rec_lst_base_max'], df3.sum(axis=0)['ac_ft_rec_lst_trt_max']]
    gwrc['scenario'] = ['ref', 'med', 'max']
    gwrc.to_csv(os.path.join(outpath, 'plt_groundwater.csv'))
    return gwrc

def mba_chart_gwater(table, title = "2014-2030 Projected Loss of Groundwater Recharge"):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    
    def max_y_range(table):
        c =table.max(axis=0, numeric_only = True)
        return round(max(c) +5, -1)
        
    def min_y_range(table):
        c =table.min(axis=0, numeric_only = True)
        return round(min(c) -5, -1)        

    trace1 = {
      "x": table['Scenario'], 
      "y": table['Untreated'], 
      "name": "Untreated", 
      "type": "bar"
    }
    trace2 = {
      "x": table['Scenario'], 
      "y": table['Treated'], 
      "name": "Treated", 
      "type": "bar"
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
        "range": [-0.5, 2.5], 
        "title": "Scenario", 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": False, 
        "range": [min_y_range(table), max_y_range(table)], 
        "title": "Loss of Recharge (Acre Feet per Year)", 
        "type": "linear"
      }
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= title + '.html')