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
import platform
import sys

output_file_location = arcpy.GetParameterAsText(0)  #must be a folder
rootpath = arcpy.GetParameterAsText(1) #Rootpath of data location
activitylist = [] #Create blank list to hold abbreviations of the activities selected from the tool input
timestr = time.strftime("%Y%m%d-%H%M%S") #Create timedate stamp of when the tool is run

newdir = os.path.join(output_file_location, timestr) #This creates a directory for the tool's outputs. It will create a new folder with a timestamp in the directory specified in the parameters.
if not os.path.exists(newdir):
    os.makedirs(newdir)
    
Generic.set_paths_and_workspaces(rootpath, output_file_location) #Run the function that creates global variables for paths

#Create a logfile in the output directory and add information about the tool's input parameter's to it.
global logfile
logfile = open(os.path.join(newdir, "logfile.txt"), "w")
logfile.close()
logfile = os.path.join((newdir), "logfile.txt")
Helpers.add_to_logfile(logfile,'Tool Started at: ' + time.strftime("%Y%m%d-%H%M%S") + ' \n')
Helpers.add_to_logfile2(logfile, '')

bit = platform.architecture()

#Check if the tool is running in a 32bit environment, must be in a 64 bit environment due to memory requirements
if bit[0] == '32bit':
    Helpers.add_to_logfile(logfile, '*******************************************Tool is running in 32bit python, must have 64-bit Background Processing installed and toggled on in Geoprocessing Options.  Go to Geoprocessing-->Geoprocessing Options in ArcMap and click "enable" under background processing. Also, in the "General" tab of the properties of the tool itself, make sure that "always run in the foreground" is unchecked. *******************************************')
    sys.exit()
    
#Add all of the tool parameters to the logfile
Helpers.add_to_logfile2(logfile, 'Writing out the tool parameter inputs','----------------------------------------------------------------------------------')
Helpers.add_to_logfile(logfile,'Output Folder' + ': ' + arcpy.GetParameterAsText(0))
Helpers.add_to_logfile(logfile,'Data Rootpath' + ': ' + arcpy.GetParameterAsText(1))
Helpers.add_to_logfile(logfile,'Conservation Mask' + ': ' + arcpy.GetParameterAsText(2))
Helpers.add_to_logfile(logfile,'Custom Processing Area' + ': ' + arcpy.GetParameterAsText(3))
Helpers.add_to_logfile(logfile,'Development Scenario' + ': ' + arcpy.GetParameterAsText(4))
Helpers.add_to_logfile(logfile,'Custom Development Mask' + ': ' + arcpy.GetParameterAsText(5))
Helpers.add_to_logfile(logfile,'Treatment Mask' + ': ' + arcpy.GetParameterAsText(44))

#Create a look up dictionary for activity abbreviations to full names
ludict = {'ac_wet_arc':'AC Wetland to Annual Row Crop','ac_gra_arc':'AC Grassland to Annual Row Crop','ac_irr_arc':'AC Irrigated Pasture to Annual Row Crop','ac_orc_arc': 'AC Orchard to Annual Row Crop','ac_arc_urb':'AC Annual Row Crop to Urban','ac_gra_urb':'AC Grassland to Urban','ac_irr_urb':'AC Irrigated Pasture to Urban','ac_orc_urb':'AC Orchard to Urban','ac_arc_orc':'AC Annual Row Crop to Orchard','ac_gra_orc':'AC Grassland to Orchard','ac_irr_orc':'AC Irrigated Pasture to Orchard','ac_vin_orc':'AC Vineyard to Orchard','ac_arc_irr':'AC Annual Row Crop to Irrigated Pasture','ac_orc_irr':'AC Orchard to Irrigated Pasture','rre':'Riparian Restoration','oak':'Oak Woodland Restoration','ccr':'Cover Crops','mul':'Mulching','nfm':'Improved Nitrogen Fertilizer Management','hpl':'Hedgerow Planting','urb':'Urban Tree Planting','gra':'Native Grassland Restoration','cam':'Replacing Synthetic Nitrogen Fertilizer with Soil Amendments','cag':'Compost Application to Non-irrigated Grasslands'}

