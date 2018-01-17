from __future__ import unicode_literals #Can Delete This
def set_paths_and_workspaces(workspace = 'E:/mercedtool', root_data_path = 'E:/mercedtool', mask_fc = 'D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Vectors.gdb/Test_Mask', CVA_List_L = '', midpath = 'MASTER_DATA', output_file_loc = 'P:/Temp', run_name = 'Test', conservation_fc = ''):
    """Workspace must be a file .gdb and is the place where all temp files and outputs will be placed.
    root_data_path -->  This path the top level folder for the data files (e.g., D:/CLOUD/Shared/Open Space/)
    midpath -->  This path is the path to the data files from roopath down the tree (e.g., Carbon Framework/GIS Data/SAMPLE_DATA/)
    """

    import arcpy
    import os
    import sys
    import pandas as pd
    arcpy.env.overwriteOutput = True


    arcpy.env.workspace = output_file_loc
    arcpy.env.scratchWorkspace = output_file_loc


    global ArcWorkspace
    ArcWorkspace = output_file_loc

    global ArcScratchWorkspace
    ArcScratchWorkspace = output_file_loc


    all_layers = []

    global LANDFIRE2001
##    LANDFIRE2001 = os.path.join(root_data_path, midpath, 'Rasters.gdb/LF2001_Combined')
    LANDFIRE2001 ='D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Landcover_Rasters/Landcover_2001.tif'
    all_layers.append(LANDFIRE2001)

    global LANDFIRE2014
##    LANDFIRE2014 = os.path.join(root_data_path, midpath, 'Rasters.gdb/LF2014_Combined')
    LANDFIRE2014 ='D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Landcover_Rasters/Landcover_2014.tif'
    all_layers.append(LANDFIRE2014)

    global SPATIAL_REFERENCE_TEXT
    SPATIAL_REFERENCE_TEXT = "PROJCS['NAD_1983_California_Teale_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',-4000000.0],PARAMETER['Central_Meridian',-120.0],PARAMETER['Standard_Parallel_1',34.0],PARAMETER['Standard_Parallel_2',40.5],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
    arcpy.env.cellSize = LANDFIRE2014
    arcpy.env.snapRaster = LANDFIRE2014

    global pts
    #Set Local Variables
    ##
    #Paths

    global tempwork
    tempwork = workspace

    global RDP
    RDP = root_data_path

    global MP
    MP = midpath

    global Root_Mid_Path
    Root_Mid_Path = os.path.join(RDP, MP)

    global tempgdb
    tempgdb = os.path.join(root_data_path,midpath,'temppts.gdb')

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

    global WS
    WS = workspace



    #Vectors
    global Points
    Points = os.path.join('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Vectors.gdb/LFC_Points_Merged')
    all_layers.append(Points)

    #Tables
    global Points_Table
    Points_Table = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'pointsmerged.csv')
    all_layers.append(Points_Table)
    
    
    global Carbon2001
    Carbon2001 = os.path.join(root_data_path, midpath, 'Tables/CarbonTables/Carb01.csv')
    all_layers.append(Carbon2001)

    global Carbon2014
    Carbon2014 = os.path.join(root_data_path, midpath, 'Tables/CarbonTables/Carb14.csv')
    all_layers.append(Carbon2014)

    global Carbon2030
    Carbon2030 = os.path.join(root_data_path, midpath, 'Tables/CarbonTables/Carb30.csv')
    all_layers.append(Carbon2030)
    
    global Carbon2030mod
    Carbon2030mod = os.path.join(root_data_path, midpath, 'Tables/CarbonTables/Carb30mod.csv')
    all_layers.append(Carbon2030mod)
    
    global calenviro
    calenviro = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_calenviro.csv')
    all_layers.append(calenviro)

    global fmmp
    fmmp = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_fmmp.csv')
    all_layers.append(fmmp)

    global genplan
    genplan = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_genplan.csv')
    all_layers.append(genplan)

    global hydrovuln
    hydrovuln = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_hydrovuln.csv')
    all_layers.append(hydrovuln)

#    global slope
#    slope = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_slope.csv')
#    all_layers.append(slope)

    global scenic
    scenic = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_scenic.csv')
    all_layers.append(scenic)


    global lc
    lc = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_landcovers.csv')
    all_layers.append(lc)
    
    global trt
    trt = os.path.join(root_data_path,midpath,'Tables/trt', 'trt_reductions.csv')
    all_layers.append(trt)

    #Global Variables


    
    #Near Tables
    global near_river
    near_river = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_rivers.csv')
    all_layers.append(near_river)

    global near_rip
    near_rip = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_riparian.csv')
    all_layers.append(near_rip)

    global near_streams
    near_streams = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_streams.csv')
    all_layers.append(near_streams)

    global near_cpad
    near_cpad = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_cpad.csv')
    all_layers.append(near_cpad)

    global near_nwi
    near_nwi = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_nwi.csv')
    all_layers.append(near_nwi)

