# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 15:24:44 2018

@author: Dylan
"""
import Plotting
import plotly


outpath = r"E:\BoxSync\Box Sync\Merced Project\Report_How-To Guide\Tukman Working Material\pngs\\"

#Titles
fmmp2014title = 'temp'
fmmp2030title = 'temp'
cropvalue2014title = 'temp'
cropvalue2030title = 'temp'
fmmp2014title = 'temp'
fmmp2014title = 'temp'
fmmp2014title = 'temp'
fmmp2014title = 'temp'
fmmp2014title = 'temp'
fmmp2014title = 'temp'
fmmp2014title = 'temp'
fmmp2014title = 'temp'
fmmp2014title = 'temp'
fmmp2014title = 'temp'






#Filenames

fmmp2014 = "fmmp_2014.png"
fmmp2014title = 'temp'


fmmp2030 = "fmmp_2030.png"






def callplots():
    
    #Create 2014
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\fmmp.csv", xax = '2014 Farmland Of Interest', yax = 'Hectares', x = 'fmmp_class',y = 'ha_2014', yrange = [0,1], outfile = outpath + "2030 Ag Land Quality.png")
    
    #Create 2030 developed fmmp plot
    Plotting.mba_chart_threetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\fmmp.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'fmmp', pre = 'ha_loss', outfile = outpath + "2014 Ag Land Quality.png")

    #Crop Value 2014
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\cropvalue.csv", xax = '2014 Crop Value', yax = 'US Dollars', mba = 'cropvalue', x = 'landcover',y = 'cropvalue_usd_2014', yrange = [0,1], outfile = outpath + "2014 Crop Value.png")
    
    #Crop Value Developed Scenarios
    Plotting.mba_chart_threetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\cropvalue.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'cropvalue', pre = 'usd_change', outfile = outpath + "2030 Crop Value.png")

    #Water Conservation
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\watcon.csv", xax = '2014 Water Demand', yax = 'Acre Feet Per Year', mba = 'watcon', x = 'landcover',y = 'ac_ft_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Ag and Urban Water Conservation.png")
    
    
    Plotting.mba_chart_threetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\watcon.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'watcon', pre = 'ac_ft_change', remzeros= 1, outfile = outpath + "2030 Ag and Urban Water Conservation.png")
    
    #Groundwater Recharge
    Plotting.mba_chart_onetrace_custom(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\groundwater.csv", xax = 'Groundwater Recharge Loss From 2030 Development', yax = 'Acre Feet Per Year', mba = 'watcon', x = ["Reference", "Medium<br>Infill", "Max<br>Infill"], yrange = [0,1], y1 = 'ac_ft_rec_lst_base_bau', y2 = 'ac_ft_rec_lst_base_med', y3 = 'ac_ft_rec_lst_base_max', outfile = outpath + "2030 Groundwater Recharge.png")
    
    
    #Watershed Integrity
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\watint.csv", xax = '2014 Watershed Integrity', yax = 'Hectares', mba = 'watint', x = 'Integrity_Class',y = 'ha_2014', yrange = [0,1], remzeros= 1, qu = 'Integrity_Class', qu2 = 'na', outfile = outpath + "2014 Watershed Integrity.png")
    
    Plotting.mba_chart_watint_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\watint.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\watint.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'watint', pre = 'ha_change', remzeros = 0, qu = 'Integrity_Class', qu2 = 'na', outfile = outpath + "2014 Watershed Integrity Riparian.png")
    
    Plotting.mba_chart_watint_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\watint.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\watint.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'watint', pre = 'ha_change', remzeros = 0, qu = 'Integrity_Class', qu2 = 'na', outfile = outpath + "2014 Watershed Integrity Hedgerows.png") #No Change from hpl activity
    
    
    #Water Quality - Runoff
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\runoff_nitrates.csv", xax = 'Nitrate Runoff - 2014', yax = 'Tons of Nitrate', mba = 'runoff_nitrates', x = 'landcover',y = 'tons_no3_14', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Water Quality - Nitrate Runoff.png")
    
    
    Plotting.mba_chart_onetrace_custom2(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\nfm_25\runoff_nitrates.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\nfm_100\runoff_nitrates.csv", xax = '2014 - 2030 Change in Nitrate Runoff With Nitrogen Fertilizer Management Scenarios', yax = 'Tons of Nitrate Runoff', mba = 'runoff_nitrates', x = ['Reference - No Nitrogen<br> Fertilizer Management', '25% Nitrogen <br>Fertilizer Management','100% Nitrogen Fertilizer <br>Management Adoption'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'tons_no3_change_base_bau', y2 = 'tons_no3_change_trt_bau', y3 = 'tons_no3_change_trt_bau', qu2 = 'none', outfile = outpath + "2030 Water Quality - Nitrate Runoff NFM.png")
    
    Plotting.mba_chart_onetrace_custom2(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_25\runoff_nitrates.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\runoff_nitrates.csv", xax = '2014 - 2030 Change in Nitrate Runoff With Riparian Restoration Scenarios', yax = 'Tons of Nitrate Runoff', mba = 'runoff_nitrates', x = ['Reference - No <br>Riparian Restoration', '25% Riparian<br> Restoration Adoption','100% Riparian<br> Restoration Adoption'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'tons_no3_change_base_bau', y2 = 'tons_no3_change_trt_bau', y3 = 'tons_no3_change_trt_bau', qu2 = 'none', outfile = outpath + "2030 Water Quality - Nitrate Runoff RRE.png")
    
    
        #Water Quality - Leaching
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\leach_nitrates.csv", xax = 'Nitrate Leaching - 2014', yax = 'Tons of Nitrate', mba = 'leaching_nitrates', x = 'landcover',y = 'tons_no3_14', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Water Quality - Nitrate Leaching.png")
    
    
    Plotting.mba_chart_onetrace_custom2(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\nfm_25\leach_nitrates.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\nfm_100\leach_nitrates.csv", xax = '2014 - 2030 Change in Nitrate Runoff With Nitrogem Fertilizer Management Scenarios', yax = 'Tons of Nitrate Runoff', mba = 'runoff_nitrates', x = ['Reference - No <br>Hedgerow Planting', '25% Hedgerow<br> Planting','100% Hedgerow <br>Planting'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'tons_no3_change_base_bau', y2 = 'tons_no3_change_trt_bau', y3 = 'tons_no3_change_trt_bau', qu2 = 'none', outfile = outpath + "2014 Water Quality - Nitrate Leaching NFM.png")
    
    Plotting.mba_chart_onetrace_custom2(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\leach_nitrates.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\Riparian\RRE_COUNTY_100\leach_nitrates.csv", xax = '2014 - 2030 Change in Nitrate Leaching With Riparian Restoration Scenarios', yax = 'Tons of Nitrate Runoff', mba = 'runoff_nitrates', x = ['Reference - No <br>Riparian Restoration', '25% Riparian<br> Restoration','100% Riparian <br>Restoration'],y = 'None', yrange = [0,1], qu = 'None', remzeros = 0, y1 = 'tons_no3_change_base_bau', y2 = 'tons_no3_change_trt_bau', y3 = 'tons_no3_change_trt_bau', qu2 = 'None', outfile = outpath + "2014 Water Quality - Nitrate Leaching RRE.png")
    

    #Flood Risk Reduction
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\flood100.csv", xax = 'Landcover in 100 Year Floodplain - 2014', yax = 'Hectare', mba = 'flood100', x = 'gen_class',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Flood Risk Reduction.png")
    
    Plotting.mba_chart_flood_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\flood100.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\flood100.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'flood100', pre = 'ha_change', remzeros = 0, qu = 'gen_class', qu2 = 'na', outfile = outpath + "2030 Flood Risk Reduction.png")

    #Air Pollution
    Plotting.airquality_plot_2014(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100",  outfile = outpath + "2014 Air Quality.png")
    
    Plotting.airquality_plot(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100", outfile = outpath + "2030 Air Quality Total.png")
    
    Plotting.airquality_plot_act(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100", outfile = outpath + "2030 Air Quality Change RRE.png", scenario = 'Riparian <br>Restoration<br>', title = "Air Pollutant Sequestration for 2030 with Riparian Restoration")
    
    Plotting.airquality_plot_act(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_25", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100", outfile = outpath + "2030 Air Quality Change HPL.png", scenario = 'Hedgerow <br>Planting <br>', title = "Air Pollutant Sequestration for 2030 with Hedgerow Planting") # Hedgerow planting is not workingin tool
    
    Plotting.airquality_plot_act(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\urb_25", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\urb_100", outfile = outpath + "2030 Air Quality Change URB.png", scenario = 'Urban <br>Forestry<br>', title = "Air Pollutant Sequestration for 2030 with Urban Tree Planting")
    
    
    #Scenic Value
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\scenic.csv", xax = '2014 Landcover in Highly Visible Areas', yax = 'Hectares', x = 'gen_class',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Scenic Value.png")
    
    Plotting.mba_chart_threetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\scenic.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'scenic', pre = 'ha_change', outfile = outpath + "2030 Scenic Value.png")
    
    #Terrestrial Connectivity
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\countymovement.csv", xax = 'Terrestrial Connectivity - 2014', yax = 'Hectares', x = 'movement_potential',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Terrestrial Connectivity.png")
    
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\ecamovement.csv", xax = 'Terrestrial Connectivity in Essential <br>Connectivity Areas - 2014', yax = 'Hectares', x = 'movement_potential',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 ECA Terrestrial Connectivity.png")
    
    
    Plotting.mba_chart_ter_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\countymovement.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_25\countymovement.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'flood100', pre = 'ha_change', remzeros = 0, qu = 'None', qu2 = 'na', outfile = outpath + "2030 Terrestrial Connectivity HPL.png")
    
    Plotting.mba_chart_ter_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\countymovement.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\countymovement.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'flood100', pre = 'ha_change', remzeros = 0, qu = 'None', qu2 = 'na', outfile = outpath + "2030 Terrestrial Connectivity RRE.png")
    
    Plotting.mba_chart_ter_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_100\ecamovement.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\hedgerow_25\ecamovement.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'flood100', pre = 'ha_change', remzeros = 0, qu = 'None', qu2 = 'na', outfile = outpath + "2030 ECA Terrestrial Connectivity HPL.png")
    
    Plotting.mba_chart_ter_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\ecamovement.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\ecamovement.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'flood100', pre = 'ha_change', remzeros = 0, qu = 'None', qu2 = 'na', outfile = outpath + "2030 ECA Terrestrial Connectivity RRE.png")
    
    
    #Natural Habitat Area
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\lcchange.csv", xax = 'Landcover - 2014', yax = 'Hectares', x = 'landcover',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Natural Habitat Area.png")

    
    Plotting.mba_chart_lc_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\lcchange.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\lcchange.csv",Plotting.plot_dict, xax = 'holder', yax = 'holder', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', xlist = ['Riparian Restoration 25% Adoption','Riparian Restoration 100% Adoption'], mba = 'rre', sce = 'Riparian Restoration', outfile = outpath + "2030 Natural Habitat Area RRE.png")
    
    
    Plotting.mba_chart_oak_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_25\lcchange.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_100\lcchange.csv",Plotting.plot_dict, xax = 'holder', yax = 'holder', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', xlist = ['Oak Conversion 25% Adoption','Oak Conversion 100% Adoption'], mba = 'oak', sce = 'Oak Conversion', outfile = outpath + "2030 Natural Habitat Area OAK.png")

    #New forest in PCA
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\pca_cover_change.csv", xax = 'Landcover - 2014', yax = 'Hectares', x = 'landcover',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Priority Conservation Areas.png")

    
    Plotting.mba_chart_lc_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\pca_cover_change.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\lcchange.csv",Plotting.plot_dict, xax = 'holder', yax = 'holder', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', xlist = ['Riparian Restoration 25% Adoption','Riparian Restoration 100% Adoption'], mba = 'rre', sce = 'Riparian Restoration', outfile = outpath + "2030 Priority Conservation Areas RRE.png")
    
    
    Plotting.mba_chart_oak_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_25\pca_cover_change.csv", r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_100\lcchange.csv",Plotting.plot_dict, xax = 'holder', yax = 'holder', pre = 'ha_change', qu = 'None', remzeros = 0, qu2 = 'None', xlist = ['Oak Conversion 25% Adoption','Oak Conversion 100% Adoption'], mba = 'oak', sce = 'Oak Conversion', outfile = outpath + "2030 Priority Conservation Areas OAK.png")
    

    #Aquatic Habitat
    Plotting.mba_chart_onetrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\aquatic.csv", xax = 'General Landcover in 2014 for Watersheds with Important Aquatic Habitat', yax = 'Hectares', x = 'gen_class',y = 'ha_2014', yrange = [0,1], remzeros= 1, outfile = outpath + "2014 Aquatic Biodiversity.png")
    
    Plotting.mba_chart_aquatic_twotrace(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25\aquatic.csv",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100\aquatic.csv", Plotting.plot_dict, xax = 'holder', yax = 'holder', mba = 'flood100', pre = 'ha_change', remzeros = 0, qu = 'gen_class', qu2 = 'na', outfile = outpath + "2030 Aquatic Biodiversity RRE.png")

        #Terrestrial Habitat
    Plotting.terrestrial_habitat_plot_RRE(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\RRE_COUNTY_100", '2030 Terrestrial Habitat Value for Riparian Restoration Scenarios', 'Riparian Restoration<br> 25% Adoption', 'Riparian Restoration <br>100% Adoption', outfile = outpath + "2030 Terrestrial Habitat Value RRE.png")
    
    Plotting.terrestrial_habitat_plot_RRE(r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_25",r"E:\BoxSync\Box Sync\Merced Project\Tool\outputs\activities\oak_100", '2030 Terrestrial Habitat Value for Riparian Restoration Scenarios', 'Oak Conversion<br> 25% Adoption', 'Oak Conversion <br>100% Adoption', outfile = outpath + "2030 Terrestrial Habitat Value OAK.png")
    
    
    
    
    
    
    
    
    
    
    
    
    
    