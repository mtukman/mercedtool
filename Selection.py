#Import System Modules
''' 
This module has a function which takes the number of pixels per activity,
a selection field and an suitability flag field.

It will assign new fields to tabs_all_df. These fields will be filled with a 1/0 flag for whether a 
pixel is selected for an activity.
'''
Generic.tabs_all_df.loc[Generic.dict_activity[activity]['query'], initflag] = 1
rrequery = (Generic.tabs_all_df['LC2014'].isin(['Grassland','Shrubland','Irrigated Pasture', 'Annual Cropland', 'Vineyard', 'Rice', 'Orchard','Wetland','Barren']) & (Generic.tabs_all_df['lcchange'] == 1) & ((Generic.tabs_all_df['near_rivers'] < 650) | (Generic.tabs_all_df['near_streams'] < 100)) & (Generic.tabs_all_df['near_woody'] != 0))



import pandas as pd
import Helpers
import random 
dict_eligibility = {}



def selectionfunc (goal,flagfield,groupnumber,selfield):
    count = 0
    curgoal = goal    
    usednums = []
    Generic.tabs_all_df[selfield] = 0
    while count < goal:
        for x in range(6000):
            c = random.randint(1,groupnumber)
            if c in usednum:
                pass
            else:
                usednums.append(c)
                Generic.tabs_all_df.loc[(Generic.tabs_all_df[flagfield] == 1) & (Generic.tabs_all_df[flagfield] == c),selfield] = 1
                
                
                
oakdict = {'name':'Oak Woodland Restoration','query' : 'holder', 'ag_modifier':1, 'selfield': 'oakselect', 'grpsize':small}
rredict = {'name':'Riparian Restoration','query' : 'holder', 'ag_modifer':1, 'selfield': 'rreselect', 'grpsize':small}
muldict =  {'name':'Mulching','query' : 'holder', 'ag_modifier':.20, 'selfield': 'mulselect', 'grpsize':small}
mmadict =  {'name':'Replacing Sythetic Fertilizer with Soil Amendments','query' : 'holder', 'ag_modifier':.35, 'selfield': 'mmaselect', 'grpsize':small}
nfmdict = {'name':'Nirtrogen Fertilizer Management','query' : 'holder', 'ag_modifier':.25, 'selfield': 'nfmselect', 'grpsize':small}
ccrdict = {'name':'Cover Crops', 'query':'holder', 'ag_modifier':.20, 'selfield': 'ccrselect', 'grpsize':small}
acadict = {'name':'Avoided Conversion to Agriculture', 'query':'holder', 'ag_modifier':1, 'selfield': 'acaselect', 'grpsize':small}
acudict = {'name':'Avoided Conversion to Urban', 'query':'holder', 'ag_modifier':1, 'selfield': 'acuselect', 'grpsize':small}
hpldict = {'name':'Hedgerow Planting', 'query':'holder', 'ag_modifier':.35, 'selfield': 'hplselect', 'grpsize':small}
urbdict = {'name':'Urban Forestry', 'query':'holder', 'ag_modifier':1, 'selfield': 'urbselect', 'grpsize':small}


dict_activity = {'oak':oakdict, 'rre': rredict, 'mul':muldict, 'mma':mmadict, 'nfm':nfmdict, 'ccr':ccrdict,'aca':acadict,'acu':acudict,'hpl':hpldict, 'urb':urbdict}


#Run selection for Oak
            