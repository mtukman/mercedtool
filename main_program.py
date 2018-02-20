#run entire program
import arcpy
import Helpers
import os
import Generic
#variables passed in from ArcMap tool

run_name = arcpy.GetParameterAsText(0)       #this will be prepended to raster output file name, no spaces
output_file_location = arcpy.GetParameterAsText(1)  #must be a folder
rootpath = arcpy.GetParameterAsText(2) #Rootpath of data location
activitylist = []





#Add activity marker to list
if arcpy.GetParameterAsText(7) == 'Yes':
    activitylist.append('rre')
    arcpy.AddMessage('added rre to activity list')
if arcpy.GetParameterAsText(11) == 'Yes':
    activitylist.append('oak')
    arcpy.AddMessage('added oak to activity list')
if arcpy.GetParameterAsText(15) == 'Yes':
    activitylist.append('ccr')
    arcpy.AddMessage('added ccr to activity list')
if arcpy.GetParameterAsText(19) == 'Yes':
    activitylist.append('mul')
    arcpy.AddMessage('added mul to activity list')
if arcpy.GetParameterAsText(23) == 'Yes':
    activitylist.append('nfm')
    arcpy.AddMessage('added nfm to activity list')
if arcpy.GetParameterAsText(27) == 'Yes':
    activitylist.append('hpl')
    arcpy.AddMessage('added hpl to activity list')

if not activitylist:
    activitylist.append('rre')
    
scenario = arcpy.GetParameterAsText(5)

if not arcpy.GetParameterAsText(3):
    user_treatment_area = "None"
else:
    cm = 1
    user_treatment_area = arcpy.GetParameterAsText(3)


if not arcpy.GetParameterAsText(4):
    mask="None"
else:
    mask = arcpy.GetParameterAsText(4)
if arcpy.GetParameterAsText(4):
    cproc = 1
    Helpers.pmes('User has chosen a custom processing area')
else:
    cproc = 0
    Helpers.pmes ('No custom processing area')
Helpers.pmes (arcpy.GetParameterAsText(6))
if not arcpy.GetParameterAsText(6):
    cdev = 0
    Helpers.pmes('No custom development polygons')
else:
    cdev = 1
    Helpers.pmes('User has added custom development polygons')

    
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
    
Helpers.pmes ('Mask is :' + mask)
Generic.set_paths_and_workspaces(rootpath, mask, 'MASTER_DATA/', output_file_location, run_name)
adoptdict = {}

if 'rre' in activitylist:
    Generic.dict_activity['rre']['adoption'] = float(arcpy.GetParameterAsText(8)) #Uncomment for final
    Generic.dict_activity['rre']['years'] = float(arcpy.GetParameterAsText(10)) #Uncomment for final   
    Generic.dict_activity['rre']['adoptyear'] = float(arcpy.GetParameterAsText(9)) #Uncomment for final 
if 'oak' in activitylist:
    Generic.dict_activity['oak']['adoption'] = float(arcpy.GetParameterAsText(12)) #Uncomment for final
    Generic.dict_activity['oak']['years'] = float(arcpy.GetParameterAsText(14)) #Uncomment for final   
    Generic.dict_activity['oak']['adoptyear'] = float(arcpy.GetParameterAsText(13)) #Uncomment for final  
if 'ccr' in activitylist:
    Generic.dict_activity['ccr']['adoption'] = float(arcpy.GetParameterAsText(16)) #Uncomment for final
    Generic.dict_activity['ccr']['years'] = float(arcpy.GetParameterAsText(18)) #Uncomment for final   
    Generic.dict_activity['ccr']['adoptyear'] = float(arcpy.GetParameterAsText(17)) #Uncomment for final 
if 'mul' in activitylist:
    Generic.dict_activity['mul']['adoption'] = float(arcpy.GetParameterAsText(20)) #Uncomment for final
    Generic.dict_activity['mul']['years'] = float(arcpy.GetParameterAsText(22)) #Uncomment for final       
    Generic.dict_activity['mul']['adoptyear'] = float(arcpy.GetParameterAsText(21)) #Uncomment for final 
if 'nfm' in activitylist:
    Generic.dict_activity['nfm']['adoption'] = float(arcpy.GetParameterAsText(24)) #Uncomment for final
    Generic.dict_activity['nfm']['years'] = float(arcpy.GetParameterAsText(26)) #Uncomment for final       
    Generic.dict_activity['nfm']['adoptyear'] = float(arcpy.GetParameterAsText(25)) #Uncomment for final
if 'hpl' in activitylist:
    Generic.dict_activity['hpl']['adoption'] = float(arcpy.GetParameterAsText(28)) #Uncomment for final
    Generic.dict_activity['hpl']['years'] = float(arcpy.GetParameterAsText(30)) #Uncomment for final       
    Generic.dict_activity['hpl']['adoptyear'] = float(arcpy.GetParameterAsText(29)) #Uncomment for final  

import Initial
import ActivityApplication
import ApplyActions

Helpers.pmes ('Scenario Chosen: ' + scenario)
run_name = run_name.replace(" ", "_")
initout = Initial.DoInitial(mask, cproc, cdev, arcpy.GetParameterAsText(6), Generic.Carbon2001, Generic.Carbon2014, Generic.Carbon2030, Generic.valuetables, Generic.neartabs, Generic.Points, Generic.tempgdb, Generic.scratch, cm, user_treatment_area)
outdf = ActivityApplication.DoActivities(initout[0],activitylist, scenario, cdev, Generic.dict_activity)
templist = ApplyActions.ApplyGHG(outdf,initout[2],initout[3],activitylist, Generic.dict_activity)

templist[0].to_csv("E:/Temp/test.csv")