#Set the development mask variable, if a development mask is provided, this will point to the polygon feature class
devmask = arcpy.GetParameterAsText(5)

#Loop through the Avoided Conversion parameters and see if any avoided conversion parameters have been set. If they have, add them to the avoided conversion activity dictionary.
acdict = {}
aclist2 = [45,47,49,51,53,55,57,59,61] #The parameter inputs for avoided conversion activities
Helpers.add_to_logfile2(logfile, '')
Helpers.add_to_logfile2(logfile, 'Checking for Avoided Conversion parameters:')

import pandas as pd
total_table = pd.DataFrame(columns = ['Activity','Acres Selected','Year Started','Years to Full Adoption','Total CO2e Reduction','Total CH4 Reductions','Total N2O Reductions'])

for i in aclist2:
    if arcpy.GetParameterAsText(i) == 'Wetland to Annual Cropland':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_wet_arc'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
            
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
            
    elif arcpy.GetParameterAsText(i) == 'Grassland to Annual Cropland':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_gra_arc'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Grassland to Annual Cropland has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
               
    elif arcpy.GetParameterAsText(i) == 'Irrigated Pasture to Annual Cropland':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_irr_arc'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Irrigated Pasture to Annual Cropland has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
               
    elif arcpy.GetParameterAsText(i) == 'Orchard to Annual Cropland':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_orc_arc'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Orchard to Annual Cropland has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
               
    elif arcpy.GetParameterAsText(i) == 'Annual Cropland to Urban':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_arc_urb'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Annual Cropland to Urban has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
               
    elif arcpy.GetParameterAsText(i) == 'Grassland to Urban':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_gra_urb'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Grassland to Urban has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
               
    elif arcpy.GetParameterAsText(i) == 'Irrigated Pasture to Urban':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_irr_urb'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Irrigated Pasture to Urban has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
               
    elif arcpy.GetParameterAsText(i) == 'Orchard to Urban':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_orc_urb'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Orchard to Urban has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
               
    elif arcpy.GetParameterAsText(i) == 'Annual Cropland to Orchard':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_arc_orc'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Annual Cropland to Orchard has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
               
    elif arcpy.GetParameterAsText(i) == 'Grassland to Orchard':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_gra_orc'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Grassland to Orchard has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
               
    elif arcpy.GetParameterAsText(i) == 'Irrigated Pasture to Orchard':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_irr_orc'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Irrigated Pasture to Orchard has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
               
    elif arcpy.GetParameterAsText(i) == 'Vineyard to Orchard':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_vin_orc'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Vineyard to Orchard has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
               
    elif arcpy.GetParameterAsText(i) == 'Annual Cropland to Irrigated Pasture':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_arc_irr'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Annual Cropland to Irrigated Pasture has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
               
    elif arcpy.GetParameterAsText(i) == 'Orchard to Irrigated Pasture':
        if arcpy.GetParameterAsText(i + 1) != '':
            acdict['ac_orc_irr'] = arcpy.GetParameterAsText(i + 1)
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Orchard to Irrigated Pasture has been selected: '  + arcpy.GetParameterAsText(i + 1) + ' Acres')
        else:
            Helpers.add_to_logfile(logfile,'Avoided Conversion - Wetland to Annual Cropland has been selected, but no acreage has been specified')
               
    elif arcpy.GetParameterAsText(i) == 'None':
        pass
    
    if arcpy.GetParameterAsText(i) != 'None':
        total_table = total_table.append({'Activity': arcpy.GetParameterAsText(i), 'Acres Selected': arcpy.GetParameterAsText(i + 1), 'Year Started':0, 'Years to Full Adoption': 0,'Total CO2e Reduction':0,'Total CH4 Reductions':0,'Total N2O Reductions':0}, ignore_index=True)
        
        
outpath = newdir +  '/'
#Add activity markers to list from tool input parameters
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
if arcpy.GetParameterAsText(30) == 'Yes':
    activitylist.append('urb')
    arcpy.AddMessage('added urb to activity list')
