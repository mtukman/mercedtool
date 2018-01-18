"""
Plots/Figures needed:
Land cover change by natural,crop and urban - max, bau and min (net gain/loss for each)
Land cover change showing cropland change by dev scenario, same for natural lands and urban lands with loss and gain values for each combination
Change in above groun carbon stocks under each dev scenario
Change in below ground carbon stocks for each dev scenario
Naturalness in watershed
Naturalness in county 




"""


import plotly.graph_objs as go
import plotly.plotly as py

import numpy as np
import re

import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np


import plotly.dashboard_objs as dashboard

import IPython.display
from IPython.display import Image

def fileId_from_url(url):
    """Return fileId from a url."""
    raw_fileId = re.findall("~[A-z]+/[0-9]+", url)[0][1: ]
    return raw_fileId.replace('/', ':')
    
def sharekey_from_url(url):
    """Return the sharekey from a url."""
    if 'share_key=' not in url:
        return "This url is not 'sercret'. It does not have a secret key."
    return url[url.find('share_key=') + len('share_key='):]

my_dboard = dashboard.Dashboard()
my_dboard.get_preview()

x0 = np.random.randn(50)
x1 = np.random.randn(50) + 2
x2 = np.random.randn(50) + 4
x3 = np.random.randn(50) + 6

colors = ['#FAEE1C', '#F3558E', '#9C1DE7', '#581B98']

trace0 = go.Box(x=x0, marker={'color': colors[0]})
trace1 = go.Box(x=x1, marker={'color': colors[1]})
trace2 = go.Box(x=x2, marker={'color': colors[2]})
trace3 = go.Box(x=x3, marker={'color': colors[3]})
data = [trace0, trace1, trace2, trace3]


url_2 = py.plot(data, filename='box-plots-for-dashboard', sharing='secret', auto_open=True)
py.iplot(data, filename='box-plots-for-dashboard')

colorscale = [[0, '#FAEE1C'], [0.33, '#F3558E'], [0.66, '#9C1DE7'], [1, '#581B98']]
trace1 = go.Scatter(
    y = np.random.randn(500),
    mode='markers',
    marker=dict(
        size='16',
        color = np.random.randn(500),
        colorscale=colorscale,
        showscale=True
    )
)
data = [trace1]
url_1 = py.plot(data, filename='scatter-for-dashboard', auto_open=False)

py.iplot(data, filename='scatter-for-dashboard')

fileId_1 = fileId_from_url(url_1)
fileId_2 = fileId_from_url(url_2)


box_a = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fileId_1,
    'title': 'scatter-for-dashboard'
}

text_for_box = """ 
## Distributions: 


#### Scatter Plot
1. Ranging 0 - 500
2. Even distribution

#### Box Plot
1. Similar Range
2. Outliers present in trace 1 and trace 3

You can view more markdown tips [here](https://daringfireball.net/projects/markdown/syntax).
"""

box_b = {
    'type': 'box',
    'boxType': 'text',
    'text': text_for_box,
    'title': 'Markdown Options for Text Box'
}

box_c = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fileId_2,
    'title': 'box-for-dashboard',
    'shareKey': sharekey_from_url(url_2)
}

my_dboard.insert(box_a)

my_dboard.insert(box_b, 'above', 1)
my_dboard.insert(box_c, 'left', 2)


my_dboard['settings']['title'] = 'My First Dashboard with Python'
my_dboard['settings']['logoUrl'] = 'https://images.plot.ly/language-icons/api-home/python-logo.png'

my_dboard['settings']['links'] = []
my_dboard['settings']['links'].append({'title': 'Link to Plotly', 'url': 'https://plot.ly/'})
my_dboard['settings']['links'].append({'title': 'Link to Python Website', 'url': 'https://www.python.org/'})


import plotly.plotly as py
py.dashboard_ops.upload(my_dboard, 'My First Dashboard with Python')



