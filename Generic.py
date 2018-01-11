from __future__ import unicode_literals #Can Delete This
def set_paths_and_workspaces(workspace = 'P:/Temp', root_data_path = 'E:/mercedtool', mask_fc = 'D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Vectors.gdb/Test_Mask', CVA_List_L = '', midpath = 'MASTER_DATA', output_file_loc = 'P:/Temp', run_name = 'Test', conservation_fc = ''):
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

    global slope
    slope = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_slope.csv')
    all_layers.append(slope)

    global scenic
    scenic = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_scenic.csv')
    all_layers.append(scenic)


    global lc
    lc = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_landcovers.csv')
    all_layers.append(lc)

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
global tabs_all_df


global carb01
global carb14
global carb30


# Global Dictionaries

''' Activey abbreviations are 
oak - OAK WOODLAND RESTORATION
rre - RIPARIAN RESTORATION
mul - MULCHING
mma - REPLACING SYNTHETIC FERTILIZER WITH SOIL AMENDMENTS
nfm - NITROGEN FERTILIZER MANAGEMENT
ccr - COVER CROPS
aca - AVOIDED CONVERSION TO AG
acu - AVOIDED CONVERSION TO URBAN
hpl - HEDGEROW PLANTING
urb - URBAN FORESTRY


'''
global dict_activity

oakdict = {'name':'Oak Woodland Restoration','query' : 'holder', 'ag_modifier':1}
rredict = {'name':'Riparian Restoration','query' : 'holder', 'ag_modifer':1}
muldict =  {'name':'Mulching','query' : 'holder', 'ag_modifier':.20}
mmadict =  {'name':'Replacing Sythetic Fertilizer with Soil Amendments','query' : 'holder', 'ag_modifier':.35}
nfmdict = {'name':'Nirtrogen Fertilizer Management','query' : 'holder', 'ag_modifier':.25}
ccrdict = {'name':'Cover Crops', 'query':'holder', 'ag_modifier':.20}
acadict = {'name':'Avoided Conversion to Agriculture', 'query':'holder', 'ag_modifier':1}
acudict = {'name':'Avoided Conversion to Urban', 'query':'holder', 'ag_modifier':1}
hpldict = {'name':'Hedgerow Planting', 'query':'holder', 'ag_modifier':.35}
urbdict = {'name':'Urban Forestry', 'query':'holder', 'ag_modifier':1}


dict_activity = {'oak':oakdict, 'rre': rredict, 'mul':muldict, 'mma':mmadict, 'nfm':nfmdict, 'ccr':ccrdict,'aca':acadict,'acu':acudict,'hpl':hpldict, 'urb':urbdict}
#######################################################################################################################

"""
Initialization
"""
def create_processing_table(InPoints,inmask):
    """
    This function takes a point feature class (InPoints) and the user-defined processing area (inmask), selects by location
    abd exports a CSV file and reads the file into a global variable as a Pandas DF.
    """
    import arcpy
    import os
    import pandas as pd
    import Generic
    if inmask == 'D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Vectors.gdb/Mask_Dissolved':
        pts = pd.read_csv(Generic.Points_Table)
        return pts
    else:
        pass
##        arcpy.MakeFeatureLayer_management(InPoints,'temp')
##        arcpy.SelectLayerByLocation_management('temp','INTERSECT',inmask)
##        #copy featureclass
##        arcpy.CopyFeatures_management('temp',os.path.join(Generic.tempgdb,'' )
##        #fctocsv
##        pts = pd.read_csv(os.path.join(Generic.RDP, Generic.MP,'Temp/temp.csv'))
##        return pts


#PREPROCESSING FUNCTIONS

