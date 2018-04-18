
folder = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\\"
outpath2 = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\plotting_tables\\"
mba_title_font = 18
plot_dict = {}
axis_lab_font = 16

flist = ['_base_bau','_base_med','_base_max','_trt_bau','_trt_med','_trt_max']

import plotly


outpath = r"E:\BoxSync\Box Sync\Merced Project\Report_How-To Guide\Tukman Working Material\pngs\\"

#Titles

ImportantFarmland = '2014 Important Farmland'
ProjectedConversionofImportantFarmlandtoDevelopment = '2014-2030 Projected Conversion of Important Farmland to Development'
CropValue = '2014 Crop Value'
ProjectedChangeinCropValuebyDevelopmentScenario= '2014-2030 Projected Change in Crop Value by Development Scenario'
AgandUrbanWaterUse= '2014 Ag and Urban Water Use'
ProjectedChangeinWaterUsebyDevelopmentScenario= '2014-2030 Projected Change in Water Use by Development Scenario'
GroundwaterRechargeLosttoDevelopment= '2030 Groundwater Recharge Lost to Development'
WatershedIntegrity= '2014 Watershed Integrity'
ChangeinWatershedIntegrityforRiparianRestorationScenario= '2014-2030 Change in Watershed Integrity for Riparian Restoration Scenario'
ChangeinWatershedIntegrityforHedgerowPlantingScenario= '2014-2030 Change in Watershed Integrity for Hedgerow Planting Scenario'
NitrateRunoff= '2014 Nitrate Runoff'
#temp = '2014-2030 Change in NO<sub>3</sub>Runoff With N Fertilizer Management Scenario'
#temp ='2014-2030 Change in NO<sub>3</sub> Runoff With N Fertilizer Management Scenario'
#2014 Nitrate Leaching= ''
#2014-2030 Change in NO<sub>3</sub> Leaching With N Fertilizer Management Scenario= ''
#2014-2030 Change in NO<sub>3</sub> Leaching With N Fertilizer Management Scenario= ''
#2014 Landcover in 100 Year Floodplain= ''
#2030 Flood Risk Reduction	2014-2030 Change in Landcover in 100 Year Floodplain= ''
#2014 Air Pollutant Sequestration= ''
#2030 Air Pollutant Sequestration= ''
#2030 Air Pollutant Sequestration with Riparian Restoration= ''
#2030 Air Pollutant Sequestration with Hedgerow Planting= ''
#2030 Air Pollutant Sequestration with Urban Tree Planting= ''
#2014 Landcover in Highly Visible Areas= ''
#2014-2030 Change in Landcover in Highly Visible Areas= ''
#2014 Terrestrial Connectivity= ''
#2014-2030 Change in Resistance to Species Movement by Riparian Scenario= ''
#2014-2030 Change in Resistance to Species Movement by Hedgerow Scenario= ''
#2014 Terrestrial Connectivity in Essential Connectivity Areas= ''
#2014-2030 Change in Resistance to Species Movement by<br>Riparian Scenario in Essential Connectivity Areas= ''
#2014-2030 Change in Resistance to Species Movement by<br>Hedgerow Scenario in Essential Connectivity Areas=''
#2014 Landcover=''
#2014-2030 Change in Landcover for Riparian Scenario=''
#2014-2030 Change in Landcover for Oak Conversion Scenario=''
#2014 Landcover in Priority Conservation Areas=''
#2014-2030 Change in Landcover in Priority Conservation Areas for Riparian Scenario=''
#2014-2030 Change in Landcover in Priority Conservation Areas for Oak Conversion Scenario=''
#2014-2030 Change in Terrestrial Habitat for Riparian Restoration Scenarios=''
#2014-2030 Change in Terrestrial Habitat for Riparian Restoration Scenarios=''
#2014 Landcover in Watersheds with Important Aquatic Habitat=''
#2014-2030 Landcover Change in Watersheds with Important Aquatic Habitat by Development Scenario=''
	
	
	
#Filenames

fmmp2014 = "fmmp_2014.png"
fmmp2014title = 'temp'


fmmp2030 = "fmmp_2030.png"


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







def mba_chart_onetrace(table, xax = 'holder', yax = 'holder', x = 'None',y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, qu2 = 'None', mba = 'None', outfile = 'temp', xtit = '', xfont = 12):
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
    
    
    

