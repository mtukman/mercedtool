# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 10:23:24 2018
This script holds the functions used in other modules of the tool.
@author: mtukman
"""
import arcpy
def add_to_logfile(logfile,string_to_add):
    """
    This function writes to a logfile.
    """
    import arcpy
    lf = open(logfile, "a")
    lf.write(string_to_add + "\n")
    lf.close()
    arcpy.AddMessage(string_to_add)
    print (string_to_add)
def pmes(message):
    """
    Takes a string and prints it as an arcpy msg and as a python print statement
    """
    arcpy.AddMessage(message)
    print (message)
    
def CreateEligDict(df, activity, dictact, dict_eligibility, act):
    """
    This function takes the suitably flagged points and creates a dictionary with the number of suitable points for each activity, modified by ag modifiers for annual croplands.
    
    
    """
    pmes ('Eligibility for: ' + act)
    
    #Create a suiability flag field
    initflag = act + 'suitflag'
    df = df[['LC2030_trt_bau', initflag]]
    
    #Group on landcover to get counts of suitable points
    eli = df.groupby(['LC2030_trt_bau'], as_index = False).sum()  
    
    #Apply the annual cropland ag modifier
    eli.loc[(eli['LC2030_trt_bau'] == 'Annual Cropland'),initflag] = eli[initflag] * dictact[activity]['ag_modifier']
    
    #For compost amendment, apply the orchard modifier
    if act == 'cam':
        eli.loc[(eli['LC2030_trt_bau'] == 'Orchard'),initflag] = eli[initflag] * dictact[activity]['orc_modifier']
    eli_dict_element = eli.to_dict()
    
    #Add the number of eligible points to the eligibility dictionary
    dict_eligibility[act] = eli_dict_element
    

def selectionfunc (dict_eligibility,df, activity,dictact, act, logfile):
    """
    This function takes a dictionary, a dataframe and an activity.
    It takes a user input to determine how many pixels to select for the activity.
    """
    pmes('Selecting points for: ' + activity)
    import arcpy
    #Create a temporary dictionary of the activity's dictionary from the eligibility dict
    goal = 0
    tempdict = dict_eligibility[act]
    tempdict2 = tempdict[act + 'suitflag']
    pmes(tempdict2)
    
    #Create a list of the landcovers for the activity
    klist = list(tempdict2.keys())
    
    #Add up the points to get a total number of eligible points
    for i in klist:
        pmes (i)
        pmes (goal)
        pmes (tempdict2[i])
        goal = goal + tempdict2[i]
    pmes ('Suitable pixels: ' + str(goal))
    
    #Multiply the adoption goal to convert from acres to points
    goal1 = float(dictact[activity]['adoption']) * 4.49555  #update to link to user defined acres for final tool
    cap = goal * dictact[activity]['adoptcap'] #Modify the goal by the adoption cap
    
    #Use either the cap or the user defined goal, depending on number of points available
    if cap < goal1:
        goal = goal * float(dictact[activity]['adoptcap'])
    elif cap > goal1:
        goal = float(dictact[activity]['adoption'])*4.49555
 
    count = 0
    
    #Define fields
    pmes ('Goal is : ' + str (goal))
    pmes ('Cap is : ' + str (cap))
    initflag =  act + 'suitflag'
    selflag = act + 'selected'
    df[selflag] = 0
    pmes ('group size is :' + str(dictact[activity]['grpsize']))
    
    def select(groupsize, count):
        #Group pixels by their medium group value (medium grid)
        tempdf = df.groupby('medgroup_val').sum()[['pointid',initflag]]
        
        tempdf.loc[0:,'grptemp'] = tempdf.index
        tempdf.loc[tempdf[initflag] == 1]
        vlen = len(tempdf['grptemp']) #Get the length of the number of groups
        
        # s will be a randomly sampled list of all group values
        s = tempdf['grptemp'].sample(n = vlen)
        glist = [] #Any empty list to hold selected group values
        #Now the function loops through the list of group values and adds the pixels in each group to the count until the goal is reached
        arcpy.AddMessage(goal)
        for i in s:
            if count<goal:
                count = count + tempdf.at[i,initflag]
                glist.append(i)
                
            else:
                pass
    
        pmes (str(count))
        add_to_logfile(logfile,activity + ': user specified ' + str(goal1/4.49555) + ' acres, max eligible acres are ' + str(cap/4.495555))
        query = (df['medgroup_val'].isin(glist)) & (df[act + 'suitflag'] == 1)
        add_to_logfile(logfile,activity + ': Pixels Selected: ' + str(count) + ', Acres Selected: ' + str(count/4.495555))
        df.loc[query,selflag] = 1  
        
    #Run the select function using either small or large groups of points
    if dictact[activity]['grpsize'] == 'medium':
        select('medgroup_val', count)
    elif dictact[activity]['grpsize'] == 'small':
         select('smallgroup_val', count)
    
    return df

                
                
def CreateSuitFlags(activity,df,dictact, act):
    '''Takes an activity name (a key from dict_activity) and uses
    that to calculate a 1/0 suitability flag for the activity 
    in the tabs_all_df dataframe'''
    initflag = act + 'suitflag'
    pmes ('Calculating Suitability for : ' + initflag)
    df[initflag] = 0
    df.loc[dictact[activity]['query'], initflag] = 1

    
    
"""
Initialization
"""



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
        pmes (fields)
        pmes (field_names)
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
    pmes (fields)
    pmes (field_names)
    # Now we create the output file and write the table to it
    with open(Outpath,'w') as f:
        dw = csv.DictWriter(f,field_names, lineterminator = '\n')
        #--write all field names to the output file
        dw.writeheader()

        #--now we make the search cursor that will iterate through the rows of the table
        with arcpy.da.SearchCursor(inputfc,field_names) as cursor:
            for row in cursor:
                dw.writerow(dict(zip(field_names,row)))

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
    pmes ('reading csv ' + valuefield)
    if keepfields:
        df = pd.read_csv(csv, usecols = keepfields)
    else:
        df = pd.read_csv(csv)
    pmes (len(df))
    pmes ('Finished Loading DF, finding MAX')
    max = df[idfield].max()
    if (max != length) or (len(df) != length):
        print ("LENGTH IS WRONG")
        sys.exit()
    else:
        pass
    pmes ('Checking Uniqueness')
    unique = df[idfield].is_unique
    pmes (unique)
    if unique is True:
        pass
    else:
        pmes ("ID FIELD IS NOT UNIQUE")
        exit
    if valuefield in df:
        if df[valuefield].dtype == 'O':
            df[valuefield].fillna('None')
        else:
            df[valuefield].fillna(-9999)
    if not renamefields:
        pmes ("No fields to rename.")
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
    mba = functools.reduce(lambda left,right: pd.merge(left, right,on=JoinField, how = 'left'), dflist)
    OutputDF = mba.loc[:, ~mba.columns.str.contains('^Unnamed')]
    return OutputDF


def LoadCSVs(infolder):
    """
    This function takes a folder, and reads every csv in it into a dataframe
    and appends those dataframes to a list (dflist).
    """
    import arcpy
    import os
    import pandas as pd
    #Set the Variables
    ws = infolder
    arcpy.env.workspace = ws
    arcpy.env.overwriteOutput = 1
    list1 = arcpy.ListFiles("*.csv")
    dflist = []
    pmes (list1)
    for z in list1:
        pmes (str(os.path.join(ws, z)))
        dflist.append(pd.read_csv(os.path.join(ws, z), encoding = 'latin-1')) # , encoding = 'latin-1'

    newlist = []
    for v in dflist:
        newlist.append(v.loc[:, ~v.columns.str.contains('^Unnamed')])
    pmes ('Done Loading: ' + infolder)
    return newlist


def Merge2csvs(inputcsv1,inputcsv2,mergefield,outputcsv,origcol = 'none',newcol = 'none'):
    """
    This function combines 2 CSVs into a new csv by reading them into pandas dataframes, renaming the
    column in one if necessary to match the key column names, then merging on the key field.

    The reulting merged dataframe is written to the specified CSV.
    """

    import arcpy
    import pandas as pd
    ws = "D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/MBTABLES"
    arcpy.env.workspace = ws
    arcpy.env.overwriteOutput = 1
    df1 = pd.read_csv(inputcsv1)
    df2 = pd.read_csv(inputcsv2)

    #if the column needs to be changed for the join to work rename it
    if origcol != 'none':
        df1 = df1.rename(columns={origcol : newcol})
    result = pd.merge(df2, df1, on=mergefield)
    result.to_csv(outputcsv)


def ChangeFlag(df,scenario1,scenario2):
    testquery = (df[scenario1] != df[scenario2])
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
    
def Carbon2030calc():
    """
    This function calculate weighted carbon rates for 2030 using the 2014 carbon rates and the baseline carbon data.
    
    """
    
    import pandas as pd
    import numpy as np
    lf2014lu = pd.read_csv('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/LC2014_Full.csv')
    lf2014full = pd.read_csv('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/2014_CarbonWithOID_SUM.csv')
    lf2030lu = pd.read_csv('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/LF2030_Combined.csv')
    
    lf2014lu = lf2014lu.rename(columns={'grid_code': '2014gridcode'})
    lf2014lu = lf2014lu[['pointid','2014gridcode']]
    lf2030lu = lf2030lu.rename(columns={'grid_code': '2030gridcode'})
    lf2030lu = lf2030lu[['pointid','2030gridcode']]
    lf2014full = lf2014full.rename(columns = {'OID':'2030gridcode'})
    lf2030lu.loc[lf2030lu['2030gridcode'] == 3,'2030gridcode'] = 14
    lf2030lu.loc[lf2030lu['2030gridcode'] == 5,'2030gridcode'] = 15
    lf2014lu['2014gridcode'] = lf2014lu['2014gridcode'].apply(lambda x:x+100)
    lf2014full['SumCO2_ha'] = lf2014full['SumCO2_ha'].apply(lambda x:x/11.111111111111)
    
    result = pd.merge(lf2014lu, lf2030lu, on='pointid')
    lf2014full.loc[(lf2014full['Landcover_Class'] == 'Developed Roads') |(lf2014full['Landcover_Class'] == 'Developed') ,'Landcover_Class'] = 'Urban'
    lclist = lf2014full.Landcover_Class.unique()
    temp = lclist.tolist()
    result3 = result.merge(lf2014full,on = '2030gridcode', how = 'left')
    test4 = result3.groupby(['2030gridcode']).count()
    test4 = test4['pointid']
    test4 = test4.to_frame()
    test4['2030gridcode'] = test4.index
    test4 = test4.rename(columns={'pointid': 'pcount'})
    
    
    result4 = test4.merge(lf2014full,on = '2030gridcode', how = 'left')
    result4['Sumco'] = result4['SumCO2_ha']*result4['pcount']
    df1 = pd.DataFrame(np.nan, index=[], columns=[])
    
    for i in temp:
        
        total = result3.loc[result3['Landcover_Class'] == i]
        temp1 = result4.loc[result4['Landcover_Class'] == i]
        carbsum = temp1['Sumco'].sum()
        temp1['share'] = 0
        temp1['share'] = (temp1['SumCO2_ha']*temp1['pcount'])/carbsum
        temp1['new_rate'] = (temp1['share']*temp1['Totco'])/temp1['pcount']
        df1 = pd.concat([df1,temp1])
        
def samples(workspace,outputfolder,samplesize):
    """This function takes a workspace of CSVs, takes the first # of rows and writes them to a new directory with the same csv names."""
    import pandas as pd
    import arcpy
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True
    path1 = outputfolder
    path = workspace
    templist = arcpy.ListFiles("*.csv")
    print (templist)
    for i in templist:
        print (i)
        df = pd.read_csv(path + i,encoding='latin-1')
        df.sort_values('pointid',inplace = True)
        df = df.head(samplesize)
        df.to_csv(path1 + i)
        
        
        
        
