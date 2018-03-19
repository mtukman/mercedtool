"""
This script runs each of the individual modules for the tool.

This script takes the parameter inputs from the Python tool in ArcGIS and uses them as arguments to run the tool's modules.



"""
#run entire program
import arcpy
import Helpers
import Generic
import os
import time
#variables passed in from ArcMap tool
output_file_location = arcpy.GetParameterAsText(0)  #must be a folder
rootpath = arcpy.GetParameterAsText(1) #Rootpath of data location
activitylist = []
timestr = time.strftime("%Y%m%d-%H%M%S")
newdir = os.path.join(output_file_location, timestr) #This creates a directory for the tool's outputs. It will create a new folder with a timestamp in the directory specified in the parameters.
if not os.path.exists(newdir):
    os.makedirs(newdir)

#Create a logfile in the output directory and add information about the tool's input parameter's to it.
global logfile
logfile = open(os.path.join(newdir, "logfile.txt"), "w")
logfile.close()
logfile = os.path.join((newdir), "logfile.txt")
Helpers.add_to_logfile(logfile,'Tool Started at: ' + time.strftime("%Y%m%d-%H%M%S") + ' \n')

Helpers.add_to_logfile(logfile,'Output Folder' + ': ' + arcpy.GetParameterAsText(0))
Helpers.add_to_logfile(logfile,'Data Rootpath' + ': ' + arcpy.GetParameterAsText(1))
Helpers.add_to_logfile(logfile,'Conservation Mask' + ': ' + arcpy.GetParameterAsText(2))
Helpers.add_to_logfile(logfile,'Custom Processing Area' + ': ' + arcpy.GetParameterAsText(3))
Helpers.add_to_logfile(logfile,'Development Scenario' + ': ' + arcpy.GetParameterAsText(4))
Helpers.add_to_logfile(logfile,'Custom Development Mask' + ': ' + arcpy.GetParameterAsText(5))

#Set the development mask variable, if a development mask is provided, this will point to the polygon feature class
devmask = arcpy.GetParameterAsText(5)

#Look through the Avoided Conversion parameters and see if any avoided conversion parameters have been set. If they have, add them to the avoided conversion activity dictionary.
acdict = {}
aclist2 = [35,37,39,41,43,45,47,49,51]
for i in aclist2:
    if arcpy.GetParameterAsText(i) == 'Forest to Annual Row Crop':
        acdict['ac_for_urb'] = arcpy.GetParameterAsText(i + 1)
    if arcpy.GetParameterAsText(i) == 'Forest to Urban':
        acdict['ac_for_arc'] = arcpy.GetParameterAsText(i + 1)
    if arcpy.GetParameterAsText(i) == 'Grassland to Annual Row Crop':
        acdict['ac_gra_arc'] = arcpy.GetParameterAsText(i + 1)
    if arcpy.GetParameterAsText(i) == 'Irrigated Pasture to Annual Row Crop':
        acdict['ac_irr_arc'] = arcpy.GetParameterAsText(i + 1)
    if arcpy.GetParameterAsText(i) == 'Orchard to Annual Row Crop':
        acdict['ac_orc_arc'] = arcpy.GetParameterAsText(i + 1)
    if arcpy.GetParameterAsText(i) == 'Shrubland to Annual Row Crop':
        acdict['ac_shr_arc'] = arcpy.GetParameterAsText(i + 1)
    if arcpy.GetParameterAsText(i) == 'Vineyard to Annual Row Crop':
        acdict['ac_vin_arc'] = arcpy.GetParameterAsText(i + 1)
    if arcpy.GetParameterAsText(i) == 'Shrubland to Urban':
        acdict['ac_shr_urb'] = arcpy.GetParameterAsText(i + 1)
    if arcpy.GetParameterAsText(i) == 'Orchard to Urban':
        acdict['ac_orc_urb'] = arcpy.GetParameterAsText(i + 1)
        

outpath = newdir +  '/'
#Add activity markers to list
if arcpy.GetParameterAsText(6) == 'Yes':
    activitylist.append('rre')
    arcpy.AddMessage('added rre to activity list')
if arcpy.GetParameterAsText(10) == 'Yes':
    activitylist.append('oak')
    arcpy.AddMessage('added oak to activity list')
if arcpy.GetParameterAsText(14) == 'Yes':
    activitylist.append('ccr')
    arcpy.AddMessage('added ccr to activity list')
if arcpy.GetParameterAsText(18) == 'Yes':
    activitylist.append('mul')
    arcpy.AddMessage('added mul to activity list')