if arcpy.GetParameterAsText(32) == 'Yes':
    activitylist.append('gra')
    arcpy.AddMessage('added gra to activity list')
if arcpy.GetParameterAsText(36) == 'Yes':
    activitylist.append('cam')
    arcpy.AddMessage('added cam to activity list')
if arcpy.GetParameterAsText(40) == 'Yes':
    activitylist.append('cag')
    arcpy.AddMessage('added cag to activity list')
    
    
#Set the custom development parameters
if arcpy.GetParameterAsText(4) == 'Custom (Creates Custom Scenario)':
    dev = 1
    arcpy.Project_management(arcpy.GetParameterAsText(5), newdir + '/DevMask.shp', Generic.SPATIAL_REFERENCE_TEXT)
    devmask =  newdir + '/DevMask.shp'
    arcpy.AddMessage('New BAU')
elif arcpy.GetParameterAsText(4) == 'Custom (Adds on to Reference Developed Footprint)':
    dev = 2
    arcpy.Project_management(arcpy.GetParameterAsText(5), newdir + '/DevMask.shp', Generic.SPATIAL_REFERENCE_TEXT)
    devmask =  newdir + '/DevMask.shp'
    arcpy.AddMessage('Adding on to BAU')
else:
    dev = 0

Helpers.pmes('Dev Scenario is : ' + str(dev))


#Set the conservation mask parameters and variables
if not arcpy.GetParameterAsText(2):
    cm = 0
    conmask = 'None'
    Helpers.pmes('No Conservation Mask')
else:
    cm = 1
    conmask = newdir + '/ConMask.shp'
    arcpy.Project_management(arcpy.GetParameterAsText(2), newdir + '/ConMask.shp', Generic.SPATIAL_REFERENCE_TEXT)

    Helpers.pmes('A conservation mask is being used')
#Set the custom processing area variables if one has been chosen
if arcpy.GetParameterAsText(3):
    cproc = 1
    mask = newdir + '/CustProcMask.shp'
    arcpy.Project_management(arcpy.GetParameterAsText(3), newdir + '/CustProcMask.shp', Generic.SPATIAL_REFERENCE_TEXT)
    Helpers.pmes('User has chosen a custom processing area')
else:
    cproc = 0
    mask = 'None'
    Helpers.pmes ('No custom processing area')


Helpers.pmes ('Custom Provessing Mask is :' + mask)

adoptdict = {}

Helpers.add_to_logfile2(logfile, '')
Helpers.add_to_logfile2(logfile, 'Writing out the Activity Parameters for selected Treatments','----------------------------------------------------------------------------------------')


