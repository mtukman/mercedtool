# -*- coding: utf-8 -*-
"""
This script reads, cleans up and merges Multi-benefit tables.
"""

import pandas as pd
import arcpy, calculations
ws = "D:/TGS/projects/64 - Merced Carbon/MBA/Deliverables from TNC/Urban Footprint/data/Extracted_CSVs"
arcpy.env.workspace = calculations.rev_slash(ws)
arcpy.env.overwriteOutput = 1


tempcsv = ''
def CSV_REVIEW (csv,idfield,valuefield):
    df = pd.read_csv(csv)
    max = df[idfield].max()
    if max != 5689373:
        print ("LENGTH IS WRONG")
        exit
    else:
        pass
    unique = df[idfield].is_unique
    print (unique)
    if unique is True:
        pass
    else:
        print ("ID FIELD IS NOT UNIQUE")
        exit
    if df[valuefield].dtype == 'O':
        df[valuefield].fillna('None')
    else:        
        df[valuefield].fillna(-9999)
    global tempcsv
    tempcsv = csv

#CSVs
BD = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/Bird_Density.csv'
CR= 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/california_combined_resistance.csv'
LC = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/Landcover_2001.csv'



CSV_REVIEW(BD,'pointid','Rank')
BD = pd.read_csv(tempcsv)
BD = BD.sort_values(by=['pointid'])

CSV_REVIEW(CR,'pointid','RASTERVALU')
CR = pd.read_csv(tempcsv)
CR = CR.sort_values(by=['pointid'])

CSV_REVIEW(LC,'pointid','Landcover_')
LC = pd.read_csv(tempcsv)
LC = LC.sort_values(by=['pointid'])


x = pd.concat([LC['pointid','Landcover_'], CR['RASTERVALU'],BD['Rank']], axis = 1)


#data_frames = [AgProd,] #,AgWatDem_01,AgWatDem_14,BaseCon_01,BaseCon_14,NetWat_01,NetWat_14,UrbWatDem_01,UrbWatDem_14, CarbDen_01,CarbDen_14,CombRes_01,CombRes_14,GWRech_01,GWRech_14
#for i in data_frames:
#    columns = ['OBJECTID', 'grid_code']
#    i.drop(columns, inplace=True, axis=1)
#
x.DataFrame.to_csv(df_merged, 'D:/TGS/projects/64 - Merced Carbon/MBA/Deliverables from TNC/Urban Footprint/data/Extracted_CSVs/MergedTables/MB_mergedTest.csv', sep=',', na_rep='.', index=False)
