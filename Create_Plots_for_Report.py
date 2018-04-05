# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 14:15:37 2018

@author: mtukman
"""

#This code will produce charts and panels for merced report

#RIPARIAN RESTORATION CHARTS AND GRAPHS

#Countywide GHG Reductions from Riparian Restoration


def  flying_m_reductions(table_high = r'E:\Box\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_HigDev\carbon.csv', table_medium=r'E:\Box\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\carbon.csv'):
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
    plot(fig, filename= 'Flying_M' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig
    

def riparian_reductions(table_high = r'E:\Box\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\carbon.csv'):
    import pandas as pd
    high = pd.read_csv(table_high)
    
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    
    trace1 = {
      "x": ["2001", "2014", "2030"], 
      "y": ["50793849", high['carbon2014'].sum(), high['trt_bau_total'].sum()], 
      "connectgaps": False, 
      "line": {"color": "rgb(26, 100, 26)"}, 
      "marker": {
        "color": "rgb(16, 82, 16)", 
        "size": 7
      }, 
      "mode": "lines+markers", 
      "name": "Tons Carbon RRE", 
      "type": "scatter", 
    }
    trace2 = {
      "x": ["2001", "2014", "2030"], 
      "y": ["50793849", high['carbon2014'].sum(), high['carbon_base_bau'].sum()], 
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
      "name": "Tons Carbon Ref", 
      "type": "scatter", 

    }

    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'Flying_M_reductions' + '.html')
    return fig

def groundwater_plot(high_folder, med_folder, outfile):
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
      "name": "Groundwater Recharge Loss", 
      "type": "bar"
    }


    data = go.Data([trace1])
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
    plot(fig, filename= 'groundwater_recharge' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig


def wateruse_plot(high_folder, med_folder, outfile):
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

    high = pd.read_csv(high_folder + '/watcon.csv')
    med = pd.read_csv(med_folder + '/watcon.csv')
       

    trace1 = {
      "x": ['Full Development','Partial Development', 'Conservation'], 
      "y": [high['ac_ft_change_dev_flagged'].sum(), med['ac_ft_change_dev_flagged'].sum(),med['ac_ft_base_med'].sum()], 
      "name": "Water Use", 
      "type": "bar"
    }



    data = go.Data([trace1])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": 'Water Use', 
      "titlefont": {
      "size": 24
          },
      "xaxis": {
        "autorange": True,  
        "title": ['Full Development', 'Partial Development', 'Conservation'], 
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
    plot(fig, filename= 'wateruse' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig
    
def terrestrial_habitat_plot(high_folder, med_folder, outfile):
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    high = pd.read_csv(high_folder + '/terrhab.csv')
    med = pd.read_csv(med_folder + '/terrhab.csv')
    
    high2 = high[['guild','acres_trt_bau']]
    med2 = med[['guild','acres_trt_bau']]

    high3 = high2.loc[high2['guild'].isin(['mammals_avg_deg_acres','birds_avg_deg_acres','amphibians_avg_deg_acres'])]
    med3 = med2.loc[med2['guild'].isin(['mammals_avg_deg_acres','birds_avg_deg_acres','amphibians_avg_deg_acres'])]
 

    trace1 = {
      "x": ['Mammals','Birds','Amphibians'], 
      "y": high3['acres_trt_bau'], 
      "name": "Full Development", 
      "type": "bar"
    }
    trace2 = {
      "x": ['Mammals','Birds','Amphibians'], 
      "y": med3['acres_trt_bau'], 
      "name": "Partial Development", 
      "type": "bar"
    }


    data = go.Data([trace1, trace2])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 

      "title": "Flying M Ranch - Terrestrial Habitat Degradation", 
      "xaxis": {
        "autorange": True,  
        "title": ['Mammals','Birds','Amphibians'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [50496576.7792, 55507202.8908], 
        "title": "Acres of Degraded Habitat", 
        "type": "linear"
      }
    }

   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'terr_hab' + '.html')
    
    py.image.save_as(fig, outfile, format='png')
    return fig
    
def  airquality_plot(high_folder, med_folder, outfile):
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
    plot(fig, filename= 'airpoll' + '.html')
    
    py.image.save_as(fig, outfile, format='png')
    return fig
#terrestrial_habitat_plot(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_HigDev\plotting_tables\terrhab_change.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\plotting_tables\terrhab_change.csv")
#groundwater_plot(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_HigDev\plotting_tables\groundwater_sum.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\plotting_tables\groundwater_sum.csv")

#=======
#flying_m_reductions()



def  scenicvalue_plot(high_folder, med_folder, outfile):
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

    xlist = ['Full Development','Partial Development','Conservation']
    
    
    
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
    plot(fig, filename= 'scenic' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig

def  tconnect_plot(high_folder, med_folder, outfile):
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
 

    xlist = ['Full Development','Partial Development']
    
    
    
    trace1 = {
      "x": xlist, 
      "y": [highnat['ha_change_trt_bau'].sum(), mednat['ha_change_trt_bau'].sum()], 
      "type": "bar",
      "name": "High Movement Potential", 
      
      }
    trace3 = {
      "x": xlist, 
      "y": [highag['ha_change_trt_bau'].sum(), medag['ha_change_trt_bau'].sum()], 
      "type": "bar",
      "name": "Low Movement Potential", 
      }
    
    data = go.Data([trace1,trace3])
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
        "title": 'Change in Hectares of Movement Type', 
        "type": "linear"
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'terrcon' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig


#Saved Function Calls

#    
def make_plots_flyingm():
    import os
    import plotly.plotly as py
    py.sign_in('mtukman', 'qfRazO2xuHUGVQH5rJhH')
    boxpath = 'C:/Users/mtukman/'
    print (os.path.join(boxpath,'Tool/outputs/FlyingM/FlyingM_HigDev'))
    fig_gw = groundwater_plot(os.path.join(boxpath,'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_HigDev'), os.path.join(boxpath, 'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev'), os.path.join(boxpath, 'Box/Merced Project/Case Studies/Avoided Conversion/Case Study AC Groundwater.png'))
    fig_aq = airquality_plot(os.path.join(boxpath, 'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_HigDev'), os.path.join(boxpath, 'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev'), os.path.join(boxpath, 'Box/Merced Project/Case Studies/Avoided Conversion/Case Study AC Air.png'))
    fig_sv = scenicvalue_plot(os.path.join(boxpath, 'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_HigDev'), os.path.join(boxpath, 'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev'), os.path.join(boxpath, 'Box/Merced Project/Case Studies/Avoided Conversion/Case Study AC Scenic.png'))
    fig_th = terrestrial_habitat_plot(os.path.join(boxpath, 'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_HigDev'), os.path.join(boxpath, 'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev'), os.path.join(boxpath, 'Box/Merced Project/Case Studies/Avoided Conversion/Case Study AC Terrhab.png'))
    fig_wu = wateruse_plot(os.path.join(boxpath, 'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_HigDev'), os.path.join(boxpath, 'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev'), os.path.join(boxpath, 'Box/Merced Project/Case Studies/Avoided Conversion/Case Study AC Wateruse.png'))
    fig_tc = tconnect_plot(os.path.join(boxpath, 'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_HigDev'), os.path.join(boxpath, 'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev'), os.path.join(boxpath, 'Box/Merced Project/Case Studies/Avoided Conversion/Case Study AC Terrcon.png'))
    fig_carb = flying_m_reductions(os.path.join(boxpath, r'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_HigDev/carbon.csv'), os.path.join(boxpath, r'Box/Merced Project/Tool/outputs/FlyingM/FlyingM_MedDev/carbon.csv'), os.path.join(boxpath, 'Box/Merced Project/Case Studies/Avoided Conversion/Case Study AC Reductions.png'))
        
    
    return [fig_gw, fig_aq, fig_sv, fig_th, fig_wu, fig_tc]



