# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 08:58:23 2018

@author: Dylan
"""






#def report(outpath, df):
def report(df, outpath, acdict = 'None', oak = 0, rre = 0, cd = 0 , cm = 0):
    
    """
    This function reports on the multi-benefits. 
    There are a number of sub-functions which create csv reports for each multi-benefit.
    
    Arguments:
    df: The dataframe from main program
    outpath: The path specified in the tool gui for the outputs to go
    acdict: avoided conversion dictionary, only created if avoided conversion activities are selected
    oak: 1 or 0 flag for oak conversion activity
    rre: 1 or 0 flag for riparian restoration activity
    cd: 0, 1 or 2 flag for if a custom development mask was used
    cm: 1 or 0 flag for if a consermation mask was used    
    """
    
    #Create a full list of all basic landcovers (not young shrubland, young forest, oak conversion or riparian restoration)
    lclist = ['Orchard','Annual Cropland','Vineyard', 'Rice', 'Irrigated Pasture','Forest', 'Shrubland', 'Wetland', 'Barren', 'Water','Developed','Urban','Developed Roads', 'Grassland']
    import pandas as pd
    import Helpers
    
    
    #create an empty dataframe with only landcovers, used for outer joins in functions
    lc = pd.DataFrame({'landcover':lclist})
    

    # remove unnamed fields from the dtasrame
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # create individual dataframes for each activity and scenario
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
    if cd == 2:
        df2 = df.loc[(df['dev_flag'] == 1)]
        dfdict['dev_flagged'] = df2
        Helpers.pmes('Developed Added to Reporting List')
    
        
    #Create avoided conversion dataframes if they were selected
    if acdict != 'None':
        aclist = [*acdict]
        for i in aclist:
            df2 = df.loc[(df[i+'selected'] == 1)]
            dfdict[i] = df2
    keylist = [*dfdict]





    def fmmp(df, outpath):
        """
        This function reports on Prime, Unique, Local Importance and Statewide Importance farmland classes.
        When a pixel of natural or farmland in one of those classes was converted to a developed landcover, it was reported as a loss.
        
        
        """
        #Create a list of ag/natural landcover and one of developed landcovers. Also a list of FMMP classes we will be reporting on
        aglist = ['Orchard','Annual Cropland','Vineyard', 'Rice', 'Irrigated Pasture','Forest', 'Shrubland', 'Wetland', 'Barren', 'Water', 'Grassland']
        developed = ['Developed','Urban','Developed Roads']
        flist = ['P','U','L', 'S']
        
        def ffunct (name, field, dev, df):
            
            #Create a smaller dataframe with just the required fields
            td = df[['LC2014','pointid', 'fmmp_class', field]]
            
            #Change landcover classes to match 2014 landcover classes, for reporting
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'  
            if field == 'LC2030_bau':
                td.loc[(td['LC2030_bau'] == 'Young Forest'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), field] = 'Forest'
            
            #Perform the queries, find the pixels that are natural or ag in 2014 and developed in the 2030 scenario, and are in the FMMP reporting classes
            Helpers.pmes('FMMP Reporting: ' + name + ', ' + dev)
            tempdf = td.loc[(td['LC2014'].isin(aglist))]
            tempdf = tempdf.loc[(tempdf[field].isin(developed))]
            tempdf = tempdf.loc[(tempdf['fmmp_class'].isin(flist))]
            
            #Group the rows by fmmp class in order to calculate acreage
            group = tempdf.groupby('fmmp_class', as_index = False).count()
            group = group[['fmmp_class','pointid']]
            group['pointid'] = (group['pointid']*900)/10000
            
            #If avoided conversion is being reporting, label the reporting columns differently
            if 'urb' in name:
                group['pointid'] = group['pointid']* (-1)
                group = group.rename(columns = {'pointid':'ha_loss_avoided_' + name})
                group['ha_loss_avoided_' + name].fillna(0)
            else:
                group = group.rename(columns = {'pointid':'ha_loss_' + name + '_' + dev})
                group['ha_loss_' + name + '_' + dev].fillna(0)
            # add the dataframe to the reporting dictionary
            fmmpdict[name + dev] = group
        #Create an empty dictionary to hold the reporting dataframes
        fmmpdict = {}
        
        #loop through scenarios and activities and run the reporting function
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
            elif ('dev_flag' in x):
                ffunct(x, 'LC2030_trt_bau', i, dfdict[x])
                
        #Report the baseline in 2014
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
        
        #Merge the reporting dataframes into one dataframe for exporting
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'fmmp_class', how = 'outer' )
            count = count + 1
        #Change the FMMP Class label to a full phrase
        temp.loc[temp['fmmp_class'] == 'P', 'fmmp_class' ] = 'Prime Farmland' 
        temp.loc[temp['fmmp_class'] == 'L', 'fmmp_class' ] = 'Local Importance' 
        temp.loc[temp['fmmp_class'] == 'S', 'fmmp_class' ] = 'Statewide Importance' 
        temp.loc[temp['fmmp_class'] == 'U', 'fmmp_class' ] = 'Unique Farmland' 
        
        #Fill nulls
        temp.fillna(0,inplace=True)
        
        #Export to output folder
        temp.to_csv(outpath + 'fmmp.csv')

    
    def fema(df, outpath):
        """
        This function reports on landcover change in 100 and 500 year floodplains.        
        
        """
        
        flist = [100,500]
        gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
        def femafunct(name, field,query, dev, df):
            
            #Change landcovers to reporting landcovers
            if x in ['base', 'dev','cons', 'trt']:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','fema_class', 'near_fema', field]]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','fema_class', 'near_fema', field, 'LC2030_bau']]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Forest'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), field] = 'Forest'
            
            
            Helpers.pmes('FEMA Reporting: ' + name + ', ' + dev)
            # Create a landcover acreage dataframe for 2014
            tempdf14 = td.loc[(td['fema_class'].isin(query)) & (td['near_fema'] == 0)]
            tempdf14 = pd.merge(gclass,tempdf14, how = 'outer', left_on = 'landcover', right_on = 'LC2014')
            group14 = tempdf14.groupby(['gen_class'], as_index = False).count()
            group14 = group14[['pointid','gen_class']]
            group14 = group14.rename(columns={'pointid':'count14'})
 
            # Create a landcover acreage dataframe for 2030
            tempdf30 = td.loc[(td['fema_class'].isin(query)) & (td['near_fema'] == 0)]
            tempdf30 = pd.merge(gclass,tempdf30, how = 'outer', left_on = 'landcover', right_on = field)
            group30 = tempdf30.groupby(['gen_class'], as_index = False).count()
            group30 = group30[['pointid','gen_class']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            
            #Check if there are rows (might not be any land in the floodplain if a custom processing extent was used outside of it.)
            if len(group30.index) == 0 | len(group14.index) == 0:
                Helpers.pmes('Empty rows in ' + dev)
            else:
                #Create a change field
                tempmerge = pd.merge(group14,group30, on = 'gen_class', how = 'outer')
                tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
                tempmerge['change'] = tempmerge['change']*.09
                
                if name in ['base','trt']:
                    #Finish cleaning up the dataframe for baseline and treatment scenarios
                    tempmerge = tempmerge[['gen_class', 'change','count30']]
                    tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                    tempmerge['ha_' + name+ '_'+dev] = tempmerge['ha_' + name+ '_'+dev]*.09
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name+ '_'+dev})
                    tempmerge['ha_change_' + name+ '_'+dev].fillna(0)
                else:
                    #If the scenario is not baseline or treatment, create a change raster from 2030 baseline bau to 2030 treatment bau
                    tempdf302 = td.loc[(td['fema_class'].isin(query)) & (td['near_fema'] == 0)]
                    tempdf302 = pd.merge(gclass,tempdf302, how = 'outer', left_on = 'landcover', right_on = 'LC2030_bau')
                    group302 = tempdf302.groupby(['gen_class'], as_index = False).count()
                    group302 = group302[['pointid','gen_class']]
                    group302 = group302.rename(columns={'pointid':'count302'})
                    
                    #merge the 2030 tables on general class
                    tempmerge = pd.merge(group302,group30, left_on = 'gen_class',right_on = 'gen_class', how = 'outer')
                    
                    tempmerge['count30'].fillna(0, inplace = True)
                    tempmerge['count302'].fillna(0, inplace = True)
                    
                    #Clean up the dataframe and add to the dataframe list
                    tempmerge = pd.merge(group302,group30, on = 'gen_class', how = 'outer')
                    tempmerge.fillna(0, inplace = True)
                    tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                    tempmerge['change'] = tempmerge['change']*.09
                    tempmerge = tempmerge[['change','gen_class']]
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name})

                femadict[name + dev] = tempmerge
        
        # run the function for each scenario in the list, and run each scenario twice, once for 100 and once for 500
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

                else:
                    femafunct(x, 'LC2030_trt_bau', query, 'bau', dfdict[x])
                    
            #Add 2014 Baseline
            td = df[['LC2014','pointid','fema_class', 'near_fema']]
            tempdf14 = td.loc[(td['fema_class'].isin(query)) & (td['near_fema'] == 0)]
            tempdf14 = pd.merge(tempdf14,gclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby(['gen_class'], as_index = False).count()
            group14 = group14[['pointid','gen_class']]
            group14 = group14.rename(columns={'pointid':'ha_2014'})
            group14['ha_2014'] = group14['ha_2014']*.09
            femadict['Base_2014'] = group14
            tlist = list(femadict.values())
            l = len(tlist)
            count = 1
            temp = tlist[0]
            
            #Loop through dataframes to create one dataframe for export
            while count < l:
                temp = pd.merge(temp,tlist[count],on = 'gen_class', how = 'outer' )
                count = count + 1
            temp.fillna(0,inplace = False)
            #Export dataframe to output folder
            temp.to_csv(outpath + 'flood' + str(z) + '.csv')
                    
    
    def scenic(df, outpath):
        """
        This function reports on landcover change within the most visible quintile of land in Merced County. This is 1/5 of Merced County that is the most visible from roads/towns/parks.
        """

        gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
        def scenicfunct(name, field, dev , df):        
            
            #Change the landcovers to reporting landcovers
            if name in ['base', 'trt']:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','scenic_val', field]]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','scenic_val', field, 'LC2030_bau']]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Forest'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), field] = 'Forest'
            
            
            Helpers.pmes('Scenic Reporting: ' + name + ', ' + dev)
            
            # Calculate landcover in 2014 (Generalized Classes)
            tempdf14 = td.loc[td['scenic_val'] > 5]
            tempdf14 = pd.merge(gclass,tempdf14, how = 'outer', left_on = 'landcover', right_on = 'LC2014')
            group14 = tempdf14.groupby('gen_class', as_index = False).count()
            group14 = group14[['pointid','gen_class']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # Calculate the landcover in 2014 (Generalized Classes)
            tempdf30 = td.loc[td['scenic_val'] > 5]
            tempdf30 = pd.merge(gclass,tempdf30, how = 'outer', left_on = 'landcover', right_on = field)
            group30 = tempdf30.groupby('gen_class', as_index = False).count()
            group30 = group30[['pointid','gen_class']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            if len(group30.index) == 0 | len(group14.index) == 0:
                Helpers.pmes('Empty rows in ' + i)
                
            else:
                #Merge the 2030 and 2014 general landcovers and create change values
                tempmerge = pd.merge(group14,group30, on = 'gen_class', how = 'outer')
                tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
                tempmerge['change'] = (tempmerge['change']*900)/10000
                if name in ['base','trt']:
                    tempmerge = tempmerge[['gen_class', 'change','count30']]
                    tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                    tempmerge['ha_' + name +'_'+ dev] = (tempmerge['ha_' + name +'_'+ dev]*900)/10000
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name +'_'+ dev})
                else:
                    #If the scenario is not trt or baseline, do this section instead to compare 2030 base to 2030 treatment
                    tempdf302 = td.loc[td['scenic_val'] > 5]
                    tempdf302 = pd.merge(gclass,tempdf302, how = 'outer', left_on = 'landcover', right_on = 'LC2030_bau')
                    group302 = tempdf302.groupby(['gen_class'], as_index = False).count()
                    group302 = group302[['pointid','gen_class']]
                    group302 = group302.rename(columns={'pointid':'count302'})
                    #Merge 2030 bau and 2030 trt
                    tempmerge = pd.merge(group302,group30, left_on = 'gen_class',right_on = 'gen_class', how = 'outer')
                    
                    #Calculate the change and update field names
                    tempmerge['count30'].fillna(0, inplace = True)
                    tempmerge['count302'].fillna(0, inplace = True)
                    tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                    tempmerge['change'] = (tempmerge['change']*900)/10000
                    tempmerge = tempmerge[['change','gen_class']]
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name})
                #Add the dataframe to the list of dataframes to merge and export at the end of the function
                scendict[name + dev] = tempmerge
        #Create empty holding dictionary
        scendict = {}
        
        # Loop through the scenarios and run the function
        for x in keylist:
            if x in ['base', 'trt']:
                if x == 'base':
                    for i in devlist:
                        scenicfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        scenicfunct(x, 'LC2030_trt_' + i, i, dfdict[x])

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
        
        #Loop through the dataframes created and merge into one data frame
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'gen_class', how = 'outer' )
            count = count + 1
        #Fill nulls and export the merged dataframes as a csv
        temp = temp.fillna(0)
        temp.to_csv(outpath + 'scenic' + '.csv')

    

    def wateruse(df, outpath):
        """
        This function reports on changes in water demand based on landcover change.
        Reported in acre feet (total)        
        
        """
        #Read in the water demand look up table
        wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_wateruse.csv")
        
        
        def watfunct(name, field, dev , df):      
            """
            This function is run for each scenario. It takes the scenario name, landcover field, development type (if applicable) and the dataframe.
            """
            
            #Change landcover values for reporting classes
            if name in ['base', 'trt']:
                td = df[['LC2014','pointid', field]]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'

            else:
                td = df[['LC2014','pointid', field, 'LC2030_bau']]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Forest'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), 'LC2030_bau'] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), 'LC2030_bau'] = 'Forest'
                
            Helpers.pmes('Water Conservation Reporting: ' + name + ', ' + dev)
            # Calculate the 2014 water use by landcover class
            tempdf14 = pd.merge(td,wclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('LC2014', as_index = False).sum()
            group14 = group14[['wat_val','LC2014']]
            group14 = group14.rename(columns={'wat_val':'water14'})

            # Calculate the 2030 water use by class
            tempdf30 = pd.merge(td,wclass, how = 'left', left_on = field, right_on = 'landcover')
            group30 = tempdf30.groupby(field, as_index = False).sum()
            group30 = group30[[field,'wat_val']]
            group30 = group30.rename(columns={'wat_val':'water30'})
            
            #Merge the dataframes and create a water use change field (2014 - 2030)
            tempmerge = pd.merge(group14,group30, left_on = 'LC2014', right_on= field, how = 'outer')
            tempmerge['change'] = tempmerge['water30']-tempmerge['water14']
            if name in ['base','trt']:
                tempmerge = tempmerge[['LC2014', 'change', 'water30']]
                tempmerge = tempmerge.rename(columns = {'water30':'ac_ft_' + name +'_'+ dev})
                tempmerge['ac_ft_' + name +'_'+ dev] = tempmerge['ac_ft_' + name +'_'+ dev]*4.49651111111
                tempmerge['change'] = tempmerge['change']*4.49651111111
                tempmerge = tempmerge.rename(columns = {'LC2014':'landcover','change':'ac_ft_change_' + name +'_'+ dev})
                
                #If the scenario is not a development scenario, do this section instead to find the change from 2030 baseline to 2030 treatment BAU
            else:
                tempdf302 = pd.merge(td,wclass, how = 'left', left_on = 'LC2030_bau', right_on = 'landcover')
                group302 = tempdf302.groupby(['LC2030_bau'], as_index = False).sum()
                group302 = group302[['LC2030_bau','wat_val']]
                group302 = group302.rename(columns={'wat_val':'water302'})
                
                group302 = pd.merge(lc,group302, left_on = 'landcover', right_on = 'LC2030_bau', how = 'outer')
                tempmerge = pd.merge(group302,group30, left_on = 'landcover',right_on = 'LC2030_trt_bau', how = 'outer')
                
                tempmerge['water302'].fillna(0, inplace = True)
                tempmerge['water30'].fillna(0, inplace = True)
                
                tempmerge['change'] = tempmerge['water30']-tempmerge['water302']
                tempmerge['change'] = tempmerge['change']*4.49651111111
                tempmerge = tempmerge[['change','landcover']]
                tempmerge = tempmerge.rename(columns = {'change':'ac_ft_change_' + name})
            #Add the datafrme to the dataframes dictionary
            watdict[name + dev] = tempmerge
        
        #Create an empty dictionary to hold the dataframes created
        watdict = {}
        
        #Loop through all of the scenarios and create dataframes
        for x in keylist:
            if x in ['base', 'trt']:
                if x == 'base':
                    for i in devlist:
                        watfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        watfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
            else:
                watfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
                
        #Make a baseline report for 2014
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
        
        #Loop through the dataframes and merge them into one dataframe
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
        temp = temp.fillna(0)
        temp = temp.loc[temp['landcover'] != 0]
        
        #Export the merged dataframe
        temp.to_csv(outpath+'watcon.csv')
        
    def lcchange(df, outpath):
        """
        This function reports on landcover change at the county scale
        
        """
        def lcfunct(name, field, dev, df): 
            """
            
            
            """
            
            if x in ['base', 'trt']:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field]]

            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field, 'LC2030_bau']]
                td.loc[(td['LC2030_bau'] == 'Young Forest'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), 'LC2030_bau'] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), 'LC2030_bau'] = 'Forest'
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            
            Helpers.pmes('Land Cover Change Reporting: ' + name + ', ' + dev)

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
            else:
                group302 = td.groupby(['LC2030_bau'], as_index = False).count()
                group302 = group302[['LC2030_bau','pointid']]
                group302 = group302.rename(columns={'pointid':'count302'})
                group302 = pd.merge(lc,group302, left_on = 'landcover', right_on = 'LC2030_bau', how = 'outer')
                tempmerge = pd.merge(group302,group30, left_on = 'landcover',right_on = 'index1', how = 'outer')
                tempmerge['count302'].fillna(0, inplace = True)
                tempmerge['count30'].fillna(0, inplace = True)
                tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                tempmerge['change'] = tempmerge['change']*.09
                tempmerge = tempmerge[['change','landcover']]
                tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name})

            
            lcdict[name + dev] = tempmerge
        lcdict = {}
        for x in keylist:
            if x in ['base','trt']:
                if x == 'base':
                    for i in devlist:
                        lcfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        lcfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
                    
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
        temp.fillna(0, inplace = True)
        temp.to_csv(outpath+'lcchange.csv')    
    
    def pcalcchange(df, outpath):
        
        def pcafunct(name, field, dev, df): 

            if name in ['base', 'trt']:

                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','pca_val', field]]

            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','pca_val', field, 'LC2030_bau']]
                td.loc[(td['LC2030_bau'] == 'Young Forest'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), 'LC2030_bau'] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), 'LC2030_bau'] = 'Forest'
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
                
            else:
                group302 = td.loc[td['pca_val'] == 1]
                group302 = group302.groupby(['LC2030_bau'], as_index = False).count()
                group302 = group302[['LC2030_bau','pointid']]
                group302 = group302.rename(columns={'pointid':'count302'})
                group302 = pd.merge(lc,group302, left_on = 'landcover', right_on = 'LC2030_bau', how = 'outer')
                tempmerge = pd.merge(group302,group30, left_on = 'landcover',right_on = 'index1', how = 'outer')
                tempmerge['count302'].fillna(0, inplace = True)
                tempmerge['count30'].fillna(0, inplace = True)
                tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                tempmerge['change'] = tempmerge['change']*.09
                tempmerge = tempmerge[['change','landcover']]
                tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name})

            pcadict[name + dev] = tempmerge
        pcadict = {}
        for x in keylist:
            if x in ['base', 'trt']:
                if x == 'base':
                    for i in devlist:
                        pcafunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        pcafunct(x, 'LC2030_trt_' + i, i, dfdict[x])
   
                       
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
        temp.fillna(0, inplace = True)
        temp.to_csv(outpath+'pca_cover_change.csv')       
    def aqua(df, outpath):

        gclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_genclass.csv")
        
        def aquahabfunct(name, field, dev , df):        
            
            if name in ['base', 'trt']:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','c_abf75_rnk', field]]
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','c_abf75_rnk', field, 'LC2030_bau']]
                td.loc[(td['LC2030_bau'] == 'Young Forest'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), 'LC2030_bau'] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), 'LC2030_bau'] = 'Forest'
            if field == 'LC2030_trt_' + dev:
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            
            Helpers.pmes('Aquatic Habitat Reporting: ' + name + ', ' + dev)
            
            # do 2014
            tempdf14 = td.loc[td['c_abf75_rnk'] > 0.632275]
            tempdf14 = pd.merge(gclass,tempdf14, how = 'outer', left_on = 'landcover', right_on = 'LC2014')
            group14 = tempdf14.groupby('gen_class', as_index = False).count()
            group14 = group14[['pointid','gen_class']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # do 2030
            tempdf30 = td.loc[td['c_abf75_rnk'] > 0.632275]
            tempdf30 = pd.merge(gclass,tempdf30, how = 'outer', left_on = 'landcover', right_on = field)
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
                else:
                    tempdf302 = td.loc[td['c_abf75_rnk'] > 0.632275]
                    tempdf302 = pd.merge(gclass,tempdf302, how = 'outer', left_on = 'landcover', right_on = 'LC2030_bau')
                    group302 = tempdf302.groupby('gen_class', as_index = False).count()
                    group302 = group302[['pointid','gen_class']]
                    group302 = group302.rename(columns={'pointid':'count302'})
                    
                    tempmerge = pd.merge(group30,group302, on = 'gen_class', how = 'outer')
                    tempmerge['count302'].fillna(0, inplace = True)
                    tempmerge['count30'].fillna(0, inplace = True)
                    tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                    tempmerge['change'] = (tempmerge['change']*900)/10000
                    tempmerge = tempmerge[['change','gen_class']]
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name})

                
                scendict[name + dev] = tempmerge
            
        scendict = {}
        for x in keylist:
            if x in ['base', 'trt']:
                if x == 'base':
                    for i in devlist:
                        aquahabfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        aquahabfunct(x, 'LC2030_trt_' + i, i, dfdict[x])

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
        temp.fillna(0, inplace = True)
        temp.to_csv(outpath + 'aquatic.csv')
    def termovement(df, outpath):
        
        
        rclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_resistance.csv")
        arealist = ['county','eca']
        def movefunct(name, field, dev, df, area): 
            
            
            if name in ['base','trt']:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','eca_val', field]]
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','eca_val', field, 'LC2030_bau']]
                td.loc[(td['LC2030_bau'] == 'Young Forest'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), 'LC2030_bau'] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), 'LC2030_bau'] = 'Forest'
            

            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            if area == 'eca':
                td = td.loc[td['eca_val'] == 1]
            
                
            Helpers.pmes('Terrestrial Resistance Reporting: ' + area + ','+ name + ', ' + dev)
            # do 2014
            tempdf14 = pd.merge(rclass,td, how = 'outer', left_on = 'landcover', right_on = 'LC2014')
            group14 = tempdf14.groupby('res_val', as_index = False).count()
            group14 = group14[['pointid','res_val']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # do 2030
            tempdf30 = pd.merge(rclass,td, how = 'outer', left_on = 'landcover', right_on = field)
            group30 = tempdf30.groupby('res_val', as_index = False).count()

            group30 = group30[['pointid','res_val']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            tempmerge = pd.merge(group14,group30, on = 'res_val', how = 'outer')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = (tempmerge['change']*900)/10000
            if name in ['base','trt']:
                tempmerge = tempmerge[['res_val', 'change','count30']]
                tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                tempmerge['ha_' + name +'_'+ dev] = (tempmerge['ha_' + name +'_'+ dev]*900)/10000
                tempmerge = tempmerge.rename(columns = {'res_val':'movement_potential','change':'ha_change_' + name +'_'+ dev})
            else:
                tempdf302 = pd.merge(rclass,td, how = 'outer', left_on = 'landcover', right_on = 'LC2030_bau')
                group302 = tempdf302.groupby('res_val', as_index = False).count()
                group302 = group302[['pointid','res_val']]
                group302 = group302.rename(columns={'pointid':'count302'})
                
                tempmerge = pd.merge(group30,group302, on = 'res_val', how = 'outer')
                
                tempmerge['count302'].fillna(0, inplace = True)
                tempmerge['count30'].fillna(0, inplace = True)
                tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                tempmerge['change'] = (tempmerge['change']*900)/10000
                tempmerge = tempmerge[['change', 'res_val']]
                tempmerge = tempmerge.rename(columns = {'res_val':'movement_potential','change':'ha_change_' + name})

            movedict[name + dev] = tempmerge
            
        for y in arealist:
               
            movedict = {}
            for x in keylist:
                if x in ['base','trt']:
                    if x == 'base':
                        for i in devlist:
                            movefunct(x, 'LC2030_' + i, i, dfdict[x], y)
                    else:
                        for i in devlist:
                            movefunct(x, 'LC2030_trt_' + i, i, dfdict[x], y)
     

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
            temp.fillna(0, inplace = True)
            temp.to_csv(outpath+y+'movement.csv')   
    
    
    def cropvalue(df, outpath):

        wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_crop_value.csv")
        def cropfunct(name, field, dev, df): 
            
            if x in ['base', 'trt']:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field]]
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field, 'LC2030_bau']]
                td.loc[(td['LC2030_bau'] == 'Young Forest'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), 'LC2030_bau'] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), 'LC2030_bau'] = 'Forest'
            # do 2014
            tempdf14 = pd.merge(wclass,td, how = 'outer', left_on = 'landcover', right_on = 'LC2014')
            group14 = tempdf14.groupby('landcover', as_index = False).sum()
            group14 = group14[['crop_val','landcover']]
            group14 = group14.rename(columns={'crop_val':'crop14'})
            Helpers.pmes('Crop Value Reporting: ' + name + ', ' + dev)
            
            # do 2030
            tempdf30 = pd.merge(wclass,td, how = 'outer', left_on = 'landcover', right_on = field)
            group30 = tempdf30.groupby('landcover', as_index = False).sum()
            group30 = group30[['crop_val','landcover']]
            group30 = group30.rename(columns={'crop_val':'crop30'})
            
            tempmerge = pd.merge(group30,group14, on = 'landcover', how = 'outer')
            tempmerge['change'] = tempmerge['crop30']-tempmerge['crop14']
            if name in ['base','trt']:
                tempmerge = tempmerge[['landcover', 'change','crop30']]
                tempmerge = tempmerge.rename(columns = {'crop30':'usd' + name +'_'+ dev})
                tempmerge = tempmerge.rename(columns = {'change':'usd_change_' + name +'_'+ dev})
            else:
                tempdf302 = pd.merge(wclass,td, how = 'outer', left_on = 'landcover', right_on = 'LC2030_bau')
                group302 = tempdf302.groupby('landcover', as_index = False).sum()
                group302 = group302[['crop_val','landcover']]
                group302 = group302.rename(columns = {'crop_val':'crop302'})
                tempmerge = pd.merge(group30,group302, on = 'landcover', how = 'outer')
                tempmerge['crop302'].fillna(0, inplace = True)
                tempmerge['crop30'].fillna(0, inplace = True)
                tempmerge['change'] = tempmerge['crop30']-tempmerge['crop302']
                tempmerge = tempmerge[['change','landcover']]
                tempmerge = tempmerge.rename(columns = {'change':'usd_change_' + name})

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
 
            else:
                cropfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
        td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
        
        # do 2014
        tempdf14 = pd.merge(wclass,td, how = 'outer', left_on = 'landcover', right_on = 'LC2014')
        group14 = tempdf14.groupby('landcover', as_index = False).sum()
        group14 = group14[['crop_val','landcover']]
        group14 = group14.rename(columns={'crop_val':'cropvalue_usd_2014'})
        group14['cropvalue_usd_2014'] = group14['cropvalue_usd_2014']
        cropdict['Base_2014'] = group14
        tlist = list(cropdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
        temp.fillna(0, inplace = True)
        temp = temp.loc[temp['landcover'].isin(['Annual Cropland','Rice','Orchard','Vineyard','Irrigated Pasture'])]
        temp.to_csv(outpath+'cropvalue.csv')              
            
    
    def groundwater(df, outpath):
        #6-56
        

        def gwfunct(name, field, dev, df): 
            
            if name in ['base', 'trt']:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'bcm_val', field]]
            else:
                td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'bcm_val', field, 'LC2030_trt_bau']]

            
            td['bcm_val'] =  (td['bcm_val']*.0032808) * .222394 #Turn into ac/ft/pixel/year
            
    
            Helpers.pmes('Groundwater Recharge Reporting: ' + name + ', ' + dev)
            # do 2014
            td2 = td.loc[((td[field] != td['LC2014']) & (td[field].isin(['Urban', 'Developed', 'Developed_Roads'])))]
            
            if name in ['base', 'trt']:
                
                group30 = td2.groupby([field], as_index = False).sum()
                group30 = pd.merge(lc,group30, left_on = 'landcover', right_on = field, how = 'outer')
                group30 = group30[['landcover', 'bcm_val']]
                group30 = group30.rename(columns = {'bcm_val':'ac_ft_rec_lst_' + name +'_'+ dev})
                group30['ac_ft_rec_lst_' + name +'_'+ dev].fillna(0, inplace = True)
                gwdict[name + dev] = group30
                
            else:
                group30 = td2.groupby([field], as_index = False).sum()
                group30 = pd.merge(lc,group30, left_on = 'landcover', right_on = 'LC2030_bau', how = 'outer')
                group30 = group30[['landcover', 'bcm_val']]
                group30 = group30.rename(columns = {'bcm_val':'bcm_val_30'})
                group30['bcm_val_30'].fillna(0, inplace = True)
                
                
                group302 = td2.groupby(['LC2030_trt_bau'], as_index = False).sum()
                group302 = pd.merge(lc,group302, left_on = 'landcover', right_on = 'LC2030_trt_bau', how = 'outer')
                group302 = group302[['landcover', 'bcm_val']]
                group302 = group302.rename(columns = {'bcm_val':'bcm_val_302'})
                group302['bcm_val_302'].fillna(0, inplace = True)

                temp = pd.merge(group30,group302, left_on = 'landcover', right_on = 'landcover', how = 'outer')
                temp['change'] = group302['bcm_val_302'] - group30['bcm_val_30']
                temp = temp[['landcover','change']]
                temp = temp.rename(columns = {'change':'ac_ft_rec_avd_' + name})
                gwdict[name] = group30

        gwdict = {}
        for x in keylist:
            if x in ['base', 'trt']:
                if x == 'base':
                    for i in devlist:
                        gwfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        gwfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
                        
            else:
                gwfunct(x, 'LC2030_bau', 'bau', dfdict[x])
        tlist = list(gwdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
        temp.fillna(0,inplace = True)
        temp.to_csv(outpath+'groundwater.csv')       

    def nitrates(df, outpath):
        #6-56

        wclass = pd.read_csv("E:/mercedtool/MASTER_DATA/Tables/LUTables/lut_nitrates.csv")
        xlist = ['runoff','leach']
        
        def nitfunct(name, field, dev, df, y): 
                
                if x in ['base', 'trt']:
                    td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field]]
                else:
                    td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', field, 'LC2030_bau']]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                Helpers.pmes('Nitrate Reporting: ' + y + ',' + name + ', ' + dev)

                # do 2014
                group14 = td.groupby('LC2014', as_index = False).count()
                tempdf14 = pd.merge(wclass,group14, how = 'outer', left_on = 'landcover', right_on = 'LC2014')
#                group14 = tempdf14.groupby('landcover', as_index = False).count()
                
                tempdf14[y+'2'] = tempdf14[y]*tempdf14['pointid']
                group14 = tempdf14[[y+'2','landcover']]
                
                group14 = group14.rename(columns={y+'2':y + '14'})

                # do 2030
                
                group30 = td.groupby(field, as_index = False).count()
                tempdf30 = pd.merge(wclass,group30, how = 'outer', left_on = 'landcover', right_on = field)
#                group14 = tempdf14.groupby('landcover', as_index = False).count()
                
                tempdf30[y+'2'] = tempdf30[y]*tempdf30['pointid']
                group30 = tempdf30[[y+'2','landcover']]
                
                group30 = group30.rename(columns={y+'2':y + '30'})
                
                
                tempmerge = pd.merge(group14,group30, on = 'landcover', how = 'outer')
                tempmerge['change'] = tempmerge[y+'30']-tempmerge[y+'14']
                
                if name in ['base','trt']:
                    tempmerge = tempmerge[['landcover', 'change',y+'30']]
                    tempmerge = tempmerge.rename(columns = {y + '30':'kgs_no3_' + name +'_' + dev })
                    tempmerge = tempmerge.rename(columns = {'change':'kgs_no3_change_' + name + '_' + dev})
                else:
                    
                    group302 = td.groupby('LC2030_bau', as_index = False).count()
                    tempdf302 = pd.merge(wclass,group302, how = 'outer', left_on = 'landcover', right_on = 'LC2030_bau')
                    tempdf302[y+'2'] = tempdf302[y]*tempdf302['pointid']
                    
                    group302 = tempdf302[[y+'2','landcover']]
                    group302 = group302.rename(columns={y+'2':y + '302'})
                    tempmerge = pd.merge(group30,group302, on = 'landcover', how = 'outer')
                    
                    tempmerge[y + '302'].fillna(0, inplace = True)
                    tempmerge[y + '30'].fillna(0, inplace = True)
                    tempmerge['change'] = tempmerge[y+'30']-tempmerge[y+'302']
                    tempmerge = tempmerge[['change', 'landcover']]
                    tempmerge = tempmerge.rename(columns = {'change':'kgs_no3_change_' + name})

                nitdict[name + dev] = tempmerge

        for y in xlist:
            nitdict = {}
            for x in keylist:
                if x in ['base', 'trt']:
                    if x == 'base':
                        for i in devlist:
                            nitfunct(x, 'LC2030_' + i, i, dfdict[x],y)
                    else:
                        for i in devlist:
                            nitfunct(x, 'LC2030_trt_' + i, i, dfdict[x],y)
                else:
                    nitfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x],y)
                    
            td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid']]        
            tempdf14 = pd.merge(td,wclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('LC2014').sum()
            group14['index1'] = group14.index
            group14 = group14[[y,'index1']]
            group14[y] = group14[y]
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
            temp.fillna(0, inplace = True)
            temp.to_csv(outpath+y+'_nitrates.csv')                       
    
    def watershedintegrity(df, outpath):
        #6-56
        
        
        def intfunct(name, field, dev, df): 
            td = df[['LC2014','pointid', 'HUC_12', 'near_rivers','near_streams', field]]
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
        temp.fillna(0, inplace = True)
        temp.to_csv(outpath+'watint.csv')      
    
    
    #Run all of the reporting functions
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
    
    
    
def carbreport(df, outpath,activitylist,carb14, carb30,acdict = 'None', cd = 0 , cm = 0):
    import pandas as pd
    import Helpers
    lclist = ['Orchard','Annual Cropland','Vineyard', 'Rice', 'Irrigated Pasture','Forest', 'Shrubland', 'Wetland', 'Barren', 'Water','Developed','Urban','Developed Roads', 'Grassland']
    lc = pd.DataFrame({'landcover':lclist})
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

    if cd == 2:
        df4 = df.loc[df['dev_flag'] == 1]
        dfdict['dev'] = df4      
    
    if cm == 1:
        df5 = df.loc[df['con_flag'] == 1]
        dfdict['con'] = df5      

    if acdict != 'None':
            aclist = [*acdict]
            for i in aclist:
                df2 = df.loc[(df[i+'selected'] == 1)]
                dfdict[i] = df2
        
        
        

    keylist = [*dfdict]
    Helpers.pmes(keylist)
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
            lct30_bau = pd.merge(lc,lct30_bau, left_on ='landcover', right_on = 'LC2030_bau', how = 'outer')
            lct30_bau = lct30_bau.rename(columns = {'carbrate30':'sumbase'})
            lct30_trt = lct30_trt.rename(columns = {'carbrate30':'sumtrt'})
            lct = pd.merge(lct30_bau,lct30_trt, left_on ='landcover', right_on = 'LC2030_trt_bau', how = 'outer')
            lct['sumbase'].fillna(0, inplace = True)
            lct['sumtrt'].fillna(0, inplace = True)
#            lct.loc[(lct['LC2030_bau'] == 0), 'sumbase'] = lct['sumbase'].sum()
#            temp = lct.loc[lct['sumtrt'] > 0]
            
            lct['change'] = lct['sumtrt'] - lct['sumbase']
            temp = lct[['landcover', 'change']]
            
            temp = temp.rename(columns = {'change':'carbon_avoided_' + name}) 
            intdict[name] = temp
            
            
    intdict= {}
    for i in keylist:
        
        
        if i in ['base', 'trt']:
            if i == 'base':
                for x in devlist:
                    carbrepfull(dfdict[i],i, x, 'gridcode30_' + x, 'LC2030_' + x)
            else:
                for x in devlist:
                    carbrepfull(dfdict[i],i, x, 'gridcode30_trt_' + x, 'LC2030_trt_' + x)
            
        else:
            if i in dfdict[i].columns:
                carbrepfull(dfdict[i],i, 'bau', 'gridcode30_trt_bau', 'LC2030_trt_bau')
            else:
                pass
            
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
    temp.fillna(0, inplace = True)
    temp.to_csv(outpath+'carbon.csv')  
    
    
    
    
    
    
    
    
    