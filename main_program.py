#run entire program
import arcpy
import sys
import Helpers
import os
#variables passed in from ArcMap tool

run_name = arcpy.GetParameterAsText(0)       #this will be prepended to raster output file name, no spaces
output_file_location = arcpy.GetParameterAsText(1)  #must be a gdb
scratch_folder = arcpy.GetParameterAsText(2) #this is the scratch folder, automatically set to the parent folder the output file gdb

rootpath = arcpy.GetParameterAsText(3) #Rootpath of data location
activitylist = []
#if not arcpy.GetParameterAsText(8):
#    activitylist.append('rre')
#    arcpy.AddMessage('added rre to activity list')
#if not arcpy.GetParameterAsText(10):
#    activitylist.append('oak')
#    arcpy.AddMessage('added oak to activity list')
#if not arcpy.GetParameterAsText(12):
#    activitylist.append('ccr')
#    arcpy.AddMessage('added ccr to activity list')
#if not arcpy.GetParameterAsText(14):
#    activitylist.append('mul')
#    arcpy.AddMessage('added mul to activity list')
#if not arcpy.GetParameterAsText(16):
#    activitylist.append('nfm')
#    arcpy.AddMessage('added nfm to activity list')
#if not arcpy.GetParameterAsText(18):
#    activitylist.append('hpl')
#    arcpy.AddMessage('added hpl to activity list')
#if not arcpy.GetParameterAsText(20):
#    activitylist.append('urb')
#    arcpy.AddMessage('added rre to activity list')
#  

if not activitylist:
    activitylist.append('rre')
    
scenario = arcpy.GetParameterAsText(6)

if not arcpy.GetParameterAsText(4):
    user_treatment_area = "None"
else:
    user_treatment_area = arcpy.GetParameterAsText(4)
#Processing Area
mask = arcpy.GetParameterAsText(5)  #This is the user chosen mask
customdev = os.path.normpath(arcpy.GetParameterAsText(7))
mask = 'None'
if not mask:
    mask="None"
print (mask)
import Generic
run_nme = 'test'


#First check for spatial analyst, arcinfo pfodcut level, and version --> kill tool if not active
#if Generic.check_extensions('Spatial') ==0:
#    arcpy.AddMessage("********************The Spatial Analyst Extension is required to run this tool but is not available at this time.*************")
#    sys.exit()
#
#if not arcpy.ProductInfo()=='ArcInfo':
#    arcpy.AddMessage("********************The Carbon Tool requires a 10.2.2 or later ArcInfo (advanced) license - tool won't work with a standard or basic license.*************")
#    sys.exit()
#
#if (arcpy.GetInstallInfo()['Version'] not in ('10.2.2', '10.3', '10.3.1', '10.3.2')):
#    arcpy.AddMessage("********************The Carbon Tool requires an version 10.2.2 or later of ArcGIS.*************")
#    sys.exit()

#Generic.set_paths_and_workspaces(scratch_gdb, rootpath, acreage_cap_vineyard, acreage_cap_urban, 'Carbon Framework/GIS Data/MASTER_DATA/')
Helpers.pmes (mask)
Generic.set_paths_and_workspaces(scratch_folder, rootpath, mask, 'MASTER_DATA/', output_file_location, run_name)

if 'rre' in activitylist:
#    Generic.dict_activity['rre']['adoption'] = float(arcpy.GetParameterAsText(9))
    Generic.dict_activity['rre']['adoption'] = 20.00
    arcpy.AddMessage(Generic.dict_activity['rre']['adoption'])
    arcpy.AddMessage('added rre adoption to dictionary')
if 'ccr' in activitylist:
    arcpy.AddMessage(Generic.dict_activity['ccr']['adoption'])
    Generic.dict_activity['ccr']['adoption'] = float(arcpy.GetParameterAsText(11))
    
#if 'rre' in activitylist:
#    Generic.dict_activity['rre']['adoption'] = float(arcpy.GetParameterAsText(9))
#    arcpy.AddMessage(Generic.dict_activity['rre']['adoption'])
#    arcpy.AddMessage('added rre adoption to dictionary')
#if 'ccr' in activitylist:
#    arcpy.AddMessage(Generic.dict_activity['ccr']['adoption'])
#    Generic.dict_activity['ccr']['adoption'] = float(arcpy.GetParameterAsText(11))    
#    
#if 'rre' in activitylist:
#    Generic.dict_activity['rre']['adoption'] = float(arcpy.GetParameterAsText(9))
#    arcpy.AddMessage(Generic.dict_activity['rre']['adoption'])
#    arcpy.AddMessage('added rre adoption to dictionary')
#if 'ccr' in activitylist:
#    arcpy.AddMessage(Generic.dict_activity['ccr']['adoption'])
#    Generic.dict_activity['ccr']['adoption'] = float(arcpy.GetParameterAsText(11))    
#    
#if 'rre' in activitylist:
#    Generic.dict_activity['rre']['adoption'] = float(arcpy.GetParameterAsText(9))
#    arcpy.AddMessage(Generic.dict_activity['rre']['adoption'])
#    arcpy.AddMessage('added rre adoption to dictionary')
#if 'ccr' in activitylist:
#    arcpy.AddMessage(Generic.dict_activity['ccr']['adoption'])
#    Generic.dict_activity['ccr']['adoption'] = float(arcpy.GetParameterAsText(11))    
#    
#if 'rre' in activitylist:
#    Generic.dict_activity['rre']['adoption'] = float(arcpy.GetParameterAsText(9))
#    arcpy.AddMessage(Generic.dict_activity['rre']['adoption'])
#    arcpy.AddMessage('added rre adoption to dictionary')
#if 'ccr' in activitylist:
#    arcpy.AddMessage(Generic.dict_activity['ccr']['adoption'])
#    Generic.dict_activity['ccr']['adoption'] = float(arcpy.GetParameterAsText(11))    
    
    
    
    
    
    

import Initial
import ActivityApplication
import ApplyActions
import pandas as pd
Helpers.pmes (scenario)
Helpers.pmes (customdev)
run_name = run_name.replace(" ", "_")

initout = Initial.DoInitial()
outdf = ActivityApplication.DoActivities(initout[0],activitylist, scenario, customdev)
#outdf = ApplyActions.ApplyGHG(outdf,initout[2],initout[3],activitylist)

outdf.to_csv("E:/Temp/test.csv")