
folder = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\\"
outpath2 = r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\FlyingM\FlyingM_MedDev\plotting_tables\\"
mba_title_font = 18
plot_dict = {}
axis_lab_font = 2

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







def mba_chart_onetrace(table, xax = 'holder', yax = 'holder', x = 'None',y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, qu2 = 'None'):
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
    plot(fig, filename= 'temp.html')
    
    

def mba_chart_threetrace(table, plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', sce = 'base'):
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




def mba_chart_threetrace_custom(table, plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0, ytitle = 'None', x1 = 'None', y1 = 'None', x2 = 'None', y2 = 'None', x3 = 'None', y3 = 'None'):
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
        "annotations": [plot_dict[mba]['ann']
      
    ]
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= plot_dict[mba]['title'] + '.html')
    
def mba_chart_onetrace_custom(table, xax = 'holder', yax = 'holder', mba = 'temp', x = ['Reference - No Riparian Restoration', '25% Riparian Restoration','100% Riparian Restoration'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'None', y2 = 'None', y3 = 'None', x1= 'None',x2= 'None',x3= 'None'):
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
    plot(fig, filename= plot_dict[mba]['title'] + '.html')
    
def mba_chart_onetrace_custom2(table,table2, xax = 'holder', yax = 'holder', mba = 'temp', x = ['Reference - No Riparian Restoration', '25% Riparian Restoration','100% Riparian Restoration'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'None', y2 = 'None', y3 = 'None', qu2 = 'none'):
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
def mba_chart_threetrace_sum(table, table2,plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', sce = 'base', xlist = ['Reference - No Riparian Restoration', '25% Riparian Restoration','100% Riparian Restoration']):
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
        "annotations": [plot_dict[mba]['ann']
      
    ]
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= plot_dict[mba]['title'] + '.html')
def mba_chart_watint_twotrace(table, table2,plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', sce = 'base', xlist = ['Reference - No Riparian Restoration', '25% Riparian Restoration','100% Riparian Restoration']):
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
      "title": 'Watershed Integrity Change from Riparian Restoration Scenarios', 
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
        "annotations": [plot_dict[mba]['ann']
      
    ]
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= plot_dict[mba]['title'] + '.html')
def mba_chart_flood_twotrace(table, table2,plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', sce = 'base', xlist = ['Reference', 'Medium Infill','Max Infill']):
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
      "title": 'General Landcover Change in 100-Year Floodplains', 
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

plot_dict['ecamovement'] ={'title':"2014-2030 Projected Change in Terrestrial Movement Resistance by Development Scenario in Essential Connectivity Areas",'changemax': 500,'changemin' :-3,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'movement_potential', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['flood100'] ={'title':"2014-2030 Projected Change in 100 Year Floodplain Landcover by Development Scenario",'changemax': 200,'changemin' :-3,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}



plot_dict['aquatic'] ={'title':"2014-2030 Projected Change in Landcover in Watersheds With High Aquatic Habitat Value by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares of Landcover", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7}

plot_dict['groundwater'] ={'title':"2014-2030 Projected Loss of Groundwater Recharge",'changemax': 1,'changemin' :-1,'ytitle': "Loss of Recharge (Acre Feet per Year)", 'changefield':'ac_ft_rec_lst', 'totfield':  'None','rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}





plot_dict['co_val_airpollute'] ={'title':"2014-2030 Projected Change in Carbon Monoxide Sequestration by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Tons of CO", 'changefield':'tons_change', 'totfield':  'tons', 'rfield' : 'landcover', 'sum': 1,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}






plot_dict['flood500'] ={'title':"2014-2030 Projected Change in 500 Year Floodplain Landcover by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'gen_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['lcchange'] ={'title':"2014-2030 Projected Change in Landcover by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares", 'changefield':'ha_change', 'totfield':  'ha', 'rfield' : 'landcover', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

plot_dict['fmmp'] ={'title':"2014-2030 Projected Impact to Farmland by Development Scenario",'changemax': 5000000,'changemin' :-7,'ytitle': "Hectares", 'changefield':'ha_loss', 'totfield':  'None', 'rfield' : 'fmmp_class', 'sum': 0,'totmax': 5000000,'totmin' :-7,'summax': 5000000,'summin' :-7,'ann':{}}

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
        





def  airquality_plot(high_folder, outfile):
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
      "showlegend": True, 
      "title": "2030 Baseline Development Scenarios <br> Air Pollutant Sequestration", 
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
        "title": 'Tons of Pollutant Sequestered', 
        "type": "linear",
                "titlefont": {
          "color": "black",
          "size": 14
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'airpoll' + '.html')

#    py.image.save_as(fig, outfile, format='png')
    return fig


def  airquality_plot_2014(high_folder, outfile):
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
      "showlegend": True, 
      "title": "2014 Air Pollutant Sequestration", 
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
          "size": 2
        }
      },
    }
       
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= 'airpoll' + '.html')



def  airquality_plot_act(high_folder, med_folder, outfile, scenario = 'Riparian Restoration', title = 'Temp'):
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
      "name": "Reference", 
      
      }
    trace2 = {
      "x": xlist, 
      "y": [high_co['tons_change_trt_bau'].sum(), high_o3['tons_change_trt_bau'].sum(), high_no2['tons_change_trt_bau'].sum(),high_pm25['tons_change_trt_bau'].sum(),high_pm10['tons_change_trt_bau'].sum(),high_so2['tons_change_trt_bau'].sum() ], 
      "type": "bar",
      "name": scenario + ' 25% Adoption', 
      }
    trace3 = {
      "x": xlist, 
      "y": [med_co['tons_change_trt_bau'].sum(), med_o3['tons_change_trt_bau'].sum(), med_no2['tons_change_trt_bau'].sum(),med_pm25['tons_change_trt_bau'].sum(),med_pm10['tons_change_trt_bau'].sum(),med_so2['tons_change_trt_bau'].sum() ], 
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
    plot(fig, filename= 'airpoll' + '.html')

#    py.image.save_as(fig, outfile, format='png')
    return fig






def mba_chart_ter_twotrace(table, table2,plot_dict, xax = 'holder', yax = 'holder', mba = 'temp', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', sce = 'base', xlist = ['Reference', 'Medium Infill','Max Infill']):
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
      "y": [table.iat[1,1],table2.iat[1,3],table.iat[1,5]], 
      "type":"bar",
      "name":"Low"
    }
    
    trace2 = {
      "x": xlist, 
      "y": [table.iat[2,1],table2.iat[2,3],table.iat[2,5]], 
      "type":"bar",
      "name":"Medium"
    }
    
    trace3 = {
      "x": xlist, 
      "y": [table.iat[0,1],table2.iat[0,3],table.iat[0,5]], 
      "type":"bar",
       "name":"High"
    }


    data = go.Data([trace1,trace2,trace3])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": 'Terrestrial Movement Landcover Change, 2014-2030', 
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
        "annotations": [plot_dict[mba]['ann']
      
    ]
    }
   
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename= plot_dict[mba]['title'] + '.html')







