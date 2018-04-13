# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 15:24:44 2018

@author: Dylan
"""
import Plotting


def callplots():
    
    #Create 2030 developed fmmp plot
    Plotting.mba_chart_threetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\fmmp.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'fmmp', pre = 'ha_loss')
    
    #Create 2014
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\fmmp.csv", xax = '2014 Farmland Hectares', yax = 'Hectares', mba = 'fmmp', x = 'fmmp_class',y = 'ha_2014', yrange = [0,1])
    
    
    
    #Crop Value 2014
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\cropvalue.csv", xax = '2014 Crop Value', yax = 'US Dollars', mba = 'cropvalue', x = 'landcover',y = 'cropvalue_usd_2014', yrange = [0,1])
    
    #Crop Value Developed Scenarios
    Plotting.mba_chart_threetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\cropvalue.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'cropvalue', pre = 'usd')
    
    
    #Water Conservation
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\watcon.csv", xax = '2014 Water Demand', yax = 'Acre Feet Per Year', mba = 'watcon', x = 'landcover',y = 'ac_ft_2014', yrange = [0,1], remzeros= 1)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    