# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 14:15:37 2018

@author: mtukman
"""

#This code will produce charts and panels for merced report

#RIPARIAN RESTORATION CHARTS AND GRAPHS

#Countywide GHG Reductions from Riparian Restoration
carb01 = 50793849
carb14 = 52406560
titlefont = 18
large_x_labs = 14

def  flyingm_reductions(table_high = r'E:\Box\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_HighDev\carbon.csv', table_medium=r'E:\Box\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\carbon.csv', outfile = 'C:/temp/test.png'):
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
      "x": ["Full<br>Development", "Partial<br>Development", "Conservation"], 
      "y": [high['trt_bau_total'].sum(), med['trt_bau_total'].sum(), high['carbon_base_max'].sum()], 
      "type": "bar",
      }
    
    
    data = go.Data([trace1])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": False, 
      "title": "Flying M Ranch - 2030 GHG Reductions from Avoided Conversion", 
      "titlefont": {
      "size": titlefont
          },
      "xaxis": {
        "autorange": True, 
        "title": ["Full<br>Development", "Partial<br>Development", "Conservation"], 
        "type": "category",
        "tickfont": {
          "color": "black",
          "size": large_x_labs
        }, 
      }, 
      "yaxis": {
        "autorange": False, 
        "range": [0, 200000], 
        #"range": [min_y_range(table), max_y_range(table)], 
        "title": 'Tons CO2 Equivalents', 
        "type": "linear",
        "titlefont": {
          "color": "black",
          "size": large_x_labs
        },
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
    py.image.save_as(fig, outfile, format='png')
    return fig

def countywide_reductions_RRE(table_high = r'E:\Box\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\carbon.csv', outfile = 'C:/temp/test.png'):
    import pandas as pd
    high = pd.read_csv(table_high)
    
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    
    trace1 = {
      "x": ["2001", "2014", "2030"], 
      "y": [carb01, carb14, high['carbon_base_bau'].sum()], 
      "connectgaps": False, 
      "line": {"color": "rgb(25, 25, 112)",
               "width": 2.5}, 
      "marker": {
        "color": "rgb(31, 119, 180)", 
        "size": 7
      }, 
      "mode": "lines+markers", 
      "name": "Reference", 
      "type": "scatter", 
    }
    trace2 = {
      "x": ["2001", "2014", "2030"], 
      "y": [carb01, carb14, high['trt_bau_total'].sum()], 
      "connectgaps": False, 
      "line": {
        "color": "rgb(34,139,34)"
      }, 
      "marker": {
        "color": "rgb(31, 119, 180)", 
        "size": 7
      }, 
      "mode": "lines+markers", 
      "name": "Riparian<br>Restoration", 
      "type": "scatter", 

    }
    layout = {
  "autosize": True, 
  "hovermode": "closest", 
  "showlegend": True, 
  "title": "2014-2030 Countywide GHG Reductions from Fully Adopted Riparian Restoration", 
        "titlefont": {
      "size": 16
          },
  "xaxis": {
    "autorange": True, 
    "range": [2001, 2031.7864606], 
    "title": "Year", 
    "type": "linear"
  }, 
  "yaxis": {
    "autorange": True, 
    "range": [carb01, 55507202.8908], 
    "title": "Tons CO<sub>2</sub> Equivalents", 
    "type": "linear",
    "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
  }
}
    
    data =  go.Data([trace2, trace1])
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'Countywide_reductions_rre' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig

def countywide_reductions_AC(table_high = r'E:\Box\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\carbon.csv', outfile = 'C:/temp/test.png'):
    import pandas as pd
    high = pd.read_csv(table_high)
    
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    
    trace1 = {
      "x": ["2014", "2030"], 
      "y": ["52406560", high['carbon_base_max'].sum()], 
      "connectgaps": False, 
      "line": {"color": "rgb(26, 100, 26)"}, 
      "marker": {
        "color": "rgb(16, 82, 16)", 
        "size": 7
      }, 
      "mode": "lines+markers", 
      "name": "Max<br>Infill", 
      "type": "scatter", 
    }
    trace2 = {
      "x": ["2014", "2030"], 
      "y": ["52406560", high['carbon_base_bau'].sum()], 
      "connectgaps": False, 
      "line": {
        "color": "rgb(31, 119, 180)", 
        "width": 2.5
      }, 
      "marker": {
        "color": "rgb(31, 119, 180)", 
        "size": 7
      }, 
      "mode": "lines+markers", 
      "name": "Reference", 
      "type": "scatter", 

    }
    layout = {
  "autosize": True, 
  "hovermode": "closest", 
  "showlegend": True, 
  "title": "2030 Avoided Conversion - Max Infill v. Reference Scenario", 
        "titlefont": {
      "size": titlefont
          },
  "xaxis": {
    "autorange": True, 
    "range": [2014, 2031.7864606], 
    "title": "Year", 
    "type": "linear"
  }, 
  "yaxis": {
    "autorange": True, 
    "range": [52406576.7792, 55507202.8908], 
    "title": "Tons CO<sub>2</sub> Equivalents", 
    "type": "linear",
    "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
  }
}
    
    data =  go.Data([trace1, trace2])
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'Flying_M_reductions' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig


def countywide_reductions_AG(table_hr= r'E:/Box/Box Sync/Merced Project/Tool/outputs/activities/hedgerow_100/carbon.csv', table_cc = 'E:/Box/Box Sync/Merced Project/Tool/outputs/activities/cover_croppoing_100/carbon.csv', outfile = 'C:/temp/test.png'):
    import pandas as pd
    hr = pd.read_csv(table_hr)
    cc = pd.read_csv(table_cc)
    
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    
    trace1 = {
      "x": ["2001", "2014", "2030"], 
      "y": [carb01, carb14, hr['trt_bau_total'].sum() + cc['carbon_ccr'].sum() ], 
      "connectgaps": False, 
      "line": {"color": "rgb(26, 100, 26)"}, 
      "marker": {
        "color": "rgb(16, 82, 16)", 
        "size": 7
      }, 
      "mode": "lines+markers", 
      "name": "2030 Hedgerows<br>and Cover Cropping-<br>Fully Adopted", 
      "type": "scatter", 
    }
    trace2 = {
      "x": ["2001", "2014", "2030"], 
      "y": [carb01, carb14, hr['carbon_base_bau'].sum()], 
      "connectgaps": False, 
      "line": {
        "color": "rgb(31, 119, 180)", 
        "width": 2.5
      }, 
      "marker": {
        "color": "rgb(31, 119, 180)", 
        "size": 7
      }, 
      "mode": "lines+markers", 
      "name": "Reference", 
      "type": "scatter", 

    }
    layout = {
  "autosize": True, 
  "hovermode": "closest", 
  "showlegend": True, 
  "title": "2014-2030 Countywide GHG Reductions from Cover Cropping and Hedgerow Planting", 
        "titlefont": {
      "size": 16
          },
  "xaxis": {
    "autorange": True, 
    "range": [2001, 2031.7864606], 
    "title": "Year", 
    "type": "linear"
  }, 
  "yaxis": {
    "autorange": True, 
    "range": [50706576.7792, 55507202.8908], 
    "title": "Tons CO<sub>2</sub> Equivalents", 
    "type": "linear",
            "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
  }
}
    
    data =  go.Data([trace1, trace2])
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'AG Reductions' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig







def groundwater_plot_AC(high_folder, med_folder, outfile):
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    import os
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

    high = pd.read_csv(os.path.join(high_folder + '/groundwater.csv'))
    med = pd.read_csv(os.path.join(med_folder + '/groundwater.csv'))
       

    trace1 = {
      "x": ['Full Development','Partial Development'], 
      "y": [high['ac_ft_rec_lst_trt_bau'].sum(), med['ac_ft_rec_lst_trt_bau'].sum()], 
      "name": "Flying M Ranch - Groundwater Recharge Loss", 
      "type": "bar"
    }


    data = go.Data([trace1])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": False, 
      "title": 'Flying M Ranch - 2030 Groundwater Recharge Loss', 
      "titlefont": {
      "size": titlefont
          },
      "xaxis": {
        "autorange": True, 
        "range": [0, 3], 
        "title": ['Full<br>Development', 'Partial<br>Development'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": False, 
        "range": [0,3], 
        "title": 'Acre Feet of Groundwater Recharge (Per Year) Lost', 
        "type": "linear",
        "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      }
    }
   
    fig = go.Figure(data=data, layout=layout)

    plot(fig, filename= 'groundwater_recharge' + '.html')
    py.image.save_as(fig, outfile, format='png')

    plot(fig, filename= 'test' + '.html')

    return fig


def wateruse_plot_AC(high_folder, med_folder, outfile):
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

    high = pd.read_csv(high_folder + '/watcon.csv')
    med = pd.read_csv(med_folder + '/watcon.csv')
       

    trace1 = {
      "x": ['Full Development','Partial Development', 'Conservation'], 
      "y": [high['ac_ft_change_dev_flagged'].sum(), med['ac_ft_change_dev_flagged'].sum(),med['ac_ft_base_med'].sum()], 
      "name": "Flying M Ranch - 2030 Water Use", 
      "type": "bar"
    }



    data = go.Data([trace1])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": False, 
      "title": 'Flying M Ranch - 2030 Water Use', 
      "titlefont": {
      "size": titlefont
          },
      "xaxis": {
        "autorange": True,  
        "title": ['Full<br>Development', 'Partial<br>Development', 'Conservation'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,3], 
        "title": 'Acre Feet of Water Demand (Annual)', 
        "type": "linear",
        "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      }
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'wateruse' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig
    
def terrestrial_habitat_plot_AC(high_folder, med_folder, outfile):   #ADD THREATENED AND ENGANGERED
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    high = pd.read_csv(high_folder + '/terrhab.csv')
    med = pd.read_csv(med_folder + '/terrhab.csv')
    
    high2 = high[['guild','acres_trt_bau']]
    med2 = med[['guild','acres_trt_bau']]

    high3 = high2.loc[high2['guild'].isin(['mammals_avg_deg_acres','birds_avg_deg_acres','amphibians_avg_deg_acres', 'tes_avg_deg_acres'])]
    med3 = med2.loc[med2['guild'].isin(['mammals_avg_deg_acres','birds_avg_deg_acres','amphibians_avg_deg_acres', 'tes_avg_deg_acres'])]
 

    trace1 = {
      "x": ['Mammals','Birds','Amphibians', 'Threatened &<br>Endangered'], 
      "y": high3['acres_trt_bau'], 
      "name": "Full<br>Development", 
      "type": "bar"
    }
    trace2 = {
      "x": ['Mammals','Birds','Amphibians', 'Threatened &<br>Endangered'], 
      "y": med3['acres_trt_bau'], 
      "name": "Partial<br>Development", 
      "type": "bar"
    }


    data = go.Data([trace1, trace2])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 

      "title": "Flying M Ranch - 2030 Terrestrial Habitat Degradation", 
            "titlefont": {
      "size": titlefont
          },
      "xaxis": {
        "autorange": True,  
        "title": ['Mammals','Birds','Amphibians', 'Threatened &<br>Endangered'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [50496576.7792, 55507202.8908], 
        "title": "Acres of Degraded Habitat", 
        "type": "linear",
                "titlefont": {
          "color": "black",
          "size": 12
        }
      }
    }

   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'terr_hab' + '.html')
    
    py.image.save_as(fig, outfile, format='png')
    return fig
    
def  airquality_plot_AC(high_folder, med_folder, outfile):
    import pandas as pd
    
    
    #Read O3
    
    high_co = pd.read_csv(high_folder + '/co_val_airpollute.csv')
    high_o3 = pd.read_csv(high_folder + '/o3_val_airpollute.csv')
    high_no2 = pd.read_csv(high_folder + '/no2_val_airpollute.csv')
    high_pm25 = pd.read_csv(high_folder + '/pm2_5_val_airpollute.csv')
    high_pm10 = pd.read_csv(high_folder + '/pm10_val_airpollute.csv')
    high_so2 = pd.read_csv(high_folder + '/so2_val_airpollute.csv')
    
    
    med_co = pd.read_csv(med_folder + '/co_val_airpollute.csv')
    med_o3 = pd.read_csv(med_folder + '/o3_val_airpollute.csv')
    med_no2 = pd.read_csv(med_folder + '/no2_val_airpollute.csv')
    med_pm25 = pd.read_csv(med_folder + '/pm2_5_val_airpollute.csv')
    med_pm10 = pd.read_csv(med_folder + '/pm10_val_airpollute.csv')
    med_so2 = pd.read_csv(high_folder + '/so2_val_airpollute.csv')

    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
 

    xlist = ['CO','O<sub>3</sub>','PM 10','PM 2.5','NO<sub>2</sub>', 'SO<sub>2</sub>']
    
    trace1 = {
      "x": xlist, 
      "y": [high_co['tons_trt_bau'].sum(), high_o3['tons_trt_bau'].sum(), high_no2['tons_trt_bau'].sum(),high_pm25['tons_trt_bau'].sum(),high_pm10['tons_trt_bau'].sum(),high_so2['tons_trt_bau'].sum() ], 
      "type": "bar",
      "name": "Full<br>Development", 
      
      }
    trace2 = {
      "x": xlist, 
      "y": [med_co['tons_trt_bau'].sum(), med_o3['tons_trt_bau'].sum(), med_no2['tons_trt_bau'].sum(),med_pm25['tons_trt_bau'].sum(),med_pm10['tons_trt_bau'].sum(),med_so2['tons_trt_bau'].sum() ], 
      "type": "bar",
      "name": "Partial<br>Development", 
      }
    trace3 = {
      "x": xlist, 
      "y": [high_co['tons_base_bau'].sum(), high_o3['tons_base_bau'].sum(), high_no2['tons_base_bau'].sum(),high_pm25['tons_base_bau'].sum(),high_pm10['tons_base_bau'].sum(),high_so2['tons_base_bau'].sum() ], 
      "type": "bar",
      "name": "Conservation", 
      }


    data = go.Data([trace1, trace2,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": "Flying M Ranch - 2030 Air Pollutant Sequestration", 
      "titlefont": {
      "size": titlefont
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
        "type": "linear",
                "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'airpoll' + '.html')
    
    py.image.save_as(fig, outfile, format='png')
    return fig
#terrestrial_habitat_plot(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_HighDev\plotting_tables\terrhab_change.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\plotting_tables\terrhab_change.csv")
#groundwater_plot(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_HighDev\plotting_tables\groundwater_sum.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\plotting_tables\groundwater_sum.csv")

#=======
#flying_m_reductions()



def  scenicvalue_plot_AC(high_folder, med_folder, outfile):
    import pandas as pd
    
    
    #Read O3
    
    high = pd.read_csv(high_folder + '/scenic.csv')

    med = pd.read_csv(med_folder + '/scenic.csv')



    highnat = high.loc[high['gen_class'] == 'Natural']
    highdev = high.loc[high['gen_class'] == 'Developed']
    highag = high.loc[high['gen_class'] == 'Agriculture']
    
    mednat = med.loc[med['gen_class'] == 'Natural']
    meddev = med.loc[med['gen_class'] == 'Developed']
    medag = med.loc[med['gen_class'] == 'Agriculture']

    import plotly.plotly as py
    
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    
    def max_y_range(table):
        c =table.max(axis=0, numeric_only = True)
        return round(max(c) +plot_dict[1], plot_dict[2])
#        
#    def min_y_range(table):
#        c =table.min(axis=0, numeric_only = True)
#        return round(min(c) -plot_dict[1], plot_dict[2])   

    xlist = ['Full<br>Development','Partial<br>Development','Conservation']
    
    
    
    trace1 = {
      "x": xlist, 
      "y": [highnat['ha_trt_bau'].sum(), mednat['ha_trt_bau'].sum(), highnat['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "Natural", 
      
      }
    trace2 = {
      "x": xlist, 
      "y": [highdev['ha_trt_bau'].sum(), meddev['ha_trt_bau'].sum(), highdev['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "Developed", 
      }
    trace3 = {
      "x": xlist, 
      "y": [highag['ha_trt_bau'].sum(), medag['ha_trt_bau'].sum(), highag['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "Agriculture", 
      }
    
    data = go.Data([trace1, trace2,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": "Flying M Ranch - 2030 Landcover in Highly Visible Areas", 
      "titlefont": {
      "size": titlefont
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
        "type": "linear",
                "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'scenic' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig

def  tconnect_plot_AC(high_folder, med_folder, outfile):
    import pandas as pd
    
    
    #Read O3
    
    high = pd.read_csv(high_folder + '/countymovement.csv')

    med = pd.read_csv(med_folder + '/countymovement.csv')



    highnat = high.loc[high['movement_potential'] == 'high']
    highdev = high.loc[high['movement_potential'] == 'medium']
    highag = high.loc[high['movement_potential'] == 'low']
    
    mednat = med.loc[med['movement_potential'] == 'high']
    meddev = med.loc[med['movement_potential'] == 'medium']
    medag = med.loc[med['movement_potential'] == 'low']

    import plotly.plotly as py
    py.sign_in('mtukman', 'qfRazO2xuHUGVQH5rJhH')
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
 

    xlist = ['Full<br>Development','Partial<br>Development']
    
    
    
    trace1 = {
      "x": xlist, 
      "y": [highnat['ha_change_trt_bau'].sum(), mednat['ha_change_trt_bau'].sum()], 
      "type": "bar",
      "name": "High<br>Movement<br>Potential", 
      
      }
    trace3 = {
      "x": xlist, 
      "y": [highag['ha_change_trt_bau'].sum(), medag['ha_change_trt_bau'].sum()], 
      "type": "bar",
      "name": "Low<br>Movement<br>Potential", 
      }
    
    data = go.Data([trace1,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": "Flying M Ranch - 2030 Terrestrial Connectivity", 
      "titlefont": {
      "size": titlefont
          },
      "xaxis": {
        "autorange": True, 
#        "title": ['highly developed', 'medium developed', 'conserved'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
        "title": 'Change in Hectares of Movement Type', 
        "type": "linear",
        "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'terrcon' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig

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
    oak25 = pd.read_csv(folder + '/oak_25/' + table + '.csv')
    oak100 = pd.read_csv(folder + '/oak_100/' + table + '.csv') 
    urb25 = pd.read_csv(folder + '/urb_25/' + table + '.csv')
    urb100 = pd.read_csv(folder + '/urb_100/' + table + '.csv')
 
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


def  reductions_RRE(folder, outfile):
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
      "x": ["Riparian<br>Restoration", "Reference"], 
      "y": [high['trt_bau_total'].sum(), high['carbon_base_max'].sum()], 
      "type": "bar",
      }
        
    data = go.Data([trace1])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": False, 
      "title": "2014-2030 GHG Reductions from Riparian Restoration on the San Joaquin R.", 
      "titlefont": {
      "size": 16
          },

      "xaxis": {
        "autorange": True, 
        "type": "category",
            "tickfont": {
          "color": "black",
          "size": large_x_labs
        }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0, 200000], 
        #"range": [min_y_range(table), max_y_range(table)], 
        "title": 'Tons CO<sub>2</sub> Equivalents', 
        "type": "linear",
        "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      },
                                "annotations": [
      {
        "xref": "x",
        "yref": "y",
        "text":  str(round( high['trt_bau_total'].sum() -high['carbon_base_max'].sum(), 1))  + " tons <br> CO<sub>2</sub>e reductions <br> v. reference",
        "y": high['carbon_base_max'].sum(),
        "x": 'Riparian<br>Restoration',
        "font": {
          "color": "rgb(252, 252, 252)",
          "size": 14
        },
        "showarrow": False
      }
    ]

    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'Flying_M' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig
    

def wateruse_plot_RRE(high_folder, outfile):
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

    high = pd.read_csv(high_folder + '/watcon.csv')

       

    trace1 = {
      "x": ["Riparian Restoration", "Reference"], 
      "y": [high['ac_ft_trt_bau'].sum(),high['ac_ft_base_bau'].sum()], 
      "name": "San Joaquin River Restoration - Water Use", 
      "type": "bar"
    }



    data = go.Data([trace1])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": False, 
      "title": 'San Joaquin R. Restoration - 2030 Water Use', 
      "titlefont": {
      "size": titlefont
          },
      "xaxis": {
        "autorange": True,  
        "title": ["Riparian Restoration", "Reference"], 
        "type": "category",
        "tickfont": {
          "color": "black",
          "size": large_x_labs
        },
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,3], 
        "title": 'Acre Feet of Water Demand (Annual)', 
        "type": "linear",
        "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      }
    }
   
    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, outfile, format='png')
    plot(fig, filename= 'test' + '.html')
    return fig
    
def cropvalue_plot_RRE(high_folder, outfile):
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
      "title": 'San Joaquin R. Riparian Restoration - 2030 Crop Value', 
      "titlefont": {
      "size": titlefont
          },
      "xaxis": {
        "autorange": True,  
        "title": ["Riparian Restoration", "Reference"], 
        "type": "category",
        "tickfont": {
          "color": "black",
          "size": large_x_labs
        }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,3], 
        "title": 'Crop Value (US Dollars)', 
        "type": "linear", 
        "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      }
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'test' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig
    
    
def terrestrial_habitat_plot_RRE(high_folder, outfile): #ADD THREATENED AND ENGANGERED
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    high = pd.read_csv(high_folder + '/terrhab.csv')

    
    high2 = high[['guild','ha_trt_bau', 'ha_base_bau']]

#    high3 = high2.loc[high2['guild'].isin(['mammals_avg_deg_acres','birds_avg_deg_acres','amphibians_avg_deg_acres'])]
#    high4 = high2.loc[high2['guild'].isin(['mammals_avg_imp_acres','birds_avg_imp_acres','amphibians_avg_imp_acres'])]
 

    trace1 = {
      "x": ['Mammals<br>Degraded','Mammals<br>Improved', 'Birds<br>Degraded', 'Birds<br>Improved', 'Amphibs<br>Degraded', 'Amphibs<br>Improved', 'Threatened/<br>Endangered<br>Degraded', 'Threatened/<br>Engangered<br>Improved'],    #Add threatened and endangered
      "y": high2['ha_trt_bau'],  
      "name": 'Riparian<br>Restoration',
      "type": "bar"
    }
    trace2 = {
      "x": ['Mammals<br>Degraded','Mammals<br>Improved', 'Birds<br>Degraded', 'Birds<br>Improved', 'Amphibs<br>Degraded', 'Amphibs<br>Improved', 'Threatened/<br>Endangered<br>Degraded', 'Threatened/<br>Engangered<br>Improved'], 
      "y": high2['ha_base_bau'], 
      "name": "Reference",
      "type": "bar"
    }


    data = go.Data([trace1,trace2])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 

      "title": "San Joaquin R. Riparian Restoration - 2030 Habitat Quality", 
      "xaxis": {
        "autorange": True,  
        "type": "category",
        "tickangle":0,
        "tickfont":{
            "size":10,
            "color":'black'
        },
      }, 
      "yaxis": {
        "autorange": True, 
        "title": "Average Hectares of Degraded and Improved Habitat by Species Guild", 
        "type": "linear",
        "titlefont":{
            "size":12,
            "color":'black'
        }
      }
    }

   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'terrhab' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig
    
    
    
def  airquality_plot_RRE(high_folder, outfile):
    import pandas as pd
    
    #Read O3
    
    high_co = pd.read_csv(high_folder + '/co_val_airpollute.csv')
    high_o3 = pd.read_csv(high_folder + '/o3_val_airpollute.csv')
    high_no2 = pd.read_csv(high_folder + '/no2_val_airpollute.csv')
    high_pm25 = pd.read_csv(high_folder + '/pm2_5_val_airpollute.csv')
    high_pm10 = pd.read_csv(high_folder + '/pm10_val_airpollute.csv')
    high_so2 = pd.read_csv(high_folder + '/so2_val_airpollute.csv')

    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
 

    xlist = ['CO','O<sub>3</sub>','PM 10','PM 2.5','NO<sub>2</sub>', 'SO<sub>2</sub>']
    
    trace1 = {
      "x": xlist, 
      "y": [high_co['tons_trt_bau'].sum(), high_o3['tons_trt_bau'].sum(), high_no2['tons_trt_bau'].sum(),high_pm25['tons_trt_bau'].sum(),high_pm10['tons_trt_bau'].sum(), high_so2['tons_trt_bau'].sum()], 
      "type": "bar",
      "name": "Riparian<br>Restoration", 
      
      }
    trace2 = {
      "x": xlist, 
      "y": [high_co['tons_base_bau'].sum(), high_o3['tons_base_bau'].sum(), high_no2['tons_base_bau'].sum(),high_pm25['tons_base_bau'].sum(),high_pm10['tons_base_bau'].sum(), high_so2['tons_base_bau'].sum()], 
      "type": "bar",
      "name": "Reference", 
      }

    data = go.Data([trace1, trace2])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": "San Joaquin R. Restoration - 2030 Air Pollutant Sequestration", 
      "titlefont": {
      "size": titlefont
          },
      "xaxis": {
        "autorange": True, 
        "title": ['Riparian<br>Restoration', 'Reference'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0, 200000], 
        #"range": [min_y_range(table), max_y_range(table)], 
        "title": 'Tons of Pollutant Sequestered', 
        "type": "linear",
                "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'rre_air' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig
#terrestrial_habitat_plot(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_HighDev\plotting_tables\terrhab_change.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\plotting_tables\terrhab_change.csv")
#groundwater_plot(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_HighDev\plotting_tables\groundwater_sum.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\plotting_tables\groundwater_sum.csv")

#=======
#flying_m_reductions()



def  scenicvalue_plot_RRE(high_folder, outfile):
    import pandas as pd
    
    
    high = pd.read_csv(high_folder + '/scenic.csv')

    highnat = high.loc[high['gen_class'] == 'Natural']
    highdev = high.loc[high['gen_class'] == 'Developed']
    highag = high.loc[high['gen_class'] == 'Agriculture']


    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go


    xlist = ['Riparian<br>Restoration','Reference']
    
    
    
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
      "title": "San Joaquin R. Restoration - 2030 Landcover in Highly Visible Areas", 
      "titlefont": {
      "size": titlefont
          },
      "xaxis": {
        "autorange": True, 
        "title": ['highly developed', 'medium developed', 'conserved'], 
        "type": "category",
        "tickfont": {
          "color": "black",
          "size": large_x_labs
        }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0, 200000], 
        #"range": [min_y_range(table), max_y_range(table)], 
        "title": 'Hectares of Land', 
        "type": "linear",
        "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'Flying_M' + '.html')
    return fig


def  tconnect_plot_RRE(high_folder, outfile):
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


    xlist = ['Riparian<br>Restoration','Reference']

    trace1 = {
      "x": xlist, 
      "y": [highnat['ha_trt_bau'].sum(), highnat['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "High Movement <br>Potential", 
      
      }
    trace2 = {
      "x": xlist, 
      "y": [highdev['ha_trt_bau'].sum(), highdev['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "Medium Movement <br>Potential", 
      }
    trace3 = {
      "x": xlist, 
      "y": [highag['ha_trt_bau'].sum(), highag['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "Low Movement <br>Potential", 
      }
    
    data = go.Data([trace1,trace2,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": "San Joaquin River Riparian Restoration - 2030 Terrestrial Connectivity", 
      "titlefont": {
      "size": titlefont
          },
      "xaxis": {
        "autorange": True, 
#        "title": ['highly developed', 'medium developed', 'conserved'], 
        "type": "category",
        "tickfont": {
          "color": "black",
          "size": large_x_labs
        }
      }, 
      "yaxis": {
        "autorange": True, 
        "title": 'Hectares of Terrestrial Movement Resistance Class', 
        "type": "linear", 
        "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, outfile, format='png')
    plot(fig, filename= 'Flying_M' + '.html')
    return fig

def  tconnect_plot_AG(high_folder, outfile):
    import pandas as pd

    
    high = pd.read_csv(high_folder + '/countymovement.csv')


    highnat = high.loc[high['movement_potential'] == 'high']
    highdev = high.loc[high['movement_potential'] == 'medium']
    highag = high.loc[high['movement_potential'] == 'low']


    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go


    xlist = ['Riparian<br>Restoration','Reference']

    trace1 = {
      "x": xlist, 
      "y": [highnat['ha_trt_bau'].sum(), highnat['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "High Movement <br>Potential", 
      
      }
    trace2 = {
      "x": xlist, 
      "y": [highdev['ha_trt_bau'].sum(), highdev['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "Medium Movement <br>Potential", 
      }
    trace3 = {
      "x": xlist, 
      "y": [highag['ha_trt_bau'].sum(), highag['ha_base_bau'].sum()], 
      "type": "bar",
      "name": "Low Movement <br>Potential", 
      }
    
    data = go.Data([trace1,trace2,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": "Burrroughs Family Farms - 2030 Terrestrial Connectivity", 
      "titlefont": {
      "size": titlefont
          },
      "xaxis": {
        "autorange": True, 
#        "title": ['highly developed', 'medium developed', 'conserved'], 
        "type": "category",
        "tickfont": {
          "color": "black",
          "size": large_x_labs
        }
      }, 
      "yaxis": {
        "autorange": True, 
        "title": 'Hectares of Terrestrial Movement Resistance Class', 
        "type": "linear", 
        "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, outfile, format='png')
    plot(fig, filename= 'Flying_M' + '.html')
    return fig

def  airquality_plot_AG(high_folder, outfile):
    import pandas as pd
    
    #Read O3
    
    high_co = pd.read_csv(high_folder + '/co_val_airpollute.csv')
    high_o3 = pd.read_csv(high_folder + '/o3_val_airpollute.csv')
    high_no2 = pd.read_csv(high_folder + '/no2_val_airpollute.csv')
    high_pm25 = pd.read_csv(high_folder + '/pm2_5_val_airpollute.csv')
    high_pm10 = pd.read_csv(high_folder + '/pm10_val_airpollute.csv')
    high_so2 = pd.read_csv(high_folder + '/so2_val_airpollute.csv')

    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
 

    xlist = ['CO','O<sub>3</sub>','PM 10','PM 2.5','NO<sub>2</sub>', 'SO<sub>2</sub>']
    
    trace1 = {
      "x": xlist, 
      "y": [high_co['tons_trt_bau'].sum(), high_o3['tons_trt_bau'].sum(), high_no2['tons_trt_bau'].sum(),high_pm25['tons_trt_bau'].sum(),high_pm10['tons_trt_bau'].sum(), high_so2['tons_trt_bau'].sum()], 
      "type": "bar",
      "name": "Riparian<br>Restoration", 
      
      }
    trace2 = {
      "x": xlist, 
      "y": [high_co['tons_base_bau'].sum(), high_o3['tons_base_bau'].sum(), high_no2['tons_base_bau'].sum(),high_pm25['tons_base_bau'].sum(),high_pm10['tons_base_bau'].sum(), high_so2['tons_base_bau'].sum()], 
      "type": "bar",
      "name": "Reference", 
      }

    data = go.Data([trace1, trace2])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": "Burroughs Family Farms - 2030 Air Pollutant Sequestration", 
      "titlefont": {
      "size": titlefont
          },
      "xaxis": {
        "autorange": True, 
        "title": ['Riparian<br>Restoration', 'Reference'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0, 200000], 
        #"range": [min_y_range(table), max_y_range(table)], 
        "title": 'Tons of Pollutant Sequestered', 
        "type": "linear",
                "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'rre_air' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig

def  reductions_AG(carbon_table, outfile):
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

    high = pd.read_csv(carbon_table)

    
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    
    trace1 = {
      "x": ["Riparian<br>Restoration", "Reference"], 
      "y": [high['trt_bau_total'].sum(), high['carbon_base_bau'].sum()], 
      "type": "bar",
      }
        
    data = go.Data([trace1])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": False, 
      "title": "2014-2030 GHG Reductions from Ag Activites at Burroughs Family Farms", 
      "titlefont": {
      "size": 16
          },

      "xaxis": {
        "autorange": True, 
        "type": "category",
            "tickfont": {
          "color": "black",
          "size": large_x_labs
        }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0, 200000], 
        #"range": [min_y_range(table), max_y_range(table)], 
        "title": 'Tons CO<sub>2</sub> Equivalents', 
        "type": "linear",
        "titlefont": {
          "color": "black",
          "size": large_x_labs
        }
      },
                                "annotations": [
      {
        "xref": "x",
        "yref": "y",
        "text":  str(round( high['trt_bau_total'].sum() -high['carbon_base_max'].sum(), 1))  + " tons <br> CO<sub>2</sub>e reductions <br> v. reference",
        "y": high['carbon_base_max'].sum(),
        "x": 'Riparian<br>Restoration',
        "font": {
          "color": "rgb(252, 252, 252)",
          "size": 14
        },
        "showarrow": False
      }
    ]

    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'Flying_M' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig
    

def make_plots_AC():
    import os
    import plotly.plotly as py
    py.sign_in('mtukman', 'jVJrzWkFoqVCZtX33ufz')
    boxpath = 'E:/Box/'
    print (os.path.join(boxpath,'Tool/outputs/FlyingM/FlyingM_HighDev'))
    groundwater_plot_AC(os.path.join(boxpath,'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_HighDev'), os.path.join(boxpath, r'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev'), os.path.join(boxpath, r'Box Sync/Merced Project/Case Studies/Avoided Conversion/Case Study AC Groundwater.png'))
    airquality_plot_AC(os.path.join(boxpath, 'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_HighDev'), os.path.join(boxpath, r'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev'), os.path.join(boxpath, r'Box Sync/Merced Project/Case Studies/Avoided Conversion/Case Study AC Air.png'))
    scenicvalue_plot_AC(os.path.join(boxpath, r'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_HighDev'), os.path.join(boxpath, 'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev'), os.path.join(boxpath, r'Box Sync/Merced Project/Case Studies/Avoided Conversion/Case Study AC Scenic.png'))
    terrestrial_habitat_plot_AC(os.path.join(boxpath, r'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_HighDev'), os.path.join(boxpath, r'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev'), os.path.join(boxpath, r'Box Sync/Merced Project/Case Studies/Avoided Conversion/Case Study AC Terrhab.png'))
    wateruse_plot_AC(os.path.join(boxpath, 'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_HighDev'), os.path.join(boxpath, r'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev'), os.path.join(boxpath, r'Box Sync/Merced Project/Case Studies/Avoided Conversion/Case Study AC Wateruse.png'))
    tconnect_plot_AC(os.path.join(boxpath, 'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_HighDev'), os.path.join(boxpath, r'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev'), os.path.join(boxpath, r'Box Sync/Merced Project/Case Studies/Avoided Conversion/Case Study AC Terrcon.png'))
    flyingm_reductions(os.path.join(boxpath, r'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_HighDev/carbon.csv'), os.path.join(boxpath, r'Box Sync/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev/carbon.csv'), os.path.join(boxpath, r'Box Sync/Merced Project/Case Studies/Avoided Conversion/Case Study AC Reductions.png'))
    countywide_reductions_AC(os.path.join(boxpath, r'Box Sync/Merced Project/Tool/outputs/Riparian/RRE_COUNTY_100/carbon.csv'), os.path.join(boxpath, 'Box Sync/Merced Project/Case Studies/Avoided Conversion/Countywide AC Reductions.png'))
    

def make_plots_RRE():
    import os
    import plotly.plotly as py
    py.sign_in('mtukman', 'jVJrzWkFoqVCZtX33ufz')
    boxpath = 'E:/Box/'
    countywide_reductions_RRE(os.path.join(boxpath, r'Box Sync/Merced Project/Tool/outputs/Riparian/RRE_COUNTY_100/carbon.csv'), os.path.join(boxpath, 'Box Sync/Merced Project/Case Studies/Riparian/Countywide RRE Reductions.png'))
    reductions_RRE(os.path.join(boxpath, r"Box Sync/Merced Project/Tool/outputs/Riparian/RRE_COUNTY_SCENARIO"), os.path.join(boxpath, 'Box Sync/Merced Project/Case Studies/Riparian/Case Study RRE Reductions.png') )
    wateruse_plot_RRE(os.path.join(boxpath, r"Box Sync/Merced Project/Tool/outputs/Riparian/RRE_COUNTY_SCENARIO"),  os.path.join(boxpath, 'Box Sync/Merced Project/Case Studies/Riparian/Case Study RRE Wateruse.png'))
    terrestrial_habitat_plot_RRE(os.path.join(boxpath, r"Box Sync/Merced Project/Tool/outputs/Riparian/RRE_COUNTY_SCENARIO"), os.path.join(boxpath, 'Box Sync/Merced Project/Case Studies/Riparian/Case Study RRE Terrhab.png'))
    scenicvalue_plot_RRE(os.path.join(boxpath, r"Box Sync/Merced Project/Tool/outputs/Riparian/RRE_COUNTY_SCENARIO"), os.path.join(boxpath, 'Box Sync/Merced Project/Case Studies/Riparian/Case Study RRE Scenic.png'))
    tconnect_plot_RRE(os.path.join(boxpath, r"Box Sync/Merced Project/Tool/outputs/Riparian/RRE_COUNTY_SCENARIO"), os.path.join(boxpath, 'Box Sync/Merced Project/Case Studies/Riparian/Case Study RRE Terrcon.png'))
    cropvalue_plot_RRE(os.path.join(boxpath, r"Box Sync/Merced Project/Tool/outputs/Riparian/RRE_COUNTY_SCENARIO"),os.path.join(boxpath, 'Box Sync/Merced Project/Case Studies/Riparian/Case Study RRE Cropvalue.png') )
    airquality_plot_RRE(os.path.join(boxpath, r"Box Sync/Merced Project/Tool/outputs/Riparian/RRE_COUNTY_SCENARIO"),os.path.join(boxpath, 'Box Sync/Merced Project/Case Studies/Riparian/Case Study RRE Air.png') )
    
def make_plots_AG():
    import os
    import plotly.plotly as py
    py.sign_in('mtukman', 'jVJrzWkFoqVCZtX33ufz')
    boxpath = 'E:/Box/'
    countywide_reductions_AG(table_hr= os.path.join(boxpath, r'Box Sync/Merced Project/Tool/outputs/activities/hedgerow_100/carbon.csv'),   table_cc=os.path.join(boxpath, r'Box Sync/Merced Project/Tool/outputs/activities/cover_cropping_100/carbon.csv'), outfile = os.path.join(boxpath, r'Box Sync/Merced Project/Case Studies/Burroughs/Countywide AG Reductions.png'))
    reductions_AG(os.path.join(boxpath, r'Box Sync/Merced Project/Tool/Outputs/Burroughs/hpl_ccr_carbon.csv'), os.path.join(boxpath, r'Box Sync/Merced Project/Case Studies/Burroughs/Case Study AG Reductions.png') )
    
def make_countywide_reductions_all_activities():
    import os
    import plotly.plotly as py
    py.sign_in('mtukman', 'jVJrzWkFoqVCZtX33ufz')
    boxpath = 'E:/Box/'
    reductions_ALL(os.path.join(boxpath, r'Box Sync/Merced Project/Report_How-To Guide/Tukman Working Material/Countywide GHG Reductions All Activities.png'))
    
 

    
    
    
    
    
    
    
    