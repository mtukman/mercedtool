# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 08:58:23 2018

@author: Dylan
"""

import pandas as pd

developed = ['Urban', 'Developed', 'Developed Roads']
devlist = ['bau','medinfill','maxinfill']



def fmmp(df):
    aglist = ['Orchard','Annual Cropland','Vineyard', 'Rice', 'Irrigated Pasture']
    devlist = ['bau','medinfill','maxinfill']
    
    for i in devlist:
        td = df['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'fmmp_class']
        if i == 'medinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
            

        if i == 'maxinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
            
        
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
    
    
    flist = ['100','500']
    gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
    
    for i in flist:
        for x in devlist:
            td = df['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid','fema_class']
            if x == 'medinfill':
                td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
                td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
                
                
            if x == 'maxinfill':
                td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
                td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
                
            
            # do 2014
            tempdf14 = td.loc[td['fema_class'] == i]
            tempdf14 = pd.merge(tempdf14,gclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('fmmp_class','gen_class').count()
            group14['index1'] = group14.index
            group14 = group14[['pointid','index1']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # do 2030
            tempdf30 = td.loc[td['fema_class'] == i]
            tempdf30 = pd.merge(tempdf30,gclass, how = 'left', left_on = 'LC2030', right_on = 'landcover')
            group30 = tempdf30.groupby('fmmp_class','gen_class').count()
            group30['index1'] = group30.index
            group30 = group30[['pointid','index1']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = (tempmerge['change']*900)/10000
            tempmerge.to_csv(x+'_flood' + i + '.csv')

def scenic(df):
    #6-56
    devlist = ['bau','medinfill','maxinfill']
    
    
    gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
    
    for i in devlist:
        td = df['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid','scenic_val']
        if i == 'medinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
            
            
            
            
        if i == 'maxinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
            
        
        # do 2014
        tempdf14 = td.loc[td['scenic_val'] > 5]
        tempdf14 = pd.merge(tempdf14,gclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
        group14 = tempdf14.groupby('gen_class').count()
        group14['index1'] = group14.index
        group14 = group14[['pointid','index1']]
        group14 = group14.rename(columns={'pointid':'count14'})
        
        
        # do 2030
        tempdf30 = td.loc[td['scenic_val'] > 5]
        tempdf30 = pd.merge(tempdf30,gclass, how = 'left', left_on = 'LC2030', right_on = 'landcover')
        group30 = tempdf30.groupby('gen_class').count()
        group30['index1'] = group30.index
        group30 = group30[['pointid','index1']]
        group30 = group30.rename(columns={'pointid':'count30'})
        
        tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
        tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
        tempmerge['change'] = (tempmerge['change']*900)/10000
        tempmerge.to_csv(i+'_scenic' + '.csv')






def wateruse(df):
    #6-56
    devlist = ['bau','medinfill','maxinfill']
    
    
    wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_wateruse.csv")
    
    for i in devlist:
        td = df['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid']
        if i == 'medinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
            
            
        if i == 'maxinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
            
        
        # do 2014
#        tempdf14 = td.loc[td['scenic_val'] > 5]
        tempdf14 = pd.merge(td,wclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
        group14 = tempdf14.groupby('LC2014').sum()
        group14['index1'] = group14.index
        group14 = group14[['wat_val','index1']]
        group14 = group14.rename(columns={'wat_val':'water14'})
        
        
        # do 2030
#        tempdf30 = td.loc[td['scenic_val'] > 5]
        tempdf30 = pd.merge(td,wclass, how = 'left', left_on = 'LC2030', right_on = 'landcover')
        group30 = tempdf30.groupby('LC2030').sum()
        group30['index1'] = group30.index
        group30 = group30[['wat_val','index1']]
        group30 = group30.rename(columns={'wat_val':'water30'})
        
        tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
        tempmerge['change'] = tempmerge['water30']-tempmerge['water14']
        tempmerge.to_csv(i+'_waterdemand.csv')

def lcchange(df):
    devlist = ['bau','medinfill','maxinfill']
    
    for i in devlist:
        td = df['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'fmmp_class']
        if i == 'medinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
            
            
        if i == 'maxinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
            
        
        # do 2014
        group14 = td.groupby('LC2014').count()
        group14['index1'] = group14.index
        group14 = group14[['pointid','index1']]
        group14 = group14.rename(columns={'pointid':'count14'})
        
        
        # do 2030
        group30 = td.groupby('LC2030').count()
        group30['index1'] = group30.index
        group30 = group30[['pointid','index1']]
        group30 = group30.rename(columns={'pointid':'count30'})
        
        tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
        tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
        tempmerge['change'] = (tempmerge['change']*900)/10000
        tempmerge.to_csv(i+'_lcchange.csv')


def pcalcchange(df):
    devlist = ['bau','medinfill','maxinfill']
    
    for i in devlist:
        td = df['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'fmmp_class']
        if i == 'medinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
            
            
        if i == 'maxinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
            
        
        # do 2014
        tempdf14 = td.loc[td['pca_val'] == 1]
        group14 = tempdf14.groupby('LC2014').count()
        group14['index1'] = group14.index
        group14 = group14[['pointid','index1']]
        group14 = group14.rename(columns={'pointid':'count14'})
        
        
        # do 2030
        tempdf30 = td.loc[td['pca_val'] == 1]
        group30 = tempdf30.groupby('LC2030').count()
        group30['index1'] = group30.index
        group30 = group30[['pointid','index1']]
        group30 = group30.rename(columns={'pointid':'count30'})
        
        tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
        tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
        tempmerge['change'] = (tempmerge['change']*900)/10000
        tempmerge.to_csv(i+'_pca_lcchange.csv')


def termovement(df):
    devlist = ['bau','medinfill','maxinfill']
    
    rclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_resistance.csv")
    arealist = ['county','eca']
    
    for x in arealist:
           
        for i in devlist:
            td = df['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid']
            if x == 'eca':
                td = td.loc[td['eca_val'] == 1]
            if i == 'medinfill':
                td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
                td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
                
                
            if i == 'maxinfill':
                td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
                td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
                
            
            # do 2014
            tempdf14 = pd.merge(td,rclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('res_val').count()
            group14['index1'] = group14.index
            group14 = group14[['pointid','index1']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # do 2030
            tempdf30 = pd.merge(td,rclass, how = 'left', left_on = 'LC2030', right_on = 'landcover')
            group30 = tempdf30.groupby('res_val').count()
            group30['index1'] = group30.index
            group30 = group30[['pointid','index1']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = (tempmerge['change']*900)/10000
            tempmerge.to_csv(i+'_'+ x +'_resistance.csv')


def cropvalue(df):
    #6-56
    devlist = ['bau','medinfill','maxinfill']

    
    wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_crop_value.csv")
    
    for i in devlist:
        td = df['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid']
        if i == 'medinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']            
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'

            
            
            
        if i == 'maxinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']            
            td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'

        
        # do 2014
#        tempdf14 = td.loc[td['scenic_val'] > 5]
        tempdf14 = pd.merge(td,wclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
        group14 = tempdf14.groupby('crop_val').sum()
        group14['index1'] = group14.index
        group14 = group14[['crop_val','index1']]
        group14 = group14.rename(columns={'crop_val':'crop14'})
        
        
        # do 2030
#        tempdf30 = td.loc[td['scenic_val'] > 5]
        tempdf30 = pd.merge(td,wclass, how = 'left', left_on = 'LC2030', right_on = 'landcover')
        group30 = tempdf30.groupby('crop_val').sum()
        group30['index1'] = group30.index
        group30 = group30[['crop_val','index1']]
        group30 = group30.rename(columns={'crop_val':'crop30'})
        
        tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
        tempmerge['change'] = tempmerge['crop30']-tempmerge['crop14']
        tempmerge.to_csv(i+'_cropvalue.csv')
        
        

def groundwater(df):
    #6-56
    devlist = ['bau','medinfill','maxinfill']


    
    for i in devlist:
        td = df['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'bcm_val']
        
        td['bcm_val'] =  (td['bcm_val']*.0032808) * .222394
        if i == 'medinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']            
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'

            
            
            
        if i == 'maxinfill':
            td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']            
            td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'

        
        # do 2014
#        tempdf14 = td.loc[td['scenic_val'] > 5]
        
        td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban'))]
        
        group14 = td.groupby('bcm_val').sum()
        group14['index1'] = group14.index
        group14 = group14[['crop_val','index1']]
        group14 = group14.rename(columns={'crop_val':'crop14'})
        
        
        # do 2030
#        tempdf30 = td.loc[td['scenic_val'] > 5]
        group30 = td.groupby('crop_val').sum()
        group30['index1'] = group30.index
        group30 = group30[['crop_val','index1']]
        group30 = group30.rename(columns={'crop_val':'crop30'})
        
        tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
        tempmerge['change'] = (tempmerge['crop30']-tempmerge['crop14'])*.75
        tempmerge.to_csv(i+'_groundwater.csv')


def cropvalue(df):
    #6-56
    devlist = ['bau','medinfill','maxinfill']

    
    wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_nitrates.csv")
    xlist = ['runoff','leach']
    for x in xlist:
        for i in devlist:
            td = df['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid']
            if i == 'medinfill':
                td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']            
                td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
    
                
                
                
            if i == 'maxinfill':
                td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']            
                td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
    
            
            # do 2014
    #        tempdf14 = td.loc[td['scenic_val'] > 5]
            tempdf14 = pd.merge(td,wclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby(x).sum()
            group14['index1'] = group14.index
            group14 = group14[['crop_val','index1']]
            group14 = group14.rename(columns={'crop_val':'crop14'})
            
            
            # do 2030
    #        tempdf30 = td.loc[td['scenic_val'] > 5]
            tempdf30 = pd.merge(td,wclass, how = 'left', left_on = 'LC2030', right_on = 'landcover')
            group30 = tempdf30.groupby(x).sum()
            group30['index1'] = group30.index
            group30 = group30[[x,'index1']]
            group30 = group30.rename(columns={x:'crop30'})
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
            tempmerge['change'] = tempmerge['crop30']-tempmerge['crop14']
            tempmerge.to_csv(i+'_cropvalue.csv') #will be in kilograms
            

def watershedintegrity(df):
    #6-56
    devlist = ['bau','medinfill','maxinfill']

    xlist = ['runoff','leach']
    for x in xlist:
        for i in devlist:
            td = df['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'huc12_val', 'near_rivers','near_streams']
            
                
            if i == 'medinfill':
                td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']            
                td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'

            if i == 'maxinfill':
                td.loc[(td['LC2030'] != td['LC2014'] & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']            
                td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
                
            td['natural14'] = 0
            td['natural30'] = 0
            td['riparian'] = 0
            td.loc[(td['near_streams'] < 100) | (td['near_rivers'] < 650),'riparian'] = 1
            td['watint14'] = 0
            td['watint30'] = 0
            # do 2014
            huclist =  td['huc12_val'].tolist()

            td.loc[td['LC2014'].isin(['Forest, Shrubland, Young Forest, Young Shrubland, Barren, Wetland, Water', 'Grassland']),'natural14'] = 1
            
            
            
            group14 = td.groupby(x).sum()
            group14['index1'] = group14.index
            group14 = group14[['crop_val','index1']]
            group14 = group14.rename(columns={'crop_val':'crop14'})
            
            
            # do 2030

            td.loc[td['LC2014'].isin(['Forest, Shrubland, Young Forest, Young Shrubland, Barren, Wetland, Water','Grassland']),'natural30'] = 1
            
            
            for i in huclist:
                temp = td.loc[td['huc12_val'] == i]
                ctemp14 = temp.groupby(['natural14','riparian'], as_index = False).count()
                ctemp30 = temp.groupby(['natural30','riparian'], as_index = False).count()
                ctemp14perc = ctemp14.loc[(ctemp14['riparian'] == 1)]
                ctemp14perc.reset_index(inplace = True)
                tempripint = ctemp14perc.iat[1,'pointid']/(ctemp14perc.iat[0,'pointid'] + ctemp14perc.iat[1,'pointid'])
                
                ripint = 
                hucint = 
                     
            
            
#            group30 = td.groupby(x).sum()
#            group30['index1'] = group30.index
#            group30 = group30[[x,'index1']]
#            group30 = group30.rename(columns={x:'crop30'})
#            
#            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
#            tempmerge['change'] = tempmerge['crop30']-tempmerge['crop14']
#            tempmerge.to_csv(i+'_cropvalue.csv') #will be in kilograms




