def FCstoCSVs (inputgdb,Outpath):
    """
    This function takes a workspace with vector feature classes and writes out their tables as CSVs
    to a user defined folder.
    Workspace_FCs is a geodatabase with feature classes.
    Outpath is the folder where the CSVs are written to.
    """
    import arcpy
    import csv
    #Set the Variables
    arcpy.env.workspace = inputgdb
    arcpy.env.overwriteOutput = 1
    flist = arcpy.ListFeatureClasses()
    for i in flist:
        table = i
        outfile = Outpath + i + '.csv'

    #--first lets make a list of all of the fields in the table
        fields = arcpy.ListFields(table)
        field_names = [field.name for field in fields]
        print (fields)
        print (field_names)
        # Now we create the output file and write the table to it
        with open(outfile,'w') as f:
            dw = csv.DictWriter(f,field_names, lineterminator = '\n')
            #--write all field names to the output file
            dw.writeheader()

            #--now we make the search cursor that will iterate through the rows of the table
            with arcpy.da.SearchCursor(table,field_names) as cursor:
                for row in cursor:
                    dw.writerow(dict(zip(field_names,row)))
def FCtoCSV (inputfc,Outpath):
    """
    This function takes a workspace with vector feature classes and writes out their tables as CSVs
    to a user defined folder.
    Workspace_FCs is a geodatabase with feature classes.
    Outpath is the folder where the CSVs are written to.
    """
    import arcpy
    import csv
    #--first lets make a list of all of the fields in the table
    fields = arcpy.ListFields(inputfc)
    field_names = [field.name for field in fields]
    print (fields)
    print (field_names)
    # Now we create the output file and write the table to it
    with open(Outpath,'w') as f:
        dw = csv.DictWriter(f,field_names, lineterminator = '\n')
        #--write all field names to the output file
        dw.writeheader()

        #--now we make the search cursor that will iterate through the rows of the table
        with arcpy.da.SearchCursor(inputfc,field_names) as cursor:
            for row in cursor:
                dw.writerow(dict(zip(field_names,row)))
def Make_Flags (Flags,Fieldname):
    """

    """
    import pandas as pd
    import Generic
    FLG = pd.read_csv(Flags)
    Generic.pts[Fieldname] = 0
    Generic.pts.loc[Generic.pts['pointid'].isin (FLG['pointid']), Fieldname] = 1


def Clean_Table (csv,idfield,length=5689373,keepfields = [], renamefields = [],valuefield = 'TEST'):
    """
    This function takes a csv and check it for consistency (and nulls) and drops fields
    that are unwanted, and renames fields that need to be renamed
    rename fields values must be in tuples where the first value is the existing field and the 2nd value is the new field name.
    example: renamefields = [('Value','Landcover')]
    """
    import pandas as pd
    import os
    import sys
    print ('reading csv ' + valuefield)
    if keepfields:
        df = pd.read_csv(csv, usecols = keepfields)
    else:
        df = pd.read_csv(csv)
    print (len(df))
    print ('Finished Loading DF, finding MAX')
    max = df[idfield].max()
    if (max != length) or (len(df) != length):
        print ("LENGTH IS WRONG")
        sys.exit()
    else:
        pass
    print ('Checking Uniqueness')
    unique = df[idfield].is_unique
    print (unique)
    if unique is True:
        pass
    else:
        print ("ID FIELD IS NOT UNIQUE")
        exit
    if valuefield in df:
        if df[valuefield].dtype == 'O':
            df[valuefield].fillna('None')
        else:
            df[valuefield].fillna(-9999)
    if not renamefields:
        print ("No fields to rename.")
    else:
        for i in renamefields:
            df = df.rename(columns={i[0]: i[1]})
    df.sort_values(idfield,inplace = True)
    os.rename (csv, os.path.join(os.path.dirname(csv), (os.path.basename(csv).split('.'))[0] + '_orig.csv'))
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]    
    df.to_csv(csv)

def MergeMultiDF(JoinField, dflist):
    '''Takes a list of dataframes and joins them on a common field'''
    #mba = pd.concat(temp, axis = 1)
    import pandas as pd
    import functools
    mba = functools.reduce(lambda left,right: pd.merge(left, right,on=JoinField), dflist)
    OutputDF = mba.loc[:, ~mba.columns.str.contains('^Unnamed')]
    return OutputDF