def create_processing_table(InPoints,inmask, tempgdb, scratch):
    """
    This function takes a point feature class (InPoints) and the user-defined processing area (inmask), selects by location
    and exports a CSV file and reads the file into a global variable as a Pandas DF.
    """
    import arcpy
    import os
    import pandas as pd

    arcpy.MakeFeatureLayer_management(InPoints,'temp')
    arcpy.SelectLayerByLocation_management('temp','INTERSECT',inmask)
    #copy featureclass

    arcpy.env.workspace = tempgdb
    if not arcpy.Exists(tempgdb):
        arcpy.CreateFileGDB_management(scratch, tempgdb)

    else:
        if arcpy.Exists(tempgdb):
            for fc in arcpy.ListFeatureClasses(tempgdb):
                arcpy.Delete_management(fc)

    arcpy.CopyFeatures_management('temp',os.path.join(tempgdb,'temppts' ))
    
    #fctocsv
    FCtoCSV(os.path.join(tempgdb,'temppts' ),os.path.join(scratch, 'temp.csv'))
    temppts = pd.read_csv(os.path.join(scratch, 'temp.csv'))
    return temppts
        
        
        

        
        
        
        
        
def lc_mod(flagfield, label, labelfield, dataframe):
    """
    This function just simplifies the query that calculates a field"""
    dataframe.loc[(dataframe[flagfield] == 1), labelfield] = label
        
    
    

    

