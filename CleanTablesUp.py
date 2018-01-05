# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 08:32:17 2018

@author: Dylan
"""

def Clean_Table (csv,idfield,valuefield = 'TEST',keepfields = [], renamefields = []):
    import pandas as pd
    """
    This function takes a csv and check it for consistency (and nulls) and drops fields
    that are unwanted, and renames fields that need to be renamed
    rename fields values must be in tuples where the first value is the existing field and the 2nd value is the new field name.
    example: renamefields = [('Value','Landcover')]
    """
    print ('reading csv ' + valuefield)
    df = pd.read_csv(csv, usecols = keepfields)
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


#Clean Near Tables
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_cpad.csv','IN_FID',keepfields = ['IN_FID','NEAR_DIST','ACCESS_TYP','UNIT_NAME','AGNCY_NAME'], renamefields = [('IN_FID','pointid'),('ACCESS_TYP','accesstype'),('UNIT_NAME','unitname'),('AGNCYNAME','agncyname'),('NEAR_DIST','near_cpad')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_fema.csv','IN_FID',keepfields = ['IN_FID','NEAR_DIST','F_Type'], renamefields = [('F_Type','fema_class'),('IN_FID','pointid'),('NEAR_DIST','near_fema')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_nwi.csv','IN_FID',keepfields = ['IN_FID','NEAR_DIST','WETLAND_TYPE'], renamefields = [('WETLAND_TYPE','nwi_class'),('IN_FID','pointid'),('NEAR_DIST','near_nwi')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_woodyrip.csv','IN_FID',keepfields = ['IN_FID','NEAR_DIST','NVCSNAME'], renamefields = [('NVCSNAME','woodyrip_class'),('IN_FID','pointid'),('NEAR_DIST','near_woody')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_riparian.csv','IN_FID',keepfields = ['IN_FID','NEAR_DIST','NVCSNAME'], renamefields = [('NVCSNAME','rip_class'),('IN_FID','pointid'),('NEAR_DIST','near_rip')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_roads.csv','IN_FID',keepfields = ['IN_FID','NEAR_DIST'], renamefields = [('IN_FID','pointid'),('NEAR_DIST','near_roads')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_rivers.csv','IN_FID',keepfields = ['IN_FID','NEAR_DIST'], renamefields = [('IN_FID','pointid'),('NEAR_DIST','near_rivers')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_streams.csv','IN_FID',keepfields = ['IN_FID','NEAR_DIST'], renamefields = [('IN_FID','pointid'),('NEAR_DIST','near_streams')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_parks.csv','IN_FID',keepfields = ['IN_FID','NEAR_DIST'], renamefields = [('IN_FID','pointid'),('NEAR_DIST','near_parks')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_cced.csv','IN_FID',keepfields = ['IN_FID','NEAR_DIST'], renamefields = [('IN_FID','pointid'),('NEAR_DIST','near_ease')])
####Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/NearTables/env_near_streams.csv','IN_FID',keepfields = ['IN_FID','NEAR_DIST'], renamefields = [('IN_FID','pointid'),('NEAR_DIST','near_streams')])
##
##
##
##
###Clean Raster/MBA Tables
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/JoinTables/env_calenviro.csv','pointid','valuefield',keepfields = ['pointid','PollutionScore','PopCharScore','CIscore'], renamefields = [('PollutionScore','poll_score'),('PopCharScore','popchar_score'),('CIscore','ci_score')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/JoinTables/env_fmmp.csv','pointid','polygon_ty',keepfields = ['pointid','polygon_ty'], renamefields = [('polygon_ty','fmmp_class')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/JoinTables/env_genplan.csv','pointid','valuefield',keepfields = ['pointid','GP'], renamefields = [('GP','gp_code')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/JoinTables/env_hydrovuln.csv','pointid','SUBCLASS',keepfields = ['pointid','SUBCLASS'], renamefields = [('SUBCLASS','hydrovuln_flag')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/JoinTables/env_sagbi_mod.csv','pointid','rat_grp',keepfields = ['pointid','rat_grp'], renamefields = [('rat_grp','sagbi_class')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/JoinTables/env_scenic.csv','pointid','valuefield',keepfields = ['pointid','grid_code'], renamefields = [('grid_code','scenic_val')])
##Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/JoinTables/env_subsidence.csv','pointid','valuefield',keepfields = ['pointid','grid_code'], renamefields = [('grid_code','subsidence_val')])
Clean_Table ('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/ValueTables/JoinTables/env_slope.csv','pointid','valuefield',keepfields = ['pointid','RASTERVALU'], renamefields = [('RASTERVALU','slope_degrees')])