#Make MBA Raster
def MakeMBARaster(LUT,OutputPath,JoinKey,TargetKey,Lfield):
    """
    This function uses a lookup table and a raster to create a lookup raster.
    LUT = look up table CSV
    OutputPath = output raster
    JoinKey =
    """
    import arcpy
    import Generic
    from arcpy import env
    arcpy.CheckOutExtension("Spatial")
    #Set the Variables
    ws = 'E:/Temp'
    arcpy.env.workspace = ws
    arcpy.env.overwriteOutput = 1
    print ('Making Raster Layer')
    arcpy.MakeRasterLayer_management(raster,'temp')
    arcpy.AddJoin_management('temp',JoinKey,LUT,TargetKey)
    arcpy.CopyRaster_management('temp','temp2.tif')
    tempo = arcpy.sa.Lookup('temp2.tif',Lfield)
    print ('Saving Raster')
    tempo.save(OutputPath)

def RastersToPoints(Raster,ValueField,OutputName):
    """
    This function takes a raster, a value field and an output FC name, creates a point featureclass
    from the raster in the temp vector gdb in the Master Data Folder.
    """
    import arcpy
    print ('Doing: ' + Raster)
    arcpy.RasterToPoint_conversion(Raster,tempgdb+OutputName,ValueField)

def LoadCSVs(infolder):
    """
    This function takes a folder, and reads every csv in it into a dataframe
    and appends those dataframes to a list (dflist).
    """
    import arcpy
    import Generic
    import os
    from arcpy import env
    import pandas as pd
    #Set the Variables
    ws = infolder
    arcpy.env.workspace = ws
    arcpy.env.overwriteOutput = 1
    list1 = arcpy.ListFiles("*.csv")
    dflist = []
    print (list1)
    for i in list1:
        dflist.append(pd.read_csv(os.path.join(ws, i), encoding = 'latin-1'))

    newlist = []
    for i in dflist:
        newlist.append(i.loc[:, ~i.columns.str.contains('^Unnamed')])
    print (newlist)
    return newlist


def Merge2csvs(inputcsv1,inputcsv2,mergefield,outputcsv,origcol = 'none',newcol = 'none'):
    """
    This function combines 2 CSVs into a new csv by reading them into pandas dataframes, renaming the
    column in one if necessary to match the key column names, then merging on the key field.

    The reulting merged dataframe is written to the specified CSV.
    """

    import arcpy
    import functools
    import pandas as pd
    ws = "D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/MBTABLES"
    arcpy.env.workspace = ws
    arcpy.env.overwriteOutput = 1
    templist = [inputcsv1,inputcsv2]
    temp = []
    df1 = pd.read_csv(inputcsv1)
    df2 = pd.read_csv(inputcsv2)

    #if the column needs to be changed for the join to work rename it
    if origcol != 'none':
        df1 = df1.rename(columns={origcol : newcol})
    result = pd.merge(df2, df1, on=mergefield)
    result.to_csv(outputcsv)


def ChangeFlag():
    import pandas as pd
    query = '''tabs_all_df['LC2030'] != tabs_all_df['LC2014']''' 
    testquery = (tabs_all_df['LC2001'] != tabs_all_df['LC2014'])
    tabs_all_df['lcchange'] = 1
    tabs_all_df.loc[testquery, 'lcchange'] = 0

def list_csvs_in_folder(path_to_folder, filetype, option = 'basename_only'):
    
    import arcpy
    arcpy.env.workspace = path_to_folder
    
    if option == 'basename_only':
        return [i.split('.')[0] for i in arcpy.ListFiles('*.' + filetype)]
    else:
        return arcpy.ListFiles('*.' + filetype)



<<<<<<< HEAD

=======
>>>>>>> b092b0df5497f9eb24b77b20e838457a8080c110