def devscen (td):
    """
    This function takes the development scenarios and creates a new field for each, and updates the landcovers and gridcodes.
    """
    
    td.loc[(td['LC2030_bau'] == 'Urban'), 'gridcode30_bau'] = 13
    td.loc[(td['LC2030_bau'] == 'Developed'), 'gridcode30_bau'] = 6
    td.loc[(td['dcode_maxinfill'] == 6), 'LC2030_max'] = 'Developed'
    td['gridcode30_med'] = td['gridcode30_bau']
    td['LC2030_med'] = td['LC2030_bau']
    td['LC2030_max'] = td['LC2030_bau']
    td['gridcode30_max'] = td['gridcode30_bau']
    td.loc[((td['LC2030_max'] != td['LC2014']) & (td['LC2030_max'].isin(['Developed','Urban','Developed Roads']))), 'LC2030_max'] = td['LC2014']
    td.loc[((td['LC2030_med'] != td['LC2014']) & (td['LC2030_med'].isin(['Developed','Urban','Developed Roads']))), 'LC2030_med'] = td['LC2014']
    
    td.loc[(td['dcode_medinfill'] ==  14),'dcode_medinfill'] = 13
    td.loc[(td['dcode_maxinfill'] ==  14),'dcode_maxinfill'] = 13
    td.loc[(td['dcode_maxinfill'] ==  7),'dcode_maxinfill'] = 6
    td.loc[(td['dcode_medinfill'] ==  7),'dcode_medinfill'] = 6
    td.loc[(td['dcode_maxinfill'] == 13), 'LC2030_max'] = 'Urban'
    
    td.loc[(td['dcode_maxinfill'] >0), 'gridcode30_max'] = ['dcode_maxinfill']
    td.loc[(td['dcode_medinfill'] == 13), 'LC2030_med'] = 'Urban'
    td.loc[(td['dcode_medinfill'] >0), 'gridcode30_med'] = ['dcode_medinfill']
    td.loc[(td['dcode_maxinfill'] == 6), 'LC2030_max'] = 'Developed'
    
    td.loc[(td['dcode_medinfill'] == 6), 'LC2030_med'] = 'Developed'
    
    return td
    
    