if arcpy.GetParameterAsText(22) == 'Yes':
    activitylist.append('nfm')
    arcpy.AddMessage('added nfm to activity list')
if arcpy.GetParameterAsText(26) == 'Yes':
    activitylist.append('hpl')
    arcpy.AddMessage('added hpl to activity list')


#Set the custom development parameters
if arcpy.GetParameterAsText(4) == 'Custom (Replaces Business as Usual)':
    dev = 1
    arcpy.CopyFeatures_management(arcpy.GetParameterAsText(5),newdir + '/DevMask.shp' )
    
elif arcpy.GetParameterAsText(4) == 'Custom (Adds on to Business as Usual)':
    dev = 2
    arcpy.CopyFeatures_management(arcpy.GetParameterAsText(5),newdir + '/DevMask.shp' )
    
else:
    dev = 0

Helpers.pmes('Dev Scenario is : ' + str(dev))


#Set the conservation mask parameters and variables
if not arcpy.GetParameterAsText(2):
    conservation = "None"
    cm = 0
else:
    cm = 1
    conservation = arcpy.GetParameterAsText(2)
    conmask = arcpy.GetParameterAsText(2)

#Set the custom processing area variables if one has been chosen
if not arcpy.GetParameterAsText(3):
    mask="None"
else:
    mask = arcpy.GetParameterAsText(3)
if arcpy.GetParameterAsText(3):
    cproc = 1
    Helpers.pmes('User has chosen a custom processing area')
else:
    cproc = 0
    Helpers.pmes ('No custom processing area')


    
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
Generic.set_paths_and_workspaces(rootpath, mask, 'MASTER_DATA/', output_file_location)
adoptdict = {}


