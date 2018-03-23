from __future__ import unicode_literals #Can Delete This
def set_paths_and_workspaces(root_data_path = 'E:/mercedtool', mask_fc = 'None', midpath = 'MASTER_DATA', output_file_loc = 'P:/Temp'):
    """Workspace must be a file .gdb and is the place where all temp files and outputs will be placed.
    root_data_path -->  This path the top level folder for the data files (e.g., D:/CLOUD/Shared/Open Space/)
    midpath -->  This path is the path to the data files from roopath down the tree (e.g., Carbon Framework/GIS Data/SAMPLE_DATA/)
    """

    import arcpy
    import os
    import sys
    arcpy.env.overwriteOutput = True


    arcpy.env.workspace = output_file_loc
    arcpy.env.scratchWorkspace = output_file_loc


    global ArcWorkspace
    ArcWorkspace = output_file_loc

    global ArcScratchWorkspace
    ArcScratchWorkspace = output_file_loc


    all_layers = []

    global SPATIAL_REFERENCE_TEXT
    SPATIAL_REFERENCE_TEXT = "PROJCS['NAD_1983_California_Teale_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',-4000000.0],PARAMETER['Central_Meridian',-120.0],PARAMETER['Standard_Parallel_1',34.0],PARAMETER['Standard_Parallel_2',40.5],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"

    global pts
    #Set Local Variables
    ##
    #Paths

    global RDP
    RDP = root_data_path

    global MP
    MP = midpath

    global Root_Mid_Path
    Root_Mid_Path = os.path.join(RDP, MP)

    global scratch
    scratch = os.path.join(root_data_path,midpath,'Scratch')

    global tempgdb
    tempgdb = os.path.join(root_data_path,midpath,'Scratch','Scratch.gdb')
    
    

    global MBTABS
    MBTABS = os.path.join(root_data_path,midpath,'Tables/MBATables')

    global neartabs
    neartabs = os.path.join(root_data_path,midpath,'Tables/NearTables')

    global vects
    vects = os.path.join(root_data_path,midpath,'Vectors.gdb')

    global lutables
    lutables = os.path.join(root_data_path,midpath,'Tables/LUTables')

    global valuetables
    valuetables = os.path.join(root_data_path,midpath,'Tables/ValueTables')




    #Look up tables for reporting functions
    
    global lut_genclass
    lut_genclass = os.path.join(lutables,'lut_genclass.csv')
    global lut_wateruse
    lut_wateruse = os.path.join(lutables,'lut_wateruse.csv')
    global lut_resistance
    lut_resistance = os.path.join(lutables,'lut_resistance.csv')
    global lut_crop_value
    lut_crop_value = os.path.join(lutables,'lut_crop_value.csv')
    global lut_nitrates
    lut_nitrates = os.path.join(lutables,'lut_nitrates.csv')
    global trt_reductions
    trt_reductions = os.path.join(root_data_path,midpath,'Tables/trt/trt_reductions.csv')

    #Vectors
    global Points
    Points = os.path.join('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Vectors.gdb/Just_PointID')
    all_layers.append(Points)


#    
#    
    global Carbon2001
    Carbon2001 = os.path.join(root_data_path, midpath, 'Tables/CarbonTables/Carb01.csv')
    all_layers.append(Carbon2001)

    global Carbon2014
    Carbon2014 = os.path.join(root_data_path, midpath, 'Tables/CarbonTables/Carb14.csv')
    all_layers.append(Carbon2014)

    global Carbon2030
    Carbon2030 = os.path.join(root_data_path, midpath, 'Tables/CarbonTables/Carb30.csv')
    all_layers.append(Carbon2030)



    #other vars

    global treatments_with_overlap
    treatments_with_overlap =[]

    global output_gdb
    output_gdb = output_file_loc
    #parse CVA_list

    #send error if any of the above layers don't exist on their specified path
    for layer in all_layers:
        if not arcpy.Exists(layer):
            print("Layer or dataset: " + layer + " doesn't exist")
            arcpy.AddMessage("Layer or dataset: " + layer + " doesn't exist")
            sys.exit()



