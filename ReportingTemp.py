# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 08:58:23 2018

@author: Dylan
"""


#def report(outpath, df):
def report(df, outpath, acdict = 'None', oak = 0, rre = 0, cd = 0 , cm = 0):
    import pandas as pd
    import Helpers
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
        dfdict['dev'] = 'cust'
    if cm == 1:
        df5 = df.loc[df['con_flag'] == 1]
        dfdict['con'] = df5          
    if cd == 1:
        devlist = ['bau','med','max', 'cust']
    else:
        devlist = ['bau','med','max']
    if acdict != 'None':
        aclist = [*acdict]
        for i in aclist:
            df2 = df.loc[(df[i+'selected'] == 1)]
            dfdict[i] = df2
    keylist = [*dfdict]

    def fmmp(df, outpath):
        aglist = ['Orchard','Annual Cropland','Vineyard', 'Rice', 'Irrigated Pasture','Forest', 'Shrubland', 'Wetland', 'Barren', 'Water']
        developed = ['Developed','Urban','Developed Roads']
        
        flist = ['P','U','L', 'S']
        def ffunct (name, field, dev, df):
            td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'fmmp_class', field]]

            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'  
            Helpers.pmes('FMMP Reporting: ' + name + ', ' + dev)
            tempdf = td.loc[(td['LC2014'].isin(aglist))]
            tempdf = tempdf.loc[(tempdf[field].isin(developed))]
            tempdf = tempdf.loc[(tempdf['fmmp_class'].isin(flist))]
            group = tempdf.groupby('fmmp_class', as_index = False).count()
            group = group[['fmmp_class','pointid']]
            group['pointid'] = (group['pointid']*900)/10000
            if 'urb' in name:
                group['pointid'] = group['pointid']* (-1)
                group = group.rename(columns = {'pointid':'ha_loss_avoided_' + name})
            else:
                group = group.rename(columns = {'pointid':'ha_loss_' + name + '_' + dev})
                
            fmmpdict[name + dev] = group

        fmmpdict = {}
        for x in keylist:
            if x in ['base', 'dev', 'trt', 'con']:
                if x == 'base':
                    for i in devlist:
                        ffunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        ffunct(x, 'LC2030_trt_' + i, i, dfdict[x])
            elif ('urb' in x):
                ffunct(x, 'LC2030_bau', i, dfdict[x])
                
        td = df[['LC2014','pointid', 'fmmp_class']]
        tempdf = td.loc[(~td['LC2014'].isin(developed))]
        tempdf = tempdf.loc[(tempdf['fmmp_class'].isin(flist))]
        group = tempdf.groupby('fmmp_class', as_index = False).count()
        group = group[['fmmp_class','pointid']]
        group['pointid'] = (group['pointid']*900)/10000
        group = group.rename(columns = {'pointid':'ha_2014'})
        fmmpdict['Base_2014'] = group
        tlist = list(fmmpdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'fmmp_class', how = 'outer' )
            count = count + 1
        temp.loc[temp['fmmp_class'] == 'P', 'fmmp_class' ] = 'Prime Farmland' 
        temp.loc[temp['fmmp_class'] == 'L', 'fmmp_class' ] = 'Local Importance' 
        temp.loc[temp['fmmp_class'] == 'S', 'fmmp_class' ] = 'Statewide Importance' 
        temp.loc[temp['fmmp_class'] == 'U', 'fmmp_class' ] = 'Unique Farmland' 
        temp.fillna(0)
        temp.to_csv(outpath + 'fmmp.csv')

    
    def fema(df, outpath):

        flist = [100,500]
        gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
        def femafunct(name, field,query, dev, df):
            if 'ac' in name:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','fema_class', 'near_fema', field, 'LC2030_bau']]
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','fema_class', 'near_fema', field]]
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            Helpers.pmes('FEMA Reporting: ' + name + ', ' + dev)
            # do 2014
            tempdf14 = td.loc[(td['fema_class'].isin(query)) & (td['near_fema'] == 0)]
            tempdf14 = pd.merge(tempdf14,gclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby(['gen_class'], as_index = False).count()
            group14 = group14[['pointid','gen_class']]
            group14 = group14.rename(columns={'pointid':'count14'})
 
            # do 2030
            tempdf30 = td.loc[(td['fema_class'].isin(query)) & (td['near_fema'] == 0)]
            tempdf30 = pd.merge(tempdf30,gclass, how = 'outer', left_on = field, right_on = 'landcover')
            group30 = tempdf30.groupby(['gen_class'], as_index = False).count()
            group30 = group30[['pointid','gen_class']]
            group30 = group30.rename(columns={'pointid':'count30'})

            if len(group30.index) == 0 | len(group14.index) == 0:
                Helpers.pmes('Empty rows in ' + dev)
            else:
                tempmerge = pd.merge(group14,group30, on = 'gen_class', how = 'outer')
                tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
                tempmerge['change'] = (tempmerge['change']*900)/10000
                if name in ['base','trt']:
                    tempmerge = tempmerge[['gen_class', 'change','count30']]
                    tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                    tempmerge['ha_' + name+ '_'+dev] = (tempmerge['ha_' + name+ '_'+dev]*900)/10000
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name+ '_'+dev})
                elif 'ac' in x:
                    tempdf302 = td.loc[(td['fema_class'].isin(query)) & (td['near_fema'] == 0)]
                    tempdf302 = pd.merge(tempdf302,gclass, how = 'outer', left_on = 'LC2030_bau', right_on = 'landcover')
                    group302 = tempdf302.groupby(['gen_class'], as_index = False).count()
                    group302 = group302[['pointid','gen_class']]
                    group302 = group302.rename(columns={'pointid':'count302'})
                    tempmerge = pd.merge(group302,group30, on = 'gen_class', how = 'outer')
                    tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                    tempmerge['change'] = (tempmerge['change']*900)/10000
                    tempmerge = tempmerge[['change','gen_class']]
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name})
                else:
                    tempmerge = tempmerge[['gen_class', 'change']]
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name})
                femadict[name + dev] = tempmerge
                
        for z in flist:
            femadict = {}
            if z == 100:
                query = [100]
            if z == 500:
                query = [100,500]

            for x in keylist:
                Helpers.pmes('Doing : ' + x)
                if x in ['base', 'dev','cons', 'trt']:
                    if x == 'base':
                        for i in devlist:
                            femafunct(x, 'LC2030_' + i, query, i, dfdict[x])
                    else:
                        for i in devlist:
                            femafunct(x, 'LC2030_trt_' + i, query, i, dfdict[x])
                elif 'ac' in x:
                    femafunct(x, 'LC2030_trt_bau',query, 'bau',dfdict[x])

                else:
                    femafunct(x, 'LC2030_trt_bau', query, 'bau', dfdict[x])
                    
            #Add 2014 Base
            td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','fema_class', 'near_fema']]
            tempdf14 = td.loc[(td['fema_class'].isin(query)) & (td['near_fema'] == 0)]
            tempdf14 = pd.merge(tempdf14,gclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby(['gen_class'], as_index = False).count()
            group14 = group14[['pointid','gen_class']]
            group14 = group14.rename(columns={'pointid':'ha_2014'})
            group14['ha_2014'] = (group14['ha_2014']*900)/10000
            femadict['Base_2014'] = group14
            tlist = list(femadict.values())
            l = len(tlist)
            count = 1
            temp = tlist[0]
            while count < l:
                temp = pd.merge(temp,tlist[count],on = 'gen_class', how = 'outer' )
                count = count + 1
            temp.fillna(0)
            temp.to_csv(outpath + 'flood' + str(z) + '.csv')
                    
    
    def scenic(df, outpath):
        #6-56

        gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
        def scenicfunct(name, field, dev , df):        
            if 'ac' in name:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','scenic_val', field, 'LC2030_bau']]
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','scenic_val', field]]
            
            
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            
            Helpers.pmes('Scenic Reporting: ' + name + ', ' + dev)
            
            # do 2014
            tempdf14 = td.loc[td['scenic_val'] > 5]
            tempdf14 = pd.merge(tempdf14,gclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('gen_class', as_index = False).count()
            group14 = group14[['pointid','gen_class']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # do 2030
            tempdf30 = td.loc[td['scenic_val'] > 5]
            tempdf30 = pd.merge(tempdf30,gclass, how = 'outer', left_on = field, right_on = 'landcover')
            group30 = tempdf30.groupby('gen_class', as_index = False).count()
            group30 = group30[['pointid','gen_class']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            if len(group30.index) == 0 | len(group14.index) == 0:
                Helpers.pmes('Empty rows in ' + i)
                
            else:
                tempmerge = pd.merge(group14,group30, on = 'gen_class', how = 'outer')
                tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
                tempmerge['change'] = (tempmerge['change']*900)/10000
                if name in ['base','trt']:
                    tempmerge = tempmerge[['gen_class', 'change','count30']]
                    tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                    tempmerge['ha_' + name +'_'+ dev] = (tempmerge['ha_' + name +'_'+ dev]*900)/10000
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name +'_'+ dev})
                elif 'ac' in x:
                    tempdf302 = td.loc[td['scenic_val'] > 5]
                    tempdf302 = pd.merge(tempdf302,gclass, how = 'outer', left_on = 'LC2030_bau', right_on = 'landcover')
                    group302 = tempdf302.groupby(['gen_class'], as_index = False).count()
                    group302 = group302[['pointid','gen_class']]
                    group302 = group302.rename(columns={'pointid':'count302'})
                    tempmerge = pd.merge(group302,group30, on = 'gen_class', how = 'outer')
                    tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                    tempmerge['change'] = (tempmerge['change']*900)/10000
                    tempmerge = tempmerge[['change','gen_class']]
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name})
                else:
                    tempmerge = tempmerge[['gen_class', 'change']]
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name})
                scendict[name + dev] = tempmerge
        scendict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        scenicfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        scenicfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
            elif 'ac' in x:
                    scenicfunct(x, 'LC2030_trt_bau', 'bau',dfdict[x])

            else:
                scenicfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
                
                
        #Add 2014 Base
        td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','scenic_val']]
        tempdf14 = td.loc[td['scenic_val'] > 5]
        tempdf14 = pd.merge(tempdf14,gclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
        group14 = tempdf14.groupby(['gen_class'], as_index = False).count()
        group14 = group14[['pointid','gen_class']]
        group14 = group14.rename(columns={'pointid':'ha_2014'})
        group14['ha_2014'] = (group14['ha_2014']*900)/10000
        scendict['Base_2014'] = group14
        tlist = list(scendict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'gen_class', how = 'outer' )
            count = count + 1
        temp.fillna(0)
        temp.to_csv(outpath + 'scenic' + '.csv')

    

    def wateruse(df, outpath):


        wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_wateruse.csv")
        def watfunct(name, field, dev , df):      
            if 'ac' in name:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field, 'LC2030_bau']]
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field]]
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            Helpers.pmes('Water Conservation Reporting: ' + name + ', ' + dev)
            # do 2014
            tempdf14 = pd.merge(td,wclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('LC2014', as_index = False).sum()
            group14 = group14[['wat_val','LC2014']]
            group14 = group14.rename(columns={'wat_val':'water14'})
            
            
            # do 2030
            tempdf30 = pd.merge(td,wclass, how = 'outer', left_on = field, right_on = 'landcover')
            group30 = tempdf30.groupby(field, as_index = False).sum()
            group30 = group30[['wat_val',field]]
            group30 = group30.rename(columns={'wat_val':'water30'})
            
            tempmerge = pd.merge(group14,group30, left_on = 'LC2014', right_on= field, how = 'outer')
            tempmerge['change'] = tempmerge['water30']-tempmerge['water14']
            if name in ['base','trt']:
                tempmerge = tempmerge[['LC2014', 'change', 'water30']]
                tempmerge = tempmerge.rename(columns = {'water30':'ac_ft_' + name +'_'+ dev})
                tempmerge['ac_ft_' + name +'_'+ dev] = tempmerge['ac_ft_' + name +'_'+ dev]*4.49651111111
                tempmerge['change'] = tempmerge['change']*4.49651111111
                tempmerge = tempmerge.rename(columns = {'LC2014':'landcover','change':'ac_ft_change_' + name +'_'+ dev})
            elif 'ac' in name:
                tempdf302 = pd.merge(td,wclass, how = 'outer', left_on = 'LC2030_bau', right_on = 'landcover')
                group302 = tempdf302.groupby(['LC2030_bau'], as_index = False).sum()
                group302 = group302[['LC2030_bau','wat_val']]
                group302 = group302.rename(columns={'wat_val':'water302'})
                tempmerge = pd.merge(group302,group30, left_on = 'LC2030_bau',right_on = 'LC2030_trt_bau', how = 'outer')
                tempmerge['change'] = tempmerge['water30']-tempmerge['water302']
                tempmerge['change'] = tempmerge['change']*4.49651111111
                tempmerge = tempmerge[['change','LC2030_bau']]
                tempmerge = tempmerge.rename(columns = {'change':'ac_ft_change_' + name, 'LC2030_bau':'landcover'})
                
            else:
                tempmerge = tempmerge[['LC2014', 'change']]
                tempmerge = tempmerge.rename(columns = {'LC2014':'landcover','change':'ac_ft_change_' + name})
            watdict[name + dev] = tempmerge
        
        watdict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        watfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        watfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
            elif 'ac' in x:
                watfunct(x, 'LC2030_trt_bau', 'bau',dfdict[x])
            else:
                watfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
        td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
        tempdf14 = pd.merge(td,wclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
        
        group14 = tempdf14.groupby('LC2014', as_index = False).sum()
        group14 = group14[['wat_val','LC2014']]
        group14 = group14.rename(columns={'wat_val':'ac_ft_2014','LC2014':'landcover'})
        group14['ac_ft_2014'] = group14['ac_ft_2014']*4.49651111111
        watdict['Base_2014'] = group14
        tlist = list(watdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
        temp.fillna(0)
        temp.to_csv(outpath+'watcon.csv')
    
    def lcchange(df, outpath):
        
        def lcfunct(name, field, dev, df): 
            
            if 'ac' in name:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field, 'LC2030_bau']]
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field]]
            
            Helpers.pmes('Land Cover Change Reporting: ' + name + ', ' + dev)

            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
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
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'outer')
            
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = tempmerge['change']*0.09
            if name in ['base','trt']:
                tempmerge = tempmerge[['index1', 'change','count30']]
                tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                tempmerge['ha_' + name +'_'+ dev] = tempmerge['ha_' + name +'_'+ dev]*0.09
                tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'ha_change_' + name +'_'+ dev})
            elif 'ac' in name:
                group302 = td.groupby(['LC2030_bau'], as_index = False).count()
                group302 = group302[['LC2030_bau','pointid']]
                group302 = group302.rename(columns={'pointid':'count302'})
                tempmerge = pd.merge(group302,group30, left_on = 'LC2030_bau',right_on = 'index1', how = 'outer')
                tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                tempmerge['change'] = tempmerge['change']*.09
                tempmerge = tempmerge[['change','index1']]
                tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'ha_change_' + name})
            else:
                tempmerge = tempmerge[['index1', 'change']]
                tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'ha_change_' + name})
            
            lcdict[name + dev] = tempmerge
        lcdict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        lcfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        lcfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
                        pass
            elif 'ac' in x:
                lcfunct(x, 'LC2030_trt_bau', 'bau',dfdict[x])   
            else:
                lcfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
                
                
        td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
        group14 = td.groupby('LC2014').count()
        group14['index1'] = group14.index
        group14 = group14[['pointid','index1']]
        group14 = group14.rename(columns={'pointid':'ha_2014','index1':'landcover'})
        group14['ha_2014'] = group14['ha_2014']*0.09
        lcdict['Base_2014'] = group14
        
        tlist = list(lcdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
        temp.fillna(0)
        temp.to_csv(outpath+'lcchange.csv')    
    
    def pcalcchange(df, outpath):
        
        def pcafunct(name, field, dev, df): 
            if 'ac' in name:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'pca_val', field, 'LC2030_bau']]
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'pca_val', field]]
            
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            
            Helpers.pmes('Land Cover in Priority Conservation Reporting: ' + name + ', ' + dev)
            
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
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'outer')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = (tempmerge['change']*900)/10000
            if name in ['base','trt']:
                tempmerge = tempmerge[['index1', 'change','count30']]
                tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                tempmerge['ha_' + name +'_'+ dev] = (tempmerge['ha_' + name +'_'+ dev]*900)/10000
                tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'ha_change_' + name +'_'+ dev})
            elif 'ac' in name:
                group302 = td.groupby(['LC2030_bau'], as_index = False).count()
                group302 = group302[['LC2030_bau','pointid']]
                group302 = group302.rename(columns={'pointid':'count302'})
                tempmerge = pd.merge(group302,group30, left_on = 'LC2030_bau',right_on = 'index1', how = 'outer')
                tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                tempmerge['change'] = tempmerge['change']*.09
                tempmerge = tempmerge[['change','index1']]
                tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name, 'index1':'landcover'})
            else:
                tempmerge = tempmerge[['index1', 'change']]
                tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name, 'index1':'landcover'})
            pcadict[name + dev] = tempmerge
        pcadict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        pcafunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        pcafunct(x, 'LC2030_trt_' + i, i, dfdict[x])
            elif 'ac' in x:
                pcafunct(x, 'LC2030_trt_bau', 'bau',dfdict[x])      
                       
            else:
                pcafunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
        td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'pca_val']]
        tempdf14 = td.loc[td['pca_val'] == 1]
        group14 = tempdf14.groupby('LC2014').count()
        group14['index1'] = group14.index
        group14 = group14[['pointid','index1']]
        group14 = group14.rename(columns={'pointid':'ha_2014','index1':'landcover'})
        group14['ha_2014'] = (group14['ha_2014']*900)/10000
        pcadict['Base_2014'] = group14
        tlist = list(pcadict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
        temp.fillna(0)
        temp.to_csv(outpath+'pca_cover_change.csv')       
    def aqua(df, outpath):

        gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
        
        def aquahabfunct(name, field, dev , df):        
            if 'ac' in name:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','c_abf75_rnk', field, 'LC2030_bau']]
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','c_abf75_rnk', field]]
            
            if field == 'LC2030_trt_' + dev:
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            
            Helpers.pmes('Aquatic Habitat Reporting: ' + name + ', ' + dev)
            
            # do 2014
            tempdf14 = td.loc[td['c_abf75_rnk'] > 0.632275]
            tempdf14 = pd.merge(tempdf14,gclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('gen_class', as_index = False).count()
            group14 = group14[['pointid','gen_class']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # do 2030
            tempdf30 = td.loc[td['c_abf75_rnk'] > 0.632275]
            tempdf30 = pd.merge(tempdf30,gclass, how = 'outer', left_on = field, right_on = 'landcover')
            group30 = tempdf30.groupby('gen_class', as_index = False).count()
            group30 = group30[['pointid','gen_class']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            if len(group30.index) == 0 | len(group14.index) == 0:
                Helpers.pmes('Empty rows in ' + i)
                
            else:
                tempmerge = pd.merge(group14,group30, on = 'gen_class', how = 'outer')
                tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
                tempmerge['change'] = (tempmerge['change']*900)/10000
                if name in ['base','trt']:
                    tempmerge = tempmerge[['gen_class', 'change','count30']]
                    tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                    tempmerge['ha_' + name +'_'+ dev] = (tempmerge['ha_' + name +'_'+ dev]*900)/10000
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name +'_'+ dev})
                elif 'ac' in name:
                    tempdf302 = td.loc[td['c_abf75_rnk'] > 0.632275]
                    tempdf302 = pd.merge(tempdf302,gclass, how = 'outer', left_on = 'LC2030_bau', right_on = 'landcover')
                    group302 = tempdf302.groupby('gen_class', as_index = False).count()
                    group302 = group302[['pointid','gen_class']]
                    group302 = group302.rename(columns={'pointid':'count302'})
                    tempmerge = pd.merge(group30,group302, on = 'gen_class', how = 'outer')
                    tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                    tempmerge['change'] = (tempmerge['change']*900)/10000
                    tempmerge = tempmerge[['change','gen_class']]
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name})
                else:
                    tempmerge = tempmerge[['gen_class', 'change']]
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name})
                
                scendict[name + dev] = tempmerge
            
        scendict = {}
        for x in keylist:
            if x in ['base', 'dev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        aquahabfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        aquahabfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
            elif 'ac' in x:
                    aquahabfunct(x, 'LC2030_trt_bau', 'bau',dfdict[x])
                    
            else:
                aquahabfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
        td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','c_abf75_rnk']]
        tempdf14 = td.loc[td['c_abf75_rnk'] > 0.632275]
        tempdf14 = pd.merge(tempdf14,gclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
        group14 = tempdf14.groupby('gen_class', as_index = False).count()
        group14 = group14[['pointid','gen_class']]
        group14 = group14.rename(columns={'pointid':'ha_2014'})
        group14['ha_2014'] = (group14['ha_2014']*900)/10000
        scendict['Base_2014'] = group14
        tlist = list(scendict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'gen_class', how = 'outer' )
            count = count + 1
        temp.fillna(0)
        temp.to_csv(outpath + 'aquatic.csv')
    def termovement(df, outpath):
        
        
        rclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_resistance.csv")
        arealist = ['county','eca']
        def movefunct(name, field, dev, df, area): 
            
            if 'ac' in name:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','eca_val', field, 'LC2030_bau']]
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','eca_val', field]]
            
            
            if 'trt' in field:
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            if area == 'eca':
                td = td.loc[td['eca_val'] == 1]
            
                
            Helpers.pmes('Terrestrial Resistance Reporting: ' + area + ','+ name + ', ' + dev)
            # do 2014
            tempdf14 = pd.merge(td,rclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('res_val').count()
            group14['index1'] = group14.index
            group14 = group14[['pointid','index1']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # do 2030
            tempdf30 = pd.merge(td,rclass, how = 'outer', left_on = field, right_on = 'landcover')
            group30 = tempdf30.groupby('res_val').count()
            group30['index1'] = group30.index
            group30 = group30[['pointid','index1']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'outer')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = (tempmerge['change']*900)/10000
            if name in ['base','trt']:
                tempmerge = tempmerge[['index1', 'change','count30']]
                tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                tempmerge['ha_' + name +'_'+ dev] = (tempmerge['ha_' + name +'_'+ dev]*900)/10000
                tempmerge = tempmerge.rename(columns = {'index1':'movement_potential','change':'ha_change_' + name +'_'+ dev})
            elif 'ac' in name:
                tempdf302 = pd.merge(td,rclass, how = 'outer', left_on = 'LC2030_bau', right_on = 'landcover')
                group302 = tempdf302.groupby('res_val').count()
                group302['index1'] = group302.index
                group302 = group302[['pointid','index1']]
                group302 = group302.rename(columns={'pointid':'count302'})
                tempmerge = pd.merge(group30,group302, on = 'index1', how = 'outer')
                tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                tempmerge['change'] = (tempmerge['change']*900)/10000
                tempmerge = tempmerge[['change', 'index1']]
                tempmerge = tempmerge.rename(columns = {'index1':'movement_potential','change':'ha_change_' + name})
            else:
                tempmerge = tempmerge[['index1', 'change']]
                tempmerge = tempmerge.rename(columns = {'index1':'movement_potential','change':'ha_change_' + name})
            movedict[name + dev] = tempmerge
            
        for y in arealist:
               
            movedict = {}
            for x in keylist:
                if x in ['base', 'cdev','cons', 'trt']:
                    if x == 'base':
                        for i in devlist:
                            movefunct(x, 'LC2030_' + i, i, dfdict[x], y)
                    else:
                        for i in devlist:
                            movefunct(x, 'LC2030_trt_' + i, i, dfdict[x], y)
                elif 'ac' in x:
                    movefunct(x, 'LC2030_trt_bau', 'bau',dfdict[x],y)             

                else:
                    movefunct(x, 'LC2030_trt_bau', 'bau', dfdict[x], y)
            td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','eca_val']]
            tempdf14 = pd.merge(td,rclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('res_val').count()
            group14['index1'] = group14.index
            group14 = group14[['pointid','index1']]
            group14 = group14.rename(columns={'pointid':'ha_2014','index1':'movement_potential'})
            group14['ha_2014'] = (group14['ha_2014']*900)/10000
            movedict['Base_2014'] = group14
            
            tlist = list(movedict.values())
            l = len(tlist)
            count = 1
            temp = tlist[0]
            while count < l:
                temp = pd.merge(temp,tlist[count],on = 'movement_potential', how = 'outer' )
                count = count + 1
            temp.fillna(0)
            temp.to_csv(outpath+y+'movement.csv')   
    
    
    def cropvalue(df, outpath):

        wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_crop_value.csv")
        def cropfunct(name, field, dev, df): 
            if 'ac' in name:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field, 'LC2030_bau']]
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field]]
            
            # do 2014
            tempdf14 = pd.merge(td,wclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('LC2014').sum()
            group14['index1'] = group14.index
            group14 = group14[['crop_val','index1']]
            group14 = group14.rename(columns={'crop_val':'crop14'})
            Helpers.pmes('Crop Value Reporting: ' + name + ', ' + dev)
            
            # do 2030
            tempdf30 = pd.merge(td,wclass, how = 'left', left_on = field, right_on = 'landcover')
            group30 = tempdf30.groupby(field).sum()
            group30['index1'] = group30.index
            group30 = group30[['crop_val','index1']]
            group30 = group30.rename(columns={'crop_val':'crop30'})
            
            tempmerge = pd.merge(group30,group14, on = 'index1', how = 'outer')
            tempmerge['change'] = tempmerge['crop30']-tempmerge['crop14']
            if name in ['base','trt']:
                tempmerge = tempmerge[['index1', 'change','crop30']]
                tempmerge = tempmerge.rename(columns = {'crop30':'usd' + name +'_'+ dev})
                tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'usd_change_' + name +'_'+ dev})
            elif 'ac' in name:
                tempdf302 = pd.merge(td,wclass, how = 'left', left_on = 'LC2030_bau', right_on = 'landcover')
                group302 = tempdf302.groupby(field).sum()
                group302['index1'] = group30.index
                group302 = group302[['crop_val','index1']]
                group302 = group302.rename(columns={'crop_val':'crop302'})
                tempmerge = pd.merge(group30,group302, on = 'index1', how = 'outer')
                tempmerge['change'] = tempmerge['crop30']-tempmerge['crop302']
                tempmerge = tempmerge[['change','index1']]
                tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'usd_change_' + name})
            else:
                
                tempmerge = tempmerge[['index1', 'change']]
                tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'usd_change_' + name})
            cropdict[name + dev] = tempmerge
            
        cropdict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        cropfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        cropfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
            elif 'ac' in x:
                cropfunct(x, 'LC2030_trt_bau', 'bau',dfdict[x])
 
            else:
                cropfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
        td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
        
        # do 2014
        tempdf14 = pd.merge(td,wclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
        group14 = tempdf14.groupby('LC2014').sum()
        group14['index1'] = group14.index
        group14 = group14[['crop_val','index1']]
        group14 = group14.rename(columns={'crop_val':'cropvalue_usd_2014','index1':'landcover'})
        group14['cropvalue_usd_2014'] = group14['cropvalue_usd_2014']
        cropdict['Base_2014'] = group14
        tlist = list(cropdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
        temp.fillna(0)
        temp = temp.loc[temp['landcover'].isin(['Annual Cropland','Rice','Orchard','Vineyard','Irrigated Pasture'])]
        temp.to_csv(outpath+'cropvalue.csv')              
            
    
    def groundwater(df, outpath):
        #6-56
        

        def gwfunct(name, field, dev, df): 
            if 'ac' in name:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'bcm_val', field, 'LC2030_bau']]
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'bcm_val', field]]
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            td['bcm_val'] =  (td['bcm_val']*.0032808) * .222394 #Turn into ac/ft/pixel/year
            
    
            Helpers.pmes('Groundwater Recharge Reporting: ' + name + ', ' + dev)
            # do 2014
            td2 = td.loc[((td[field] != td['LC2014']) & (td[field].isin(['Urban', 'Developed', 'Developed_Roads'])))]
            
            group30 = td2.groupby([field], as_index = False).sum()
            group30 = group30[[field, 'bcm_val']]
            group30 = group30.rename(columns={field:'landcover'})
            group30 = group30.rename(columns = {'bcm_val':'ac_ft_rec_lst_' + name +'_'+ dev})
            temp['ac_ft_rec_lst_' + name +'_'+ dev].fillna(0)
            gwdict[name + dev] = group30

        gwdict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        gwfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        gwfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
            elif 'urb' in x:
                gwfunct(x, 'LC2030_bau', 'bau',dfdict[x])  

            else:
                gwfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
        tlist = list(gwdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
        
        temp.to_csv(outpath+'groundwater.csv')       

    def nitrates(df, outpath):
        #6-56

        wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_nitrates.csv")
        xlist = ['runoff','leach']
        
        def nitfunct(name, field, dev, df, y): 
                if 'ac' in name:
                    td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field, 'LC2030_bau']]
                else:
                    td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field]]
                
                if 'trt' in field:
                    td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                    td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                    td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                    td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                Helpers.pmes('Nitrate Reporting: ' + y + ',' + name + ', ' + dev)

                # do 2014
                tempdf14 = pd.merge(td,wclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
                group14 = tempdf14.groupby('LC2014').sum()
                group14['index1'] = group14.index
                group14 = group14[[y,'index1']]
                group14[y] = group14[y]*.09
                group14 = group14.rename(columns={y:y + '14'})

                # do 2030
                tempdf30 = pd.merge(td,wclass, how = 'outer', left_on = field, right_on = 'landcover')
                group30 = tempdf30.groupby(field).sum()
                group30['index1'] = group30.index
                group30 = group30[[y,'index1']]
                group30[y] = group30[y]*.09
                
                group30 = group30.rename(columns={y:y + '30'})
 
                tempmerge = pd.merge(group14,group30, on = 'index1', how = 'outer')
                tempmerge['change'] = tempmerge[y+'30']-tempmerge[y+'14']
                if name in ['base','trt']:
                    tempmerge = tempmerge[['index1', 'change',y+'30']]
                    tempmerge = tempmerge.rename(columns = {y + '30':'kgs_no3_' + name +'_' + dev })
                    tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'kgs_no3_change_' + name + '_' + dev})
                elif 'ac' in name:
                    tempdf302 = pd.merge(td,wclass, how = 'outer', left_on = 'LC2030_bau', right_on = 'landcover')
                    group302 = tempdf302.groupby(field).sum()
                    group302['index1'] = group30.index
                    group302 = group302[[y,'index1']]
                    group302[y] = group302[y]*.09
                    group302 = group302.rename(columns={y:y + '302'})
                    tempmerge = pd.merge(group30,group302, on = 'index1', how = 'outer')
                    tempmerge['change'] = tempmerge[y+'30']-tempmerge[y+'302']
                    tempmerge = tempmerge[['change', 'index1']]
                    tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'kgs_no3_change_' + name})
                else:
                    tempmerge = tempmerge[['index1', 'change']]
                    tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'kgs_no3_change_' + name})
                nitdict[name + dev] = tempmerge

        for y in xlist:
            nitdict = {}
            for x in keylist:
                if x in ['base', 'cdev','cons', 'trt']:
                    if x == 'base':
                        for i in devlist:
                            nitfunct(x, 'LC2030_' + i, i, dfdict[x],y)
                    else:
                        for i in devlist:
                            nitfunct(x, 'LC2030_trt_' + i, i, dfdict[x],y)
                elif 'ac' in x:
                    nitfunct(x, 'LC2030_trt_bau', 'bau',dfdict[x],y)  
                    pass
                else:
                    nitfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x],y)
                    
            td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid']]        
            tempdf14 = pd.merge(td,wclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('LC2014').sum()
            group14['index1'] = group14.index
            group14 = group14[[y,'index1']]
            group14[y] = group14[y]*.09
            group14 = group14.rename(columns={y:'kgs_no3_14','index1':'landcover'})
            group14['kgs_no3_14'] = group14['kgs_no3_14']
            nitdict['Base_2014'] = group14
            
            tlist = list(nitdict.values())
            l = len(tlist)
            count = 1
            temp = tlist[0]
            while count < l:
                temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
                count = count + 1
            temp.fillna(0)
            temp.to_csv(outpath+y+'_nitrates.csv')                       
    
    def watershedintegrity(df, outpath):
        #6-56
        
        
        def intfunct(name, field, dev, df): 
            td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'HUC_12', 'near_rivers','near_streams', field]]
            if 'trt' in field:
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            import pandas as pd
            tdf = pd.DataFrame()
                
            Helpers.pmes('Watershed Integrity Reporting: ' + name + ', ' + dev)
            
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
            
            td.loc[td['LC2014'].isin(['Forest', 'Shrubland', 'Young Forest', 'Young Shrubland', 'Barren', 'Wetland', 'Water', 'Grassland']),'natural14'] = 1

            # do 2030
    
            td.loc[td[field].isin(['Forest', 'Shrubland', 'Young Forest', 'Young Shrubland', 'Barren', 'Wetland', 'Water','Grassland']),'natural30'] = 1
            tdict = {}
            
            for i in huclist:
#                Helpers.pmes('HUC is :' + str(i))
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
                    elif (tempripint14 < .7) & (hucpcent14 < .7):
                        temp['watint14'] = 'Degraded'
                        tdict[i]['watint14'] =  'Degraded'
                    elif (hucpcent14 > .7) & (tempripint14 < .7):
                        temp['watint14'] = 'Degraded'
                        tdict[i]['watint14'] =  'Degraded'
                    
                #Calculate watershed integrity
                if tempripint30:
#                    Helpers.pmes('riparian is :' + str(tempripint30) + ' AND watershed is :' + str(hucpcent30))
                    if (tempripint30 > .7) & (hucpcent30 > .7):
                        temp['watint30'] = 'Natural Catchment'
                        tdict[i]['watint30'] =  'Natural Catchment'
                    elif (tempripint30 > .7) & (hucpcent30 < .7):
                        temp['watint30'] = 'Important Riparian Buffer'
                        tdict[i]['watint30'] =  'Important Riparian Buffer'
                    elif (hucpcent30 < .7) & (tempripint30 < .7) :
                        temp['watint30'] = 'Degraded'
                        tdict[i]['watint30'] =  'Degraded'
                    elif (hucpcent30 > .7) &(tempripint30 < .7) :
                        temp['watint30'] = 'Degraded'
                        tdict[i]['watint30'] =  'Degraded'

                tdf = tdf.append(temp)
            
                
            
#            Helpers.pmes(tdict)
            tdf.to_csv('E:/Temp/watint.csv')
            temp14 = tdf.groupby(['watint14'], as_index = False).count()
            temp14 = temp14[['pointid','watint14']]
            temp14 = temp14.rename(columns = {'pointid':'count14'})
            if 'Base_2014' not in intdict:
                temp15 = temp14
                temp15 = temp15.rename(columns={'watint14':'Integrity_Class','count14':'ha_2014'})
                temp15['ha_2014'] = (temp15['ha_2014']*900)/10000
                intdict['Base_2014'] = temp15
            temp30 = tdf.groupby(['watint30'], as_index = False).count()
            temp30 = temp30[['pointid','watint30']]
            temp30 = temp30.rename(columns = {'pointid':'count30'})

            tempmerge = pd.merge(temp14,temp30, left_on = 'watint14',right_on='watint30', how = 'outer')
            
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
#            Helpers.pmes(tempmerge)
            tempmerge['change'] = (tempmerge['change']*900)/10000
            if name in ['base','trt']:
                tempmerge = tempmerge[['watint14', 'change','count30']]
                tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                tempmerge['ha_' + name +'_'+ dev] = (tempmerge['ha_' + name +'_'+ dev]*900)/10000
#
#            else:
#                tempmerge = tempmerge[['watint14', 'change']]
            tempmerge = tempmerge.rename(columns = {'watint14':'Integrity_Class','change':'ha_change_' + name +'_'+ dev})
            intdict[name + dev] = tempmerge
            

        intdict = {}
        for x in keylist:
            if x in ['base', 'trt']:
                if x == 'base':
                    for i in devlist:
                        intfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        intfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
        tlist = list(intdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'Integrity_Class', how = 'outer' )
            count = count + 1
        temp.fillna(0)
        temp.to_csv(outpath+'watint.csv')      
        
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
    aqua(df,outpath)
    
    
    
def carbreport(df, outpath,activitylist,carb14, carb30, cd = 0 , cm = 0):
    import pandas as pd
    import Helpers
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.loc[(df['LC2030_trt_bau'] == 'Woody Riparian'), 'gridcode30_trt_bau'] = df['gridcode30_bau']
    df.loc[(df['LC2030_trt_bau'] == 'Oak Conversion'), 'gridcode30_trt_bau'] = df['gridcode30_bau']
    df.loc[(df['LC2030_trt_med'] == 'Woody Riparian'), 'gridcode30_trt_med'] = df['gridcode30_med']
    df.loc[(df['LC2030_trt_med'] == 'Oak Conversion'), 'gridcode30_trt_med'] = df['gridcode30_med']
    df.loc[(df['LC2030_trt_max'] == 'Woody Riparian'), 'gridcode30_trt_max'] = df['gridcode30_max']
    df.loc[(df['LC2030_trt_max'] == 'Oak Conversion'), 'gridcode30_trt_max'] = df['gridcode30_max']
    df.loc[(df['LC2030_trt_bau'] == 'Woody Riparian'), 'LC2030_trt_bau'] = df['LC2030_bau']
    df.loc[(df['LC2030_trt_bau'] == 'Oak Conversion'), 'LC2030_trt_bau'] = df['LC2030_bau']
    df.loc[(df['LC2030_trt_med'] == 'Woody Riparian'), 'LC2030_trt_med'] = df['LC2030_med']
    df.loc[(df['LC2030_trt_med'] == 'Oak Conversion'), 'LC2030_trt_med'] = df['LC2030_med']
    df.loc[(df['LC2030_trt_max'] == 'Woody Riparian'), 'LC2030_trt_max'] = df['LC2030_max']
    df.loc[(df['LC2030_trt_max'] == 'Oak Conversion'), 'LC2030_trt_max'] = df['LC2030_max']
    
    dfdict = {}
    dfdict['base'] = df
    dfdict['trt'] = df
    if cd ==1:
        devlist = ['bau','med','max', 'cust']
    else:
        devlist = ['bau','med','max']
    Helpers.pmes(activitylist)
    for i in activitylist:
        df9 = df.loc[(df[i+'selected'] == 1)]
        dfdict[i] = df9

    if cd == 1:
        df4 = df.loc[df['dev_flag'] == 1]
        dfdict['dev'] = df4      
    if cm == 1:
        df5 = df.loc[df['con_flag'] == 1]
        dfdict['con'] = df5      

        
        
        
        

    keylist = [*dfdict]

    def carbrepfull(df, name, dev, gridcode, field):
        if dev in devlist:
            if name == 'base':
            
                td = df[['LC2030_'+dev, 'LC2014', 'gridcode14', 'gridcode30_' + dev]]
            elif name == 'trt':
                td = df[['LC2030_trt_'+dev, 'LC2014', 'gridcode14', 'gridcode30_trt_' + dev]]
            else:
                td = df[['LC2030_bau', 'LC2030_trt_bau', 'LC2014', 'gridcode14', 'gridcode30_bau', 'gridcode30_trt_bau']]
        if name in activitylist:
            td = df[['LC2030_bau', 'LC2030_trt_bau', 'LC2014', 'gridcode14', 'gridcode30_bau', 'gridcode30_trt_bau', name + '_carbred']]
            if name in ['rre','oak']:
                td.loc[(td['LC2030_trt_bau'] == 'Woody Riparian'), 'LC2030_trt_bau'] = td['LC2030_bau']
                td.loc[(td['LC2030_trt_bau'] == 'Oak Conversion'), 'LC2030_trt_bau'] = td['LC2030_bau']
        if name in ['con']:
            td = df[['LC2030_bau', 'LC2030_trt_bau', 'LC2014', 'gridcode14', 'gridcode30_bau', 'gridcode30_trt_bau']]
        if 'ac' in name:
            td = df[['LC2030_bau', 'LC2030_trt_bau','gridcode30_bau', 'gridcode30_trt_bau']]
        
        c30 = pd.read_csv(carb30)
        c14 = pd.read_csv(carb14)
        Helpers.pmes(td.dtypes)
        if name == 'base':
            temp = pd.merge(td,c30, how = 'left', left_on = 'gridcode30_'+ dev, right_on = 'gridcode30')
            lct = temp.groupby(['LC2030_'+ dev], as_index = False).sum()

            lct = lct[['LC2030_'+ dev, 'carbrate30']]
            lct = lct.rename(columns = {'LC2030_'+ dev:'landcover','carbrate30':'carbon_' + name +'_'+ dev})
            intdict[name +'_'+ dev] = lct
            
        elif name == 'trt':
            temp = pd.merge(td,c30, how = 'left', left_on = 'gridcode30_trt_'+ dev, right_on ='gridcode30' )
            lct = temp.groupby(['LC2030_trt_'+ dev], as_index = False).sum()
            lct = lct[['LC2030_trt_'+ dev, 'carbrate30']]
            lct = lct.rename(columns = {'LC2030_trt_'+ dev:'landcover','carbrate30':'carbon_' + name +'_'+ dev})
            intdict[name +'_'+ dev] = lct



        elif name in activitylist:
            lct = td.groupby(['LC2030_trt_bau'], as_index = False).sum()
            lct = lct[['LC2030_trt_bau', name + '_carbred']]
            lct = lct.rename(columns = {'LC2030_trt_bau':'landcover',name + '_carbred':'carbon_' + name}) 
            intdict[name] = lct
        
        elif name in ['con']:
            temp14 = pd.merge(td,c14, how = 'left', left_on = 'gridcode14', right_on = 'gridcode14')
            temp30 = pd.merge(td,c30, how = 'left', left_on = 'gridcode30_trt_bau', right_on = 'gridcode30')

            lct14 = temp14.groupby(['LC2014'], as_index = False).sum()
            lct30 = temp30.groupby(['LC2030_trt_bau'], as_index = False).sum()
            lct = pd.merge(lct30,lct14, left_on ='LC2030_trt_bau', right_on = 'LC2014', how = 'outer')
            lct['carbrate14'].fillna(0)
            lct['conchange'] = lct['carbrate14'] - lct['carbrate30']
            lct = lct[['LC2030_trt_bau', 'conchange']]
            
            lct = lct.rename(columns = {'LC2030_trt_bau':'landcover','conchange':'carbon_change_' + name}) 
            intdict[name] = lct
        elif 'ac' in name:
            temp30_bau = pd.merge(td,c30, how = 'left', left_on = 'gridcode30_bau', right_on = 'gridcode30')
            temp30_trt = pd.merge(td,c30, how = 'left', left_on = 'gridcode30_trt_bau', right_on = 'gridcode30')

            lct30_bau = temp30_bau.groupby(['LC2030_bau'], as_index = False).sum()
            lct30_trt = temp30_trt.groupby(['LC2030_trt_bau'], as_index = False).sum()
            lct30_bau = lct30_bau.rename(columns = {'carbrate30':'sumbase'})
            lct30_trt = lct30_trt.rename(columns = {'carbrate30':'sumtrt'})
            lct = pd.merge(lct30_bau,lct30_trt, left_on ='LC2030_bau', right_on = 'LC2030_trt_bau', how = 'outer')
            lct['sumbase'].fillna(0)
            lct['sumtrt'].fillna(0)
            lct.loc[(lct['LC2030_bau'] == 0), 'sumbase'] = lct['sumbase'].sum()
            temp = lct.loc[lct['sumtrt'] > 0]
            temp['change'] = temp['sumtrt'] - temp['sumbase']
            temp = temp[['LC2030_trt_bau', 'change']]
            
            temp = temp.rename(columns = {'LC2030_trt_bau':'landcover','change':'carbon_avoided_' + name}) 
            intdict[name] = temp
            
            
    intdict= {}
    for i in keylist:
        
        
        if i in ['base', 'trt', 'dev', 'con']:
            if i == 'base':
                for x in devlist:
                    carbrepfull(dfdict[i],i, x, 'gridcode30_' + x, 'LC2030_' + x)
            else:
                for x in devlist:
                    carbrepfull(dfdict[i],i, x, 'gridcode30_trt_' + x, 'LC2030_trt_' + x)
            
        else:
            carbrepfull(dfdict[i],i, 'bau', 'gridcode30_trt_bau', 'LC2030_trt_bau')
            
    c14 = pd.read_csv(carb14)
    
    def do2014(df, c14):
        td = df[['LC2014', 'gridcode14']]
        temp = pd.merge(td,c14, how = 'left', on = 'gridcode14')
        lct = temp.groupby(['LC2014'], as_index = False).sum()
        return lct
    lct = do2014(df, c14)
    lct.to_csv('E:/Temp/carbon14.csv')
      
    lct = lct[['LC2014', 'carbrate14']]
    lct = lct.rename(columns = {'LC2014':'landcover','carbrate14':'carbon2014'})
    intdict['Carbon2014'] = lct

    tlist = list(intdict.values())
    l = len(tlist)
    count = 1
    temp = tlist[0]
    Helpers.pmes(tlist)
    Helpers.pmes('Combining Dataframes')
#    for i in tlist:
#        i.to_csv(outpath+str(i)+'.csv')
    while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
    temp.fillna(0)
    temp.to_csv(outpath+'carbon.csv')  
    
    
    
    
    
    
    
    
    