def carbon30(df):
    """
    This function calculate weighted carbon rates for 2030 using the 2014 carbon rates and the baseline carbon data.
    
    """
    import Generic
    import pandas as pd
    c14 = pd.read_csv(Generic.Carbon2014)
    c14['gridcode30_bau'] = c14['gridcode14'] + 100
    df2 = df[['gridcode30_bau','LC2030_bau','gridcode14','pointid']]
    df2 = df2.groupby(['gridcode30_bau','LC2030_bau','gridcode14'],as_index = False).count()
    d3 = pd.merge(df2,c14, left_on = 'gridcode14', right_on = 'gridcode14', how = 'left')
    d3['carb*pointid'] = d3['pointid'] * d3['carbrate14']
    d3.loc[(d3['landcover'] ==  'Developed'),'landcover'] = 'Urban'
    d3.loc[(d3['landcover'] ==  'Developed Roads'),'landcover'] = 'Urban'
    tsum = d3.groupby(['landcover'], as_index = False).sum()
    tsum = tsum[['landcover','carb*pointid', 'pointid']]
    tsum['avgrate'] = tsum['carb*pointid']/tsum['pointid']
    tsum2 = tsum[['landcover','avgrate']]
    tsum3 = tsum2.loc[tsum2['landcover'].isin(['Forest','Shrubland', 'Urban'])]
    tsum3.loc[(tsum3['landcover'] == 'Forest'), 'landcover'] = 'Young Forest'
    tsum3.loc[(tsum3['landcover'] == 'Shrubland'), 'landcover'] = 'Young Shrubland'
    tsum3.loc[(tsum3['landcover'] == 'Urban'), 'landcover'] = 'Developed'
    tsum4 = tsum2.loc[tsum2['landcover'].isin(['Urban'])]
    tsum4.loc[(tsum4['landcover'] == 'Urban'), 'landcover'] = 'Developed Roads'
    tsum5 = pd.concat([tsum2,tsum3,tsum4], ignore_index=True)
    
    
    d4 = pd.merge(d3,tsum5, left_on = 'LC2030_bau',right_on = 'landcover', how = 'left')
    d4['carb30temp'] = 0
    d4.loc[(d4['gridcode30_bau_x'] < 20), 'carb30temp'] = d4['avgrate']
    d4.loc[(d4['gridcode30_bau_x'] > 20), 'carb30temp'] = d4['carbrate14']
    
    d4['templc'] = d4['LC2030_bau']
    d4.loc[(d4['templc'] == 'Young Forest'), 'templc'] = 'Forest'
    d4.loc[(d4['templc'] == 'Young Shrubland'), 'templc'] = 'Shrubland'
    d4.loc[(d4['templc'] == 'Developed'), 'templc'] = 'Urban'
    d4.loc[(d4['templc'] == 'Developed Roads'), 'templc'] = 'Urban'
    
    newdf = d4.groupby(['gridcode30_bau_x', 'templc','LC2030_bau', 'carb30temp' ], as_index = False).sum()
    newdf['carb30*pointid'] = newdf['pointid'] * newdf['carb30temp'] #Make total carbon per gridcode
    
    
    newdf2 = newdf.groupby(['templc'], as_index = False).sum()
    newdf2 = newdf2[['templc','carb30*pointid']]
    
    newdf2 = newdf2.rename(columns = {'carb30*pointid':'sumcarb30'})
    
    newdf3 = pd.merge(newdf,newdf2, left_on = 'templc',right_on = 'templc', how = 'left')
    newdf3['share30'] = newdf3['carb30*pointid']/newdf3['sumcarb30']
    total30 = pd.read_csv(r"D:\TGS\projects\64 - Merced Carbon\MBA\ToolData\Tables\LookUpTables\carbon2030totals.csv")
    newdf4 = pd.merge(newdf3, total30, left_on = 'templc',right_on = 'landcover', how = 'left')
    newdf4['totshare30'] = newdf4['share30']*newdf4['carbontotal']
    newdf4['finalcarb30rate'] = newdf4['totshare30']/newdf4['pointid']
    return newdf4


    
        