######################################################################################################################
#Global Dataframe Variables
# Global Dictionaries

''' Activey abbreviations are 
oak - OAK WOODLAND RESTORATION
rre - RIPARIAN RESTORATION
mul - MULCHING
nfm - NITROGEN FERTILIZER MANAGEMENT
ccr - COVER CROPS
aca - AVOIDED CONVERSION TO AG
acu - AVOIDED CONVERSION TO URBAN
hpl - HEDGEROW PLANTING
urb - URBAN FORESTRY
'''
global dict_activity

oakdict = {'name':'Oak Woodland Restoration','query' : 'holder', 'ag_modifier':1, 'grpsize':'medium', 'suitflag':'oaksuitflag','selquery':'holder','adoption':'holder','years':'holder','adoptyear':'holder', 'adoptcap':.2}
rredict = {'name':'Riparian Restoration','query' : 'holder', 'ag_modifier':1, 'grpsize':'medium', 'suitflag':'ripsuitflag','selquery':'holder','adoption':'holder','years':'holder','adoptyear':'holder', 'adoptcap':1}
muldict =  {'name':'Mulching','query' : 'holder', 'ag_modifier':1, 'grpsize':'small', 'suitflag':'mulsuitflag','selquery':'holder','adoption':'holder','years':'holder','adoptyear':'holder', 'adoptcap':.2}
nfmdict = {'name':'Nirtrogen Fertilizer Management','query' : 'holder', 'ag_modifier':.684,  'grpsize':'small', 'suitflag':'nfmsuitflag','selquery':'holder','adoption':'holder','years':'holder','adoptyear':'holder', 'adoptcap':.25}
ccrdict = {'name':'Cover Crops', 'query':'holder', 'ag_modifier':.449,  'grpsize':'small', 'suitflag':'ccrsuitflag','selquery':'holder','adoption':'holder','years':'holder','adoptyear':'holder', 'adoptcap':.2}
hpldict = {'name':'Hedgerow Planting', 'query':'holder', 'ag_modifier':1,  'grpsize':'small', 'suitflag':'hplsuitflag','selquery':'holder','adoption':'holder','years':'holder','adoptyear':'holder', 'adoptcap':.3}
urbdict = {'name':'Urban Forestry', 'query':'holder', 'ag_modifier':1, 'grpsize':'small', 'suitflag':'urbsuitflag','selquery':'holder','adoption':'holder','years':'holder','adoptyear':'holder', 'adoptcap':.25}
acodict = {'name':'Avoid Conversion', 'query':'holder', 'ag_modifier':1, 'grpsize':'small', 'suitflag':'urbsuitflag','selquery':'holder','adoption':'holder','years':'holder','adoptyear':'holder', 'adoptcap':1}
camdict = {'name':'Compost Amendment', 'query':'holder', 'ag_modifier':0.259797042, 'grpsize':'small', 'suitflag':'camsuitflag','selquery':'holder','adoption':'holder','years':'holder','adoptyear':'holder', 'adoptcap':.2, 'orc_modifier': .25}
gradict = {'name':'Oak Woodland Restoration','query' : 'holder', 'ag_modifier':1, 'grpsize':'medium', 'suitflag':'oaksuitflag','selquery':'holder','adoption':'holder','years':'holder','adoptyear':'holder', 'adoptcap':.2}
cagdict = {'name':'Grassland Compost Amendment', 'query':'holder', 'ag_modifier':1, 'grpsize':'small', 'suitflag':'camsuitflag','selquery':'holder','adoption':'holder','years':'holder','adoptyear':'holder', 'adoptcap':.2}



dict_activity = {'oak':oakdict, 'rre': rredict, 'mul':muldict, 'nfm':nfmdict, 'ccr':ccrdict,'hpl':hpldict, 'urb':urbdict, 'aco':acodict, 'gra':gradict, 'cam':camdict, 'cag':cagdict}


#######################################################################################################################





