# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 15:49:39 2018

@author: Dylan
"""

def  riparian_reductions():
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    folder = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities"
    table = 'carbon'
    
    
    
    cam25 = pandas.read_csv(folder + '/compost_amendment_25/' + table + '.csv')
    cam100 = pandas.read_csv(folder + '/compost_amendment_100/' + table + '.csv')
    ccr25 = pandas.read_csv(folder + '/cover_cropping_25/' + table + '.csv')
    ccr100 = pandas.read_csv(folder + '/cover_cropping_100/' + table + '.csv')
    cag25 = pandas.read_csv(folder + '/grass_compost_amendment_25/' + table + '.csv')
    cag100 = pandas.read_csv(folder + '/grass_compost_amendment_100/' + table + '.csv')
    gra25 = pandas.read_csv(folder + '/grassland_resto_25/' + table + '.csv')
    gra100 = pandas.read_csv(folder + '/grassland_resto_100/' + table + '.csv')
    hpl25 = pandas.read_csv(folder + '/hedgerow_25/' + table + '.csv')
    hpl100 = pandas.read_csv(folder + '/hedgerow_100/' + table + '.csv')
    mul25 = pandas.read_csv(folder + '/mulching_25/' + table + '.csv')
    mul100 = pandas.read_csv(folder + '/mulching_100/' + table + '.csv')
    nfm25 = pandas.read_csv(folder + '/nfm_25/' + table + '.csv')
    nfm100 = pandas.read_csv(folder + '/nfm_100/' + table + '.csv')
    rre25 = pandas.read_csv(folder + '/RRE_COUNTY_30/' + table + '.csv')
    rre100 = pandas.read_csv(folder + '/RRE_COUNTY_100/' + table + '.csv')
    oak25 = pandas.read_csv(folder + '/oak_25/' + table + '.csv')
    oak100 = pandas.read_csv(folder + '/oak_100/' + table + '.csv') 
    urb25 = pandas.read_csv(folder + '/urb_25/' + table + '.csv')
    urb100 = pandas.read_csv(folder + '/urb_100/' + table + '.csv')


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go



    
    trace1 = {
      "x": ["25% Adoption", "100% Adoption"], 
      "y": [cam25['carbon_cam'].sum(), cam100['carbon_cam'].sum()], 
      "type": "bar",
      }
    trace2 = {
      "x": ["25% Adoption", "100% Adoption"], 
      "y": [ccr25['carbon_ccr'].sum(), ccr100['carbon_ccr'].sum()], 
      "type": "bar",
      }
    trace3 = {
      "x": ["25% Adoption", "100% Adoption"], 
      "y": [cam25['carbon_cag'].sum(), cam100['carbon_cag'].sum()], 
      "type": "bar",
      }
    trace4 = {
      "x": ["25% Adoption", "100% Adoption"], 
      "y": [cam25['carbon_gra'].sum(), cam100['carbon_gra'].sum()], 
      "type": "bar",
      }
    trace5 = {
      "x": ["25% Adoption", "100% Adoption"], 
      "y": [cam25['carbon_hpl'].sum(), cam100['carbon_hpl'].sum()], 
      "type": "bar",
      }
    
    

    
    
    data = go.Data([trace1, trace2, trace3, trace4, trace5])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": False, 
      "title": "San Joaquin Riparian Restoration - Carbon Reductions", 
      "titlefont": {
      "size": 24
          },
      "xaxis": {
        "autorange": True, 
        "title": ['highly developed', 'medium developed', 'conserved'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0, 200000], 
        #"range": [min_y_range(table), max_y_range(table)], 
        "title": 'Tons CO2 Equivalents', 
        "type": "linear"
      },

      }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'Flying_M' + '.html')