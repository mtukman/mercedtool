# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 14:15:37 2018

@author: mtukman
"""

#This code will produce charts and panels for merced report

#RIPARIAN RESTORATION CHARTS AND GRAPHS

#Countywide GHG Reductions from Riparian Restoration


def flying_m_reductions(table_high = r'E:\Box\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_HigDev\carbon.csv', table_medium=r'E:\Box\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\carbon.csv'):
    import pandas as pd
    high = pd.read_csv(table_high)
    med = pd.read_csv(table_medium)
    
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
      "x": ["Full Development", "Partial Development", "Conservation"], 
      "y": [high['trt_bau_total'].sum(), med['trt_bau_total'].sum(), high['carbon_base_max'].sum()], 
      "type": "bar",
      "text": ['', '', 50]
      }
    
    
    data = go.Data([trace1])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": False, 
      "title": "Flying M Ranch - Avoided Conversion", 
      "titlefont": {
      "size": 24
          },
      "xaxis": {
        "autorange": True, 
        "title": ['highly developed', 'medium developed', 'conserved'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": False, 
        "range": [0, 200000], 
        #"range": [min_y_range(table), max_y_range(table)], 
        "title": 'Tons CO2 Equivalents', 
        "type": "linear"
      },
                  "annotations": [
      {
        "xref": "x",
        "yref": "y",
        "text":  str(round(high['carbon_base_max'].sum() - high['trt_bau_total'].sum(), 1))  + " tons <br> CO2e reductions <br> v. full development",
        "y": high['trt_bau_total'].sum(),
        "x": 2,
        "font": {
          "color": "rgb(252, 252, 252)",
          "size": 12
        },
        "showarrow": False
      }
    ]
    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'TT' + '.html')
    
<<<<<<< HEAD
def groundwater_plot(high_dev, med_dev):
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    high = pd.read_csv(high_dev)
    med = pd.read_csv(med_dev)
    
    high2 = high.loc[high['scenario'] == 'ref']
    med2 = med.loc[med['scenario'] == 'ref']

    def max_y_range(table):
        c =table.max(axis=0, numeric_only = True)
        return round(max(c) +plot_dict[1], plot_dict[2])
        
    def min_y_range(table):
        c =table.min(axis=0, numeric_only = True)
        return round(min(c) -plot_dict[1], plot_dict[2])        

    trace1 = {
      "x": ['Full Development'], 
      "y": high2['Treated'], 
      "name": "Full Development", 
      "type": "bar"
    }
    trace2 = {
      "x": ['Partial Development'], 
      "y": med2['Treated'], 
      "name": "Partial Development", 
      "type": "bar"
    }

    data = go.Data([trace1, trace2])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": 'Groundwater Recharge Loss', 
      "titlefont": {
      "size": 24
          },
      "xaxis": {
        "autorange": True, 
        "range": [0, 3], 
        "title": ['Full Development', 'Partial Development'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": False, 
        "range": [0,3], 
        "title": 'Acre Feet of Groundwater Recharge (Per Year) Lost', 
        "type": "linear"
      }
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'test' + '.html')


def terrestrial_habitat_plot(high_dev, med_dev):
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    high = pd.read_csv(high_dev)
    med = pd.read_csv(med_dev)
    
    high2 = high[['guild','acres_trt_bau']]
    med2 = med[['guild','acres_trt_bau']]
    
#    high3 = high2.iloc[0]
#    med3 = med2.iloc[0]
    high3 = high2.loc[high2['guild'].isin(['mammals_avg_deg_acres','birds_avg_deg_acres','amphibians_avg_deg_acres'])]
    med3 = med2.loc[med2['guild'].isin(['mammals_avg_deg_acres','birds_avg_deg_acres','amphibians_avg_deg_acres'])]
    
    def max_y_range(table):
        c =table.max(axis=0, numeric_only = True)
        return round(max(c) +plot_dict[1], plot_dict[2])
        
    def min_y_range(table):
        c =table.min(axis=0, numeric_only = True)
        return round(min(c) -plot_dict[1], plot_dict[2])        

    trace1 = {
      "x": high3['guild'], 
      "y": high3['acres_trt_bau'], 
      "name": "Full Development", 
      "type": "bar"
    }
    trace2 = {
      "x": med3['guild'], 
      "y": med3['acres_trt_bau'], 
      "name": "Partial Development", 
      "type": "bar"
    }

    data = go.Data([trace1, trace2])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": 'Terrestrial Habitat Impacts', 
      "titlefont": {
      "size": 24
          },
      "xaxis": {
        "autorange": True, 
#        "range": [0, 3], 
        "title": ['Full Development', 'Partial Development'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
#        "range": [0,3], 
        "title": 'Acres of Habitat Degraded', 
        "type": "linear"
      }
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'test' + '.html')
    
    
def fmmp_plot(high_dev, med_dev): #No difference between medium and high development. Check in arcmap and decide if want to use?
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    high = pd.read_csv(high_dev)
    med = pd.read_csv(med_dev)
    
    high2 = high[['fmmp_class','acres_trt_bau']]
    med2 = med[['fmmp_class','acres_trt_bau']]
    
#    high3 = high2.iloc[0]
#    med3 = med2.iloc[0]
    high3 = high2.loc[high2['guild'].isin(['mammals_avg_deg_acres','birds_avg_deg_acres','amphibians_avg_deg_acres'])]
    med3 = med2.loc[med2['guild'].isin(['mammals_avg_deg_acres','birds_avg_deg_acres','amphibians_avg_deg_acres'])]
    
    def max_y_range(table):
        c =table.max(axis=0, numeric_only = True)
        return round(max(c) +plot_dict[1], plot_dict[2])
        
    def min_y_range(table):
        c =table.min(axis=0, numeric_only = True)
        return round(min(c) -plot_dict[1], plot_dict[2])        

    trace1 = {
      "x": high3['guild'], 
      "y": high3['acres_trt_bau'], 
      "name": "Full Development", 
      "type": "bar"
    }
    trace2 = {
      "x": med3['guild'], 
      "y": med3['acres_trt_bau'], 
      "name": "Partial Development", 
      "type": "bar"
    }

    data = go.Data([trace1, trace2])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": 'Terrestrial Habitat Impacts', 
      "titlefont": {
      "size": 24
          },
      "xaxis": {
        "autorange": True, 
#        "range": [0, 3], 
        "title": ['Full Development', 'Partial Development'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
#        "range": [0,3], 
        "title": 'Acres of Habitat Degraded', 
        "type": "linear"
      }
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'test' + '.html')
    
    
    
def airquality_plot(high_dev_folder, med_dev_folder): #No difference between medium and high development. Check in arcmap and decide if want to use?
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    high = pd.read_csv(high_dev)
    med = pd.read_csv(med_dev)
    
    high2 = high[['fmmp_class','acres_trt_bau']]
    med2 = med[['fmmp_class','acres_trt_bau']]
    
#    high3 = high2.iloc[0]
#    med3 = med2.iloc[0]
    high3 = high2.loc[high2['guild'].isin(['mammals_avg_deg_acres','birds_avg_deg_acres','amphibians_avg_deg_acres'])]
    med3 = med2.loc[med2['guild'].isin(['mammals_avg_deg_acres','birds_avg_deg_acres','amphibians_avg_deg_acres'])]
    
    def max_y_range(table):
        c =table.max(axis=0, numeric_only = True)
        return round(max(c) +plot_dict[1], plot_dict[2])
        
    def min_y_range(table):
        c =table.min(axis=0, numeric_only = True)
        return round(min(c) -plot_dict[1], plot_dict[2])        

    trace1 = {
      "x": high3['guild'], 
      "y": high3['acres_trt_bau'], 
      "name": "Full Development", 
      "type": "bar"
    }
    trace2 = {
      "x": med3['guild'], 
      "y": med3['acres_trt_bau'], 
      "name": "Partial Development", 
      "type": "bar"
    }

    data = go.Data([trace1, trace2])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": 'Terrestrial Habitat Impacts', 
      "titlefont": {
      "size": 24
          },
      "xaxis": {
        "autorange": True, 
#        "range": [0, 3], 
        "title": ['Full Development', 'Partial Development'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
#        "range": [0,3], 
        "title": 'Acres of Habitat Degraded', 
        "type": "linear"
      }
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'test' + '.html')
#terrestrial_habitat_plot(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_HigDev\plotting_tables\terrhab_change.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\plotting_tables\terrhab_change.csv")
#groundwater_plot(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_HigDev\plotting_tables\groundwater_sum.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\plotting_tables\groundwater_sum.csv")

#=======
#flying_m_reductions()
#>>>>>>> 52bdb8f541bcc4a9aaa9953f39ba2fb0d0bc0005