#Check to see what activities have been selected. For each activity that has been selected, add the relevant variables into the activity dictionary and send a message to the console.
if 'rre' in activitylist:
    rre = 1
    Generic.dict_activity['rre']['adoption'] = float(arcpy.GetParameterAsText(7)) 
    Generic.dict_activity['rre']['years'] = float(arcpy.GetParameterAsText(9))    
    Generic.dict_activity['rre']['adoptyear'] = float(arcpy.GetParameterAsText(8))  
    Helpers.add_to_logfile(logfile,'Riparian Restoration Adoption Acres' + ': ' + arcpy.GetParameterAsText(7))
    Helpers.add_to_logfile(logfile,'Riparian Restoration Beginning Year' + ': ' + arcpy.GetParameterAsText(8))
    Helpers.add_to_logfile(logfile,'Riparian Restoration Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(9))
    total_table = total_table.append({'Activity': 'Riparian Restoration', 'Acres Selected': arcpy.GetParameterAsText(7), 'Year Started':arcpy.GetParameterAsText(8), 'Years to Full Adoption': arcpy.GetParameterAsText(9),'Total CO2e Reduction':0,'Total CH4 Reductions':0,'Total N2O Reductions':0}, ignore_index=True)
else:
    rre = 0
Helpers.add_to_logfile(logfile,'Oak Woodland Restoration' + ': ' + arcpy.GetParameterAsText(10))
if 'oak' in activitylist:
    oak = 1
    Generic.dict_activity['oak']['adoption'] = float(arcpy.GetParameterAsText(11)) 
    Generic.dict_activity['oak']['years'] = float(arcpy.GetParameterAsText(13))    
    Generic.dict_activity['oak']['adoptyear'] = float(arcpy.GetParameterAsText(12))  
    Helpers.add_to_logfile(logfile,'Oak Woodland Restoration Adoption Acres' + ': ' + arcpy.GetParameterAsText(11))
    Helpers.add_to_logfile(logfile,'Oak Woodland Restoration Beginning Year' + ': ' + arcpy.GetParameterAsText(12))
    Helpers.add_to_logfile(logfile,'Oak Woodland Restoration Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(13))
    total_table = total_table.append({'Activity': 'Oak Woodland Restoration', 'Acres Selected': arcpy.GetParameterAsText(11), 'Year Started':arcpy.GetParameterAsText(12), 'Years to Full Adoption':  arcpy.GetParameterAsText(13),'Total CO2e Reduction':0,'Total CH4 Reductions':0,'Total N2O Reductions':0}, ignore_index=True)
else:
    oak = 0
Helpers.add_to_logfile(logfile,'Cover Cropping' + ': ' + arcpy.GetParameterAsText(14))    
if 'ccr' in activitylist:
    x = 14
    Generic.dict_activity['ccr']['adoption'] = float(arcpy.GetParameterAsText(15)) 
    Generic.dict_activity['ccr']['years'] = float(arcpy.GetParameterAsText(17))    
    Generic.dict_activity['ccr']['adoptyear'] = float(arcpy.GetParameterAsText(16))  
    Helpers.add_to_logfile(logfile,'Cover Cropping Adoption Acres' + ': ' + arcpy.GetParameterAsText(15))
    Helpers.add_to_logfile(logfile,'Cover Cropping Beginning Year' + ': ' + arcpy.GetParameterAsText(16))
    Helpers.add_to_logfile(logfile,'Cover Cropping Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(17))
    total_table = total_table.append({'Activity': 'Cover Cropping', 'Acres Selected': arcpy.GetParameterAsText(15), 'Year Started':arcpy.GetParameterAsText(16), 'Years to Full Adoption':  arcpy.GetParameterAsText(17),'Total CO2e Reduction':0,'Total CH4 Reductions':0,'Total N2O Reductions':0}, ignore_index=True)
    
Helpers.add_to_logfile(logfile,'Mulching' + ': ' + arcpy.GetParameterAsText(18))    
if 'mul' in activitylist:
    x = 18
    Generic.dict_activity['mul']['adoption'] = float(arcpy.GetParameterAsText(x + 1)) 
    Generic.dict_activity['mul']['years'] = float(arcpy.GetParameterAsText(x + 3))        
    Generic.dict_activity['mul']['adoptyear'] = float(arcpy.GetParameterAsText(x + 2))  
    Helpers.add_to_logfile(logfile,'Mulching Adoption Acres' + ': ' + arcpy.GetParameterAsText(x + 1))
    Helpers.add_to_logfile(logfile,'Mulching Beginning Year' + ': ' + arcpy.GetParameterAsText(x + 2))
    Helpers.add_to_logfile(logfile,'Mulching Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(x + 3))
    total_table = total_table.append({'Activity': 'Mulching', 'Acres Selected': arcpy.GetParameterAsText(x + 1), 'Year Started':arcpy.GetParameterAsText(x + 2), 'Years to Full Adoption':  arcpy.GetParameterAsText(x + 3),'Total CO2e Reduction':0,'Total CH4 Reductions':0,'Total N2O Reductions':0}, ignore_index=True)
    
Helpers.add_to_logfile(logfile,'Improved Nitrogen Fertilizer Management' + ': ' + arcpy.GetParameterAsText(22))    
if 'nfm' in activitylist:
    x = 22
    Generic.dict_activity['nfm']['adoption'] = float(arcpy.GetParameterAsText(x + 1)) 
    Generic.dict_activity['nfm']['years'] = float(arcpy.GetParameterAsText(x + 3))        
    Generic.dict_activity['nfm']['adoptyear'] = float(arcpy.GetParameterAsText(x + 2)) 
    Helpers.add_to_logfile(logfile,'Improved Nitrogen Fertilizer Management Adoption %' + ': ' + arcpy.GetParameterAsText(x + 1))
    Helpers.add_to_logfile(logfile,'Improved Nitrogen Fertilizer Management Beginning Year' + ': ' + arcpy.GetParameterAsText(x + 2))
    Helpers.add_to_logfile(logfile,'Improved Nitrogen Fertilizer Management Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(x + 3))
    total_table = total_table.append({'Activity': 'Improved Nitrogen Fertilizer Management', 'Acres Selected': arcpy.GetParameterAsText(x + 1), 'Year Started':arcpy.GetParameterAsText(x + 2), 'Years to Full Adoption':  arcpy.GetParameterAsText(x + 3),'Total CO2e Reduction':0,'Total CH4 Reductions':0,'Total N2O Reductions':0}, ignore_index=True)
    
Helpers.add_to_logfile(logfile,'Hedgerow Planting' + ': ' + arcpy.GetParameterAsText(26))    
if 'hpl' in activitylist:
    x = 26
    Generic.dict_activity['hpl']['adoption'] = float(arcpy.GetParameterAsText(x + 1)) 
    Generic.dict_activity['hpl']['years'] = float(arcpy.GetParameterAsText(x + 3))        
    Generic.dict_activity['hpl']['adoptyear'] = float(arcpy.GetParameterAsText(x + 2))   
    Helpers.add_to_logfile(logfile,'Hedgerow Planting Adoption Acres' + ': ' + arcpy.GetParameterAsText(x + 1))
    Helpers.add_to_logfile(logfile,'Hedgerow Planting Beginning Year' + ': ' + arcpy.GetParameterAsText(x + 2))
    Helpers.add_to_logfile(logfile,'Hedgerow Planting Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(x + 3))
    total_table = total_table.append({'Activity': 'Hedgerow Planting', 'Acres Selected': arcpy.GetParameterAsText(x + 1), 'Year Started':arcpy.GetParameterAsText(x + 2), 'Years to Full Adoption':  arcpy.GetParameterAsText(x + 3),'Total CO2e Reduction':0,'Total CH4 Reductions':0,'Total N2O Reductions':0}, ignore_index=True)
    
Helpers.add_to_logfile(logfile,'Replacing Synthetic Nitrogen Fertilizer with Soil Amendments' + ': ' + arcpy.GetParameterAsText(36))   
if 'cam' in activitylist:
    x = 36
    Generic.dict_activity['cam']['adoption'] = float(arcpy.GetParameterAsText(x + 1)) 
    Generic.dict_activity['cam']['years'] = float(arcpy.GetParameterAsText(x + 3))        
    Generic.dict_activity['cam']['adoptyear'] = float(arcpy.GetParameterAsText(x + 2))   
    Helpers.add_to_logfile(logfile,'Replacing Synthetic Nitrogen Fertilizer with Soil Amendments Adoption Acres' + ': ' + arcpy.GetParameterAsText(x + 1))
    Helpers.add_to_logfile(logfile,'Replacing Synthetic Nitrogen Fertilizer with Soil Amendments Beginning Year' + ': ' + arcpy.GetParameterAsText(x + 2))
    Helpers.add_to_logfile(logfile,'Replacing Synthetic Nitrogen Fertilizer with Soil Amendments Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(x + 3))
    total_table = total_table.append({'Activity': 'Replacing Synthetic Nitrogen Fertilizer with Soil Amendments', 'Acres Selected': arcpy.GetParameterAsText(x + 1), 'Year Started':arcpy.GetParameterAsText(x + 2), 'Years to Full Adoption':  arcpy.GetParameterAsText(x + 3),'Total CO2e Reduction':0,'Total CH4 Reductions':0,'Total N2O Reductions':0}, ignore_index=True)

Helpers.add_to_logfile(logfile,'Native Grassland Restoration' + ': ' + arcpy.GetParameterAsText(32))   
if 'gra' in activitylist:
    gra = 1
    x = 32
    Generic.dict_activity['gra']['adoption'] = float(arcpy.GetParameterAsText(x + 1)) 
    Generic.dict_activity['gra']['years'] = float(arcpy.GetParameterAsText(x + 3))        
    Generic.dict_activity['gra']['adoptyear'] = float(arcpy.GetParameterAsText(x + 2))   
    Helpers.add_to_logfile(logfile,'Native Grassland Restoration Adoption Acres' + ': ' + arcpy.GetParameterAsText(x + 1))
    Helpers.add_to_logfile(logfile,'Native Grassland Restoration Beginning Year' + ': ' + arcpy.GetParameterAsText(x + 2))
    Helpers.add_to_logfile(logfile,'Native Grassland Restoration Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(x + 3))
    total_table = total_table.append({'Activity': 'Native Grassland Restoration', 'Acres Selected': arcpy.GetParameterAsText(x + 1), 'Year Started':arcpy.GetParameterAsText(x + 2), 'Years to Full Adoption':  arcpy.GetParameterAsText(x + 3),'Total CO2e Reduction':0,'Total CH4 Reductions':0,'Total N2O Reductions':0}, ignore_index=True)
else: 
    gra = 0
Helpers.add_to_logfile(logfile,'Compost Application to Non-irrigated Grasslands' + ': ' + arcpy.GetParameterAsText(40))   
if 'cag' in activitylist:
    x = 40
    Generic.dict_activity['cag']['adoption'] = float(arcpy.GetParameterAsText(x + 1)) 
    Generic.dict_activity['cag']['years'] = float(arcpy.GetParameterAsText(x + 3))        
    Generic.dict_activity['cag']['adoptyear'] = float(arcpy.GetParameterAsText(x + 2))   
    Helpers.add_to_logfile(logfile,'Compost Application to Non-irrigated Grasslands Adoption Acres' + ': ' + arcpy.GetParameterAsText(x + 1))
    Helpers.add_to_logfile(logfile,'Compost Application to Non-irrigated Grasslands Beginning Year' + ': ' + arcpy.GetParameterAsText(x + 2))
    Helpers.add_to_logfile(logfile,'Compost Application to Non-irrigated Grasslands Years to Full Adoption' + ': ' + arcpy.GetParameterAsText(x + 3))
    total_table = total_table.append({'Activity': 'Compost Application to Non-irrigated Grasslands', 'Acres Selected': arcpy.GetParameterAsText(x + 1), 'Year Started':arcpy.GetParameterAsText(x + 2), 'Years to Full Adoption': arcpy.GetParameterAsText(x + 3),'Total CO2e Reduction':0,'Total CH4 Reductions':0,'Total N2O Reductions':0}, ignore_index=True)
    
Helpers.add_to_logfile(logfile,'Urban Tree Planting' + ': ' + arcpy.GetParameterAsText(30))   
if 'urb' in activitylist:
    x = 30
    Generic.dict_activity['urb']['adoption'] = float(arcpy.GetParameterAsText(x + 1)) 
    total_table = total_table.append({'Activity': 'Urban Tree Planting', 'Acres Selected': arcpy.GetParameterAsText(x + 1), 'Year Started':0, 'Years to Full Adoption': 0,'Total CO2e Reduction':0,'Total CH4 Reductions':0,'Total N2O Reductions':0}, ignore_index=True)
    Helpers.add_to_logfile(logfile,'Urban Canopy Growth' + ': ' + arcpy.GetParameterAsText(x + 1))



trt = Generic.trt_reductions
gen = Generic.lut_genclass
water = Generic.lut_wateruse
resistance =  Generic.lut_resistance
crop = Generic.lut_crop_value
nitrate = Generic.lut_nitrates
air = Generic.lut_air
cover14 = Generic.lut_cover14
cover30 = Generic.lut_cover30


#Set the reporting units
if arcpy.GetParameterAsText(68) == 'Acres':
    units = 'Acres'

if arcpy.GetParameterAsText(68) == 'Hectares':
    units = 'Hectares'


#If a treatment mask has been provided, set the variable
if arcpy.GetParameterAsText(44):
    treatmask = newdir + '/TreatMask.shp'
    arcpy.Project_management(arcpy.GetParameterAsText(44), newdir + '/TreatMask.shp', Generic.SPATIAL_REFERENCE_TEXT)

else:
    treatmask = 'None'

#Set the terrestrial habitat reporting flag
if arcpy.GetParameterAsText(63) == 'No':
    terflag = 0
    Helpers.pmes('Terrestrial Habitat reporting is turned off')

else:
    terflag = 1
    Helpers.pmes('Terrestrial Habitat reporting is turned on')

#Set the watershed integrity reporting flag
if arcpy.GetParameterAsText(64) == 'No':
    watflag = 0
    Helpers.pmes('Watershed Integrity reporting is turned off')

else:
    watflag = 1
    Helpers.pmes('Watershed Integrity reporting is turned on')



#Set the urban forest canopy values
if arcpy.GetParameterAsText(30) == 'Yes':
    ug = float(arcpy.GetParameterAsText(31))
    
    ucc = .102 + ug

else:
    ug = 0
    ucc = .102

#Check if plots are desired, if so set username and password variables for plotly
if arcpy.GetParameterAsText(65) == 'Yes':
    plotlykey = arcpy.GetParameterAsText(66)
else:
    plotlykey = 'None'
    
if arcpy.GetParameterAsText(65) == 'Yes':
    username = arcpy.GetParameterAsText(67)
else:
    username = 'None'
 
#check for plotly package and check plotly creds
import imp
if (username != "None") and (arcpy.GetParameterAsText(65) == 'Yes'):
    try:
        imp.find_module('plotly')
        found = True
        if found == True:
            try:
                import plotly.plotly as py
                py.sign_in(username, plotlykey)
            except:
                Helpers.add_to_logfile(logfile, '*******************************************Plotly user name ('+ username + ') or API key(' + plotlykey + ') is not valid.*******************************************')
                sys.exit()        
    except ImportError:
        Helpers.add_to_logfile(logfile, '*******************************************Plotly package is not installed.  Either install plotly package or uncheck Generate Plots.*******************************************')
        sys.exit()   

    
#Import the modules
import Initial
import ActivityApplication
import ApplyActions
import Reporting

#Run each module
initout = Initial.DoInitial(mask, cproc, dev, devmask, Generic.Carbon2001, Generic.Carbon2014, Generic.Carbon2030, Generic.valuetables, Generic.neartabs, Generic.Points, Generic.tempgdb, Generic.scratch, cm, conmask, treatmask)


Helpers.pmes('**FINISHED WITH INITIALIZATION MODULE, ENTERING ACTIVITY APPLICATION MODULE...***')
outdf = ActivityApplication.DoActivities(total_table,initout[0],activitylist, Generic.dict_activity,acdict,logfile, treatmask, dev, ug)


Helpers.pmes('**FINISHED WITH ACTIVITY APPLICATION MODULE, ENTERING CARBON ACCOUNTING MODULE...')
templist = ApplyActions.ApplyGHG(outdf[0],activitylist, Generic.dict_activity, trt, ug, logfile, dev)

##Use this line below for debugging purposes

Helpers.pmes("**CREATING MULTIBENEFIT REPORTS...**")
Reporting.report(templist[0],outpath,gen, water, resistance,crop,nitrate,air,cover14, cover30, Generic.lutables, acdict,oak ,rre ,dev,cm, gra, cproc, terflag, ug, ucc, logfile, units, watflag)
Helpers.pmes("**CREATING CARBON REPORTS...**")


#Finish other Reports
Reporting.emis_report(templist[0],outpath,activitylist,Generic.em14,Generic.em30, acdict,dev,cm, ug, logfile)
Reporting.carbreport(templist[0],outpath,activitylist,Generic.Carbon2014, Generic.Carbon2030,acdict, dev,cm, ug, logfile)

temptable = Reporting.report_acres(outdf[1],templist[0],activitylist,outpath, acdict, logfile)
Reporting.emissions(temptable,outpath,activitylist,acdict, logfile)
if plotlykey != 'None':
    import Create_Plots
    Create_Plots.Plots(outpath, acdict, activitylist, terflag,cproc,plotlykey, username, units, watflag)

