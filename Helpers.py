# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 10:23:24 2018
This script holds the functions used in other modules of the tool.
@author: mtukman
"""
import Generic





    
    
def CreateEligDict(df, activity, dict_activity, dict_eligibility):
    import sys
    import Generic
    initflag = activity + 'suitflag'
    print ()
    if activity in dict_eligibility.keys():
        print('The activity is already in the dict_eligibility dictionary')
        sys.exit('***The activity is already in the dict_eligibility dictionary***')
    eli = df.groupby('LC2014').sum()[initflag]
    eli.loc['Annual Cropland'] = eli.loc['Annual Cropland'] * Generic.dict_activity[activity]['ag_modifier']
    #Need to add modifier for adoption accross the board from user input
    
    eli_dict_element = eli.to_dict()
    dict_eligibility[activity] = eli_dict_element
    

def selectionfunc (dict_eligibility,df, activity):
    """
    
    """
    import Generic
    import pandas as pd
    goal = 0
    tempdict = dict_eligibility[activity]
    klist = list(tempdict.keys())
    for i in klist:
        goal = goal + tempdict[i]
    goal = goal*.1
    count = 0
    print ('Goal is : ' + str (goal))
    initflag =  activity + 'suitflag'
    selflag = activity + 'selected'
    df[selflag] = 0
    print (selflag)
    print ('group size is :' + str(Generic.dict_activity[activity]['grpsize']))
    tempdf = df.groupby('medgroup_val').sum()[['pointid',initflag]]
    tempdf.loc[0:,'grptemp'] = tempdf.index
    vlen = len(tempdf['grptemp'])
    s = tempdf['grptemp'].sample(n = vlen)
    glist = []
    for i in s:
        if count<goal:
            count = count + tempdf.at[i,initflag]
            glist.append(i)
            
        else:
            pass
    print (len (glist))
    print (str(count))
    df.loc[df['medgroup_val'].isin(glist), selflag] = 1
    if activity == 'rre':
        df.loc[df['medgroup_val'].isin(glist), 'LC2014'] = 'Riparian Restoration' #CHANGE FIELD BEFORE FINAL
        df.loc[df['medgroup_val'].isin(glist), 'gridcode14'] = 9999 
        df.loc[df['medgroup_val'].isin(glist), 'lcchange'] = 0 
    if activity == 'oak':
        df.loc[df['medgroup_val'].isin(glist), 'LC2014'] = 'Oak Conversion' #CHANGE FIELD BEFORE FINAL
        df.loc[df['medgroup_val'].isin(glist), 'gridcode14'] = 11111
    return df
                
                
def CreateSuitFlags(activity,df):
    '''Takes an activity name (a key from dict_activity) and uses
    that to calculate a 1/0 suitability flag for the activity 
    in the tabs_all_df dataframe'''
    import Generic

    initflag = activity + 'suitflag'
    print (initflag)
    df[initflag] = 0
    df.loc[Generic.dict_activity[activity]['query'], initflag] = 1
    
    
    
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


def ChangeFlag(df,scenario):
    import pandas as pd
    query = '''tabs_all_df['LC2030'] != tabs_all_df['LC2014']''' 
    testquery = (df['LC2001'] != df[scenario])
    df['lcchange'] = 1
    df.loc[testquery, 'lcchange'] = 0

def list_csvs_in_folder(path_to_folder, filetype, option = 'basename_only'):
    
    import arcpy
    arcpy.env.workspace = path_to_folder
    
    if option == 'basename_only':
        return [i.split('.')[0] for i in arcpy.ListFiles('*.' + filetype)]
    else:
        return arcpy.ListFiles('*.' + filetype)
        
        
def CreateSpeciesTable(spcsv = "E:\\temp\\speciesranges.csv", 
luts = "D:\\TGS\\projects\\64 - Merced Carbon\\MBA\Deliverables from TNC\\Urban Footprint\\data\\lookup_tables", 
rids_only = "D:\\TGS\\projects\\64 - Merced Carbon\\MBA\\ToolData\\Vector\\speciesranges\\rids_in_county.csv" ):
    
    ''' Create species tables from CWHR tables.  Output is a dataframe
    that provides # of amphibians, birds, mammals, reptiles, and 
    threatened/endangered species by range ID.  Ranges are roughly 90
    acre square polygons
    INPUTS - Various CSVS
    OUTPUT - Dataframe
    NOTE THAT THE SPECIES RANGE CSV IS ALSO AT:
    "D:\\TGS\\projects\\64 - Merced Carbon\\MBA\\ToolData\\Vector\\speciesranges\\speciesranges.csv"
    '''
    
    spcsv = spcsv
    import os
    import pandas as pd
        
    climate_birds_csv = os.path.join(luts, 'list_climate_change_birds.csv')
    climate_except_birds_csv = os.path.join(luts, 'list_climate_change_except_birds.csv')
    threatened_endangered_csv = os.path.join(luts, 'list_threatened_endangered.csv')
    outdict = {}
    

    rids = pd.read_csv(spcsv)
    climate_birds = pd.read_csv(climate_birds_csv)
    climate_except_birds = pd.read_csv(climate_except_birds_csv)
    threated_endangered = pd.read_csv(threatened_endangered_csv)
    constrain = pd.read_csv(rids_only)
    rids = rids[rids['rid'].isin(constrain['rid'])][['rid', 'species_ranges']]
    
    #let t = a long string of species  -->  t = rids.loc[0,'species_ranges' ]
    def add_to_dict (row):
        q = row['species_ranges'][1:-1]
        outdict[row['rid']]={}
        outdict[row['rid']]['birds'] = len([i for i in q.split(',') if i.startswith('b')])
        outdict[row['rid']]['mammals'] = len([i for i in q.split(',') if i.startswith('m')])
        outdict[row['rid']]['amphibians'] = len([i for i in q.split(',') if i.startswith('a')])
        outdict[row['rid']]['reptiles'] = len([i for i in q.split(',') if i.startswith('r')])
        a = [i for i in q.split(',')]
        outdict[row['rid']]['climate_birds'] = len(climate_birds[climate_birds['species'].isin(a)])
        outdict[row['rid']]['climate_except_birds'] = len(climate_except_birds[climate_except_birds['species'].isin(a)])
        outdict[row['rid']]['threatened_endangered'] = len(threated_endangered[threated_endangered['species'].isin(a)])
    
    rids.apply(add_to_dict, axis = 1)
    
    out_df = pd.DataFrame.from_dict(outdict, 'index')
    return out_df
    
def ghgupdate(activity,df,carb30,carb30mod):

    import pandas as pd
    import Generic
    trt_temp = trt.loc[trt['Activity'] == 'rre']
    MergeMultiDF('LC2030MOD',[df,trt_temp])
    