#    global near_fema
#    near_fema = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_fema.csv')
#    all_layers.append(near_fema)

    global near_roads
    near_roads = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_roads.csv')
    all_layers.append(near_roads)

    global near_woodyrip
    near_woodyrip = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_woodyrip.csv')
    all_layers.append(near_woodyrip)

    global near_woodycrop
    near_woodycrop = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_woodycrop.csv')
    all_layers.append(near_woodycrop)

    #Lookup Tables
    global NitrateLU
    NitrateLU = os.path.join(root_data_path, midpath, 'Tables/LUTables/lut_nitrates.csv')
    all_layers.append(NitrateLU)

    global WaterUse
    WaterUse = os.path.join(root_data_path, midpath, 'Tables/LUTables/lut_wateruse.csv')
    all_layers.append(WaterUse)

    global Resistance
    Resistance = os.path.join(root_data_path, midpath, 'Tables/LUTables/lut_resistance.csv')
    all_layers.append(Resistance)

    global Crop_Value_LUT
    Crop_Value_LUT = os.path.join(root_data_path, midpath, 'Tables/LUTables/lut_crop_value.csv')
    all_layers.append(Crop_Value_LUT)

    global Air_Pollution
    Air_Pollution = os.path.join(root_data_path, midpath, 'Tables/LUTables/lut_air_pollution.csv')
    all_layers.append(Air_Pollution)

    global Activity_LUT
    Activity_LUT = os.path.join(root_data_path, midpath, 'Tables/trt/trt_reductions.csv')
    all_layers.append(Activity_LUT)




    #MISC
    global run_
    run = run_name
    #Outputs
    global CarbonRaster
    CarbonRaster = os.path.join(output_file_loc, run_name + "_CARBON_ALL")
    global CarbonStats
    CarbonStats = os.path.join(output_file_loc, run_name + "_CARBON_STATS")
    global CarbonStatsDetail
    CarbonStatsDetail = os.path.join(output_file_loc, run_name + "_CARBON_STATS_DETAIL")
    global CarbonStatsUrban
    CarbonStatsUrban = os.path.join(output_file_loc, run_name + "_CARBON_STATS_URBAN")

    #other vars
    vineyard_count =0
    global rr_count
    rr_count =0

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

    #set mask
    global MASK
    global VECTOR_MASK
    if mask_fc == "None":
        arcpy.AddMessage("Using county boundary as processing area...")
        MASK = os.path.join(root_data_path, midpath, 'Vectors.gdb/Mask_Dissolved')
        VECTOR_MASK = os.path.join(root_data_path, midpath, 'Vectors.gdb/Mask_Dissolved')
    else:
        VECTOR_MASK = mask_fc
        arcpy.AddMessage("Using user-defined data area as processing area...")
        #first check coordinate system and project if necessary
        desc= arcpy.Describe(mask_fc)
        desc2 = arcpy.Describe(LANDFIRE2014)
        sr_mask = desc.spatialReference
        sr_landfire =  desc2.spatialReference

        if sr_mask.Name != sr_landfire.Name:
            arcpy.AddMessage ("Projecting user-defined processing area...")
            arcpy.Project_management(mask_fc, os.path.join(arcpy.env.workspace,"MASK"), SPATIAL_REFERENCE_TEXT)
            MASK = os.path.join(arcpy.env.workspace,"MASK")
            all_layers.append(MASK)

        else:
            MASK = mask_fc

    all_layers.append(MASK)
    all_layers.append(VECTOR_MASK)



    #create logfile
    global logfile
    logfile = open(os.path.join(output_file_loc, "logfile.txt"), "w")
    logfile.close()
    logfile = os.path.join((output_file_loc), "logfile.txt")



######################################################################################################################
#Global Dataframe Variables
global small
global medium
small = 15000
medium = 15000


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

oakdict = {'name':'Oak Woodland Restoration','query' : 'holder', 'ag_modifier':1, 'grpsize':small, 'suitflag':'oaksuitflag','selquery':'holder'}
rredict = {'name':'Riparian Restoration','query' : 'holder', 'ag_modifier':1, 'grpsize':medium, 'suitflag':'ripsuitflag','selquery':'holder'}
muldict =  {'name':'Mulching','query' : 'holder', 'ag_modifier':.20, 'grpsize':small, 'suitflag':'mulsuitflag','selquery':'holder'}
nfmdict = {'name':'Nirtrogen Fertilizer Management','query' : 'holder', 'ag_modifier':.25,  'grpsize':small, 'suitflag':'nfmsuitflag','selquery':'holder'}
ccrdict = {'name':'Cover Crops', 'query':'holder', 'ag_modifier':.20,  'grpsize':small, 'suitflag':'ccrsuitflag','selquery':'holder'}
acadict = {'name':'Avoided Conversion to Agriculture', 'query':'holder', 'ag_modifier':1, 'grpsize':small, 'suitflag':'acasuitflag','selquery':'holder'}
acudict = {'name':'Avoided Conversion to Urban', 'query':'holder', 'ag_modifier':1,  'grpsize':small, 'suitflag':'acusuitflag','selquery':'holder'}
hpldict = {'name':'Hedgerow Planting', 'query':'holder', 'ag_modifier':.35,  'grpsize':small, 'suitflag':'hplsuitflag','selquery':'holder'}
urbdict = {'name':'Urban Forestry', 'query':'holder', 'ag_modifier':1, 'grpsize':small, 'suitflag':'urbsuitflag','selquery':'holder'}


dict_activity = {'oak':oakdict, 'rre': rredict, 'mul':muldict, 'mma':mmadict, 'nfm':nfmdict, 'ccr':ccrdict,'aca':acadict,'acu':acudict,'hpl':hpldict, 'urb':urbdict}


#######################################################################################################################