#Check to see what activities have been selected. For each activity that has been selected, add the relevant variables into the activity dictionary and send a message to the console.
if 'rre' in activitylist:
    rre = 1
    Generic.dict_activity['rre']['adoption'] = float(arcpy.GetParameterAsText(7)) #Uncomment for final
    Generic.dict_activity['rre']['years'] = float(arcpy.GetParameterAsText(9)) #Uncomment for final   
    Generic.dict_activity['rre']['adoptyear'] = float(arcpy.GetParameterAsText(8)) #Uncomment for final 
    Helpers.add_to_logfile(logfile,'Riparian Restoration Adoption %' + ': ' + arcpy.GetParameterAsText(7))
    Helpers.add_to_logfile(logfile,'Riparian Restoration Beginning Year' + ': ' + arcpy.GetParameterAsText(8))
    Helpers.add_to_logfile(logfile,'Riparian Restoration Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(9))
else:
    rre = 0
Helpers.add_to_logfile(logfile,'Oak Woodland Conversion' + ': ' + arcpy.GetParameterAsText(10))
if 'oak' in activitylist:
    oak = 1
    Generic.dict_activity['oak']['adoption'] = float(arcpy.GetParameterAsText(11)) #Uncomment for final
    Generic.dict_activity['oak']['years'] = float(arcpy.GetParameterAsText(13)) #Uncomment for final   
    Generic.dict_activity['oak']['adoptyear'] = float(arcpy.GetParameterAsText(12)) #Uncomment for final 
    Helpers.add_to_logfile(logfile,'Oak Woodland Conversion Adoption %' + ': ' + arcpy.GetParameterAsText(11))
    Helpers.add_to_logfile(logfile,'Oak Woodland Conversion Beginning Year' + ': ' + arcpy.GetParameterAsText(12))
    Helpers.add_to_logfile(logfile,'Oak Woodland Conversion Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(13))
else:
    oak = 0
Helpers.add_to_logfile(logfile,'Cover Cropping' + ': ' + arcpy.GetParameterAsText(14))    
if 'ccr' in activitylist:
    Generic.dict_activity['ccr']['adoption'] = float(arcpy.GetParameterAsText(15)) #Uncomment for final
    Generic.dict_activity['ccr']['years'] = float(arcpy.GetParameterAsText(17)) #Uncomment for final   
    Generic.dict_activity['ccr']['adoptyear'] = float(arcpy.GetParameterAsText(16)) #Uncomment for final 
    Helpers.add_to_logfile(logfile,'Cover Cropping Adoption %' + ': ' + arcpy.GetParameterAsText(15))
    Helpers.add_to_logfile(logfile,'Cover Cropping Beginning Year' + ': ' + arcpy.GetParameterAsText(16))
    Helpers.add_to_logfile(logfile,'Cover Cropping Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(17))
    
    
Helpers.add_to_logfile(logfile,'Mulching' + ': ' + arcpy.GetParameterAsText(18))    
if 'mul' in activitylist:
    Generic.dict_activity['mul']['adoption'] = float(arcpy.GetParameterAsText(19)) #Uncomment for final
    Generic.dict_activity['mul']['years'] = float(arcpy.GetParameterAsText(21)) #Uncomment for final       
    Generic.dict_activity['mul']['adoptyear'] = float(arcpy.GetParameterAsText(20)) #Uncomment for final 
    Helpers.add_to_logfile(logfile,'Mulching Adoption %' + ': ' + arcpy.GetParameterAsText(19))
    Helpers.add_to_logfile(logfile,'Mulching Beginning Year' + ': ' + arcpy.GetParameterAsText(20))
    Helpers.add_to_logfile(logfile,'Mulching Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(21))
    
Helpers.add_to_logfile(logfile,'Nitrogen Fertilizer Management' + ': ' + arcpy.GetParameterAsText(22))    
if 'nfm' in activitylist:
    Generic.dict_activity['nfm']['adoption'] = float(arcpy.GetParameterAsText(23)) #Uncomment for final
    Generic.dict_activity['nfm']['years'] = float(arcpy.GetParameterAsText(25)) #Uncomment for final       
    Generic.dict_activity['nfm']['adoptyear'] = float(arcpy.GetParameterAsText(24)) #Uncomment for final
    Helpers.add_to_logfile(logfile,'Nitrogen Fertilizer Management Adoption %' + ': ' + arcpy.GetParameterAsText(23))
    Helpers.add_to_logfile(logfile,'Nitrogen Fertilizer Management Beginning Year' + ': ' + arcpy.GetParameterAsText(24))
    Helpers.add_to_logfile(logfile,'Nitrogen Fertilizer Management Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(25))
    
Helpers.add_to_logfile(logfile,'Hedgerow Planting' + ': ' + arcpy.GetParameterAsText(26))    
if 'hpl' in activitylist:
    Generic.dict_activity['hpl']['adoption'] = float(arcpy.GetParameterAsText(27)) #Uncomment for final
    Generic.dict_activity['hpl']['years'] = float(arcpy.GetParameterAsText(29)) #Uncomment for final       
    Generic.dict_activity['hpl']['adoptyear'] = float(arcpy.GetParameterAsText(29)) #Uncomment for final  
    Helpers.add_to_logfile(logfile,'Hedgerow Planting Adoption %' + ': ' + arcpy.GetParameterAsText(27))
    Helpers.add_to_logfile(logfile,'Hedgerow Planting Beginning Year' + ': ' + arcpy.GetParameterAsText(28))
    Helpers.add_to_logfile(logfile,'Hedgerow Planting Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(29))
    

#Helpers.add_to_logfile(logfile,'Urban Forestry' + ': ' + arcpy.GetParameterAsText(30))
#Helpers.add_to_logfile(logfile,'Urban Forestry Adoption %' + ': ' + arcpy.GetParameterAsText(31))
#Helpers.add_to_logfile(logfile,'Urban Forestry Beginning Year' + ': ' + arcpy.GetParameterAsText(32))
#Helpers.add_to_logfile(logfile,'Urban Forestry Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(33))


#If a treatment mask has been provided, set the variable
if arcpy.GetParameterAsText(34):
    treatmask = arcpy.GetParameterAsText(34)
else:
    treatmask = 'None'

#Import the modules
import Initial
import ActivityApplication
import ApplyActions
import ReportingTemp


#Run each module
initout = Initial.DoInitial(mask, cproc, devmask, arcpy.GetParameterAsText(6), Generic.Carbon2001, Generic.Carbon2014, Generic.Carbon2030, Generic.valuetables, Generic.neartabs, Generic.Points, Generic.tempgdb, Generic.scratch, cm, conmask, treatmask)
outdf = ActivityApplication.DoActivities(initout[0],activitylist, Generic.dict_activity,acdict, treatmask, dev)
templist = ApplyActions.ApplyGHG(outdf,activitylist, Generic.dict_activity)
templist[0].to_csv('P:/Temp/Temperino.csv')
ReportingTemp.report(templist[0],outpath, acdict,oak ,rre , dev,cm)
ReportingTemp.carbreport(templist[0],outpath,activitylist,Generic.Carbon2014, Generic.Carbon2030, dev,cm)


