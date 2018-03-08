# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 08:58:23 2018

@author: Dylan
"""


#def report(outpath, df):
def report(df, outpath,aca = 0, acu = 0, oak = 0, rre = 0, cd = 0 , cm = 0):
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
    if aca == 1:
        df6 = df.loc[df['aca_flag'] == 1]
        dfdict['aca'] = df6      
    if acu == 1:
        df7 = df.loc[df['acu_flag'] == 1]
        dfdict['acu'] = df7         
    
    if cd ==1:
        devlist = ['bau','med','max', 'cust']
    else:
        devlist = ['bau','med','max']
    keylist = [*dfdict]

    def fmmp(df, outpath):
        aglist = ['Orchard','Annual Cropland','Vineyard', 'Rice', 'Irrigated Pasture']
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
            group = group.rename(columns = {'pointid':'ha_loss_' + name + '_' + dev})
#            if name in ['aca','acu']:
            
            fmmpdict[name + dev] = group

        fmmpdict = {}
        for x in keylist:
            
            
            if x in ['base', 'dev','con', 'trt']:
                if x == 'base':
                    for i in devlist:
                        ffunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        ffunct(x, 'LC2030_trt_' + i, i, dfdict[x])
        
#        if 'acu' in fmmpdict:
#            ffunct('acu', 'LC2030_ac', 'bau',dfdict['acu'])
#        if 'aca' in fmmpdict:
#            ffunct('aca', 'LC2030_ac', 'bau',dfdict['aca'])
                
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
        temp.to_csv(outpath + 'fmmp.csv')
        
            

    
    def fema(df, outpath):
        
        
        
        flist = [100,500]
        gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
        def femafunct(name, field,query, dev, df):

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
                if dev in ['base','trt']:
                    tempmerge = tempmerge.rename(columns = {'count30':dev+'30', 'count14':dev+'14'})
                    tempmerge[dev+'30'] = (tempmerge[dev+'30']*900)/10000
                    tempmerge[dev+'14'] = (tempmerge[dev+'14']*900)/10000
                else:
                    tempmerge = tempmerge[['gen_class', 'change']]
                tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name+ '_'+dev})
                femadict[name + dev] = tempmerge
                
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
                            femafunct(x, 'LC2030_' + i, query, i, dfdict[x])
                    else:
                        for i in devlist:
                            femafunct(x, 'LC2030_trt_' + i, query, i, dfdict[x])
                elif x in ['acu', 'aca']:
#                    femafunct(x, 'LC2030_ac',query, 'bau',dfdict[x])
                    pass
                else:
                    femafunct(x, 'LC2030_trt_bau', query, 'bau', dfdict[x])
            tlist = list(femadict.values())
            l = len(tlist)
            count = 1
            temp = tlist[0]
            while count < l:
                temp = pd.merge(temp,tlist[count],on = 'gen_class', how = 'outer' )
                count = count + 1
            temp.to_csv(outpath + 'fema' + str(z) + '.csv')
                    
    
    def scenic(df, outpath):
        #6-56
        
        
        
        gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
        def scenicfunct(name, field, dev , df):        
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
                if dev in ['base','trt']:
                    tempmerge = tempmerge.rename(columns = {'count30':dev+'30', 'count14':dev+'14'})
                    tempmerge[dev+'30'] = (tempmerge[dev+'30']*900)/10000
                    tempmerge[dev+'14'] = (tempmerge[dev+'14']*900)/10000
                else:
                    tempmerge = tempmerge[['gen_class', 'change']]
                tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name +'_'+ dev})
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
            elif x in ['acu', 'aca']:
#                    scenicfunct(x, 'LC2030_ac', 'bau',dfdict[x])
                    pass
            else:
                scenicfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
        tlist = list(scendict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
                temp = pd.merge(temp,tlist[count],on = 'gen_class', how = 'outer' )
                count = count + 1
        temp.to_csv(outpath + 'scenic' + '.csv')

    

    def wateruse(df, outpath):


        wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_wateruse.csv")
        def watfunct(name, field, dev , df):       
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
            if dev in ['base','trt']:
                    tempmerge = tempmerge.rename(columns = {'water30':dev+'30', 'water14':dev+'14'})
                    tempmerge[dev+'30'] = (tempmerge[dev+'30']*900)/10000
                    tempmerge[dev+'14'] = (tempmerge[dev+'14']*900)/10000
            else:
                tempmerge = tempmerge[['LC2014', 'change']]
            tempmerge = tempmerge.rename(columns = {'LC2014':'landcover','change':'ac_ft_change' + name +'_'+ dev})
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
            elif x in ['acu', 'aca']:
#                    watfunct(x, 'LC2030_ac', 'bau',dfdict[x]) 
                    pass                       
            else:
                watfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
        tlist = list(watdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
                temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
                count = count + 1
        
        temp.to_csv(outpath+'waterdemand.csv')
    
    def lcchange(df, outpath):
        
        def lcfunct(name, field, dev, df): 
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
            tempmerge['change'] = (tempmerge['change']*900)/10000
            if dev in ['base','trt']:
                tempmerge = tempmerge.rename(columns = {'count30':dev+'30', 'count14':dev+'14'})
                tempmerge[dev+'30'] = (tempmerge[dev+'30']*900)/10000
                tempmerge[dev+'14'] = (tempmerge[dev+'14']*900)/10000
            else:
                tempmerge = tempmerge[['index1', 'change']]
            tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'ha_change_' + name +'_'+ dev})
            lcdict[name + dev] = tempmerge
        lcdict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        lcfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
#                        lcfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
                        pass
            elif x in ['acu', 'aca']:
#                    lcfunct(x, 'LC2030_ac', 'bau',dfdict[x])   
                    pass                        
            else:
                lcfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
        tlist = list(lcdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
                temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
                count = count + 1
        
        temp.to_csv(outpath+'cover_change.csv')    
    
    def pcalcchange(df, outpath):
        
        def pcafunct(name, field, dev, df): 

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
            if dev in ['base','trt']:
                tempmerge = tempmerge.rename(columns = {'count30':dev+'30', 'count14':dev+'14'})
                tempmerge[dev+'30'] = (tempmerge[dev+'30']*900)/10000
                tempmerge[dev+'14'] = (tempmerge[dev+'14']*900)/10000
            else:
                tempmerge = tempmerge[['index1', 'change']]
            tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'ha_change_' + name +'_'+ dev})
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
            elif x in ['acu', 'aca']:
#                    pcafunct(x, 'LC2030_ac', 'bau',dfdict[x])      
                    pass                        
            else:
                pcafunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
        tlist = list(pcadict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
                temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
                count = count + 1
        
        temp.to_csv(outpath+'pca_cover_change.csv')       
    def aqua(df, outpath):

        gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
        
        def aquahabfunct(name, field, dev , df):        
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
                if dev in ['base','trt']:
                    tempmerge = tempmerge.rename(columns = {'count30':dev+'30', 'count14':dev+'14'})
                    tempmerge[dev+'30'] = (tempmerge[dev+'30']*900)/10000
                    tempmerge[dev+'14'] = (tempmerge[dev+'14']*900)/10000
                else:
                    tempmerge = tempmerge[['gen_class', 'change']]
                tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name +'_'+ dev})
                scendict[name + dev] = tempmerge
            
        scendict = {}
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        aquahabfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        aquahabfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
            elif x in ['acu', 'aca']:
#                    aquahabfunct(x, 'LC2030_ac', 'bau',dfdict[x])
                    pass
            else:
                aquahabfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
        tlist = list(scendict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
                temp = pd.merge(temp,tlist[count],on = 'gen_class', how = 'outer' )
                count = count + 1
        temp.to_csv(outpath + 'aquatic.csv')
    def termovement(df, outpath):
        
        
        rclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_resistance.csv")
        arealist = ['county','eca']
        def movefunct(name, field, dev, df, area): 
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
            if dev in ['base','trt']:
                tempmerge = tempmerge.rename(columns = {'count30':dev+'30', 'count14':dev+'14'})
                tempmerge[dev+'30'] = (tempmerge[dev+'30']*900)/10000
                tempmerge[dev+'14'] = (tempmerge[dev+'14']*900)/10000
            else:
                tempmerge = tempmerge[['index1', 'change']]
            tempmerge = tempmerge.rename(columns = {'index1':'movement_potential','change':'ha_change_' + name +'_'+ dev})
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
                elif x in ['acu', 'aca']:
#                    movefunct(x, 'LC2030_ac', 'bau',dfdict[x],y)             
                    pass
                else:
                    movefunct(x, 'LC2030_trt_bau', 'bau', dfdict[x], y)
            tlist = list(movedict.values())
            l = len(tlist)
            count = 1
            temp = tlist[0]
            while count < l:
                temp = pd.merge(temp,tlist[count],on = 'movement_potential', how = 'outer' )
                count = count + 1
        
            temp.to_csv(outpath+y+'movement.csv')   
    
    
    def cropvalue(df, outpath):

        wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_crop_value.csv")
        def cropfunct(name, field, dev, df): 
            td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field]]
            
            # do 2014
            tempdf14 = pd.merge(td,wclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('LC2014').sum()
            group14['index1'] = group14.index
            group14 = group14[['crop_val','index1']]
            group14 = group14.rename(columns={'crop_val':'crop14'})
            Helpers.pmes('Crop Value Reporting: ' + name + ', ' + dev)
            
            # do 2030
            tempdf30 = pd.merge(td,wclass, how = 'outer', left_on = field, right_on = 'landcover')
            group30 = tempdf30.groupby(field).sum()
            group30['index1'] = group30.index
            group30 = group30[['crop_val','index1']]
            group30 = group30.rename(columns={'crop_val':'crop30'})
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'outer')
            tempmerge['change'] = tempmerge['crop30']-tempmerge['crop14']
            if dev in ['base','trt', 'con', 'dev', 'acu', 'aca']:
                tempmerge = tempmerge.rename(columns = {'count30':dev+'30', 'count14':dev+'14'})
                tempmerge[dev+'30'] = (tempmerge[dev+'30']*900)/10000
                tempmerge[dev+'14'] = (tempmerge[dev+'14']*900)/10000
            else:
                tempmerge = tempmerge[['index1', 'change']]
            tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'Change in Value' + name +'_'+ dev})
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
            elif x in ['acu', 'aca']:
#                cropfunct(x, 'LC2030_ac', 'bau',dfdict[x])
                pass
            else:
                cropfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
        tlist = list(cropdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
                temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
                count = count + 1
    
        temp.to_csv(outpath+'cropvalue.csv')              
            
    
    def groundwater(df, outpath):
        #6-56
        

        def gwfunct(name, field, dev, df): 
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
            group30 = group30.rename(columns = {'bcm_val':'ac_ft_rec_lst' + name +'_'+ dev})
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
            elif x in ['acu', 'aca']:
#                gwfunct(x, 'LC2030_ac', 'bau',dfdict[x])  
                pass
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
                if dev in ['base','trt']:
                    tempmerge = tempmerge.rename(columns = {y + '30':dev+'30',y+'14':dev+'14'})
                    tempmerge[dev+'30'] = (tempmerge[dev+'30']*900)/10000
                    tempmerge[dev+'14'] = (tempmerge[dev+'14']*900)/10000
                else:
                    tempmerge = tempmerge[['index1', 'change']]
                tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'kgs_nitrate_' + name + '_' + dev})
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
                elif x in ['acu', 'aca']:
#                    nitfunct(x, 'LC2030_ac', 'bau',dfdict[x],y)  
                    pass
                else:
                    nitfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x],y)
            tlist = list(nitdict.values())
            l = len(tlist)
            count = 1
            temp = tlist[0]
            while count < l:
                temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
                count = count + 1
        
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
                    elif (tempripint14 < .7):
                        temp['watint14'] = 'Degraded'
                        tdict[i]['watint14'] =  'Degraded'
                        
                    elif (tempripint14 > .7):
                        temp['watint14'] = 'Natural Catchment'
                        tdict[i]['watint14'] =  'Natural Catchment'                     
                       
#                    else:
#                        temp['watint14'] = 'Degraded'
#                        tdict[i]['watint14'] =  'Degraded'
                    
                #Calculate watershed integrity
                if tempripint30:
#                    Helpers.pmes('riparian is :' + str(tempripint30) + ' AND watershed is :' + str(hucpcent30))
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
#                    else:                
#                        temp['watint30'] = 'Degraded'
#                        tdict[i]['watint30'] =  'Degraded'
                tdf = tdf.append(temp)
            
#            Helpers.pmes(tdict)
            
            temp14 = tdf.groupby(['watint14'], as_index = False).count()
            temp14 = temp14[['pointid','watint14']]
            temp14 = temp14.rename(columns = {'pointid':'count14'})
    
            
            temp30 = tdf.groupby(['watint30'], as_index = False).count()
            temp30 = temp30[['pointid','watint30']]
            temp30 = temp30.rename(columns = {'pointid':'count30'})

            tempmerge = pd.merge(temp14,temp30, left_on = 'watint14',right_on='watint30', how = 'outer')
            
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
#            Helpers.pmes(tempmerge)
            tempmerge['change'] = (tempmerge['change']*900)/10000
            if dev in ['base','trt']:
                tempmerge = tempmerge.rename(columns = {'count30':dev+'30','count14':dev+'14'})
                tempmerge[dev+'30'] = (tempmerge[dev+'30']*900)/10000
                tempmerge[dev+'14'] = (tempmerge[dev+'14']*900)/10000
            else:
                tempmerge = tempmerge[['watint14', 'change']]
            tempmerge = tempmerge.rename(columns = {'watint14':'Integrity_Class','change':'ha_change_' + name +'_'+ dev})
            intdict[name + dev] = tempmerge
            import pandas as pd
            tempo = pd.DataFrame([tdict])
            tempo.to_csv(outpath+dev+name+'watint.csv')

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
    
    
    
def carbreport(df, outpath,activitylist,carb14, carb30,aca = 0, acu = 0, cd = 0 , cm = 0):
    import pandas as pd
    import Helpers
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    dfdict = {}
    dfdict['base'] = df
    dfdict['trt'] = df
    if cd ==1:
        devlist = ['bau','med','max', 'cust']
    else:
        devlist = ['bau','med','max']
    
    for i in activitylist:
        df9 = df.loc[(df[i+'selected'] == 1)]
        dfdict[i] = df9

    if cd == 1:
        df4 = df.loc[df['dev_flag'] == 1]
        dfdict['dev'] = df4      
    if cm == 1:
        df5 = df.loc[df['con_flag'] == 1]
        dfdict['con'] = df5      
    if aca == 1:
        df6 = df.loc[df['aca_flag'] == 1]
        dfdict['aca'] = df6      
    if acu == 1:
        df7 = df.loc[df['acu_flag'] == 1]
        dfdict['acu'] = df7
        
        
        
        

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
        
        
        c30 = pd.read_csv(carb30)
        Helpers.pmes(td.dtypes)
        if name == 'base':
            temp = pd.merge(td,c30, how = 'left', left_on = 'gridcode30_'+ dev, right_on = 'gridcode30')
            lct = temp.groupby(['LC2030_'+ dev], as_index = False).sum()

            lct = lct[['LC2030_'+ dev, 'carbrate_30']]
            lct = lct.rename(columns = {'LC2030_'+ dev:'landcover','carbrate_30':'carbon_' + name +'_'+ dev})
            intdict[name +'_'+ dev] = lct
        elif name == 'trt':
            temp = pd.merge(td,c30, how = 'left', left_on = 'gridcode30_trt_'+ dev, right_on ='gridcode30' )
            lct = temp.groupby(['LC2030_trt_'+ dev], as_index = False).sum()
            lct = lct[['LC2030_trt_'+ dev, 'carbrate_30']]
            lct = lct.rename(columns = {'LC2030_trt_'+ dev:'landcover','carbrate_30':'carbon_' + name +'_'+ dev})
            intdict[name +'_'+ dev] = lct

        elif name in activitylist:
            lct = td.groupby(['LC2030_trt_bau'], as_index = False).sum()
            lct = lct[['LC2030_trt_bau', name + '_carbred']]
            lct = lct.rename(columns = {'LC2030_trt_bau':'landcover',name + '_carbred':'carbon_' + name}) 
            intdict[name +'_'+ dev] = lct
#            elif name in ['aca', 'acu']:
#                
#                lct = td.loc[td[name + '_flag'] == 1]
        else:
#            lct = td[['LC2030_bau']]
#            lct = lct.groupby(['LC2030_bau'])
#            lct = lct.rename(columns= {'LC2030_bau':'landcover'})
#            intdict[name +'_'+ dev] = lct     
            pass
#                lct = lct[['LC2030_trt_bau', 'gridcode30_trt_bau', 'gridcode14']]
#                temp = pd.merge(lct,c30, how = 'left', left_on = 'gridcode30_trt_bau', right_on = 'gridcode30_bau')
#                temp['gridcode14'] = temp['gridcode14'] + 100
#                temp = pd.merge(temp,c30, how = 'left', left_on = 'gridcode14', right_on = 'gridcode30_bau')
#                temp = temp.groupby(['LC2030_trt_bau'], as_index = False).sum()
#                temp[name + '_avoided'] = temp['carbrate_14'] - temp['carbrate_30']
#                temp = temp[[name + '_avoided', 'LC2030_trt_bau']]
#                lct = lct.rename(columns = {'LC2030_trt_bau':'landcover'}) 
                
                
#            elif name in ['con', 'dev']:

        
#        lct.to_csv(outpath+name +'_'+ dev + '.csv')  
    
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

    temp.to_csv(outpath+'carbon.csv')  
    
    
    
    
    
    
    
    
    