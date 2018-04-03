# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 08:20:30 2018

@author: Dylan
"""
import arcpy

arcpy.ImportToolbox(r'E:\mercedtool\C-CAT.tbx','')
arcpy.MercedCarbonTool(r"E:\Temp\tooloutputs", r"E:\TGS\projects\Merced Carbon", None, None, "None", None, "Yes", 30000, 2014, 6, "No", 1000, 2014, 5, "No", 1000, 2014, 5, "No", 1000, 2014, 5, "No", 1000, 2014, 5, "No", 1000, 2014, 5, "No", 0.001, 2014, 2030, "No", 20, 2014, 5, "No", 20, 2014, 5, "No", 20, 2014, 5, None, "None", None, "None", None, "None", None, "None", None, "None", None, "None", None, "None", None, "None", None, "None", None, True, None)

