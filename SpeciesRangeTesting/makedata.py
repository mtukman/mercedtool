# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:39:04 2018

@author: Dylan
"""

import Generic
global pts
import pandas as pd
import Helpers
import arcpy



path = "E:/mercedtool/SpeciesRangeTesting/MASTER_DATA/Tables/SpecRangecsvs"
#full set
pointiddf  = path + '/merge'

tdf = Helpers.LoadCSVs(pointiddf)
df = Helpers.MergeMultiDF('pointid', tdf)
evt = pd.read_csv(path + '/EVT2014LU.csv')
list2 = [df,evt]
df = Helpers.MergeMultiDF('gridcode14', list2)
habsuitdf = pd.read_csv(path + '/habsuitlu.csv')
lu2014veg = pd.read_csv(path + '/LU2014veg.csv')
del tdf
del list2
mammals = pd.read_csv(path + '/list_mammals.csv')
amphibs = pd.read_csv(path + '/list_amphibians.csv')
birds = pd.read_csv(path + '/list_birds.csv')
ccbirds = pd.read_csv(path + '/list_climate_change_birds.csv')
ccnobird = pd.read_csv(path + '/list_climate_change_except_birds.csv')
reptiles = pd.read_csv(path + '/list_reptiles.csv')
tespp = pd.read_csv(path + '/list_threatened_endangered.csv')

def get_suitability(suitcsv, landcover, year):
    
    #return a count of pixels
##
    
dict spp = {}
