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
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\fmmp.csv", xax = '2014 Farmland Hectares', yax = 'Hectares', mba = 'fmmp', x = 'fmmp_class',y = 'ha_2014', yrange = [0,1])
    
    
    
    #Crop Value 2014
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\cropvalue.csv", xax = '2014 Crop Value', yax = 'US Dollars', mba = 'cropvalue', x = 'landcover',y = 'cropvalue_usd_2014', yrange = [0,1])
    
    #Crop Value Developed Scenarios
    Plotting.mba_chart_threetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\cropvalue.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'cropvalue', pre = 'usd')
    
    
    #Water Conservation
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\watcon.csv", xax = '2014 Water Demand', yax = 'Acre Feet Per Year', mba = 'watcon', x = 'landcover',y = 'ac_ft_2014', yrange = [0,1], remzeros= 1)
    
    
    Plotting.mba_chart_threetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\watcon.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'watcon', pre = 'ac_ft_change', remzeros= 1)
    
    #Groundwater Recharge

    Plotting.mba_chart_onetrace_custom(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\groundwater.csv", xax = 'Groundwater Recharge Loss From 2030 Development', yax = 'Acre Feet Per Year', mba = 'watcon', x = ["Reference", "Medium<br>Infill", "Max<br>Infill"], yrange = [0,1], y1 = 'ac_ft_rec_lst_base_bau', y2 = 'ac_ft_rec_lst_base_med', y3 = 'ac_ft_rec_lst_base_max')
    
    
    #Watershed Integrity
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\watint.csv", xax = '2014 Watershed Integrity', yax = 'Hectares', mba = 'watint', x = 'Integrity_Class',y = 'ha_2014', yrange = [0,1], remzeros= 1, qu = 'Integrity_Class', qu2 = 'na')
    
    Plotting.mba_chart_watint_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\watint.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\watint.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'watint', pre = 'ha_change', remzeros = 0, qu = 'Integrity_Class', qu2 = 'na')
    
    Plotting.mba_chart_watint_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\watint.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\watint.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'watint', pre = 'ha_change', remzeros = 0, qu = 'Integrity_Class', qu2 = 'na')
    
    
    #Water Quality - Runoff
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\runoff_nitrates.csv", xax = 'Nitrate Runoff - 2014', yax = 'Tons of Nitrate', mba = 'runoff_nitrates', x = 'landcover',y = 'tons_no3_14', yrange = [0,1], remzeros= 1)
    
    
    Plotting.mba_chart_onetrace_custom2(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\leaching_nitrates.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_25\leaching_nitrates.csv", xax = 'holder', yax = 'holder', mba = 'runoff_nitrates', x = ['Reference - No Hedgerow Planting', '25% Hedgerow Planting','100% Hedgerow Planting'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'tons_no3_change_base_bau', y2 = 'tons_no3_change_trt_bau', y3 = 'tons_no3_change_trt_bau', qu2 = 'none')
    
    Plotting.mba_chart_onetrace_custom2(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\runoff_nitrates.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\runoff_nitrates.csv", xax = 'holder', yax = 'holder', mba = 'runoff_nitrates', x = ['Reference - No Riparian Restoration', '25% Riparian Restoration','100% Riparian Restoration'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'tons_no3_change_base_bau', y2 = 'tons_no3_change_trt_bau', y3 = 'tons_no3_change_trt_bau', qu2 = 'none')
    
    
    
    
    
        #Water Quality - Leaching
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\leaching_nitrates.csv", xax = 'Nitrate Leaching - 2014', yax = 'Tons of Nitrate', mba = 'leaching_nitrates', x = 'landcover',y = 'tons_no3_14', yrange = [0,1], remzeros= 1)
    
    
    Plotting.mba_chart_onetrace_custom2(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\leaching_nitrates.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_25\leaching_nitrates.csv", xax = 'holder', yax = 'holder', mba = 'runoff_nitrates', x = ['Reference - No Hedgerow Planting', '25% Hedgerow Planting','100% Hedgerow Planting'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'tons_no3_change_base_bau', y2 = 'tons_no3_change_trt_bau', y3 = 'tons_no3_change_trt_bau', qu2 = 'none')
    
    Plotting.mba_chart_onetrace_custom2(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\runoff_nitrates.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_25\runoff_nitrates.csv", xax = 'holder', yax = 'holder', mba = 'runoff_nitrates', x = ['Reference - No Riparian Restoration', '25% Riparian Restoration','100% Riparian Restoration'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'tons_no3_change_base_bau', y2 = 'tons_no3_change_trt_bau', y3 = 'tons_no3_change_trt_bau', qu2 = 'none')
    

    #Flood Risk Reduction
    
    
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\flood100.csv", xax = 'Landcover in 100 Year Floodplain - 2014', yax = 'Hectare', mba = 'flood100', x = 'gen_class',y = 'ha_2014', yrange = [0,1], remzeros= 1)
    
    Plotting.mba_chart_flood_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\flood100.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\flood100.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'flood100', pre = 'ha_change', remzeros = 0, qu = 'gen_class', qu2 = 'na')
    
    
    
    #Air Pollution
    Plotting.airquality_plot_2014(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100", 'temp')
    
    Plotting.airquality_plot(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100", 'temp')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    