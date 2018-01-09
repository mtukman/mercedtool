#Import System Modules
import arcpy
from arcpy import env
import Generic
import functools
import pandas as pd

Generic.set_paths_and_workspaces()
#merge value_df and near_df
tabs_all_df = pd.merge(value_df, near_df, how = 'inner', on='pointid')

#delete original dfs from memory
del value_df, near_df


#Calculate the land cover change flag
Generic.ChangeFlag()

#Calculate Oak and Riparian Suitability Flags
#Generic.oakrip_Suitability_Flags(1,1)

#Create Oak and Riparian Eligibility


#Create Oak and Riparian Selection


#Change Landcover Labels from Selection


#Update Change Flag List










#Calculate Agricultural Activity Suitability Flags


#Create Agricultural Activity Eligibility


#Create Agricultural Activity Selection


#Update Activity GHG values in Carbon Table







