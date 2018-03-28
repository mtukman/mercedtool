# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:39:04 2018

@author: Dylan
"""
#(df, outpath, glu, wlu, rlu, clu, nlu, lupath, acdict = 'None', oak = 0, rre = 0, cd = 0 , cm = 0, gra = 0, cproc = 0):
    
#def terspe(df, outputpath):


#!!!!!!----------------**************
#MAKE INTO A FUNCTION THAT TAKES A DF WITH RID, customcode2014, customcode2030mod

import Generic
global pts
import pandas as pd
import Helpers

#    if x in ['base', 'dev','cons', 'trt']:
#                td = df[['LC2014','pointid', 'rid', field]]
#                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
#                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
#                td = td.loc[td['LC2014'] != td[field]]
#                
#    else:
#        td = df[['LC2014','pointid', 'rid', 'LC2030_bau', 'LC2030_trt_bau']]
#        td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
#        td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
#        td.loc[(td['LC2030_bau'] == 'Young Forest'), field] = 'Forest'
#        td.loc[(td['LC2030_bau'] == 'Young Shrubland'), field] = 'Shrubland'
#        td = td.loc[td['LC2030_bau'] != td['LC2030_trt_bau']]

td = df[['LC2014','pointid', 'rid', field]]
    
    
Generic.set_paths_and_workspaces()

habsuit = pd.read_csv(lupath + '/lut_habsuit.csv')
lut_uf14 = pd.read_csv(lupath + '/lut_urbanfootprint14.csv')
lut_uf30 = pd.read_csv(lupath + '/lut_urbanfootprint30.csv')
mammals = pd.read_csv(lupath + '/list_mammals.csv')
amphibs = pd.read_csv(lupath + '/list_amphibians.csv')
birds = pd.read_csv(lupath + '/list_birds.csv')
ccbirds = pd.read_csv(lupath + '/list_climate_change_birds.csv')
ccnobird = pd.read_csv(lupath + '/list_climate_change_except_birds.csv')
reptiles = pd.read_csv(lupath + '/list_reptiles.csv')
tespp = pd.read_csv(lupath + '/list_threatened_endangered.csv')
mcount = 0
bcount = 0
acount = 0
tcount = 0
countdict = {'m':mcount, 'b':bcount,'a':acount,'t':tcount,}

glist = ['m','b','a','t']
    
specieslist = []

def initialize_dict(row):
    species_string = rids.loc[rids['rid']==row['rid'], 'species_ranges'].values[0]
    species_string = species_string[1:-1]
    for i in [i for i in species_string.split(',')]:
        if not i in dev_dict.keys():
            dev_dict[i]={}
            dev_dict[i]['degraded'] = 0
            dev_dict[i]['improved'] = 0
            
def initialize_suit_lu(row):
    if row['cwhr_id'] not in suit_dict.keys():
        suit_dict[row['cwhr_id']] = {}
    else:
        suit_dict[row['cwhr_id']][row['whr13_code']] = row['habitat_suitability']

def initialize_uf_lu14(row):
    uf_dict14[row['gridcode14']] =  row['ufcode']
    
def initialize_uf_lu30(row):
    uf_dict30[row['gridcode30']] =  row['ufcode']    
            
def tally(row):
    species_string = rids.loc[rids['rid']==row['rid'], 'species_ranges'].values[0]
    species_string = species_string[1:-1]
    
    for i in [i for i in species_string.split(',')]:
        if i.upper() in suit_dict.keys():
            
            if i not in specieslist:
                specieslist.append(i)
                if 'm' in i:
                    countdict['m'] = countdict['m'] + 1
                elif 'b' in i:
                    countdict['b'] = countdict['b'] + 1
                elif 'a' in i:
                    countdict['a'] = countdict['a'] + 1
                elif 't' in i:
                    countdict['t'] = countdict['t'] + 1
            
            

            if row['gridcode14'] in uf_dict14.keys():
                lc14 = uf_dict14[row['gridcode14']]
            else:
                lc14 = -9999
            if row['gridcode30_bau'] in uf_dict30.keys():
                lc30 = uf_dict30[row['gridcode30_bau']]
            else:
                lc30 = -9999
                
            if lc14 in suit_dict[i.upper()].keys():
                cust14suit = suit_dict[i.upper()][lc14]
            else:
                cust14suit = 0
                
            if lc30 in suit_dict[i.upper()].keys():
                cust30suit = suit_dict[i.upper()][lc30]
            else:
                cust30suit = 0
                
            if cust14suit < cust30suit:
                dev_dict[i]['improved'] = dev_dict[i]['improved'] + row['pointid']

            if cust30suit < cust14suit:
                dev_dict[i]['degraded'] = dev_dict[i]['degraded'] + row['pointid']

        else:
            print (i.upper() + 'is missing')
            
def summarize(first_letter, guild):
    if countdict[first_letter] == 0:
        pass
    else:
        if guild=='tes':
            new_dict = {x: v for x,v in dev_dict.items() if x in list(tespp['species']) }
        else:
            new_dict = {x: v for x,v in dev_dict.items() if x.startswith(first_letter) }
        
        deg= (pd.DataFrame.from_dict(new_dict, orient = 'index')['degraded'].sum()*900*0.000247105)/countdict[first_letter]
        imp = (pd.DataFrame.from_dict(new_dict, orient = 'index')['improved'].sum()*900*0.000247105)/countdict[first_letter]
        summary_dict[guild + '_avg_deg_acres']=deg
        summary_dict[guild + '_avg_imp_acres']=imp
    
    
a = df2.groupby(['rid','LC2014', 'LC2030_bau'], as_index = False).count()

suit_dict = {}
dev_dict = {}
uf_dict14 = {}
uf_dict30 = {}
summary_dict = {}
lut_uf14.apply(initialize_uf_lu14, axis=1)
lut_uf30.apply(initialize_uf_lu30, axis=1)
habsuit.apply(initialize_suit_lu, axis=1)
a.apply(initialize_dict, axis=1)
a.apply(tally, axis = 1)
summarize('m', 'mammals')
summarize('b', 'birds')
summarize('a', 'amphibians')
summarize('t', 'tes')
a =pd.DataFrame.from_dict(summary_dict, orient='index')
a.reset_index(inplace=True)
a.columns=['guild', 'acres']
a.to_csv('P:/Temp/TerrHab.csv')
# ADD A RETURN A
#!!!!!!----------------**************














    
    
    
    
    
    
    
    
    
    
    