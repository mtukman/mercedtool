# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 08:58:23 2018

@author: Dylan
"""

import pandas as pd
import arcpy



#
#def report_csvs ():
#    
#    
#def acre_change (groupbyfields,dataframe):
#    
#    
#    
#    
#
#    
    
#FMMP

developed = ['Urban', 'Developed', 'Developed Roads']
devlist = ['bau','medinfill','maxinfill']



def fmmp(df):
    aglist = ['Orchard','Annual Cropland','Vineyard', 'Rice', 'Irrigated Pasture']
    devlist = ['bau','medinfill','maxinfill']
    td = df['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'fmmp_class']
    for i in devlist:
        if i == 'medinfill':
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            
            
            
        if i == 'maxinfill':
            td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
        
        # do 2014
        tempdf14 = td.loc[td['LC2014'].isin(aglist)]
        group14 = tempdf14.groupby('fmmp_class').count()
        group14['index1'] = group14.index
        group14 = group14[['pointid','index1']]
        group14 = group14.rename(columns={'pointid':'count14'})
        
        
        # do 2030
        tempdf30 = td.loc[td['LC2030'].isin(aglist)]
        group30 = tempdf30.groupby('fmmp_class').count()
        group30['index1'] = group30.index
        group30 = group30[['pointid','index1']]
        group30 = group30.rename(columns={'pointid':'count30'})
        
        tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
        tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
        tempmerge['change'] = (tempmerge['change']*900)/10000
        tempmerge.to_csv('fmmp_' + i+'.csv')





def fema(df):
    devlist = ['bau','medinfill','maxinfill']
    td = df['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid','fema_class']
    
    flist = ['100','500']
    for i in flist:
        for i in devlist:
            if i == 'medinfill':
                td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
                td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
                
                
                
            if i == 'maxinfill':
                td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
                td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            
            # do 2014
            tempdf14 = td.loc[td['fema_class'] == i]
            group14 = tempdf14.groupby('fmmp_class').count()
            group14['index1'] = group14.index
            group14 = group14[['pointid','index1']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # do 2030
            tempdf30 = td.loc[td['fema_class'] == i]
            group30 = tempdf30.groupby('fmmp_class').count()
            group30['index1'] = group30.index
            group30 = group30[['pointid','index1']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = (tempmerge['change']*900)/10000
            tempmerge.to_csv('flood100_' + i+'.csv')




























