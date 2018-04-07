# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:07:02 2018

@author: Dylan
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 14:15:37 2018

@author: mtukman
"""

#This code will produce charts and panels for merced report

#RIPARIAN RESTORATION CHARTS AND GRAPHS

#Countywide GHG Reductions from Riparian Restoration


def  riparian_reductions(folder):
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

    high = pd.read_csv(folder + '/carbon.csv')

    
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go



    
    trace1 = {
      "x": ["Riparian Restoration", "Reference"], 
      "y": [high['trt_bau_total'].sum(), high['carbon_base_max'].sum()], 
      "type": "bar",
      }
    
    
    data = go.Data([trace1])
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
    plot(fig, filename= 'Flying_M' + '.html')
    return fig
    

#def riparian_reductions(table_high = r'E:\Box\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\carbon.csv'):
#    import pandas as pd
#    high = pd.read_csv(table_high)
#    
#    import plotly.plotly as py
#    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#    #import plotly.plotly as py
#    from plotly import tools
#    import plotly.graph_objs as go
#    
#    trace1 = {
#      "x": ["2001", "2014", "2030"], 
#      "y": ["50793849", high['carbon2014'].sum(), high['trt_bau_total'].sum()], 
#      "connectgaps": False, 
#      "line": {"color": "rgb(26, 100, 26)"}, 
#      "marker": {
#        "color": "rgb(16, 82, 16)", 
#        "size": 7
#      }, 
#      "mode": "lines+markers", 
#      "name": "Tons Carbon RRE", 
#      "type": "scatter", 
#    }
#    trace2 = {
#      "x": ["2001", "2014", "2030"], 
#      "y": ["50793849", high['carbon2014'].sum(), high['carbon_base_bau'].sum()], 
#      "connectgaps": False, 
#      "line": {
#        "color": "rgb(31, 119, 180)", 
#        "width": 2.5
#      }, 
#      "marker": {
#        "color": "rgb(31, 119, 180)", 
#        "size": 7
#      }, 
#      "mode": "lines+markers", 
#      "name": "Tons Carbon Ref", 
#      "type": "scatter", 
#
#    }
#
#    fig = go.Figure(data=data, layout=layout)
#    plot(fig, filename= 'Flying_M' + '.html')
#    return fig


def wateruse_plot_RRE(high_folder):
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

    high = pd.read_csv(high_folder + '/watcon.csv')

       

    trace1 = {
      "x": ["Riparian Restoration", "Reference"], 
      "y": [high['ac_ft_trt_bau'].sum(),high['ac_ft_base_bau'].sum()], 
      "name": "Water Use", 
      "type": "bar"
    }



    data = go.Data([trace1])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": False, 
      "title": 'Water Use', 
      "titlefont": {
      "size": 24
          },
      "xaxis": {
        "autorange": True,  
        "title": ["Riparian Restoration", "Reference"], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,3], 
        "title": 'Acre Feet of Water Demand (Annual)', 
        "type": "linear"
      }
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'test' + '.html')
    
def cropvalue_plot_RRE(high_folder):
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

    high = pd.read_csv(high_folder + '/cropvalue.csv')

       

    trace1 = {
      "x": ["Riparian Restoration", "Reference"], 
      "y": [high['usd_trt_bau'].sum(),high['usd_base_bau'].sum()], 
      "name": "Water Use", 
      "type": "bar"
    }



    data = go.Data([trace1])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": False, 
      "title": 'Crop Value', 
      "titlefont": {
      "size": 24
          },
      "xaxis": {
        "autorange": True,  
        "title": ["Riparian Restoration", "Reference"], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,3], 
        "title": 'Crop Value (US Dollars)', 
        "type": "linear"
      }
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'test' + '.html')
    
    
def terrestrial_habitat_plot_RRE(high_folder):
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    high = pd.read_csv(high_folder + '/terrhab.csv')

    
    high2 = high[['guild','acres_trt_bau', 'acres_base_bau']]

    high3 = high2.loc[high2['guild'].isin(['mammals_avg_deg_acres','birds_avg_deg_acres','amphibians_avg_deg_acres'])]
    high4 = high2.loc[high2['guild'].isin(['mammals_avg_imp_acres','birds_avg_imp_acres','amphibians_avg_imp_acres'])]
 

    trace1 = {
      "x": ['Mammal Habitat Degraded','Bird Habitat Degraded','Amphibian Habitat Degraded'], 
      "y": high3['acres_trt_bau'], 
      "name": "Riparian Restoration Degraded", 
      "type": "bar"
    }
    trace2 = {
      "x": ['Mammal Habitat Degraded','Bird Habitat Degraded','Amphibian Habitat Degraded'], 
      "y": high3['acres_base_bau'], 
      "name": "Reference Degraded", 
      "type": "bar"
    }
    trace3 = {
      "x": ['Mammal Habitat Improved','Bird Habitat Improved','Amphibian Habitat Improved'], 
      "y": high4['acres_trt_bau'], 
      "name": "Riparian Restoration Improved", 
      "type": "bar"
    }
    trace4 = {
      "x": ['Mammal Habitat Improved','Bird Habitat Improved','Amphibian Habitat Improved'], 
      "y": high4['acres_base_bau'], 
      "name": "Reference Improved", 
      "type": "bar"
    }


    data = go.Data([trace1,trace2,trace3,trace4])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 

      "title": "San Joaquin Riparian Restoration - Terrestrial Habitat Quality", 
      "xaxis": {
        "autorange": True,  
        "title": ['Mammals','Birds','Amphibians'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [50496576.7792, 55507202.8908], 
        "title": "Average Acres of Degraded Habitat by Guild", 
        "type": "linear"
      }
    }

   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'test' + '.html')
    return fig
    
    
    
def  airquality_plot_RRE(high_folder, med_folder):
    import pandas as pd
    
    
    #Read O3
    
    high_co = pd.read_csv(high_folder + '/co_val_airpollute.csv')
    high_o3 = pd.read_csv(high_folder + '/o3_val_airpollute.csv')
    high_no2 = pd.read_csv(high_folder + '/no2_val_airpollute.csv')
    high_pm25 = pd.read_csv(high_folder + '/pm2_5_val_airpollute.csv')
    high_pm10 = pd.read_csv(high_folder + '/pm10_val_airpollute.csv')
    
    
    med_co = pd.read_csv(med_folder + '/co_val_airpollute.csv')
    med_o3 = pd.read_csv(med_folder + '/o3_val_airpollute.csv')
    med_no2 = pd.read_csv(med_folder + '/no2_val_airpollute.csv')
    med_pm25 = pd.read_csv(med_folder + '/pm2_5_val_airpollute.csv')
    med_pm10 = pd.read_csv(med_folder + '/pm10_val_airpollute.csv')

    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
 

    xlist = ['CO','O3','PM 10','PM 2.5','NO2']
    
    trace1 = {
      "x": xlist, 
      "y": [high_co['tons_trt_bau'].sum(), high_o3['tons_trt_bau'].sum(), high_no2['tons_trt_bau'].sum(),high_pm25['tons_trt_bau'].sum(),high_pm10['tons_trt_bau'].sum()], 
      "type": "bar",
      "name": "Full Development", 
      
      }
    trace2 = {
      "x": xlist, 
      "y": [med_co['tons_trt_bau'].sum(), med_o3['tons_trt_bau'].sum(), med_no2['tons_trt_bau'].sum(),med_pm25['tons_trt_bau'].sum(),med_pm10['tons_trt_bau'].sum()], 
      "type": "bar",
      "name": "Partial Development", 
      }
    trace3 = {
      "x": xlist, 
      "y": [high_co['tons_base_bau'].sum(), high_o3['tons_base_bau'].sum(), high_no2['tons_base_bau'].sum(),high_pm25['tons_base_bau'].sum(),high_pm10['tons_base_bau'].sum()], 
      "type": "bar",
      "name": "Conservation", 
      }


    data = go.Data([trace1, trace2,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": "Flying M Ranch - Air Pollutant Sequestration", 
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
        "title": 'Tons of Pollutant Sequestered', 
        "type": "linear"
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'Flying_M' + '.html')
    return fig
#terrestrial_habitat_plot(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_HigDev\plotting_tables\terrhab_change.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\plotting_tables\terrhab_change.csv")
#groundwater_plot(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_HigDev\plotting_tables\groundwater_sum.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\plotting_tables\groundwater_sum.csv")

#=======
#flying_m_reductions()



def  scenicvalue_plot_RRE(high_folder):
    import pandas as pd
    
    
    #Read O3
    
    high = pd.read_csv(high_folder + '/scenic.csv')




    highnat = high.loc[high['gen_class'] == 'Natural']
    highdev = high.loc[high['gen_class'] == 'Developed']
    highag = high.loc[high['gen_class'] == 'Agriculture']


    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go


    xlist = ['Riparian Restoration','Reference']
    
    
    
    trace1 = {
      "x": xlist, 
      "y": [highnat['ha_trt_bau'].sum(), highnat['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "Natural", 
      
      }
    trace2 = {
      "x": xlist, 
      "y": [highdev['ha_trt_bau'].sum(), highdev['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "Developed", 
      }
    trace3 = {
      "x": xlist, 
      "y": [highag['ha_trt_bau'].sum(), highag['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "Agriculture", 
      }
    
    data = go.Data([trace1, trace2,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": "Flying M Ranch - Landcover in Highly Visible Areas", 
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
        "title": 'Hectares of Land', 
        "type": "linear"
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'Flying_M' + '.html')



def  tconnect_plot_RRE(high_folder):
    import pandas as pd
    
    
    #Read O3
    
    high = pd.read_csv(high_folder + '/countymovement.csv')




    highnat = high.loc[high['movement_potential'] == 'high']
    highdev = high.loc[high['movement_potential'] == 'medium']
    highag = high.loc[high['movement_potential'] == 'low']


    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
 

    xlist = ['Riparian Restoration','Rererence']
    
    
    
    trace1 = {
      "x": xlist, 
      "y": [highnat['ha_trt_bau'].sum(), highnat['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "High Movement Potential", 
      
      }
    trace2 = {
      "x": xlist, 
      "y": [highdev['ha_trt_bau'].sum(), highdev['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "Medium Movement Potential", 
      }
    trace3 = {
      "x": xlist, 
      "y": [highag['ha_trt_bau'].sum(), highag['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "Low Movement Potential", 
      }
    
    data = go.Data([trace1,trace2,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": "Flying M Ranch - Terrestrial Connectivity", 
      "titlefont": {
      "size": 24
          },
      "xaxis": {
        "autorange": True, 
#        "title": ['highly developed', 'medium developed', 'conserved'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
        "title": 'Hectares of Terrestrial Movement Resistance Class', 
        "type": "linear"
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'Flying_M' + '.html')









#Saved Function Calls
    
def make_plots_sanjoaquin():



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    