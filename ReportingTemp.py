# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 08:58:23 2018

@author: Dylan
"""


#def report(outpath, df):

import pandas as pd

developed = ['Urban', 'Developed', 'Developed Roads']
devlist = ['bau','medinfill','maxinfill']
import Helpers


def fmmp(df):
    aglist = ['Orchard','Annual Cropland','Vineyard', 'Rice', 'Irrigated Pasture']
    devlist = ['bau','medinfill','maxinfill']
    
    for i in devlist:
        td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'fmmp_class']]
        if i == 'medinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
            

        if i == 'maxinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
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
        tempmerge = tempmerge[['index1','change']]
        tempmerge = tempmerge.rename(columns = {'index1':'fmmp_class','change':'hectares_of_change'})
        tempmerge.to_csv('P:/' + i+'_fmmp.csv')





def fema(df):
    devlist = ['bau','medinfill','maxinfill']
    
    
    flist = [100,500]
    gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
    
    for i in flist:
        if i == 100:
            query = [100]
        if i == 500:
            query = [100,500]
        for x in devlist:
            td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid','fema_class', 'near_fema']]
            if x == 'medinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
                td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
                
                
            if x == 'maxinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
                td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
                
            
            # do 2014
            tempdf14 = td.loc[(td['fema_class'].isin(query)) & (td['near_fema'] == 0)]
            tempdf14 = pd.merge(tempdf14,gclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby(['gen_class'], as_index = False).count()
            group14 = group14[['pointid','gen_class']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # do 2030
            tempdf30 = td.loc[(td['fema_class'].isin(query)) & (td['near_fema'] == 0)]
            tempdf30 = pd.merge(tempdf30,gclass, how = 'left', left_on = 'LC2030', right_on = 'landcover')
            group30 = tempdf30.groupby(['gen_class'], as_index = False).count()
            group30 = group30[['pointid','gen_class']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            if len(group30.index) == 0 | len(group14.index) == 0:
                Helpers.pmes('Empty rows in ' + i)
            else:
                tempmerge = pd.merge(group14,group30, on = 'gen_class', how = 'left')
                tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
                tempmerge['change'] = (tempmerge['change']*900)/10000
                tempmerge = tempmerge[['gen_class','change']]
                tempmerge = tempmerge.rename(columns = {'change':'hectares_of_change'})
                tempmerge.to_csv('P:/Temp/' +x+'_flood' + str(i) + '.csv')

def scenic(df):
    #6-56
    devlist = ['bau','medinfill','maxinfill']
    
    
    gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
    
    for i in devlist:
        td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid','scenic_val']]
        if i == 'medinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'

        if i == 'maxinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
            
        
        # do 2014
        tempdf14 = td.loc[td['scenic_val'] > 5]
        tempdf14 = pd.merge(tempdf14,gclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
        group14 = tempdf14.groupby('gen_class', as_index = False).count()
        group14 = group14[['pointid','gen_class']]
        group14 = group14.rename(columns={'pointid':'count14'})
        
        
        # do 2030
        tempdf30 = td.loc[td['scenic_val'] > 5]
        tempdf30 = pd.merge(tempdf30,gclass, how = 'left', left_on = 'LC2030', right_on = 'landcover')
        group30 = tempdf30.groupby('gen_class', as_index = False).count()
        group30 = group30[['pointid','gen_class']]
        group30 = group30.rename(columns={'pointid':'count30'})
        
        if len(group30.index) == 0 | len(group14.index) == 0:
            Helpers.pmes('Empty rows in ' + i)
            
        else:
            tempmerge = pd.merge(group14,group30, on = 'gen_class', how = 'left')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = (tempmerge['change']*900)/10000
            tempmerge = tempmerge[['gen_class','change']]
            tempmerge = tempmerge.rename(columns = {'change':'hectares_of_change'})
            tempmerge.to_csv(i+'_scenic' + '.csv')






def wateruse(df):
    #6-56
    devlist = ['bau','medinfill','maxinfill']
    
    
    wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_wateruse.csv")
    
    for i in devlist:
        td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid',]]
        if i == 'medinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
            
            
        if i == 'maxinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
            
        
        # do 2014
        tempdf14 = pd.merge(td,wclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
        group14 = tempdf14.groupby('LC2014', as_index = False).sum()
        group14 = group14[['wat_val','LC2014']]
        group14 = group14.rename(columns={'wat_val':'water14'})
        
        
        # do 2030
        tempdf30 = pd.merge(td,wclass, how = 'left', left_on = 'LC2030', right_on = 'landcover')
        group30 = tempdf30.groupby('LC2030', as_index = False).sum()
        group30 = group30[['wat_val','LC2030']]
        group30 = group30.rename(columns={'wat_val':'water30'})
        
        tempmerge = pd.merge(group14,group30, left_on = 'LC2014', right_on= 'LC2030', how = 'left')
        tempmerge['change'] = tempmerge['water30']-tempmerge['water14']
        tempmerge = tempmerge[['LC2014','change']]
        tempmerge = tempmerge.rename(columns = {'LC2014':'landcover','change':'hectares_of_change'})
        tempmerge.to_csv(i+'_waterdemand.csv')

def lcchange(df):
    devlist = ['bau','medinfill','maxinfill']
    
    for i in devlist:
        td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
        if i == 'medinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
            
            
        if i == 'maxinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
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
        tempmerge = tempmerge[['index1','change']]
        tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'hectares_of_change'})
        tempmerge.to_csv(i+'_lcchange.csv')


def pcalcchange(df):
    devlist = ['bau','medinfill','maxinfill']
    
    for i in devlist:
        td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'pca_val']]
        if i == 'medinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
            
            
        if i == 'maxinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
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
        tempmerge = tempmerge[['index1','change']]
        tempmerge = tempmerge.rename(columns = {'index1':'lancover','change':'hectares_of_change'})
        tempmerge.to_csv(i+'_pca_lcchange.csv')


def termovement(df):
    devlist = ['bau','medinfill','maxinfill']
    
    rclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_resistance.csv")
    arealist = ['county','eca']
    
    for x in arealist:
           
        for i in devlist:
            td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid','eca_val']]
            if x == 'eca':
                td = td.loc[td['eca_val'] == 1]
            if i == 'medinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
                td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
                
                
            if i == 'maxinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
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
            tempmerge = tempmerge[['index1','change']]
            tempmerge = tempmerge.rename(columns = {'index1':'resistance','change':'hectares_of_change'})
            tempmerge.to_csv('P:/Temp/' + i+'_'+ x +'_resistance.csv')


def cropvalue(df):
    #6-56
    devlist = ['bau','medinfill','maxinfill']

    
    wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_crop_value.csv")
    
    for i in devlist:
        td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
        if i == 'medinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']           
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'

        if i == 'maxinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']            
            td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'

        
        # do 2014
        tempdf14 = pd.merge(td,wclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
        group14 = tempdf14.groupby('LC2014').sum()
        group14['index1'] = group14.index
        group14 = group14[['crop_val','index1']]
        group14 = group14.rename(columns={'crop_val':'crop14'})
        
        
        # do 2030
        tempdf30 = pd.merge(td,wclass, how = 'left', left_on = 'LC2030', right_on = 'landcover')
        group30 = tempdf30.groupby('LC2030').sum()
        group30['index1'] = group30.index
        group30 = group30[['crop_val','index1']]
        group30 = group30.rename(columns={'crop_val':'crop30'})
        
        tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
        tempmerge['change'] = tempmerge['crop30']-tempmerge['crop14']
        tempmerge = tempmerge[['index1','change']]
        tempmerge = tempmerge.rename(columns = {'index1':'crop_value','change':'Change in Value'})
        tempmerge.to_csv(i+'_cropvalue.csv')
        
        

def groundwater(df):
    #6-56
    devlist = ['bau','medinfill','maxinfill']

    for i in devlist:
        td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'bcm_val']]
        
        td['bcm_val'] =  (td['bcm_val']*.0032808) * .222394 #Turn into ac/ft/pixel/year
        if i == 'medinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']            
            td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
  
        if i == 'maxinfill':
            td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']           
            td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'

        
        # do 2014
        td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'].isin(['Urban', 'Developed', 'Developed_Roads'])))]
        
        group14 = td.groupby('LC2014').sum()
        group14['index1'] = group14.index
        group14 = group14[['bcm_val','index1']]
        group14 = group14.rename(columns={'bcm_val':'water14'})
        
        # do 2030
        group30 = td.groupby('LC2030').sum()
        group30['index1'] = group30.index
        group30 = group30[['crop_val','index1']]
        group30 = group30.rename(columns={'bcm_val':'water30'})
        
        tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
        tempmerge['change'] = (tempmerge['crop30']-tempmerge['crop14'])*.75
        tempmerge = tempmerge[['index1','change']]
        tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'ac_ft_change'})
        tempmerge.to_csv(i+'_groundwater.csv')


def nitrates(df):
    #6-56
    devlist = ['bau','medinfill','maxinfill']

    
    wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_nitrates.csv")
    xlist = ['runoff','leach']
    for x in xlist:
        for i in devlist:
            td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
            if i == 'medinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']          
                td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'

            if i == 'maxinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']         
                td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
    
            
            # do 2014
    #        tempdf14 = td.loc[td['scenic_val'] > 5]
            tempdf14 = pd.merge(td,wclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby(x).sum()
            group14['index1'] = group14.index
            group14 = group14[['crop_val','index1']]
            group14 = group14.rename(columns={x:x + '14'})
            
            
            # do 2030
    #        tempdf30 = td.loc[td['scenic_val'] > 5]
            tempdf30 = pd.merge(td,wclass, how = 'left', left_on = 'LC2030', right_on = 'landcover')
            group30 = tempdf30.groupby(x).sum()
            group30['index1'] = group30.index
            group30 = group30[[x,'index1']]
            group30 = group30.rename(columns={x:x + '30'})
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
            tempmerge['change'] = tempmerge[x+'30']-tempmerge[x+'14']
            tempmerge = tempmerge[['index1','change']]
            tempmerge = tempmerge.rename(columns = {'index1':'fmmp_class','change':'hectares_of_change'})
            tempmerge.to_csv(i+'_nitrates.csv') #will be in kilograms
            

def watershedintegrity(df):
    #6-56
    devlist = ['bau','medinfill','maxinfill']

    xlist = ['runoff','leach']
    for x in xlist:
        for i in devlist:
            td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'huc12_val', 'near_rivers','near_streams']]
            
                
            if i == 'medinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']           
                td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'

            if i == 'maxinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']          
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
                ctemp14huc = temp.groupby(['natural14'], as_index = False).count()
                
                ctemp30 = temp.groupby(['natural30','riparian'], as_index = False).count()
                ctemp30huc = temp.groupby(['natural30'], as_index = False).count()
                
                ctemp14perc = ctemp14.loc[(ctemp14['riparian'] == 1)]
                ctemp14perc.reset_index(inplace = True)
                
                ctemp30perc = ctemp30.loc[(ctemp14['riparian'] == 1)]
                ctemp30perc.reset_index(inplace = True)

                
                tempripint14 = ctemp14perc.iloc[1]['pointid']/(ctemp14perc.iloc[0]['pointid'] + ctemp14perc.iloc[1]['pointid'])
                tempripint30 = ctemp30perc.iloc[1]['pointid']/(ctemp30perc.iloc[0]['pointid'] + ctemp30perc.iloc[1]['pointid'])
                hucpcent14 = ctemp14huc.iloc[1]['pointid']/(ctemp14huc.iloc[0]['pointid'] + ctemp14huc.iloc[1]['pointid'])
                hucpcent30 = ctemp30huc.iloc[1]['pointid']/(ctemp30huc.iloc[0]['pointid'] + ctemp30huc.iloc[1]['pointid'])
                
                if tempripint14 > .7 & hucpcent14> .7:
                    td['watint14'] = 'Natural Catchment'
                if tempripint14 > .7 & hucpcent14< .7:
                    td['watint14'] = 'Import Riparian Buffer'
                if tempripint14 < .7:
                    td['watint14'] = 'Degraded'
                    
                if tempripint30 > .7 & hucpcent30> .7:
                    td['watint30'] = 'Natural Catchment'
                if tempripint30 > .7 & hucpcent30< .7:
                    td['watint30'] = 'Import Riparian Buffer'
                if tempripint30 < .7:                
                    td['watint30'] = 'Degraded'
                
                              
            
            
#            group30 = td.groupby(x).sum()
#            group30['index1'] = group30.index
#            group30 = group30[[x,'index1']]
#            group30 = group30.rename(columns={x:'crop30'})
#            
#            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
#            tempmerge['change'] = tempmerge['crop30']-tempmerge['crop14']
                    tempmerge = tempmerge[['index1','change']]
                    tempmerge = tempmerge.rename(columns = {'index1':'fmmp_class','change':'hectares_of_change'})
#            tempmerge.to_csv(i+'_cropvalue.csv') #will be in kilograms




















