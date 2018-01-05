#run entire program
import arcpy
import sys
#variables passed in from ArcMap tool

run_name = arcpy.GetParameterAsText(0)       #this will be prepended to raster output file name, no spaces

output_file_location = arcpy.GetParameterAsText(1)  #must be a gdb

scratch_folder = arcpy.GetParameterAsText(2) #this is the scratch folder, automatically set to the parent folder the output file gdb

rootpath = arcpy.GetParameterAsText(3) #Rootpath of data location

conserved_acreage = arcpy.GetParameterAsText(4)  #in the toolbox, this text must match exactly what's in the dict below
dict={'No conserved lands in next 20 years':'None', \
'Less than 40K acres conserved in the next 20 years':"Scenario_Acre <= 40000", \
'Less than 80K acres conserved in the next 20 years':"Scenario_Acre <= 80000", \
'Less than 120K acres conserved in the next 20 years':"Scenario_Acre <= 120000",\
'Use my own feature class for conserved areas':"Custom"}

if not arcpy.GetParameterAsText(5):
    custom_conservation_fc = "None"
else:
    custom_conservation_fc = arcpy.GetParameterAsText(5)  #in the toolbox, this text must match exactly what's in the dict below

acreage_cap_vineyard = arcpy.GetParameterAsText(6)  #Field for numeric input, default 25K
acreage_cap_urban = arcpy.GetParameterAsText(7)     #Field for numeric input, default 7.5K

scenario_name= arcpy.GetParameterAsText(8)  #Choices will be, for now, "None", "Improved Conifer Forest Management", "Fire Hazard Management", "Riparian Area Restoration", "Valley Oak Restoration", "Urban Tree Planting"
scenario_name2 = arcpy.GetParameterAsText(9)#Choices will be, for now, "None", "Improved Conifer Forest Management", "Fire Hazard Management", "Riparian Area Restoration", "Valley Oak Restoration", "Urban Tree Planting"
scenario_name3 = arcpy.GetParameterAsText(10)

if not arcpy.GetParameterAsText(11):
    user_treatment_area = "None"
else:
    user_treatment_area = arcpy.GetParameterAsText(11)

#Processing Area
mask = arcpy.GetParameterAsText(12)  #This is the user chosen mask

CVA_List = arcpy.GetParameterAsText(13)
#CVA_List = CVA_List.split(";")

bols = {14:'newburn_rr', 15:'newburn_vine', 16:'units', 17:'tpz', 18:'urban'}
if arcpy.GetParameterAsText(14) == 'true':
    newburn_rr = 1
else:
    newburn_rr = 0

if arcpy.GetParameterAsText(15) == 'true':
    newburn_vine = 1
else:
    newburn_vine = 0

if arcpy.GetParameterAsText(16) == 'true':
    units = 1
else:
    units = 0

if arcpy.GetParameterAsText(17) == 'true':
    tpz = 1
else:
    tpz = 0

if arcpy.GetParameterAsText(18) == 'true':
    urban = 1
else:
    urban = 0

if not mask:
    mask="None"

#SARAH--->inserted imports and set paths here - has to be down here
import Generic

#First check for spatial analyst, arcinfo pfodcut level, and version --> kill tool if not active
if Generic.check_extensions('Spatial') ==0:
    arcpy.AddMessage("********************The Spatial Analyst Extension is required to run this tool but is not available at this time.*************")
    sys.exit()

if not arcpy.ProductInfo()=='ArcInfo':
    arcpy.AddMessage("********************The Carbon Tool requires a 10.2.2 or later ArcInfo (advanced) license - tool won't work with a standard or basic license.*************")
    sys.exit()

if (arcpy.GetInstallInfo()['Version'] not in ('10.2.2', '10.3', '10.3.1', '10.3.2')):
    arcpy.AddMessage("********************The Carbon Tool requires an version 10.2.2 or later of ArcGIS.*************")
    sys.exit()

#Generic.set_paths_and_workspaces(scratch_gdb, rootpath, acreage_cap_vineyard, acreage_cap_urban, 'Carbon Framework/GIS Data/MASTER_DATA/')
Generic.set_paths_and_workspaces(scratch_folder, rootpath, acreage_cap_vineyard, acreage_cap_urban, mask, CVA_List, 'MASTER_DATA/', output_file_location, run_name, conserved_acreage  )
import arcpy, Carbon_Change, Treatment, Reporting

scenario_dict= {"Riparian Area Restoration":Generic.RiparianRestoration, "Valley Oak Restoration":Generic.OakRestoration, "Improved Conifer Forest Management":Generic.Zoning, "Urban Tree Planting":Generic.UrbanTree, "Fire Hazard Management":Generic.FireHazard, "Buckeye Forest":Generic.BuckeyeRRD, "Preservation Ranch Vineyards":Generic.PresRanchVineyards, "Preservation Ranch Estates":Generic.PresRanchEstates, "None":"None"}
treatment_list= []

if scenario_name != "None":
    treatment_list.append([scenario_name, scenario_dict[scenario_name]])
if scenario_name2!= "None" and (scenario_name2 != scenario_name):
    treatment_list.append([scenario_name2, scenario_dict[scenario_name2]])
if scenario_name3!= "None" and (scenario_name3 != scenario_name):
    treatment_list.append([scenario_name3, scenario_dict[scenario_name3]])
if scenario_name4!= "None" and (scenario_name3 != scenario_name):
    treatment_list.append([scenario_name4, scenario_dict[scenario_name4]])
if scenario_name5!= "None" and (scenario_name3 != scenario_name):
    treatment_list.append([scenario_name5, scenario_dict[scenario_name5]])
if scenario_name6!= "None" and (scenario_name3 != scenario_name):
    treatment_list.append([scenario_name6, scenario_dict[scenario_name6]])
if scenario_name7!= "None" and (scenario_name3 != scenario_name):
    treatment_list.append([scenario_name7, scenario_dict[scenario_name7]])
if scenario_name8!= "None" and (scenario_name3 != scenario_name):
    treatment_list.append([scenario_name8, scenario_dict[scenario_name8]])

run_name = run_name.replace(" ", "_")



Treatment.create_treatment_scenario(treatment_list, user_treatment_area)
Carbon_Change.carbon_change(scenario_name, run_name, treatment_list, urban)
if conserved_acreage == 'Use my own feature class for conserved areas':
    conserved_acreage =  'User defined conservation area'
Reporting.create_reports (treatment_list, conserved_acreage, output_file_location, Generic.vineyard_count, Generic.rr_count)
