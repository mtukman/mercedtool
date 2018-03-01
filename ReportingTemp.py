# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 08:58:23 2018

@author: Dylan
"""


#def report(outpath, df):
def report(df, outpath,aca = 0, acu = 0, oak = 0, rre = 0, cd = 0 , cm = 0):
    import pandas as pd
    import Helpers
    from functools import reduce
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    dfdict = {}
    dfdict['base'] = df
    dfdict['trt'] = df
    
    if rre == 1:
        df2 = df.loc[(df['rreselected'] == 1)]
        dfdict['rre'] = df2
        
    if oak == 1:
        df3 = df.loc[df['oakselected'] == 1]
        dfdict['oak'] = df3  
    if cd == 1:
        df4 = df.loc[df['dev_flag'] == 1]
        dfdict['cdev'] = df4      
    if cm == 1:
        df5 = df.loc[df['con_flag'] == 1]
        dfdict['cons'] = df5          
    if aca == 1:
        df6 = df.loc[df['aca_flag'] == 1]
        dfdict['aca'] = df6      
    if acu == 1:
        df7 = df.loc[df['acu_flag'] == 1]
        dfdict['acu'] = df7         
    
    
    keylist = [*dfdict]
    
    
    def fmmp(df, outpath):
        aglist = ['Orchard','Annual Cropland','Vineyard', 'Rice', 'Irrigated Pasture']
        developed = ['Developed','Urban','Developed Roads']
        devlist = ['bau','medinfill','maxinfill']
        flist = ['P','U','L', 'S']
        def ffunct (name, field, dev, df):
            td = df[[field,'LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'fmmp_class']]
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            if dev == 'medinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_medinfill'] != 0, field] = 'Urban'
            if dev == 'maxinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_maxinfill'] != 0, field] = 'Urban'
                
            Helpers.pmes('Doing 2014 FMMP, ' + name + ', ' + dev)
            tempdf = td.loc[(td['LC2014'].isin(aglist)) & (td[field].isin(developed)) & (td['fmmp_class'].isin(flist))]
    #        # do 2014
    
            group = tempdf.groupby('fmmp_class', as_index = False).count()
            group = group[['fmmp_class','pointid']]
            group['pointid'] = (group['pointid']*900)/10000
            group = group.rename(columns = {'pointid':'ha_loss_' + name + '_' + dev})
            fmmpdict[name + dev] = group
            group.to_csv(outpath +name+dev +'fmmp.csv')
        fmmpdict = {}
        for x in keylist:
            Helpers.pmes('Doing : ' + x)
            
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        ffunct(x, 'LC2030', i, dfdict[x])
                else:
                    for i in devlist:
                        ffunct(x, 'LC2030_trt', i, dfdict[x])
            elif x in ['acu', 'aca']:
                ffunct(x, 'LC2030_ac', 'bau',dfdict[x])
            else:
                ffunct(x, 'LC2030_trt', 'bau',dfdict[x])
                
        tlist = list(fmmpdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'fmmp_class', how = 'left' )
            count = count + 1
#        temp = Helpers.MergeMultiDF('fmmp_class',tlist )
                
        temp.to_csv(outpath + 'fmmp.csv')
        
            

    
    def fema(df, outpath):
        devlist = ['bau','medinfill','maxinfill']
        
        
        flist = [100,500]
        gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
        def femafunct(name, field,query, dev, df):

            td = df[[field,'LC2014','dcode_medinfill','dcode_maxinfill','pointid','fema_class', 'near_fema']]
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            

            if dev == 'medinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_medinfill'] != 0, field] = 'Urban'
            if dev == 'maxinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_maxinfill'] != 0, field] = 'Urban'

            # do 2014
            tempdf14 = td.loc[(td['fema_class'].isin(query)) & (td['near_fema'] == 0)]
            tempdf14 = pd.merge(tempdf14,gclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby(['gen_class'], as_index = False).count()
            group14 = group14[['pointid','gen_class']]
            group14 = group14.rename(columns={'pointid':'count14'})
 
            # do 2030
            tempdf30 = td.loc[(td['fema_class'].isin(query)) & (td['near_fema'] == 0)]
            tempdf30 = pd.merge(tempdf30,gclass, how = 'left', left_on = field, right_on = 'landcover')
            group30 = tempdf30.groupby(['gen_class'], as_index = False).count()
            group30 = group30[['pointid','gen_class']]
            group30 = group30.rename(columns={'pointid':'count30'})

            if len(group30.index) == 0 | len(group14.index) == 0:
                Helpers.pmes('Empty rows in ' + dev)
            else:
                tempmerge = pd.merge(group14,group30, on = 'gen_class', how = 'left')
                tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
                tempmerge['change'] = (tempmerge['change']*900)/10000
                tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name+ '_'+dev})
                femadict[name + dev] = tempmerge
                group.to_csv(outpath +name+dev +'fema.csv')
                
        for z in flist:
            femadict = {}
            if z == 100:
                query = [100]
            if z == 500:
                query = [100,500]

            for x in keylist:
                Helpers.pmes('Doing : ' + x)
                if x in ['base', 'cdev','cons', 'trt']:
                    if x == 'base':
                        for i in devlist:
                            femafunct(x, 'LC2030', query, i, dfdict[x])
                    else:
                        for i in devlist:
                            femafunct(x, 'LC2030_trt', query, i, dfdict[x])
                elif x in ['acu', 'aca']:
                    femafunct(x, 'LC2030_ac',query, 'bau',dfdict[x])
                else:
                    femafunct(x, 'LC2030_trt', query, 'bau', dfdict[x])
            tlist = list(femadict.values())
            
            df = reduce(lambda df1,df2: pd.merge(df1,df2,on='fema_class'), tlist)
#            temp = Helpers.MergeMultiDF('fema_class',tlist )
            temp.to_csv(outpath + 'fema' + str(i) + '.csv')
                    
    
    def scenic(df, outpath):
        #6-56
        devlist = ['bau','medinfill','maxinfill']
        
        
        gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
        def scenicfunct(name, field, dev , df):        
            td = df[[field,'LC2014','dcode_medinfill','dcode_maxinfill','pointid','scenic_val']]
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            if dev == 'medinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_medinfill'] != 0, field] = 'Urban'
    
            if dev == 'maxinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_maxinfill'] != 0, field] = 'Urban'
                
            
            # do 2014
            tempdf14 = td.loc[td['scenic_val'] > 5]
            tempdf14 = pd.merge(tempdf14,gclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('gen_class', as_index = False).count()
            group14 = group14[['pointid','gen_class']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # do 2030
            tempdf30 = td.loc[td['scenic_val'] > 5]
            tempdf30 = pd.merge(tempdf30,gclass, how = 'left', left_on = field, right_on = 'landcover')
            group30 = tempdf30.groupby('gen_class', as_index = False).count()
            group30 = group30[['pointid','gen_class']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            if len(group30.index) == 0 | len(group14.index) == 0:
                Helpers.pmes('Empty rows in ' + i)
                
            else:
                tempmerge = pd.merge(group14,group30, on = 'gen_class', how = 'left')
                tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
                tempmerge['change'] = (tempmerge['change']*900)/10000
                tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name +'_'+ dev})
                scendict[name + dev] = tempmerge
        scendict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        scenicfunct(x, 'LC2030', i, dfdict[x])
                else:
                    for i in devlist:
                        scenicfunct(x, 'LC2030_trt', i, dfdict[x])
            elif x in ['acu', 'aca']:
                    scenicfunct(x, 'LC2030_ac', 'bau',dfdict[x])
            else:
                scenicfunct(x, 'LC2030_trt', 'bau', dfdict[x])
        tlist = list(scendict.values())
        temp = Helpers.MergeMultiDF('fema_class',tlist )
        temp.to_csv(outpath + 'scenic' + '.csv')

    

    def wateruse(df, outpath):
        #6-56
        devlist = ['bau','medinfill','maxinfill']
        
        
        wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_wateruse.csv")
        def watfunct(name, field, dev , df):       
            td = df[[field,'LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            if dec == 'medinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_medinfill'] != 0, field] = 'Urban'
                
                
            if i == 'maxinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_maxinfill'] != 0, field] = 'Urban'
                
            
            # do 2014
            tempdf14 = pd.merge(td,wclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('LC2014', as_index = False).sum()
            group14 = group14[['wat_val','LC2014']]
            group14 = group14.rename(columns={'wat_val':'water14'})
            
            
            # do 2030
            tempdf30 = pd.merge(td,wclass, how = 'left', left_on = field, right_on = 'landcover')
            group30 = tempdf30.groupby(field, as_index = False).sum()
            group30 = group30[['wat_val',field]]
            group30 = group30.rename(columns={'wat_val':'water30'})
            
            tempmerge = pd.merge(group14,group30, left_on = 'LC2014', right_on= field, how = 'left')
            tempmerge['change'] = tempmerge['water30']-tempmerge['water14']
            tempmerge = tempmerge.rename(columns = {'LC2014':'landcover','change':'ac_ft_change' + name +'_'+ dev})
            watdict[name + dev] = tempmerge
        
        watdict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        watfunct(x, 'LC2030', i, dfdict[x])
                else:
                    for i in devlist:
                        watfunct(x, 'LC2030_trt', i, dfdict[x])
            elif x in ['acu', 'aca']:
                    watfunct(x, 'LC2030_ac', 'bau',dfdict[x])                        
            else:
                watfunct(x, 'LC2030_trt', 'bau', dfdict[x])
        tlist = list(watdict.values())
        temp = Helpers.MergeMultiDF('landcover',tlist )
        
        temp.to_csv(outpath+'_waterdemand.csv')
    
    def lcchange(df, outpath):
        devlist = ['bau','medinfill','maxinfill']
        def lcfunct(name, field, dev, df): 
            td = df[[field,'LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            if dev == 'medinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_medinfill'] != 0, field] = 'Urban'
            if dev == 'maxinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_maxinfill'] != 0, field] = 'Urban'
            # do 2014
            group14 = td.groupby('LC2014').count()
            group14['index1'] = group14.index
            group14 = group14[['pointid','index1']]
            group14 = group14.rename(columns={'pointid':'count14'})
            # do 2030
            group30 = td.groupby(field).count()
            group30['index1'] = group30.index
            group30 = group30[['pointid','index1']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = (tempmerge['change']*900)/10000
            tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'ha_change_' + name +'_'+ dev})
            lctdict[name + dev] = tempmerge
        lcdict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        lcfunct(x, 'LC2030', i, dfdict[x])
                else:
                    for i in devlist:
                        lcfunct(x, 'LC2030_trt', i, dfdict[x])
            elif x in ['acu', 'aca']:
                    lcfunct(x, 'LC2030_ac', 'bau',dfdict[x])                           
            else:
                lcfunct(x, 'LC2030_trt', 'bau', dfdict[x])
        tlist = list(lcdict.values())
        temp = Helpers.MergeMultiDF('landcover',tlist )
        
        temp.to_csv(outpath+'_cover_change.csv')    
    
    def pcalcchange(df, outpath):
        devlist = ['bau','medinfill','maxinfill']
        def pcafunct(name, field, dev, df): 

            td = df[[field,'LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'pca_val']]
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            if i == 'medinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_medinfill'] != 0, field] = 'Urban'
                
                
            if i == 'maxinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_maxinfill'] != 0, field] = 'Urban'
                
            
            # do 2014
            tempdf14 = td.loc[td['pca_val'] == 1]
            group14 = tempdf14.groupby('LC2014').count()
            group14['index1'] = group14.index
            group14 = group14[['pointid','index1']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # do 2030
            tempdf30 = td.loc[td['pca_val'] == 1]
            group30 = tempdf30.groupby(field).count()
            group30['index1'] = group30.index
            group30 = group30[['pointid','index1']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = (tempmerge['change']*900)/10000
            tempmerge = tempmerge.rename(columns = {'index1':'lancover','change':'ha_change_' + name +'_'+ dev})
            pcadict[name + dev] = tempmerge
        pcadict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        pcafunct(x, 'LC2030', i, dfdict[x])
                else:
                    for i in devlist:
                        pcafunct(x, 'LC2030_trt', i, dfdict[x])
            elif x in ['acu', 'aca']:
                    pcafunct(x, 'LC2030_ac', 'bau',dfdict[x])                              
            else:
                pcafunct(x, 'LC2030_trt', 'bau', dfdict[x])
        tlist = list(pcadict.values())
        temp = Helpers.MergeMultiDF('landcover',tlist )
        
        temp.to_csv(outpath+'pca_cover_change.csv')       
    
    def termovement(df, outpath):
        devlist = ['bau','medinfill','maxinfill']
        
        rclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_resistance.csv")
        arealist = ['county','eca']
        def movefunct(name, field, dev, df, area): 
            td = df[[field,'LC2014','dcode_medinfill','dcode_maxinfill','pointid','eca_val']]
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            if area == 'eca':
                td = td.loc[td['eca_val'] == 1]
            if dev == 'medinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_medinfill'] != 0, field] = 'Urban'
                
                
            if dev == 'maxinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']
                td.loc[td['dcode_maxinfill'] != 0, field] = 'Urban'
                
            
            # do 2014
            tempdf14 = pd.merge(td,rclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('res_val').count()
            group14['index1'] = group14.index
            group14 = group14[['pointid','index1']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # do 2030
            tempdf30 = pd.merge(td,rclass, how = 'left', left_on = field, right_on = 'landcover')
            group30 = tempdf30.groupby('res_val').count()
            group30['index1'] = group30.index
            group30 = group30[['pointid','index1']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = (tempmerge['change']*900)/10000
            tempmerge = tempmerge.rename(columns = {'index1':'movement_potential','change':'ha_change_' + name +'_'+ dev})
            movedict[name + dev] = tempmerge
            
        for y in arealist:
               
            movedict = {}
            for x in keylist:
                if x in ['base', 'cdev','cons', 'trt']:
                    if x == 'base':
                        for i in devlist:
                            movefunct(x, 'LC2030', i, dfdict[x], y)
                    else:
                        for i in devlist:
                            movefunct(x, 'LC2030_trt', i, dfdict[x], y)
                elif x in ['acu', 'aca']:
                    movefunct(x, 'LC2030_ac', 'bau',dfdict[x],y)                              
                else:
                    movefunct(x, 'LC2030_trt', 'bau', dfdict[x], y)
            tlist = list(movedict.values())
            temp = Helpers.MergeMultiDF('movement_potential',tlist )
        
            temp.to_csv(outpath+y+'_movement.csv')   
    
    
    def cropvalue(df, outpath):

        devlist = ['bau','medinfill','maxinfill']
    
        
        wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_crop_value.csv")
        def cropfunct(name, field, dev, df): 
            td = df[[field,'LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
            if i == 'medinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']           
                td.loc[td['dcode_medinfill'] != 0, field] = 'Urban'
    
            if i == 'maxinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']            
                td.loc[td['dcode_maxinfill'] != 0, field] = 'Urban'
    
            
            # do 2014
            tempdf14 = pd.merge(td,wclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('LC2014').sum()
            group14['index1'] = group14.index
            group14 = group14[['crop_val','index1']]
            group14 = group14.rename(columns={'crop_val':'crop14'})
            
            
            # do 2030
            tempdf30 = pd.merge(td,wclass, how = 'left', left_on = field, right_on = 'landcover')
            group30 = tempdf30.groupby(field).sum()
            group30['index1'] = group30.index
            group30 = group30[['crop_val','index1']]
            group30 = group30.rename(columns={'crop_val':'crop30'})
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
            tempmerge['change'] = tempmerge['crop30']-tempmerge['crop14']
            tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'Change in Value' + name +'_'+ dev})
            cropdict[name + dev] = tempmerge
            
        cropdict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        cropfunct(x, 'LC2030', i, dfdict[x])
                else:
                    for i in devlist:
                        cropfunct(x, 'LC2030_trt', i, dfdict[x])
            elif x in ['acu', 'aca']:
                cropfunct(x, 'LC2030_ac', 'bau',dfdict[x])  
            else:
                cropfunct(x, 'LC2030_trt', 'bau', dfdict[x])
        tlist = list(cropdict.values())
        temp = Helpers.MergeMultiDF('landcover',tlist )
    
        temp.to_csv(outpath+'_cropvalue.csv')              
            
    
    def groundwater(df, outpath):
        #6-56
        devlist = ['bau','medinfill','maxinfill']
        def gwfunct(name, field, dev, df): 
            td = df[[field,'LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'bcm_val']]
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            td['bcm_val'] =  (td['bcm_val']*.0032808) * .222394 #Turn into ac/ft/pixel/year
            if i == 'medinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']            
                td.loc[(td['dcode_medinfill'] != 0), field] = 'Urban'
      
            if i == 'maxinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']           
                td.loc[(td['dcode_maxinfill'] != 0), field] = 'Urban'
    
            
            # do 2014
            td2 = td.loc[((td[field] != td['LC2014']) & (td[field].isin(['Urban', 'Developed', 'Developed_Roads'])))]
            
            group30 = td2.groupby(field).sum()
            group30['index1'] = group30.index
            group30 = group30.rename(columns={'index1':'landcover'})
            group30 = group30.rename(columns = {'bcm_val':'ac_ft_rec_lst' + name +'_'+ dev})
            gwdictdict[name + dev] = tempmerge

        gwdict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        gwfunct(x, 'LC2030', i, dfdict[x])
                else:
                    for i in devlist:
                        gwfunct(x, 'LC2030_trt', i, dfdict[x])
            elif x in ['acu', 'aca']:
                gwfunct(x, 'LC2030_ac', 'bau',dfdict[x])  
            else:
                gwfunct(x, 'LC2030_trt', 'bau', dfdict[x])
        tlist = list(gwdict.values())
        temp = Helpers.MergeMultiDF('landcover',tlist )
    
        temp.to_csv(outpath+'_groundwater.csv')       



         
    def nitrates(df, outpath):
        #6-56
        devlist = ['bau','medinfill','maxinfill']
    
        
        wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_nitrates.csv")
        xlist = ['runoff','leach']
        
        def nitfunct(name, field, dev, df, y): 
                td = df[[field,'LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                if dev == 'medinfill':
                    td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']          
                    td.loc[td['dcode_medinfill'] != 0, field] = 'Urban'
    
                if dev == 'maxinfill':
                    td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']         
                    td.loc[td['dcode_maxinfill'] != 0, field] = 'Urban'

                # do 2014
                tempdf14 = pd.merge(td,wclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
                group14 = tempdf14.groupby('LC2014').sum()
                group14['index1'] = group14.index
                group14 = group14[[x,'index1']]
                group14[x] = group14[x]*.09
                group14 = group14.rename(columns={x:x + '14'})

                # do 2030
                tempdf30 = pd.merge(td,wclass, how = 'left', left_on = field, right_on = 'landcover')
                group30 = tempdf30.groupby(field).sum()
                group30['index1'] = group30.index
                group30 = group30[[x,'index1']]
                group30[x] = group30[x]*.09
                group30 = group30.rename(columns={x:x + '30'})
 
                tempmerge = pd.merge(group14,group30, on = 'index1', how = 'left')
                tempmerge['change'] = tempmerge[x+'30']-tempmerge[x+'14']
                tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'kgs_nitrate'})
                nitdict[name + dev] = tempmerge

        for y in xlist:
            nitdict = {}
            for x in keylist:
                if x in ['base', 'cdev','cons', 'trt']:
                    if x == 'base':
                        for i in devlist:
                            nitfunct(x, 'LC2030', i, dfdict[x],y)
                    else:
                        for i in devlist:
                            nitfunct(x, 'LC2030_trt', i, dfdict[x],y)
                elif x in ['acu', 'aca']:
                    nitfunct(x, 'LC2030_ac', 'bau',dfdict[x])  
                else:
                    nitfunct(x, 'LC2030_trt', 'bau', dfdict[x],y)
            tlist = list(nitdict.values())
            temp = Helpers.MergeMultiDF('landcover',tlist )
        
            temp.to_csv(outpath+y+'_nitrates.csv')                       
    
    def watershedintegrity(df, outpath):
        #6-56
        devlist = ['bau','medinfill','maxinfill']
        
        def intfunct(name, field, dev, df, y): 
            td = df[[field,'LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'HUC_12', 'near_rivers','near_streams']]
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            tdf = pd.DataFrame()
                
            if dev == 'medinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']           
                td.loc[(td['dcode_medinfill'] != 0), field] = 'Urban'
    
            if dev == 'maxinfill':
                td.loc[((td[field] != td['LC2014']) & (td[field] == 'Urban')), field] = td['LC2014']          
                td.loc[(td['dcode_maxinfill'] != 0), field] = 'Urban'
            
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
    
            td.loc[td[field].isin(['Forest, Shrubland, Young Forest, Young Shrubland, Barren, Wetland, Water','Grassland']),'natural30'] = 1
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
            tempmerge = tempmerge.rename(columns = {'watint14':'Integrity_Class','change':'ha_change_' + name +'_'+ dev})
            cropdict[name + dev] = tempmerge


        intdict = {}
        for x in keylist:
            if x in ['base', 'trt']:
                if x == 'base':
                    for i in devlist:
                        intfunct(x, 'LC2030', i, dfdict[x])
                else:
                    for i in devlist:
                        intfunct(x, 'LC2030_trt', i, dfdict[x])
        tlist = list(intdict.values())
        temp = Helpers.MergeMultiDF('Integrity_Class',tlist )
    
        temp.to_csv(outpath+y+'_nitrates.csv')      
        
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