def mba_chart_threetrace(table, plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', sce = 'base', outfile = 'temp', title = 'holder'):
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
        table.set_index([plot_dict[mba]['rfield']], inplace = True)
        
        table = table[table.values.sum(axis=1) != 0]
        table.reset_index(inplace = True)
        
            

    trace1 = {
      "x": table[plot_dict[mba]['rfield']], 
      "y": table[pre + '_'+ sce+ '_bau'], 
      "type":"bar",
      "name":"Reference<br>Scenario"
    }
    
    trace2 = {
      "x": table[plot_dict[mba]['rfield']], 
      "y": table[pre + '_'+ sce+ '_med'], 
      "type":"bar",
       "name":"Medium<br>Infill"
    }
    trace3 = {
      "x": table[plot_dict[mba]['rfield']], 
      "y": table[pre + '_'+ sce+ '_max'], 
"type":"bar",
 "name":"Max<br>Infill"
    }


    data = go.Data([trace1, trace2, trace3])
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
        "type": "category",
        "tickfont": {
      "size": 12
          }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,1], 
        "title": plot_dict[mba]['ytitle'], 
        "type": "linear",
        "titlefont": {
                "size": axis_lab_font
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




def mba_chart_threetrace_custom(table, plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0, ytitle = 'None', x1 = 'None', y1 = 'None', x2 = 'None', y2 = 'None', x3 = 'None', y3 = 'None', outfile = 'temp'):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
    if qu != 'None':
        qu
    if remzeros == 1:
        table.set_index([plot_dict[mba]['rfield']], inplace = True)
        
        table = table[table.values.sum(axis=1) != 0]
        table.reset_index(inplace = True)
        

    trace1 = {
      "x": table[x1], 
      "y": table[x2], 
      "type":"bar",
      "name":"Reference<br>Scenario"
    }
    
    trace2 = {
      "x": table[x1], 
      "y": table[x2],  
      "type":"bar",
       "name":"Medium<br>Infill"
    }
    trace3 = {
      "x": table[x1], 
      "y": table[x2], 
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
        "range": [0,1], 
        "title": ytitle, 
        "type": "linear",
        "titlefont": {
                "size": axis_lab_font
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
    
def mba_chart_onetrace_custom(table, xax = 'holder', yax = 'holder', mba = 'temp', x = ['Reference - No Riparian Restoration', '25% Riparian Restoration','100% Riparian Restoration'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'None', y2 = 'None', y3 = 'None', x1= 'None',x2= 'None',x3= 'None', outfile = 'temp'):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
    if qu != 'None':
        qu
    if remzeros == 1:
        table.set_index(x, inplace = True)
        table = table[table.values.sum(axis=1) != 0]
        table.reset_index(inplace = True)
    
    
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
      "x": x, 
      "y": [table[y1].sum(), table[y2].sum(), table[y3].sum()], 
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
#    plot(fig, filename= plot_dict[mba]['title'] + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig
    
def mba_chart_onetrace_custom2(table,table2, xax = 'holder', yax = 'holder', mba = 'temp', x = ['Reference - No Riparian<br> Restoration', '25% Riparian<br> Restoration','100% Riparian<br> Restoration'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'None', y2 = 'None', y3 = 'None', qu2 = 'none', outfile = 'temp'):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
    
    table2 = pd.read_csv(table2)
    table2 = table2.loc[:, ~table2.columns.str.contains('^Unnamed')]
    
    if qu != 'None':
        table = table.loc[table[qu] != qu2]
        table2 = table2.loc[table2[qu] != qu2]
        
    if remzeros == 1:
        table.set_index([plot_dict[mba]['rfield']], inplace = True)
        
        table = table[table.values.sum(axis=1) != 0]
        table.reset_index(inplace = True)
     

    trace1 = {
      "x": x, 
      "y": [table[y1].sum(), table[y2].sum(), table2[y3].sum()], 
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
      "size": 14
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
def mba_chart_threetrace_sum(table, table2,plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', sce = 'base', xlist = ['Reference - No Riparian Restoration', '25% Riparian Restoration','100% Riparian Restoration'], outfile = 'temp'):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
    
    table2 = pd.read_csv(table2)
    table2 = table2.loc[:, ~table2.columns.str.contains('^Unnamed')]
    
    if qu != 'None':
        table = table.loc[table[qu] != qu2]
        table2 = table2.loc[table2[qu] != qu2]
        
    if remzeros == 1:
        table.set_index([plot_dict[mba]['rfield']], inplace = True)
        
        table = table[table.values.sum(axis=1) != 0]
        table.reset_index(inplace = True)
        
    
    trace1 = {
      "x": xlist, 
      "y": [table[pre + '_base_bau'].sum(), table2[pre + '_trt_bau'].sum(), table[pre + '_trt_bau'].sum()], 
      "type":"bar",
      "name":"Degraded"
    }
    
    trace2 = {
      "x": xlist, 
      "y": [table['ha_trt_bau'].sum(), table2['ha_base_bau'].sum(), table['ha_base_bau'].sum()], 
      "type":"bar",
      "name":"Important Riparian Buffer"
    }
    
    trace3 = {
      "x": xlist, 
      "y": [table['ha_trt_bau'].sum(), table2['ha_base_bau'].sum(), table['ha_base_bau'].sum()], 
      "type":"bar",
       "name":"Natural"
    }


    data = go.Data([trace1,trace2,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": 'Watershed Integrity Change from Riparian Restoration Scenarios', 
      "titlefont": {
      "size": mba_title_font
          },
      "xaxis": {
        "autorange": True, 
        "type": "category",
        "tickfont": {
      "size": 14
          }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,1], 
        "title": 'Hectares', 
        "type": "linear",
        "titlefont": {
                "size": axis_lab_font
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
def mba_chart_watint_twotrace(table, table2,plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', sce = 'base', xlist = ['Reference - No Riparian Restoration', '25% Riparian Restoration','100% Riparian Restoration'], outfile = 'temp', title = 'temp', xtit = ''):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
    
    table2 = pd.read_csv(table2)
    table2 = table2.loc[:, ~table2.columns.str.contains('^Unnamed')]
    
    if qu != 'None':
        table = table.loc[table[qu] != qu2]
        table2 = table2.loc[table2[qu] != qu2]
        
    if remzeros == 1:
        table.set_index([plot_dict[mba]['rfield']], inplace = True)
        
        table = table[table.values.sum(axis=1) != 0]
        table.reset_index(inplace = True)
        
    
    trace1 = {
      "x": xlist, 
      "y": [table.iat[0,2],table2.iat[0,8],table.iat[0,8]], 
      "type":"bar",
      "name":"Degraded"
    }
    
    trace2 = {
      "x": xlist, 
      "y": [table.iat[1,2],table2.iat[1,8],table.iat[1,8]], 
      "type":"bar",
      "name":"Important Riparian Buffer"
    }
    
    trace3 = {
      "x": xlist, 
      "y": [table.iat[2,2],table2.iat[2,8],table.iat[2,8]], 
      "type":"bar",
       "name":"Natural"
    }


    data = go.Data([trace1,trace2,trace3])
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
        "type": "category",
        'title': xtit,
        "tickfont": {
      "size": axis_lab_font
          }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,1], 
        "title": 'Hectares', 
        "type": "linear",
        "titlefont": {
                "size": axis_lab_font
          }
      },
#        "annotations": [plot_dict[mba]['ann']
#      
#    ]
    }
       
    fig = go.Figure(data=data, layout=layout)
#    py.image.save_as(fig, outfile, format='png')
#    plot(fig, filename= 'test' + '.html')
    return fig
def mba_chart_flood_twotrace(table, table2,plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', sce = 'base', xlist = ['Reference', 'Medium Infill','Max Infill'], outfile = 'temp', title = 'temp'):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
    
    table2 = pd.read_csv(table2)
    table2 = table2.loc[:, ~table2.columns.str.contains('^Unnamed')]
    
    if qu != 'None':
        table = table.loc[table[qu] != qu2]
        table2 = table2.loc[table2[qu] != qu2]
        
    if remzeros == 1:
        table.set_index([plot_dict[mba]['rfield']], inplace = True)
        
        table = table[table.values.sum(axis=1) != 0]
        table.reset_index(inplace = True)
        
    
    trace1 = {
      "x": xlist, 
      "y": [table.iat[0,1],table2.iat[0,3],table.iat[0,5]], 
      "type":"bar",
      "name":"Agriculture"
    }
    
    trace2 = {
      "x": xlist, 
      "y": [table.iat[1,1],table2.iat[1,3],table.iat[1,5]], 
      "type":"bar",
      "name":"Developed"
    }
    
    trace3 = {
      "x": xlist, 
      "y": [table.iat[2,1],table2.iat[2,3],table.iat[2,5]], 
      "type":"bar",
       "name":"Natural"
    }


    data = go.Data([trace1,trace2,trace3])
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
        "type": "category",
        "tickfont": {
      "size": axis_lab_font
          }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,1], 
        "title": 'Hectares', 
        "type": "linear",
        "titlefont": {
                "size": axis_lab_font
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
#Dictionary entries
plot_dict['cropvalue'] ={'title':"2014 - 2030 Projected Change in Crop Value by Development Scenario",'changemax': 10000000,'changemin' :-7,'ytitle': "Crop Value (Millions of Dollars)", 'changefield':'usd_change', 'totfield':  'usd', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{
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

plot_dict['ecamovement'] ={'title':"2014-2030 Projected Change in Terrestrial Movement Resistance by Development Scenario in Essential Connectivity Areas",'changemax': 500,'changemin' :-3,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'movement_potential', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['flood100'] ={'title':"2014-2030 Projected Change in 100 Year Floodplain Landcover by Development Scenario",'changemax': 200,'changemin' :-3,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}



plot_dict['aquatic'] ={'title':"2014-2030 Projected Change in Landcover in Watersheds With High Aquatic Habitat Value by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares of Landcover", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['groundwater'] ={'title':"2014-2030 Projected Loss of Groundwater Recharge",'changemax': 1,'changemin' :-1,'ytitle': "Loss of Recharge (Acre Feet per Year)", 'changefield':'ac_ft_rec_lst', 'totfield':  'None','rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}





plot_dict['co_val_airpollute'] ={'title':"2014-2030 Projected Change in Carbon Monoxide Sequestration by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of CO", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}






plot_dict['flood500'] ={'title':"2014-2030 Projected Change in 500 Year Floodplain Landcover by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['lcchange'] ={'title':"2014-2030 Projected Change in Landcover by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'landcover', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['fmmp'] ={'title':"2014-2030 Projected Conversion of Important Farmland to Development",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares", 'changefield':'ha_loss', 'totfield':  'None', 'rfield' : 'fmmp_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['leach_nitrates'] ={'title':"2014-2030 Projected Change in Nitrate Leaching by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Nitrate", 'changefield':'tons_no3_change', 'totfield':  'tons_no3', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['no2_val_airpollute'] ={'title':"2014-2030 Projected Change in NO2 Sequestration by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['o3_val_airpollute'] ={'title':"2014-2030 Projected Change in O3 Sequestration by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['pca_cover_change'] ={'title':"2014-2030 Projected Change in Priority Conservation Area Landcover by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares",'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['pm2_5_val_airpollute'] ={'title':"2014-2030 Projected Change in PM 2.5 Sequestration by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['pm10_val_airpollute'] ={'title':"2014-2030 Projected Change in PM 10 Sequestration by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['runoff_nitrates'] ={'title':"2014-2030 Projected Change in Nitrate Runoff by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Nitrate", 'changefield':'tons_no3_change', 'totfield':  'tons_no3', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['scenic'] ={'title':"2014-2030 Projected Change in Highly Visible Landcover by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares",'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['so2_val_airpollute'] ={'title':"2014-2030 Projected Change in SO2 Sequestration by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of Pollutant Sequestered", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['terrhab'] ={'title':"2014-2030 Projected Change in Terrestrial Habitat Quality by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Acres", 'changefield':'acres', 'totfield':  'None', 'rfield' : 'guild', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['watcon'] ={'title':"2014-2030 Projected Change in Water Usage by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Acre Feet of Water (Per Year)", 'changefield':'ac_ft_change', 'totfield':  'ac_ft', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['watint'] ={'title':"2014-2030 Projected Change of Watershed Integrity by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'Integrity_Class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}


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
        





def  airquality_plot(high_folder, outfile, title = 'temp', xlist = []):
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
 

    xlist = ['CO','O3','PM 10','PM 2.5','NO2', 'SO2']
    
    
    
    trace1 = {
      "x": ['Reference<br>Scenario','Medium<br>Infill','Max<br>Infill'], 
      "y": [high_co['tons_change_base_bau'].sum(), high_o3['tons_change_base_bau'].sum(), high_no2['tons_change_base_bau'].sum(),high_pm25['tons_change_base_bau'].sum(),high_pm10['tons_change_base_bau'].sum(),high_so2['tons_change_base_bau'].sum() ], 
      "type": "bar",
      "name": "Reference", 
      
      }
    trace2 = {
      "x": xlist, 
      "y": [high_co['tons_change_base_med'].sum(), high_o3['tons_change_base_med'].sum(), high_no2['tons_change_base_med'].sum(),high_pm25['tons_change_base_med'].sum(),high_pm10['tons_change_base_med'].sum(),high_so2['tons_change_base_med'].sum() ], 
      "type": "bar",
      "name": "Medium<br>Infill", 
      }
    trace3 = {
      "x": xlist, 
      "y": [high_co['tons_change_base_max'].sum(), high_o3['tons_change_base_max'].sum(), high_no2['tons_change_base_max'].sum(),high_pm25['tons_change_base_max'].sum(),high_pm10['tons_change_base_max'].sum(),high_so2['tons_change_base_max'].sum() ], 
      "type": "bar",
      "name": "Max<br>Infill", 
      }


    data = go.Data([trace1, trace2,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": False, 
      "title": title, 
      "titlefont": {
      "size": 24
          },
      "xaxis": {
        "autorange": True, 
        "title": ['Reference', 'Medium Infill', 'Max Infill'], 
        "type": "category"
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0, 200000], 
        #"range": [min_y_range(table), max_y_range(table)], 
        "title": 'Tons Per Year of Pollutant Sequestered', 
        "type": "linear",
                "titlefont": {
          "color": "black",
          "size": axis_lab_font
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
#    plot(fig, filename= 'airpoll' + '.html')

    py.image.save_as(fig, outfile, format='png')
    return fig


def  airquality_plot_2014(high_folder, outfile, title = 'temp'):
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
 

    xlist = ['CO','O3','PM 10','PM 2.5','NO2', 'SO2']
    
    trace1 = {
      "x": xlist, 
      "y": [high_co['tons_14'].sum(), high_o3['tons_14'].sum(), high_no2['tons_14'].sum(),high_pm25['tons_14'].sum(),high_pm10['tons_14'].sum(),high_so2['tons_14'].sum()], 
      "type": "bar",
      "name": "2014<br>Baseline", 
      
      }



    data = go.Data([trace1])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": False, 
      "title": title, 
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
        "type": "linear",
                "titlefont": {
          "color": "black",
          "size": axis_lab_font
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
#    plot(fig, filename= 'airpoll' + '.html')


    py.image.save_as(fig, outfile, format='png')
    return fig
def  airquality_plot_act(high_folder, med_folder, outfile = 'temp', scenario = 'Riparian Restoration', title = 'Temp'):
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
 

    xlist = ['CO','O3','PM 10','PM 2.5','NO2', 'SO2']
    
    
    
    trace1 = {
      "x": xlist, 
      "y": [high_co['tons_change_base_bau'].sum(), high_o3['tons_change_base_bau'].sum(), high_no2['tons_change_base_bau'].sum(),high_pm25['tons_change_base_bau'].sum(),high_pm10['tons_change_base_bau'].sum(),high_so2['tons_change_base_bau'].sum() ], 
      "type": "bar",
      "name": "No Activity", 
      
      }
    trace2 = {
      "x": xlist, 
      "y": [high_co['tons_change_trt_bau'].sum(), high_o3['tons_change_trt_bau'].sum(), high_no2['tons_change_trt_bau'].sum(),high_pm25['tons_change_trt_bau'].sum(),high_pm10['tons_change_trt_bau'].sum(),high_so2['tons_change_trt_bau'].sum() ], 
      "type": "bar",
      "name": scenario + ' <br>25% Adoption', 
      }
    trace3 = {
      "x": xlist, 
      "y": [med_co['tons_change_trt_bau'].sum(), med_o3['tons_change_trt_bau'].sum(), med_no2['tons_change_trt_bau'].sum(),med_pm25['tons_change_trt_bau'].sum(),med_pm10['tons_change_trt_bau'].sum(),med_so2['tons_change_trt_bau'].sum() ], 
      "type": "bar",
      "name": scenario + ' <br>100% Adoption', 
      }


    data = go.Data([trace1, trace2,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": title, 
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
        "title": 'Tons Per Year of Pollutant Sequestered', 
        "type": "linear",
                "titlefont": {
          "color": "black",
          "size": 14
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
#    plot(fig, filename= 'airpoll' + '.html')

    py.image.save_as(fig, outfile, format='png')
    return fig






def mba_chart_ter_twotrace(table, table2,plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', sce = 'base', xlist = ['No<br>Activity', '25%fff','Max Infill'], outfile = 'temp', title = 'temp'):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
    
    table2 = pd.read_csv(table2)
    table2 = table2.loc[:, ~table2.columns.str.contains('^Unnamed')]
    
    if qu != 'None':
        table = table.loc[table[qu] != qu2]
        table2 = table2.loc[table2[qu] != qu2]
        
    if remzeros == 1:
        table.set_index([plot_dict[mba]['rfield']], inplace = True)
        
        table = table[table.values.sum(axis=1) != 0]
        table.reset_index(inplace = True)
        
    
    trace1 = {
      "x": xlist, 
      "y": [table.iat[1,1],table2.iat[1,7],table.iat[1,7]], 
      "type":"bar",
      "name":"High<br>Resistance"
    }
    
    trace2 = {
      "x": xlist, 
      "y": [table.iat[2,1],table2.iat[2,7],table.iat[2,7]], 
      "type":"bar",
      "name":"Medium<br>Resistance"
    }
    
    trace3 = {
      "x": xlist, 
      "y": [table.iat[0,1],table2.iat[0,7],table.iat[0,7]], 
      "type":"bar",
       "name":"Low<br>Resistance"
    }


    data = go.Data([trace3,trace2,trace1])
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
        "type": "category",
        "tickfont": {
      "size": axis_lab_font
          }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,1], 
        "title": 'Hectares', 
        "type": "linear",
        "titlefont": {
                "size": axis_lab_font
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






def mba_chart_lc_twotrace(table, table2,plot_dict, xax = 'holder', yax = 'holder', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', xlist = ['Riparian Restoration 25% Adoption','Riparian Restoration 100% Adoption'], mba = 'rre', sce = 'Riparian Restoration', outfile = 'temp', title = ''):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
    table = table[['landcover','ha_change_' + mba]]
    
    table2 = pd.read_csv(table2)
    table2 = table2.loc[:, ~table2.columns.str.contains('^Unnamed')]
    table2 = table2[['landcover','ha_change_' + mba]]

        
    if remzeros == 1:
        table.set_index(['landcover'], inplace = True)
        
        table = table[table.values.sum(axis=1) != 0]
        table.reset_index(inplace = True)
        
    
    trace1 = {
      "x": ["Riparian Restoration 25% Adoption", "Riparian Restoration 100% Adoption"], 
      "y": [table.iat[0,1],table2.iat[0,1]],
      "type":"bar",
      "name":"Annual Cropland"
    }
    trace2 = {
      "x": ["Riparian Restoration 25% Adoption", "Riparian Restoration 100% Adoption"], 
      "y": [table.iat[1,1],table2.iat[1,1]],
      "type":"bar",
      "name":"Barren"
    }
    trace3 = {
      "x": ["Riparian Restoration 25% Adoption", "Riparian Restoration 100% Adoption"], 
      "y": [table.iat[4,1],table2.iat[4,1]],
      "type":"bar",
      "name":"Woody Riparian"
    }
    trace4 = {
      "x": ["Riparian Restoration 25% Adoption", "Riparian Restoration 100% Adoption"], 
      "y": [table.iat[5,1],table2.iat[5,1]],
      "type":"bar",
      "name":"Grassland"
    }
    trace5 = {
      "x": ["Riparian Restoration 25% Adoption", "Riparian Restoration 100% Adoption"], 
      "y": [table.iat[6,1],table2.iat[6,1]],
      "type":"bar",
      "name":"Irrigated Pasture"
    }
    trace6 = {
      "x": ["Riparian Restoration 25% Adoption", "Riparian Restoration 100% Adoption"], 
      "y": [table.iat[7,1],table2.iat[7,1]],
      "type":"bar",
      "name":"Orchard"
    }
    trace7 = {
      "x": ["Riparian Restoration 25% Adoption", "Riparian Restoration 100% Adoption"], 
      "y": [table.iat[8,1],table2.iat[8,1]],
      "type":"bar",
      "name":"Rice"
    }
    trace8 = {
      "x": ["Riparian Restoration 25% Adoption", "Riparian Restoration 100% Adoption"], 
      "y": [table.iat[11,1],table2.iat[11,1]],
      "type":"bar",
      "name":"Vineyard"
    }
    trace9 = {
      "x": ["Riparian Restoration 25% Adoption", "Riparian Restoration 100% Adoption"], 
      "y": [table.iat[13,1],table2.iat[13,1]],
      "type":"bar",
      "name":"Wetland"
    }

    
    data = go.Data([trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title":title, 
      "titlefont": {
      "size": mba_title_font
          },
      "xaxis": {
        "autorange": True, 
        "type": "category",
        "tickfont": {
      "size": 12
          }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,1], 
        "title": 'Hectares', 
        "type": "linear",
        "titlefont": {
                "size": 20
          }
      },
#        "annotations": [plot_dict[mba]['ann']
#      
#    ]
    }
   
    fig = go.Figure(data=data, layout=layout)
#    plot(fig, filename= 'temp.html')

    py.image.save_as(fig, outfile, format='png')
    return fig



def mba_chart_oak_twotrace(table, table2,plot_dict, xax = 'holder', yax = 'holder', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', xlist = ['Riparian Restoration 25% Adoption','Riparian Restoration 100% Adoption'], mba = 'rre', sce = 'Riparian Restoration', outfile = 'temp', title = ''):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
    table = table[['landcover','ha_change_' + mba]]
    
    table2 = pd.read_csv(table2)
    table2 = table2.loc[:, ~table2.columns.str.contains('^Unnamed')]
    table2 = table2[['landcover','ha_change_' + mba]]

        
    if remzeros == 1:
        table.set_index(['landcover'], inplace = True)
        
        table = table[table.values.sum(axis=1) != 0]
        table.reset_index(inplace = True)
        
    
    trace1 = {
      "x": xlist, 
      "y": [table.iat[1,1],table2.iat[1,1]],
      "type":"bar",
      "name":"Barren"
    }
    trace2 = {
      "x": xlist, 
      "y": [table.iat[4,1],table2.iat[4,1]],
      "type":"bar",
      "name":"Oak Conversion"
    }
    trace3 = {
      "x": xlist, 
      "y": [table.iat[5,1],table2.iat[5,1]],
      "type":"bar",
      "name":"Grassland"
    }
    trace4 = {
      "x": xlist, 
      "y": [table.iat[6,1],table2.iat[6,1]],
      "type":"bar",
      "name":"Irrigated Pasture"
    }
    trace5 = {
      "x": xlist, 
      "y": [table.iat[9,1],table2.iat[9,1]],
      "type":"bar",
      "name":"Shrubland"
    }


    
    data = go.Data([trace1,trace2,trace3,trace4,trace5])
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
        "type": "category",
        "tickfont": {
      "size": 12
          }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,1], 
        "title": 'Hectares', 
        "type": "linear",
        "titlefont": {
                "size": 20
          }
      },
#        "annotations": [plot_dict[mba]['ann']
#      
#    ]
    }
   
    fig = go.Figure(data=data, layout=layout)
#    plot(fig, filename= 'terrhab' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig




def terrestrial_habitat_plot_RRE(high_folder, high_folder2, title, name1, name2, outfile = 'temp'): #ADD THREATENED AND ENGANGERED
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    high = pd.read_csv(high_folder + '/terrhab.csv')
    high2 = pd.read_csv(high_folder2 + '/terrhab.csv')
    
    high = high[['guild','ha_trt_bau', 'ha_base_bau']]
    high2 = high2[['guild','ha_trt_bau']]


    trace1 = {
      "x": ['Mammals<br>Degraded','Mammals<br>Improved', 'Birds<br>Degraded', 'Birds<br>Improved', 'Amphibs<br>Degraded', 'Amphibs<br>Improved', 'Threatened/<br>Endangered<br>Degraded', 'Threatened/<br>Engangered<br>Improved'],    
      "y": high['ha_base_bau'],  
      "name": "Reference",
      "type": "bar"
    }
    trace2 = {
      "x": ['Mammals<br>Degraded','Mammals<br>Improved', 'Birds<br>Degraded', 'Birds<br>Improved', 'Amphibs<br>Degraded', 'Amphibs<br>Improved', 'Threatened/<br>Endangered<br>Degraded', 'Threatened/<br>Engangered<br>Improved'], 
      "y": high['ha_trt_bau'], 
      "name": name1,
      "type": "bar"
    }
    trace3 = {
      "x": ['Mammals<br>Degraded','Mammals<br>Improved', 'Birds<br>Degraded', 'Birds<br>Improved', 'Amphibs<br>Degraded', 'Amphibs<br>Improved', 'Threatened/<br>Endangered<br>Degraded', 'Threatened/<br>Engangered<br>Improved'],    
      "y": high2['ha_trt_bau'],  
      "name": name2,
      "type": "bar"
    }


    data = go.Data([trace1,trace2,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 

      "title": title, 
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
        "title": "Average Hectares of Degraded and<br>Improved Habitat by Species Guild", 
        "type": "linear",
        "titlefont":{
            "size":12,
            "color":'black'
        }
      }
    }

   
    fig = go.Figure(data=data, layout=layout)
#    plot(fig, filename= 'terrhab' + '.html')
    py.image.save_as(fig, outfile, format='png')
    return fig




def  aquatic_plot_act(high_folder, med_folder, outfile = 'temp', scenario = 'Riparian Restoration', title = 'Temp'):
    import pandas as pd
    
    
    #Read O3
    
    table = pd.read_csv(high_folder + '/co_val_airpollute.csv')



    table2 = pd.read_csv(med_folder + '/co_val_airpollute.csv')



    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
 

    xlist = ['Reference', 'Riparian 25%', 'Riparian 100']
    
    
    
    trace1 = {
      "x": xlist, 
      "y": [table.iat[0,1],table.iat[0,1],table2.iat[0,1]], 
      "type": "bar",
      "name": "Reference", 
      
      }
    trace2 = {
      "x": xlist, 
      "y": [table.iat[0,1],table.iat[0,1],table2.iat[0,1]], 
      "type": "bar",
      "name": scenario + ' 25% Adoption', 
      }
    trace3 = {
      "x": xlist, 
      "y": [table.iat[0,1],table.iat[0,1],table2.iat[0,1]], 
      "type": "bar",
      "name": scenario + ' 100% Adoption', 
      }


    data = go.Data([trace1, trace2,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": title, 
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
        "title": 'Tons of Pollutant Sequestered', 
        "type": "linear",
                "titlefont": {
          "color": "black",
          "size": 14
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
#    plot(fig, filename= 'airpoll' + '.html')

    py.image.save_as(fig, outfile, format='png')
    return fig







def mba_chart_aquatic_twotrace(table, table2,plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', sce = 'base', xlist = ['Reference', 'Medium Infill','Max Infill'], outfile = 'temp', title = 'temp'):
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    #import plotly.plotly as py
    from plotly import tools
    import plotly.graph_objs as go
    import pandas as pd
    table = pd.read_csv(table)
    table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
    
    table2 = pd.read_csv(table2)
    table2 = table2.loc[:, ~table2.columns.str.contains('^Unnamed')]
    
    if qu != 'None':
        table = table.loc[table[qu] != qu2]
        table2 = table2.loc[table2[qu] != qu2]
        
    if remzeros == 1:
        table.set_index([plot_dict[mba]['rfield']], inplace = True)
        
        table = table[table.values.sum(axis=1) != 0]
        table.reset_index(inplace = True)
        
    
    trace1 = {
      "x": xlist, 
      "y": [table.iat[0,1],table2.iat[0,3],table.iat[0,5]], 
      "type":"bar",
      "name":"Agriculture"
    }
    
    trace2 = {
      "x": xlist, 
      "y": [table.iat[1,1],table2.iat[1,3],table.iat[1,5]], 
      "type":"bar",
      "name":"Developed"
    }
    
    trace3 = {
      "x": xlist, 
      "y": [table.iat[2,1],table2.iat[2,3],table.iat[2,5]], 
      "type":"bar",
       "name":"Natural"
    }


    data = go.Data([trace1,trace2,trace3])
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
        "type": "category",
        "tickfont": {
      "size": 16
          }
      }, 
      "yaxis": {
        "autorange": True, 
        "range": [0,1], 
        "title": 'Hectares', 
        "type": "linear",
        "titlefont": {
                "size": 16
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







def mergecsvs(table25,table100, actname = 'cam',outcsv = 'temp'):
    import pandas as pd
    t25 = pd.read_csv(table25 + r'\carbon.csv')
    t100 = pd.read_csv(table100 + r'\carbon.csv')
    at25 = pd.read_csv(table25 + r'\act_acres.csv')
    at100 = pd.read_csv(table100 + r'\act_acres.csv')
    
    t25 = t25[['carbon_' + actname]]
    t25 = t25.rename(columns = {'carbon_' + actname:'Carbon_25'})
    t100 = t100[['carbon_' + actname]]
    t100 = t100.rename(columns = {'carbon_' + actname :'Carbon_100'})
    
    sum25 = t25['Carbon_25'].sum()
    sum100 = t100['Carbon_100'].sum()
    sum252 = at25[actname + '_acres'].sum()
    sum1002 = at100[actname + '_acres'].sum()
    
    
    df = pd.DataFrame([['Reductions',sum25,sum100],['Acres',sum252,sum1002]], columns = ['Field','25% Adoption','100% Adoption'])
    

    
    df.to_csv(outcsv)
    


def runmerges():
    mergecsvs(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\compost_amendment_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\compost_amendment_100", actname = 'cam',outcsv = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\carbon_tables\cam_carbon.csv")
    
    mergecsvs(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\grass_compost_amendment_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\grass_compost_amendment_100", actname = 'cag',outcsv = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\carbon_tables\cag_carbon.csv")
    mergecsvs(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\cover_cropping_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\cover_cropping_100", actname = 'ccr',outcsv = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\carbon_tables\ccr_carbon.csv")
    mergecsvs(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\grassland_resto_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\grassland_resto_100", actname = 'gra',outcsv = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\carbon_tables\gra_carbon.csv")
    mergecsvs(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100", actname = 'hpl',outcsv = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\carbon_tables\hpl_carbon.csv")
    mergecsvs(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\mulching_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\mulching_100", actname = 'mul',outcsv = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\carbon_tables\mul_carbon.csv")
    mergecsvs(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\nfm_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\nfm_100", actname = 'nfm',outcsv = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\carbon_tables\nfm_carbon.csv")
    mergecsvs(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_100", actname = 'oak',outcsv = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\carbon_tables\oak_carbon.csv")
    mergecsvs(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100", actname = 'rre',outcsv = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\carbon_tables\rre_carbon.csv")
    
    mergecsvs(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\urb_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\urb_100", actname = 'urb',outcsv = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\carbon_tables\urb_carbon.csv")









def callplots():
    
    #Create 2014
    mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\fmmp.csv", xax = '2014 Important Farmland', yax = 'Hectares', x = 'fmmp_class',y = 'ha_2014', yrange = [0,1], outfile = outpath + "2030 Ag Land Quality.png")
    
    #Create 2030 developed fmmp plot
    mba_chart_threetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\fmmp.csv", plot_dict, xax = 'holder', yax = 'holder', mba = 'fmmp', pre = 'ha_loss', outfile = outpath + "2014 Ag Land Quality.png", title = '2014-2030 Projected Conversion of Important Farmland to Development')

    #Crop Value 2014
    mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\cropvalue.csv", xax = '2014 Crop Value', yax = 'US Dollars', mba = 'cropvalue', x = 'landcover',y = 'cropvalue_usd_2014', yrange = [0,1], outfile = outpath + "2014 Crop Value.png")
    
    #Crop Value Developed Scenarios
    mba_chart_threetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\cropvalue.csv", plot_dict, xax = 'holder', yax = 'holder', mba = 'cropvalue', pre = 'usd_change', outfile = outpath + "2030 Crop Value.png", title = '2014-2030 Projected Change in Crop Value by Development Scenario')

    #Water Conservation
    mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\watcon.csv", xax = '2014 Ag and Urban Water Use', yax = 'Acre Feet Per Year', mba = 'watcon', x = 'landcover',y = 'ac_ft_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Ag and Urban Water Conservation.png")
    
    
    mba_chart_threetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\watcon.csv", plot_dict, xax = 'holder', yax = 'holder', mba = 'watcon', pre = 'ac_ft_change', remzeros= 1, outfile = outpath + "2030 Ag and Urban Water Conservation.png", title = '2014-2030 Projected Change in Water Use by Development Scenario')
    
    #Groundwater Recharge
    mba_chart_onetrace_custom(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\groundwater.csv", xax = '2030 Groundwater Recharge Lost to Development', yax = 'Acre Feet Per Year', mba = 'watcon', x = ["Reference", "Medium<br>Infill", "Max<br>Infill"], yrange = [0,1], y1 = 'ac_ft_rec_lst_base_bau', y2 = 'ac_ft_rec_lst_base_med', y3 = 'ac_ft_rec_lst_base_max', outfile = outpath + "2030 Groundwater Recharge.png")
    
    
    #Watershed Integrity ADD XAXIS TITLE
    mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\watint.csv", xax = '2014 Watershed Integrity', yax = 'Hectares', mba = 'watint', x = 'Integrity_Class',y = 'ha_2014', yrange = [0,1], remzeros= 1, qu = 'Integrity_Class', qu2 = 'na', outfile = outpath + "2014 Watershed Integrity.png", xtit = 'Watershed Classification')
    
    mba_chart_watint_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\watint.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\watint.csv", plot_dict, xax = 'holder', yax = 'holder', mba = 'watint', pre = 'ha_change', remzeros = 0, qu = 'Integrity_Class', qu2 = 'na', outfile = outpath + "2030 Watershed Integrity Riparian.png", title = '2014-2030 Change in Watershed Integrity for Riparian Restoration Scenario',xtit = 'Watershed Classification')
    
    mba_chart_watint_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\watint.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\watint.csv", plot_dict, xax = 'holder', yax = 'holder', mba = 'watint', pre = 'ha_change', remzeros = 0, qu = 'Integrity_Class', qu2 = 'na', outfile = outpath + "2030 Watershed Integrity Hedgerows.png", title = '2014-2030 Change in Watershed Integrity for Hedgerow Planting Scenarios',xtit = 'Watershed Classification') #No Change from hpl activity
    
    
    #Water Quality - Runoff
    mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\runoff_nitrates.csv", xax = '2014 Nitrate Runoff', yax = 'Tons of Nitrate Runoff', mba = 'runoff_nitrates', x = 'landcover',y = 'tons_no3_14', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Water Quality - Nitrate Runoff.png")
    
    
    mba_chart_onetrace_custom2(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\nfm_25\runoff_nitrates.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\nfm_100\runoff_nitrates.csv", xax = '2014-2030 Change in NO<sub>3</sub> Runoff With Nitrogen Fertilizer Management Scenarios', yax = 'Tons of Nitrate Runoff', mba = 'runoff_nitrates', x = ['Reference - No Nitrogen<br> Fertilizer Management', '25% Nitrogen <br>Fertilizer Management','100% Nitrogen Fertilizer <br>Management'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'tons_no3_change_base_bau', y2 = 'tons_no3_change_trt_bau', y3 = 'tons_no3_change_trt_bau', qu2 = 'none', outfile = outpath + "2030 Water Quality - Nitrate Runoff NFM.png")
    
    mba_chart_onetrace_custom2(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_25\runoff_nitrates.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\runoff_nitrates.csv", xax = '2014-2030 Change in NO<sub>3</sub> Runoff With Riparian Restoration Scenarios', yax = 'Tons of Nitrate Runoff', mba = 'runoff_nitrates', x = ['Reference - No <br>Riparian Restoration', '25% Riparian<br> Restoration Adoption','100% Riparian<br> Restoration Adoption'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'tons_no3_change_base_bau', y2 = 'tons_no3_change_trt_bau', y3 = 'tons_no3_change_trt_bau', qu2 = 'none', outfile = outpath + "2030 Water Quality - Nitrate Runoff RRE.png")
    
    
        #Water Quality - Leaching
    mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\leach_nitrates.csv", xax = '2014 Nitrate Leaching', yax = 'Tons of Nitrate Leaching', mba = 'leaching_nitrates', x = 'landcover',y = 'tons_no3_14', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Water Quality - Nitrate Leaching.png")
    
    
    mba_chart_onetrace_custom2(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\nfm_25\leach_nitrates.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\nfm_100\leach_nitrates.csv", xax = '2014-2030 Change in NO<sub>3</sub> Leaching With N Fertilizer Management Scenario', yax = 'Tons of Nitrate Leaching', mba = 'runoff_nitrates', x = ['Reference - No <br>Nitrogen Fertilizer<br>Management', '25% Nitrogen<br> Fertilizer Management','100% Nitrogen<br> Fertilizer<br> Management'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'tons_no3_change_base_bau', y2 = 'tons_no3_change_trt_bau', y3 = 'tons_no3_change_trt_bau', qu2 = 'none', outfile = outpath + "2014 Water Quality - Nitrate Leaching NFM.png")
    
    mba_chart_onetrace_custom2(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\leach_nitrates.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\leach_nitrates.csv", xax = '2014-2030 Change in NO<sub>3</sub> Leaching With Riparian Restoration Scenario', yax = 'Tons of Nitrate Leaching', mba = 'runoff_nitrates', x = ['Reference - No <br>Riparian Restoration', '25% Riparian<br> Restoration','100% Riparian <br>Restoration'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'tons_no3_change_base_bau', y2 = 'tons_no3_change_trt_bau', y3 = 'tons_no3_change_trt_bau', qu2 = 'None', outfile = outpath + "2014 Water Quality - Nitrate Leaching RRE.png")
    

    #Flood Risk Reduction
    mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\flood100.csv", xax = '2014 Landcover in 100 Year Floodplain', yax = 'Hectares', mba = 'flood100', x = 'gen_class',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Flood Risk Reduction.png")
    
    mba_chart_flood_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\flood100.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\flood100.csv", plot_dict, xax = 'holder', yax = 'holder', mba = 'flood100', pre = 'ha_change', remzeros = 0, qu = 'gen_class', qu2 = 'na', outfile = outpath + "2030 Flood Risk Reduction.png", title = '2014-2030 Change in Landcover in 100 Year Floodplain')

    #Air Pollution
    airquality_plot_2014(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100",  outfile = outpath + "2014 Air Quality.png", title = '2014 Air Pollutant Sequestration')
    
    airquality_plot(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100", outfile = outpath + "2030 Air Quality Total.png", title = '2030 Air Pollutant Sequestration')
    
    airquality_plot_act(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100", outfile = outpath + "2030 Air Quality Change RRE.png", scenario = 'Riparian <br>Restoration', title = "Air Pollutant Sequestration for 2030 with Riparian Restoration")
    
    airquality_plot_act(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_25", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100", outfile = outpath + "2030 Air Quality Change HPL.png", scenario = 'Hedgerow <br>Planting', title = "Air Pollutant Sequestration for 2030 with Hedgerow Planting") # Hedgerow planting is not workingin tool
    
    airquality_plot_act(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\urb_25", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\urb_100", outfile = outpath + "2030 Air Quality Change URB.png", scenario = 'Urban <br>Tree Planting', title = "Air Pollutant Sequestration for 2030 with Urban Tree Planting")
    
    airquality_plot_act(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_25", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_100", outfile = outpath + "2030 Air Quality Change OAK.png", scenario = 'Oak <br>Conversion', title = "Air Pollutant Sequestration for 2030 with Oak Conversion")
    
    
    
    
    #Scenic Value
    mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\scenic.csv", xax = '2014 Landcover in Highly Visible Areas', yax = 'Hectares', x = 'gen_class',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Scenic Value.png")
    
    mba_chart_threetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\scenic.csv", plot_dict, xax = 'holder', yax = 'holder', mba = 'scenic', pre = 'ha_change', outfile = outpath + "2030 Scenic Value.png", title = '2014-2030 Change in Landcover in Highly Visible Areas')
    
    #Terrestrial Connectivity
    mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\countymovement.csv", xax = '2014 Terrestrial Connectivity', yax = 'Hectares', x = 'movement_potential',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Terrestrial Connectivity.png", xtit = 'Resistance to Movement')
    
    mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\ecamovement.csv", xax = '2014 Resistance to Species Movement in <br>Essential Connectivity Areas', yax = 'Hectares', x = 'movement_potential',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 ECA Terrestrial Connectivity.png", xtit = 'Resistance to Movement')
    
    
    mba_chart_ter_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\countymovement.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_25\countymovement.csv", plot_dict, xax = 'holder', yax = 'holder', mba = 'flood100', pre = 'ha_change', remzeros = 0, qu = 'None', qu2 = 'na', outfile = outpath + "2030 Terrestrial Connectivity HPL.png", xlist = ['No<br>Activity', '25% Hedgerow<br>Adoption','100% Hedgerow<br>Adoption'], title = '2014-2030 Change in Resistance to Species Movement for Hedgerow Scenarios')
    
    mba_chart_ter_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\countymovement.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\countymovement.csv", plot_dict, xax = 'holder', yax = 'holder', mba = 'flood100', pre = 'ha_change', remzeros = 0, qu = 'None', qu2 = 'na', outfile = outpath + "2030 Terrestrial Connectivity RRE.png", xlist = ['No<br>Activity', '25% Riparian<br>Adoption','100% Riparian<br>Adoption'], title = '2014-2030 Change in Resistance to Species Movement for Riparian Scenarios')
    
    mba_chart_ter_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\ecamovement.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_25\ecamovement.csv", plot_dict, xax = 'holder', yax = 'holder', mba = 'flood100', pre = 'ha_change', remzeros = 0, qu = 'None', qu2 = 'na', outfile = outpath + "2030 ECA Terrestrial Connectivity HPL.png", xlist = ['No<br>Activity', '25% Hedgerow<br>Adoption','100% Hedgerow<br>Adoption'], title = '2014-2030 Change in Resistance to Species Movement for<br>Hedgerow Scenarios in Essential Connectivity Areas')
    
    mba_chart_ter_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\ecamovement.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\ecamovement.csv", plot_dict, xax = 'holder', yax = 'holder', mba = 'flood100', pre = 'ha_change', remzeros = 0, qu = 'None', qu2 = 'na', outfile = outpath + "2030 ECA Terrestrial Connectivity RRE.png", xlist = ['No<br>Activity', '25% Riparian<br>Adoption','100% Riparian<br>Adoption'], title = '2014-2030 Change in Resistance to Species Movement for<br>Riparian Scenarios in Essential Connectivity Areas')
    
    
    #Natural Habitat Area
    mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\lcchange.csv", xax = '2014 Landcover', yax = 'Hectares', x = 'landcover',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Natural Habitat Area.png")

    
    mba_chart_lc_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\lcchange.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\lcchange.csv",plot_dict, xax = 'holder', yax = 'holder', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', xlist = ['Riparian Restoration 25% Adoption','Riparian Restoration 100% Adoption'], mba = 'rre', sce = 'Riparian Restoration', outfile = outpath + "2030 Natural Habitat Area RRE.png", title = '2014-2030 Change in Landcover for Riparian Scenarios')
    
    
    mba_chart_oak_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_25\lcchange.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_100\lcchange.csv",plot_dict, xax = 'holder', yax = 'holder', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', xlist = ['Oak Conversion 25% Adoption','Oak Conversion 100% Adoption'], mba = 'oak', sce = 'Oak Conversion', outfile = outpath + "2030 Natural Habitat Area OAK.png", title = '2014-2030 Change in Landcover for Oak Conversion Scenarios')

    #New forest in PCA
    mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\pca_cover_change.csv", xax = '2014 Landcover in Priority Conservation Areas', yax = 'Hectares', x = 'landcover',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Priority Conservation Areas.png")

    
    mba_chart_lc_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\pca_cover_change.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\pca_cover_change.csv",plot_dict, xax = 'holder', yax = 'holder', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', xlist = ['Riparian Restoration 25% Adoption','Riparian Restoration 100% Adoption'], mba = 'rre', sce = 'Riparian Restoration', outfile = outpath + "2030 Priority Conservation Areas RRE.png", title = '2014-2030 Change in Landcover in Priority<br>Conservation Areas for Riparian Scenarios')
    
    
    mba_chart_oak_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_25\pca_cover_change.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_100\pca_cover_change.csv",plot_dict, xax = 'holder', yax = 'holder', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', xlist = ['Oak Conversion 25% Adoption','Oak Conversion 100% Adoption'], mba = 'oak', sce = 'Oak Conversion', outfile = outpath + "2030 Priority Conservation Areas OAK.png", title = '2014-2030 Change in Landcover in Priority<br>Conservation Areas for Oak Conversion Scenarios')
    



        #Terrestrial Habitat
    terrestrial_habitat_plot_RRE(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100", '2014-2030 Change in Terrestrial Habitat for Riparian Restoration Scenarios', 'Riparian<br>Restoration<br>25% Adoption', 'Riparian<br>Restoration<br>100% Adoption', outfile = outpath + "2030 Terrestrial Habitat Value RRE.png")
    
    terrestrial_habitat_plot_RRE(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_100", '2014-2030 Change in Terrestrial Habitat<br>for Oak Conservation Scenarios', 'Oak<br>Conversion<br>25% Adoption', 'Oak<br>Conversion<br>100% Adoption', outfile = outpath + "2030 Terrestrial Habitat Value OAK.png")
    
    #Aquatic Habitat
    mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\aquatic.csv", xax = '2014 Landcover in Watersheds with Important Aquatic Habitat', yax = 'Hectares', x = 'gen_class',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Aquatic Biodiversity.png")
    
    mba_chart_aquatic_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\aquatic.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\aquatic.csv", plot_dict, xax = 'holder', yax = 'holder', mba = 'flood100', pre = 'ha_change', remzeros = 0, qu = 'gen_class', qu2 = 'na', outfile = outpath + "2030 Aquatic Biodiversity RRE.png", title = '2014-2030 Landcover Change in Watersheds with Important Aquatic Habitat by Development Scenario')





















