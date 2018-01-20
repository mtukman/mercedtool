# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:39:04 2018

@author: Dylan
"""
#
#MAKE INTO A FUNCTION THAT TAKES A DF WITH RID, customcode2014, customcode2030mod
import Generic
global pts
import pandas as pd
import Helpers
import arcpy



path = "E:\mercedtool\MASTER_DATA\Tables\LUTables"
#full set
pointiddf  = 'E:/mercedtool/SpeciesRangeTesting/MASTER_DATA/Tables/SpecRangecsvs/merge'

tdf = Helpers.LoadCSVs(pointiddf)
df = Helpers.MergeMultiDF('pointid', tdf)
evt = pd.read_csv("E:/mercedtool/SpeciesRangeTesting/MASTER_DATA/Tables/SpecRangecsvs/EVT2014LU.csv")
list2 = [df,evt]
df = Helpers.MergeMultiDF('gridcode14', list2)
habsuit = pd.read_csv(path + '/lut_habsuit.csv')
lut_uf = pd.read_csv(path + '/lut_urbanfootprint.csv')
del tdf
del list2
mammals = pd.read_csv(path + '/list_mammals.csv')
amphibs = pd.read_csv(path + '/list_amphibians.csv')
birds = pd.read_csv(path + '/list_birds.csv')
ccbirds = pd.read_csv(path + '/list_climate_change_birds.csv')
ccnobird = pd.read_csv(path + '/list_climate_change_except_birds.csv')
reptiles = pd.read_csv(path + '/list_reptiles.csv')
tespp = pd.read_csv(path + '/list_threatened_endangered.csv')


rids_only = "E:\\mercedtool\\MASTER_DATA\\Tables\\ValueTables\\env_rids.csv"
rids= pd.read_csv(rids_only)

#need to change update later on
df2 = df[df['LC2014'] != df['LC2030MOD']]
df2['customcode30mod'] = list(lut_uf['custcode'].sample(len(df2), replace=True))
df2['customcode14'] = list(lut_uf['custcode'].sample(len(df2), replace=True))


#need to merge whr3 code with custom code
hablut = pd.merge(habsuit, lut_uf, how='left', left_on = 'whr13_code', right_on='ufcode')

def get_suitability(custcode, sppcode, suitdf = habsuit, lut=lut_uf):
    a = lut_uf.loc[lut_uf['custcode']==custcode, 'ufcode'].values[0]
    if not habsuit.loc[(habsuit['cwhr_id'] == sppcode.upper()) & (habsuit['whr13_code']==a), 'habitat_suitability'].empty:
        b = habsuit.loc[(habsuit['cwhr_id'] == sppcode.upper()) & (habsuit['whr13_code']==a), 'habitat_suitability'].values[0]
    else:
        b = 0
    return b
    
def initialize_dict(row):
    species_string = rids.loc[rids['rid']==row['rid'], 'species_ranges'].values[0]
    species_string = species_string[1:-1]
    #add entries to dict
    for i in [i for i in species_string.split(',')]:
        if not i in dev_dict.keys():
            dev_dict[i]={}
            dev_dict[i]['degraded'] = 0
            dev_dict[i]['improved'] = 0
            
def initialize_suit_lu(row):
    if row['cwhr_id'] not in suit_dict.keys():
        suit_dict[row['cwhr_id']] = {}
    else:
        print(row['whr13_code'])
        #custcode = lut_uf.loc[lut_uf['ufcode']==row['whr13_code'], 'custcode'].values[0]
        suit_dict[row['cwhr_id']][row['whr13_code']] = row['habitat_suitability']
            
def tally(row):
    species_string = rids.loc[rids['rid']==row['rid'], 'species_ranges'].values[0]
    species_string = species_string[1:-1]
    
    for i in [i for i in species_string.split(',')]:
        if i.upper() in suit_dict.keys():
            if not lut_uf.loc[lut_uf['custcode']==row['customcode14']].empty:
                lc14 = lut_uf.loc[lut_uf['custcode']==row['customcode14'], 'ufcode'].values[0]
            else:
                lc14 = -9999
            if not lut_uf.loc[lut_uf['custcode']==row['customcode30mod']].empty:
                lc30 = lut_uf.loc[lut_uf['custcode']==row['customcode30mod'], 'ufcode'].values[0]
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
                print('improved')
            if cust30suit < cust14suit:
                dev_dict[i]['degraded'] = dev_dict[i]['degraded'] + row['pointid']
                print('degraded')
            print('cc ' + str(row['customcode14']))
            print ('lc14 ' + str(lc14))
            print(i)
            print('14 ' + str(cust14suit))
            print('30 ' + str(cust30suit))
        else:
            print (i.upper() + 'is missing')

a = df2.groupby(['rid','customcode14', 'customcode30mod']).count()

a.reset_index(inplace=True)
#a['customcode30mod']= 723
suit_dict = {}
dev_dict = {}
habsuit.apply(initialize_suit_lu, axis=1)
a=a[0:1]
a.apply(initialize_dict, axis=1)

a.apply(tally, axis = 1)



#deg_dict = {}

#build species dictionary
    
#dict spp = {}