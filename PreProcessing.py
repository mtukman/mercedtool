import arcpy
from Generic import *

def FCtoCSV (flist,Outpath):
    """
    This function takes a workspace with vector feature classes and writes out their tables as CSVs
    to a user defined folder.
    Workspace_FCs is a geodatabase with feature classes.
    Outpath is the folder where the CSVs are written to.
    """
    import arcpy
    import csv
    #Set the Variables
    ws = Workspace_FCs
    arcpy.env.workspace = ws
    arcpy.env.overwriteOutput = 1
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


def create_policy_knockouts(slope, outputcsv):
    """
    This function takes the point feature class (center points of landfire cells),
    applies a selection using the processing area mask,
    adds binary flags using pre-created csvs and creates a combined 'Knockout_Flag'.

    It then joins the carbon tables together, and the carbon table to the kockout table.
    The end result is a large csv with carbon and flag fields.

    Creates a vector ("policy_knockout" = 1)

    """

    #Import System Modules
    import arcpy
    import pandas as pd
    import Generic
    arcpy.env.overwriteOutput = True
    arcpy.env.extent = Generic.MASK

    #Create processing table
    Generic.create_processing_table(Generic.Points,Generic.MASK)


    #Create and Calculate Flag Fields- MUST RUN IN ORDER OR IT WILL NOT WORK
    print ('Creating Flags')
    Generic.add_to_logfile("FLAGGING PIXELS")
    Generic.Make_Flags (Generic.Wet_Flag,'Wet_Flag')
    Generic.Make_Flags (Generic.Rip_Flag,'Rip_Flag')
    Generic.Make_Flags (Generic.Rec_Flag,'Rec_Flag')
    Generic.Make_Flags (Generic.CPAD_Flag,'CPAD_Flag')
    Generic.pts.to_csv('E:/Temp/flags.csv')
    #Calculate the slope flag based on the slope value argument
    def SlopeFlag (Degree,Fieldname):
        import pandas as pd
        import Generic
        slp = pd.read_csv("D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/Slope.csv")
        query = slp[slp['RASTERVALU'] > Degree]
        Generic.pts[Fieldname] = 0
        Generic.pts.loc[Generic.pts['pointid'].isin (query['pointid']), Fieldname] = 1
        del slp
        del query

    SlopeFlag(slope,'Slope_Flag')
    #Flag pixels for knockout
    print ('Calculating Knockout Flags')
    Generic.KnockoutFinish(['Wet_Flag','Rip_Flag','Rec_Flag','CPAD_Flag','Slope_Flag'])
    Generic.pts = Generic.pts.loc[:, ~Generic.pts.columns.str.contains('^Unnamed')]
    Generic.pts.to_csv('E:/Temp/test2.csv')
    #Read the
    df1 = pd.read_csv(Generic.Carbon2001)
    df2 = pd.read_csv(Generic.Carbon2014)
    df3 = pd.read_csv(Generic.Carbon2030)
    print ('Combining Carbon Data')
    DFname = Generic.pts.join(df1, on='gridcode01',rsuffix='_other')
    DFname2 = DFname.join(df2, on='gridcode14',rsuffix = 'other')
    Final = DFname2.join(df3, on = 'gridcode14', rsuffix = 'other')
    print ('Outputting csv')
    Final.to_csv(outputcsv)


def CombineCSVs(outputcsv):
    """
    This function combines CSVs created by turning rasters into point layers, and
    by then writing the tables of those point layers into CSVs.

    The function reviews the CSVs for errors, and if there are no error, the function merges the CSVs on the
    'pointid' field and saves them to the specified output csv.
    """

    import arcpy
    import functools
    import pandas as pd
    ws = "D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/MBTABLES"
    arcpy.env.workspace = ws
    arcpy.env.overwriteOutput = 1
    def CSV_REVIEW (csv,idfield,valuefield,newname):
        print ('reading csv ' + valuefield)
        df = pd.read_csv(csv, usecols = [idfield,valuefield])
        print ('Finished Loading DF, finding MAX')
        max = df[idfield].max()
        if max != 5689373:
            print ("LENGTH IS WRONG")
            exit
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
        df = df.rename(columns={valuefield: newname})
    #    df.sort_values(idfield,inplace = True)
        df.to_csv(csv)

    CSV_REVIEW(ws+ "/" +'Landcover_2014.csv','pointid','Landcover_','LC')
    CSV_REVIEW(ws+ "/" +'Merced_Slope.csv','pointid','grid_code','SLP')
    CSV_REVIEW(ws+ "/" +'Nitrate_2001.csv','pointid','Nitrate_Va','N2V')
    CSV_REVIEW(ws+ "/" +'Viewshed.csv','pointid','grid_code','View')
    CSV_REVIEW(ws+ "/" +'WaterDemand2014.csv','pointid','grid_code','H2O')
    CSV_REVIEW(ws+ "/" +'Crop_Value_LU.csv','pointid','grid_code','Crp_Valu')
    #
    templist = arcpy.ListFiles()
    temp = []
    for i in templist:
        temp.append(pd.read_csv(ws+ "/" +i))
    #mba = pd.concat(temp, axis = 1)
    mba = functools.reduce(lambda left,right: pd.merge(left,right,on='pointid'), temp)
    mba = mba.loc[:, ~mba.columns.str.contains('^Unnamed')]
    mba.to_csv(outputcsv)


def Clean_Table (csv,idfield,valuefield,keepfields = [], renamefields = []):
    """
    This function takes a csv and check it for consistency (and nulls) and drops fields
    that are unwanted, and renames fields that need to be renamed
    rename fields values must be in tuples where the first value is the existing field and the 2nd value is the new field name.
    example: renamefields = [('Value','Landcover')]
    """
    print ('reading csv ' + valuefield)
    df = pd.read_csv(csv, usecols = [idfield,valuefield])
    print ('Finished Loading DF, finding MAX')
    max = df[idfield].max()
    if max != 5689373:
        print ("LENGTH IS WRONG")
        exit
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
    df[keepfields]
    if not renamefields:
        print ("No fields to rename.")
    else:
        for i in renamefields:
            df = df.rename(columns={i[0]: i[1]})
    #    df.sort_values(idfield,inplace = True)
    df.to_csv(csv)

def MergeMultiDF(Dataframes,JoinField,OutputDF):
    Dataframes
    #mba = pd.concat(temp, axis = 1)
    mba = functools.reduce(lambda left,right: pd.merge(left,right,on=JoinField), Dataframes)
    OutputDF = mba.loc[:, ~mba.columns.str.contains('^Unnamed')]

#Make MBA Raster
def MakeMBARaster(LUT,OutputPath,JoinKey,TargetKey,Lfield):
    import arcpy
    import Generic
    from arcpy import env

    arcpy.CheckOutExtension("Spatial")
    #Set the Variables
    ws = 'E:/Temp'
    arcpy.env.workspace = ws
    arcpy.env.overwriteOutput = 1

    arcpy.MakeRasterLayer_management(Generic.LC2014,'temp')
    arcpy.AddJoin_management('temp',JoinKey,LUT,TargetKey)
    arcpy.CopyRaster_management('temp','temp2.tif')
    tempo = arcpy.sa.Lookup('temp2.csv',Lfield)
    tempo.save(OutputPath)

def RastersToPoints(Raster,ValueField,OutputName,OutputGDB):
    import arcpy
    arcpy.RasterToPoint_conversion(Raster,OutputGDB+'/'+OutputName)