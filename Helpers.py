# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 10:23:24 2018
This script holds the functions used in other modules of the tool.
@author: mtukman
"""
import ActivityApplication
import generic



def CreateEligDict(df, activity, dict_activity, dict_eligibility):
    import sys
    initflag = dict_activity[activity]['suitflag']
    if activity in dict_eligibility.keys():
        print('The activity is already in the dict_eligibility dictionary')
        sys.exit('***The activity is already in the dict_eligibility dictionary***')
    eli = df.groupby('LC2014').sum()[initflag]
    eli.loc['Annual Cropland'] = eli.loc['Annual Cropland'] * dict_activity[activity]['ag_modifier']
    #Need to add modifier for adoption accross the board from user input
    
    eli_dict_element = eli.to_dict()
    dict_eligibility[activity] = eli_dict_element
    

def selectionfunc (dict_eligibility,dict_activity):
    count = 0
    curgoal = goal    
    usednums = []
    Generic.tabs_all_df[selfield] = 0
    while count < goal:
        for x in range(500000):
            c = random.randint(1,groupnumber)
            if c in usednum:
                pass
            else:
                usednums.append(c)
                Generic.tabs_all_df.loc[(Generic.tabs_all_df[flagfield] == 1) & (Generic.tabs_all_df[flagfield] == c),selfield] = 1
                x =  len(Generic.tabs_all_df.loc[(Generic.tabs_all_df[flagfield] == 1) & (Generic.tabs_all_df[flagfield] == c)])
                count = count + x
                
                
def CreateSuitFlags(activity):
    '''Takes an activity name (a key from dict_activity) and uses
    that to calculate a 1/0 suitability flag for the activity 
    in the tabs_all_df dataframe'''
    import pandas as pd
    import Generic

    initflag = [Generic.dict_activity[activity]['suitflag']
    Generic.tabs_all_df[initflag] = 0
    Generic.tabs_all_df.loc[Generic.dict_activity[activity]['query'], initflag] = 1
    
    
    
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