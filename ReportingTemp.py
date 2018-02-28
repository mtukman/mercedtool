# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 08:58:23 2018

@author: Dylan
"""


#def report(outpath, df):
def report(df, outpath):
    import pandas as pd
    import Helpers

    def fmmp(df, outpath):
        aglist = ['Orchard','Annual Cropland','Vineyard', 'Rice', 'Irrigated Pasture']
        developed = ['Developed','Urban','Developed Roads']
        devlist = ['bau','medinfill','maxinfill']
        flist = ['P','U','L', 'S']
        for i in devlist:
            td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'fmmp_class']]
            td.loc[(td['LC2030'] == 'Young Forest'), 'LC2030'] = 'Forest'
            td.loc[(td['LC2030'] == 'Young Shrubland'), 'LC2030'] = 'Shrubland'
            if i == 'medinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
                td.loc[td['dcode_medinfill'] != 0, 'LC2030'] = 'Urban'
                
    
            if i == 'maxinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']
                td.loc[td['dcode_maxinfill'] != 0, 'LC2030'] = 'Urban'
                
            Helpers.pmes('Doing 2014 FMMP')
            
            
            tempdf = td.loc[(td['LC2014'].isin(aglist)) & (td['LC2030'].isin(developed)) & (td['fmmp_class'].isin(flist))]
    #        # do 2014
    
            group = tempdf.groupby('fmmp_class', as_index = False).count()
            group = group[['fmmp_class','pointid']]
            group['pointid'] = (group['pointid']*900)/10000
            group = group.rename(columns = {'pointid':'hectares_of_loss'})
            group.to_csv('P:/' + i+'_fmmp.csv')
    
    def fema(df, outpath):
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
                td.loc[(td['LC2030'] == 'Young Forest'), 'LC2030'] = 'Forest'
                td.loc[(td['LC2030'] == 'Young Shrubland'), 'LC2030'] = 'Shrubland'
    #            td.to_csv('P:/Temp/' +x+'_flood' + str(i) + '14.csv')
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
    #            tempdf30.to_csv('P:/Temp/' +x+'_flood' + str(i) + '30.csv')
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
                    tempmerge = tempmerge.rename(columns = {'change':'hectares_of_change'})
                    tempmerge.to_csv('P:/Temp/' +x+'_flood' + str(i) + '.csv')
                    
    
    def scenic(df, outpath):
        #6-56
        devlist = ['bau','medinfill','maxinfill']
        
        
        gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
        
        for i in devlist:
            td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid','scenic_val']]
            td.loc[(td['LC2030'] == 'Young Forest'), 'LC2030'] = 'Forest'
            td.loc[(td['LC2030'] == 'Young Shrubland'), 'LC2030'] = 'Shrubland'
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
                tempmerge = tempmerge.rename(columns = {'change':'hectares_of_change'})
                tempmerge.to_csv('P:/Temp/'+i+'_scenic' + '.csv')
    

    def wateruse(df, outpath):
        #6-56
        devlist = ['bau','medinfill','maxinfill']
        
        
        wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_wateruse.csv")
        
        for i in devlist:
            td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
            td.loc[(td['LC2030'] == 'Young Forest'), 'LC2030'] = 'Forest'
            td.loc[(td['LC2030'] == 'Young Shrubland'), 'LC2030'] = 'Shrubland'
            
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
            tempmerge = tempmerge.rename(columns = {'LC2014':'landcover','change':'ac_ft_water_change'})
            tempmerge.to_csv('P:/Temp/'+i+'_waterdemand.csv')
    
    def lcchange(df, outpath):
        devlist = ['bau','medinfill','maxinfill']
        
        for i in devlist:
            td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
            td.loc[(td['LC2030'] == 'Young Forest'), 'LC2030'] = 'Forest'
            td.loc[(td['LC2030'] == 'Young Shrubland'), 'LC2030'] = 'Shrubland'
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
            tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'hectares_of_change'})
            tempmerge.to_csv('P:/Temp/'+i+'_lcchange.csv')
    
    
    def pcalcchange(df, outpath):
        devlist = ['bau','medinfill','maxinfill']
        
        for i in devlist:
            td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'pca_val']]
            td.loc[(td['LC2030'] == 'Young Forest'), 'LC2030'] = 'Forest'
            td.loc[(td['LC2030'] == 'Young Shrubland'), 'LC2030'] = 'Shrubland'
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
            tempmerge = tempmerge.rename(columns = {'index1':'lancover','change':'hectares_of_change'})
            tempmerge.to_csv('P:/Temp/'+i+'_pca_lcchange.csv')
    
    
    def termovement(df, outpath):
        devlist = ['bau','medinfill','maxinfill']
        
        rclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_resistance.csv")
        arealist = ['county','eca']
        
        for x in arealist:
               
            for i in devlist:
                td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid','eca_val']]
                td.loc[(td['LC2030'] == 'Young Forest'), 'LC2030'] = 'Forest'
                td.loc[(td['LC2030'] == 'Young Shrubland'), 'LC2030'] = 'Shrubland'
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
                tempmerge = tempmerge.rename(columns = {'index1':'resistance','change':'hectares_of_change'})
                tempmerge.to_csv('P:/Temp/' + i+'_'+ x +'_resistance.csv')
    
    
    def cropvalue(df, outpath):
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
            tempmerge = tempmerge.rename(columns = {'index1':'crop_value','change':'Change in Value'})
            tempmerge.to_csv('P:/Temp/' +i+'_cropvalue.csv')
            
            
    
    def groundwater(df, outpath):
        #6-56
        devlist = ['bau','medinfill','maxinfill']
    
        for i in devlist:
            td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'bcm_val']]
            td.loc[(td['LC2030'] == 'Young Forest'), 'LC2030'] = 'Forest'
            td.loc[(td['LC2030'] == 'Young Shrubland'), 'LC2030'] = 'Shrubland'
            
            td['bcm_val'] =  (td['bcm_val']*.0032808) * .222394 #Turn into ac/ft/pixel/year
            if i == 'medinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']            
                td.loc[(td['dcode_medinfill'] != 0), 'LC2030'] = 'Urban'
      
            if i == 'maxinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']           
                td.loc[(td['dcode_maxinfill'] != 0), 'LC2030'] = 'Urban'
    
            
            # do 2014
            td2 = td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'].isin(['Urban', 'Developed', 'Developed_Roads'])))]
            
            group30 = td2.groupby('LC2030').sum()
            group30['index1'] = group30.index
            group30 = group30.rename(columns={'index1':'landcover'})
            
    
            group30 = group30.rename(columns = {'bcm_val':'ac_ft_change'})
            group30.to_csv('P:/Temp/' +i+'_groundwater.csv')
    
    
    def nitrates(df, outpath):
        #6-56
        devlist = ['bau','medinfill','maxinfill']
    
        
        wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_nitrates.csv")
        xlist = ['runoff','leach']
        for x in xlist:
            for i in devlist:
                td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
                td.loc[(td['LC2030'] == 'Young Forest'), 'LC2030'] = 'Forest'
                td.loc[(td['LC2030'] == 'Young Shrubland'), 'LC2030'] = 'Shrubland'
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
                group14 = group14[[x,'index1']]
                group14[x] = group14[x]*.09
                group14 = group14.rename(columns={x:x + '14'})

                # do 2030
                tempdf30 = pd.merge(td,wclass, how = 'left', left_on = 'LC2030', right_on = 'landcover')
                group30 = tempdf30.groupby('LC2030').sum()
                group30['index1'] = group30.index
                group30 = group30[[x,'index1']]
                group30[x] = group30[x]*.09
                group30 = group30.rename(columns={x:x + '30'})
 
                tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
                tempmerge['change'] = tempmerge[x+'30']-tempmerge[x+'14']
                tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'kgs_nitrate'})
                tempmerge.to_csv('P:/Temp/' +i+'_' + x + '_nitrates.csv') #will be in kilograms
                
    
    def watershedintegrity(df, outpath):
        #6-56
        devlist = ['bau','medinfill','maxinfill']
    
        for x in devlist:
            td = df[['LC2030','LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'HUC_12', 'near_rivers','near_streams']]
            td.loc[(td['LC2030'] == 'Young Forest'), 'LC2030'] = 'Forest'
            td.loc[(td['LC2030'] == 'Young Shrubland'), 'LC2030'] = 'Shrubland'
            tdf = pd.DataFrame()
                
            if x == 'medinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']           
                td.loc[(td['dcode_medinfill'] != 0), 'LC2030'] = 'Urban'
    
            if x == 'maxinfill':
                td.loc[((td['LC2030'] != td['LC2014']) & (td['LC2030'] == 'Urban')), 'LC2030'] = td['LC2014']          
                td.loc[(td['dcode_maxinfill'] != 0), 'LC2030'] = 'Urban'
            
            #Set empty variables
            td['natural14'] = 0
            td['natural30'] = 0
            
            td['riparian'] = 0 #Riparian flag
            
            td.loc[(td['near_streams'] < 100) | (td['near_rivers'] < 650),'riparian'] = 1 #Set riparian flag to 1
            
            td['watint14'] = 'na'
            td['watint30'] = 'na'

            # do 2014
            huclist =  td['HUC_12'].tolist()
            huclist = list(set(huclist))
            td.loc[td['LC2014'].isin(['Forest, Shrubland, Young Forest, Young Shrubland, Barren, Wetland, Water', 'Grassland']),'natural14'] = 1

            # do 2030
    
            td.loc[td['LC2030'].isin(['Forest, Shrubland, Young Forest, Young Shrubland, Barren, Wetland, Water','Grassland']),'natural30'] = 1
            tdict = {}
            
            for i in huclist:
                Helpers.pmes('HUC is :' + str(i))
                tdict[i] = {}
                temp = td.loc[td['HUC_12'] == i]
                
                #Create ctemp14 = td.groupby(['natural14','riparian', 'HUC_12'], as_index = False).count()
                ctemp14 = temp.groupby(['natural14','riparian', 'HUC_12'], as_index = False).count()
                ctemp14huc = temp.groupby(['natural14'], as_index = False).count()
                
                ctemp30 = temp.groupby(['natural30','riparian'], as_index = False).count()
                ctemp30huc = temp.groupby(['natural30'], as_index = False).count()
                
                ctemp14perc = ctemp14.loc[(ctemp14['riparian'] == 1)]
                ctemp14perc.reset_index(inplace = True)
                
                ctemp30perc = ctemp30.loc[(ctemp30['riparian'] == 1)]
                ctemp30perc.reset_index(inplace = True)
                
               
                rip14nat = 0
                rip14unnat = 0
                rip30unnat = 0
                rip30nat = 0
                
                nat14 = 0
                unnat14 = 0
                unnat30 = 0
                nat30 = 0
                
                #Get Riparian Variables
                if len(ctemp14perc.loc[ctemp14perc['natural14'] == 1].index) > 0:
                    tempd = ctemp14perc.loc[ctemp14perc['natural14'] == 1]
                    rip14nat = tempd.iloc[0]['pointid']
                if len(ctemp14perc.loc[ctemp14perc['natural14'] == 0].index) > 0:
                    tempd = ctemp14perc.loc[ctemp14perc['natural14'] == 0]
                    rip14unnat = tempd.iloc[0]['pointid']
                if len(ctemp30perc.loc[ctemp30perc['natural30'] == 1].index) > 0:
                    tempd = ctemp30perc.loc[ctemp30perc['natural30'] == 1]
                    rip30nat = tempd.iloc[0]['pointid']
                if len(ctemp30perc.loc[ctemp30perc['natural30'] == 0].index) > 0:
                    tempd = ctemp30perc.loc[ctemp30perc['natural30'] == 0]
                    rip30unnat = tempd.iloc[0]['pointid']
                    
                #Get Watershed Variables
                if len(ctemp14huc.loc[ctemp14huc['natural14'] == 1].index) > 0:
                    tempd = ctemp14huc.loc[ctemp14huc['natural14'] == 1]
                    nat14 = tempd.iloc[0]['pointid']
                if len(ctemp14huc.loc[ctemp14huc['natural14'] == 0].index) > 0:
                    tempd = ctemp14huc.loc[ctemp14huc['natural14'] == 0]
                    unnat14 = tempd.iloc[0]['pointid']
                if len(ctemp30huc.loc[ctemp30huc['natural30'] == 1].index) > 0:
                    tempd = ctemp30huc.loc[ctemp30huc['natural30'] == 1]
                    nat30 = tempd.iloc[0]['pointid']
                if len(ctemp30huc.loc[ctemp30huc['natural30'] == 0].index) > 0:
                    tempd = ctemp30huc.loc[ctemp30huc['natural30'] == 0]
                    unnat30 = tempd.iloc[0]['pointid']                  
                    
                #If there are any riparian pixels, make naturalness ratio.
                if (rip14nat != 0) |  (rip14unnat != 0):
                    tempripint14 = rip14nat/(rip14nat+rip14unnat)
                    tempripint14 = float(tempripint14)
                else: 
                    tempripint14 = None
                    
                if (rip30nat != 0) |  (rip30unnat != 0):
                    tempripint30 = rip30nat/(rip30nat+rip30unnat)
                    tempripint30 = float(tempripint30)
                else: 
                    tempripint30 = None
                
                
                #If there are any HUC pixels, make naturalness ratio
                hucpcent14 = nat14/(nat14+unnat14)
                hucpcent14 = float(hucpcent14)
                
                hucpcent30 = nat30/(nat30+unnat30)
                hucpcent30 = float(hucpcent30)
                    
    #            type(np.float64(0).item())
                #Calculated Riparian Integrity
                if tempripint14:
                    if (tempripint14 > .7) & (hucpcent14 > .7):
                        temp['watint14'] = 'Natural Catchment'
                        tdict[i]['watint14'] =  'Natural Catchment'
                    elif (tempripint14 > .7) & (hucpcent14< .7):
                        temp['watint14'] = 'Important Riparian Buffer'
                        tdict[i]['watint14'] =  'Important Riparian Buffer'
                    elif (tempripint14 < .7):
                        temp['watint14'] = 'Degraded'
                        tdict[i]['watint14'] =  'Degraded'
                        
                    elif (tempripint14 > .7):
                        temp['watint14'] = 'Natural Catchment'
                        tdict[i]['watint14'] =  'Natural Catchment'                     
                       
                    else:
                        temp['watint14'] = 'Degraded'
                        tdict[i]['watint14'] =  'Degraded'
                    
                #Calculate watershed integrity
                if tempripint30:
                    Helpers.pmes('riparian is :' + str(tempripint30) + ' AND watershed is :' + str(hucpcent30))
                    if (tempripint30 > .7) & (hucpcent30 > .7):
                        temp['watint30'] = 'Natural Catchment'
                        tdict[i]['watint30'] =  'Natural Catchment'
                    elif (tempripint30 > .7) & (hucpcent30 < .7):
                        temp['watint30'] = 'Important Riparian Buffer'
                        tdict[i]['watint30'] =  'Important Riparian Buffer'
                    elif (tempripint30 < .7):
                        temp['watint30'] = 'Degraded'
                        tdict[i]['watint30'] =  'Degraded'
                    elif (tempripint30 > .7):
                        temp['watint30'] = 'Natural Catchment'
                        tdict[i]['watint30'] =  'Natural Catchment'                      
                    else:                
                        temp['watint30'] = 'Degraded'
                        tdict[i]['watint30'] =  'Degraded'
                tdf = tdf.append(temp)
    
            Helpers.pmes(tdict)
            
            temp14 = tdf.groupby(['watint14'], as_index = False).count()
            temp14 = temp14[['pointid','watint14']]
            temp14 = temp14.rename(columns = {'pointid':'count14'})
    
            
            temp30 = tdf.groupby(['watint30'], as_index = False).count()
            temp30 = temp30[['pointid','watint30']]
            temp30 = temp30.rename(columns = {'pointid':'count30'})

            tempmerge = pd.merge(temp14,temp30, left_on = 'watint14',right_on='watint30', how = 'left')
            
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            Helpers.pmes(tempmerge)
            tempmerge['change'] = (tempmerge['change']*900)/10000
            tempmerge = tempmerge.rename(columns = {'watint14':'Integrity Class','change':'hectares_of_change'})
            tempmerge.to_csv('P:/Temp/' + x+'_watershed_integrity.csv') #will be in kilograms
    
    fmmp(df,outpath)
    fema(df,outpath)
    scenic(df,outpath)
    wateruse(df,outpath)
    lcchange(df,outpath)
    pcalcchange(df,outpath)
    termovement(df,outpath)
    cropvalue(df,outpath)
    groundwater(df,outpath)
    nitrates(df,outpath)
    watershedintegrity(df,outpath)
    
    
    