def mba_chart_lc_twotrace(table, table2,plot_dict, xax = 'holder', yax = 'holder', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', xlist = ['Riparian Restoration 25% Adoption','Riparian Restoration 100% Adoption'], mba = 'rre', sce = 'Riparian Restoration'):
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
      "title": 'Landcover Change from ' + sce + ' Activity Treatment', 
      "titlefont": {
      "size": mba_title_font
          },
      "xaxis": {
        "autorange": True, 
        "type": "category",
        "tickfont": {
      "size": 20
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
    plot(fig, filename= 'temp.html')





def mba_chart_oak_twotrace(table, table2,plot_dict, xax = 'holder', yax = 'holder', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', xlist = ['Riparian Restoration 25% Adoption','Riparian Restoration 100% Adoption'], mba = 'rre', sce = 'Riparian Restoration'):
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
      "y": [table.iat[1,1],table2.iat[1,1]],
      "type":"bar",
      "name":"Barren"
    }
    trace2 = {
      "x": ["Riparian Restoration 25% Adoption", "Riparian Restoration 100% Adoption"], 
      "y": [table.iat[4,1],table2.iat[4,1]],
      "type":"bar",
      "name":"Oak Conversion"
    }
    trace3 = {
      "x": ["Riparian Restoration 25% Adoption", "Riparian Restoration 100% Adoption"], 
      "y": [table.iat[5,1],table2.iat[5,1]],
      "type":"bar",
      "name":"Grassland"
    }
    trace4 = {
      "x": ["Riparian Restoration 25% Adoption", "Riparian Restoration 100% Adoption"], 
      "y": [table.iat[6,1],table2.iat[6,1]],
      "type":"bar",
      "name":"Irrigated Pasture"
    }
    trace5 = {
      "x": ["Riparian Restoration 25% Adoption", "Riparian Restoration 100% Adoption"], 
      "y": [table.iat[9,1],table2.iat[9,1]],
      "type":"bar",
      "name":"Shrubland"
    }


    
    data = go.Data([trace1,trace2,trace3,trace4,trace5])
    layout = {
      "autosize": True, 
      "hovermode": "closest", 
      "showlegend": True, 
      "title": 'Landcover Change from ' + sce + ' Activity Treatment', 
      "titlefont": {
      "size": mba_title_font
          },
      "xaxis": {
        "autorange": True, 
        "type": "category",
        "tickfont": {
      "size": 20
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
    plot(fig, filename= 'temp.html')






def terrestrial_habitat_plot_RRE(high_folder, high_folder2, outfile, title, name1, name2): #ADD THREATENED AND ENGANGERED
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.plotly as py
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    high = pd.read_csv(high_folder + '/terrhab.csv')
    high2 = pd.read_csv(high_folder2 + '/terrhab.csv')
    
    high = high[['guild','acres_trt_bau', 'acres_base_bau']]
    high2 = high2[['guild','ha_trt_bau', 'ha_base_bau']]

#    high3 = high2.loc[high2['guild'].isin(['mammals_avg_deg_acres','birds_avg_deg_acres','amphibians_avg_deg_acres'])]
#    high4 = high2.loc[high2['guild'].isin(['mammals_avg_imp_acres','birds_avg_imp_acres','amphibians_avg_imp_acres'])]
 

    trace1 = {
      "x": ['Mammals<br>Degraded','Mammals<br>Improved', 'Birds<br>Degraded', 'Birds<br>Improved', 'Amphibs<br>Degraded', 'Amphibs<br>Improved', 'Threatened/<br>Endangered<br>Degraded', 'Threatened/<br>Engangered<br>Improved'],    #Add threatened and endangered
      "y": high['ha_base_bau'],  
      "name": name1,
      "type": "bar"
    }
    trace2 = {
      "x": ['Mammals<br>Degraded','Mammals<br>Improved', 'Birds<br>Degraded', 'Birds<br>Improved', 'Amphibs<br>Degraded', 'Amphibs<br>Improved', 'Threatened/<br>Endangered<br>Degraded', 'Threatened/<br>Engangered<br>Improved'], 
      "y": high['ha_trt_bau'], 
      "name": "Reference",
      "type": "bar"
    }
    trace3 = {
      "x": ['Mammals<br>Degraded','Mammals<br>Improved', 'Birds<br>Degraded', 'Birds<br>Improved', 'Amphibs<br>Degraded', 'Amphibs<br>Improved', 'Threatened/<br>Endangered<br>Degraded', 'Threatened/<br>Engangered<br>Improved'],    #Add threatened and endangered
      "y": high2['ha_trt_bau'],  
      "name": name2,
      "type": "bar"
    }


    data = go.Data([trace2,trace1,trace3])
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
#    py.image.save_as(fig, outfile, format='png')
    return fig












def  aquatic_plot_act(high_folder, med_folder, outfile, scenario = 'Riparian Restoration', title = 'Temp'):
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
    plot(fig, filename= 'airpoll' + '.html')

#    py.image.save_as(fig, outfile, format='png')
    return fig

























