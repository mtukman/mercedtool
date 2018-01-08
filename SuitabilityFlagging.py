#Import System Modules
import arcpy
from arcpy import env
import Generic
import functools
import pandas as pd

Generic.set_paths_and_workspaces()
#merge value_df and near_df
#tabs = pd.merge(value_df, near_df, how = 'inner', on='pointid')

#delete near_tables and value_tables


neartabs = Generic.list_csvs_in_folder(Generic.valuetables, 'csv')
print (neartabs)
valtabs = Generic.list_csvs_in_folder(Generic.neartables, 'csv')
#Calculate Oak and Riparian Suitability Flags


#Create Oak and Riparian Eligibility


#Create Oak and Riparian Selection


#Change Landcover Labels from Selection


#Update Change Flag List










#Calculate Agricultural Activity Suitability Flags


#Create Agricultural Activity Eligibility


#Create Agricultural Activity Selection


#Update Activity GHG values in Carbon Table







