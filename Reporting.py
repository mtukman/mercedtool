# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 08:58:23 2018

@author: Dylan
"""






#def report(outpath, df):
def report(df, outpath, glu, wlu, rlu, clu, nlu,alu, cov14, cov30, lupath, acdict = 'None', oak = 0, rre = 0, cd = 0 , cm = 0, gra = 0, cproc = 0, terflag = 0, ucc = 0):
    
    """
    This function reports on the multi-benefits. 
    There are a number of sub-functions which create csv reports for each multi-benefit.
    
    Arguments:
    df: The dataframe from main program
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
    
    # Load Look Up CSVs:
    gclass = pd.read_csv(glu) #general class look up
    wclass = pd.read_csv(wlu) #water use look up
    rclass = pd.read_csv(rlu) #resistance look up
    cclass = pd.read_csv(clu) #crop value look up
    nclass = pd.read_csv(nlu) #nitrate look up
    aclass = pd.read_csv(alu) #nitrate look up
    cover14 = pd.read_csv(cov14)
    cover30 =  pd.read_csv(cov30)
    ucc = ucc
    #create an empty dataframe with only landcovers, used for outer joins in functions
    lc = pd.DataFrame({'landcover':lclist})
    

    # remove unnamed fields from the dtasrame
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.loc[(df['LC2030_bau'] == 'Young Forest'), 'LC2030_bau'] = 'Forest'
    df.loc[(df['LC2030_bau'] == 'Young Shrubland'), 'LC2030_bau'] = 'Shrubland'
    df.loc[(df['LC2030_med'] == 'Young Forest'), 'LC2030_med'] = 'Forest'
    df.loc[(df['LC2030_med'] == 'Young Shrubland'), 'LC2030_med'] = 'Shrubland'
    df.loc[(df['LC2030_max'] == 'Young Forest'), 'LC2030_max'] = 'Forest'
    df.loc[(df['LC2030_max'] == 'Young Shrubland'), 'LC2030_max'] = 'Shrubland'
    df.loc[(df['LC2030_trt_bau'] == 'Young Forest'), 'LC2030_trt_bau'] = 'Forest'
    df.loc[(df['LC2030_trt_bau'] == 'Young Shrubland'), 'LC2030_trt_bau'] = 'Shrubland'
    df.loc[(df['LC2030_trt_med'] == 'Young Forest'), 'LC2030_trt_med'] = 'Forest'
    df.loc[(df['LC2030_trt_med'] == 'Young Shrubland'), 'LC2030_trt_med'] = 'Shrubland'
    df.loc[(df['LC2030_trt_max'] == 'Young Forest'), 'LC2030_trt_max'] = 'Forest'
    df.loc[(df['LC2030_trt_max'] == 'Young Shrubland'), 'LC2030_trt_max'] = 'Shrubland'
    
    # create individual dataframes for each activity and scenario
    dfdict = {}
    dfdict['base'] = df
    dfdict['trt'] = df
    dfdict['eda'] = df.loc[(df['eda_flag'] == 1)]
    dfdict['pca'] = df.loc[(df['pca_val'] == 1)]
    test = df.loc[(df['vp_flag'] == 1)]
    if len(test.index) > 0:
         dfdict['vp'] = test
    
    if rre == 1:
        df2 = df.loc[(df['rreselected'] == 1)]
        dfdict['rre'] = df2
    if oak == 1:
        df3 = df.loc[df['oakselected'] == 1]
        dfdict['oak'] = df3  
    if cd == 1:
        df3 = df.loc[df['dev_flag'] == 1]
        dfdict['cust'] = df3  
        
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
    if 'urbselected' in df.columns:
        dfdict['urb'] = df.loc[(df['urbselected'] == 1)]
    if 'hplselected' in df.columns:
        dfdict['hpl'] = df.loc[(df['hplselected'] == 1)]
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
            
            """
            This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
            name: The name of the scenario being processed
            field: The 2030 reporting field to use
            dev: Development scenario to use in the report
            df: The dataframe the report is based on
            """
            
            #Create a smaller dataframe with just the required fields
            td = df[['LC2014','pointid', 'fmmp_class', field]]
            
            #Change landcover classes to match 2014 landcover classes, for reporting
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland' 
            if field == 'LC2030_bau':
                td.loc[(td['LC2030_bau'] == 'Young Forest'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), field] = 'Shrubland'

            
            #Perform the queries, find the pixels that are natural or ag in 2014 and developed in the 2030 scenario, and are in the FMMP reporting classes
            Helpers.pmes('FMMP Reporting: ' + name + ', ' + dev)
            tempdf = td.loc[(td['LC2014'].isin(aglist))]
            tempdf = tempdf.loc[(tempdf[field].isin(developed))]
            tempdf = tempdf.loc[(tempdf['fmmp_class'].isin(flist))]
            
            #Group the rows by fmmp class in order to calculate acreage
            group = tempdf.groupby('fmmp_class', as_index = False).count()
            group = group[['fmmp_class','pointid']]
            group['pointid'] = group['pointid']*.09 #Convert to hectares
            
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
            Helpers.pmes('Doing FMMP for: ' + x)
            if x in ['base', 'dev', 'trt']:
                if x == 'base':
                    for i in devlist:
                        ffunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        ffunct(x, 'LC2030_trt_' + i, i, dfdict[x])
            elif ('_urb' in x):
                ffunct(x, 'LC2030_bau', i, dfdict[x])
            elif ('dev_flag' in x):
                ffunct(x, 'LC2030_trt_bau', i, dfdict[x])
                
        #Report the baseline in 2014
        td = df[['LC2014','pointid', 'fmmp_class']]
        tempdf = td.loc[(~td['LC2014'].isin(developed))]
        tempdf = tempdf.loc[(tempdf['fmmp_class'].isin(flist))]
        group = tempdf.groupby('fmmp_class', as_index = False).count()
        group = group[['fmmp_class','pointid']]
        group['pointid'] = group['pointid']*.09 #Convert to hectares
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
        temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
        temp.to_csv(outpath + 'fmmp.csv', index = False)

    
    def fema(df, outpath):
        """
        This function reports on landcover change in 100 and 500 year floodplains.        
        
        """
        
        flist = [100,500]
        
        def femafunct(name, field,query, dev, df):
            """
            This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
            name: The name of the scenario being processed
            field: The 2030 reporting field to use
            query: A query used to specificy whether the report is for the 100 year flood plain or 500 year floodplain
            dev: Development scenario to use in the report
            df: The dataframe the report is based on
            """
            #Change landcovers to reporting landcovers
            
            if x in ['base', 'dev','cons', 'trt']:
                if 'hpl' in df.columns:
                    flist = ['LC2014','pointid','fema_class', 'near_fema', field,'hplselected']
                else: 
                    flist = ['LC2014','pointid','fema_class', 'near_fema', field]
                td = df[flist]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                if 'trt' in field:
                    if 'hpl' in flist:
                        td.loc[(td['hplselected'] == 1), field] = 'Forest'
            else:
                if 'hpl' in df.columns:
                    td = df[['LC2014','pointid','fema_class', 'near_fema', field, 'LC2030_bau','hplselected']]
                else:
                    td = df[['LC2014','pointid','fema_class', 'near_fema', field, 'LC2030_bau']]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Forest'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), field] = 'Forest'
                if 'hpl' in td:
                    td.loc[(td['hplselected'] == 1), field] = 'Forest'
            
            
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
                tempmerge['change'] = tempmerge['change']*.09 #Convert to hectares
                
                if name in ['base','trt']:
                    #Finish cleaning up the dataframe for baseline and treatment scenarios
                    tempmerge = tempmerge[['gen_class', 'change','count30']]
                    tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                    tempmerge['ha_' + name+ '_'+dev] = tempmerge['ha_' + name+ '_'+dev]*.09 #Convert to hectares
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
                    tempmerge['change'] = tempmerge['change']*.09 #Convert to hectares
                    tempmerge = tempmerge[['change','gen_class']]
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name})
                #Add the reporting dataframe to the dictionary of dataframes
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
                    if x != 'urb':
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
            
            #Create a list of dataframe keys to loop through
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
            temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
            temp.to_csv(outpath + 'flood' + str(z) + '.csv', index = False)
                    
    
    def scenic(df, outpath):
        """
        This function reports on landcover change within the most visible quintile of land in Merced County. This is 1/5 of Merced County that is the most visible from roads/towns/parks.
        """

        def scenicfunct(name, field, dev , df):        
            """
            This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
            name: The name of the scenario being processed
            field: The 2030 reporting field to use
            dev: Development scenario to use in the report
            df: The dataframe the report is based on
            """
            #Change the landcovers to reporting landcovers
  
            if x in ['base', 'dev','cons', 'trt']:
                if 'hpl' in df.columns:
                    flist = ['LC2014','pointid','scenic_val', field,'hplselected']
                else: 
                    flist =  ['LC2014','pointid','scenic_val', field]
                td = df[flist]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                if 'trt' in field:
                    if 'hpl' in flist:
                        td.loc[(td['hplselected'] == 1), field] = 'Forest'
            else:
                if 'hpl' in df.columns:
                    td = df[['LC2014','pointid','scenic_val', field, 'LC2030_bau','hplselected']]
                else:
                    td = df[['LC2014','pointid','scenic_val', field, 'LC2030_bau']]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Forest'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), field] = 'Forest'
                if 'hpl' in td:
                    td.loc[(td['hplselected'] == 1), field] = 'Forest'
            
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
                tempmerge['change'] = tempmerge['change']*.09 #Convert to hectares
                if name in ['base','trt']:
                    tempmerge = tempmerge[['gen_class', 'change','count30']]
                    tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                    tempmerge['ha_' + name +'_'+ dev] = tempmerge['ha_' + name +'_'+ dev]*.09 #Convert to hectares
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
                    tempmerge['change'] = tempmerge['change']*.09 #Convert to hectares
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
                if x != 'urb':
                    scenicfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
                
                
        #Add 2014 Base
        td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','scenic_val']]
        tempdf14 = td.loc[td['scenic_val'] > 5]
        tempdf14 = pd.merge(tempdf14,gclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
        group14 = tempdf14.groupby(['gen_class'], as_index = False).count()
        group14 = group14[['pointid','gen_class']]
        group14 = group14.rename(columns={'pointid':'ha_2014'})
        group14['ha_2014'] = group14['ha_2014']*.09 #Convert to hectares
        scendict['Base_2014'] = group14
        
        #Create list of dataframe keys to loop through
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
        temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
        temp.to_csv(outpath + 'scenic' + '.csv', index = False)

    

    def wateruse(df, outpath):
        """
        This function reports on changes in water demand based on landcover change.
        Reported in acre feet (total)        
        
        """
        #Read in the water demand look up table
        
        
        
        def watfunct(name, field, dev , df):      
            """
            This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
            
            name: The name of the scenario being processed
            field: The 2030 reporting field to use
            dev: Development scenario to use in the report
            df: The dataframe the report is based on
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
            tempdf14 = pd.merge(wclass,td, how = 'left', right_on = 'LC2014', left_on = 'landcover')
            group14 = tempdf14.groupby('landcover', as_index = False).sum()
            group14 = group14[['wat_val','landcover']]
            group14 = group14.rename(columns={'wat_val':'water14'})

            # Calculate the 2030 water use by class
            tempdf30 = pd.merge(wclass,td, how = 'left', right_on = field, left_on = 'landcover')
            group30 = tempdf30.groupby('landcover', as_index = False).sum()
            group30 = group30[['landcover','wat_val']]
            group30 = group30.rename(columns={'wat_val':'water30'})
            
            #Merge the dataframes and create a water use change field (2014 - 2030)
            tempmerge = pd.merge(group14,group30, left_on = 'landcover', right_on= 'landcover', how = 'outer')
            tempmerge['change'] = tempmerge['water30']-tempmerge['water14']
            if name in ['base','trt']:
                tempmerge = tempmerge[['landcover', 'change', 'water30']]
                tempmerge = tempmerge.rename(columns = {'water30':'ac_ft_' + name +'_'+ dev})
                tempmerge['ac_ft_' + name +'_'+ dev] = tempmerge['ac_ft_' + name +'_'+ dev]
                tempmerge['change'] = tempmerge['change']
                tempmerge = tempmerge.rename(columns = {'change':'ac_ft_change_' + name +'_'+ dev})
                
                #If the scenario is not a development scenario, do this section instead to find the change from 2030 baseline to 2030 treatment BAU
            else:
                tempdf302 = pd.merge(wclass,td, how = 'left', right_on = 'LC2030_bau', left_on = 'landcover')
                group302 = tempdf302.groupby(['landcover'], as_index = False).sum()
                group302 = group302[['landcover','wat_val']]
                group302 = group302.rename(columns={'wat_val':'water302'})
                
                tempmerge = pd.merge(group302,group30, left_on = 'landcover',right_on = 'landcover', how = 'outer')
                
                #Fill in nulls with 0s
                tempmerge['water302'].fillna(0, inplace = True)
                tempmerge['water30'].fillna(0, inplace = True)
                
                #Create change field and clean up dataframe
                tempmerge['change'] = tempmerge['water30']-tempmerge['water302']
                tempmerge['change'] = tempmerge['change']
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
                if x != 'vp':
                    if x != 'urb':
                        watfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
                
        #Make a baseline report for 2014
        td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
        tempdf14 = pd.merge(td,wclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
        
        group14 = tempdf14.groupby('LC2014', as_index = False).sum()
        group14 = group14[['wat_val','LC2014']]
        group14 = group14.rename(columns={'wat_val':'ac_ft_2014','LC2014':'landcover'})
        group14['ac_ft_2014'] = group14['ac_ft_2014']
        watdict['Base_2014'] = group14
        
        #Create list of dataframe keys to loop through
        tlist = list(watdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        
        #Loop through the dataframes and merge them into one dataframe
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
        temp = temp.fillna(0)
        temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
        temp = temp.loc[temp['landcover'] != 0]
        
        #Export the merged dataframe
        temp.to_csv(outpath+'watcon.csv', index = False)
        
    def lcchange(df, outpath):
        """
        This function reports on landcover change at the county scale.
        
        """
        def lcfunct(name, field, dev, df): 
            """
            This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
            name: The name of the scenario being processed
            field: The 2030 reporting field to use
            dev: Development scenario to use in the report
            df: The dataframe the report is based on
            """
            
            #Create initial dataframe and clean up landcovers for reporting
            if x in ['base', 'trt']:
                td = df[['LC2014','pointid', field]]

            else:
                td = df[['LC2014','pointid', field, 'LC2030_bau']]
                td.loc[(td['LC2030_bau'] == 'Young Forest'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), 'LC2030_bau'] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), 'LC2030_bau'] = 'Forest'
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            
            Helpers.pmes('Land Cover Change Reporting: ' + name + ', ' + dev)

            # Create 2014 landcover dataframe
            group14 = td.groupby('LC2014').count()
            group14['index1'] = group14.index
            group14 = group14[['pointid','index1']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            # Create 2030 landcover dataframe
            group30 = td.groupby(field).count()
            group30['index1'] = group30.index
            group30 = group30[['pointid','index1']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            #Merge the two dataframes and create landcover change field
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'outer')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = tempmerge['change']*0.09
            
            
            #Create a reporting dataframe with the appropriate fields and field names
            if name in ['base','trt']:
                tempmerge = tempmerge[['index1', 'change','count30']]
                tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                tempmerge['ha_' + name +'_'+ dev] = tempmerge['ha_' + name +'_'+ dev]*0.09
                tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'ha_change_' + name +'_'+ dev})
                
            #For non-development scenarios, this section creates comparison fields between the baseline bau and treatment bau
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

            #Add the reporting dataframe to the dictionary of dataframes
            lcdict[name + dev] = tempmerge
        lcdict = {}
        
        # Loop through the scenarios and activities to create the reporting dataframes
        for x in keylist:
            if x in ['base','trt']:
                if x == 'base':
                    for i in devlist:
                        lcfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        lcfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
                    
            else:
                if x != 'urb':
                    lcfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
                
        #Create a reporting dataframe for the 2014 baseline
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
        
        #Loop through the created dataframes and merge into one
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
        temp.fillna(0, inplace = True)
        temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
        #Export Dataframe to csv
        temp.to_csv(outpath+'lcchange.csv', index = False)    
    
    def pcalcchange(df, outpath):
        """
        This function reports on landcover change in priority conservation areas.
        
        """
        def pcafunct(name, field, dev, df): 
            """
            This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
            name: The name of the scenario being processed
            field: The 2030 reporting field to use
            dev: Development scenario to use in the report
            df: The dataframe the report is based on
            """
            if name in ['base', 'trt']:

                td = df[['LC2014','pointid','pca_val', field]]
                
            else:
                td = df[['LC2014','pointid','pca_val', field, 'LC2030_bau']]
                td.loc[(td['LC2030_bau'] == 'Young Forest'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), 'LC2030_bau'] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), 'LC2030_bau'] = 'Forest'
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'

            
            Helpers.pmes('Land Cover in Priority Conservation Reporting: ' + name + ', ' + dev)
            
            # Create landcover table for 2014 in priority conservation areas
            tempdf14 = td.loc[td['pca_val'] == 1]
            group14 = tempdf14.groupby('LC2014').count()
            group14['index1'] = group14.index
            group14 = group14[['pointid','index1']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # Create landcover table for 2030 in priority conservation areas
            tempdf30 = td.loc[td['pca_val'] == 1]
            group30 = tempdf30.groupby(field).count()
            group30['index1'] = group30.index
            group30 = group30[['pointid','index1']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            tempmerge = pd.merge(group14,group30, on = 'index1', how = 'outer')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = (tempmerge['change']*900)/10000
            
            #Create a reporting dataframe with the appropriate fields and field names
            if name in ['base','trt']:
                tempmerge = tempmerge[['index1', 'change','count30']]
                tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                tempmerge['ha_' + name +'_'+ dev] = (tempmerge['ha_' + name +'_'+ dev]*900)/10000
                tempmerge = tempmerge.rename(columns = {'index1':'landcover','change':'ha_change_' + name +'_'+ dev})
                
            #For non-development scenarios, this section creates comparison fields between the baseline bau and treatment bau
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
            #Add the reporting dataframe to the dictionary of dataframes
            pcadict[name + dev] = tempmerge
        pcadict = {}
        
        #Loop through the development scenarios and activities to create reporting dataframes
        for x in keylist:
            if x in ['base', 'trt']:
                if x == 'base':
                    for i in devlist:
                        pcafunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        pcafunct(x, 'LC2030_trt_' + i, i, dfdict[x])
   
                       
            else:
                if x == 'eda':
                    pass
                elif x == 'urb':
                    pass
                else:
                    pcafunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
                
        #Create a 2014 baseline reporting dataframes
        td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid', 'pca_val']]
        tempdf14 = td.loc[td['pca_val'] == 1]
        group14 = tempdf14.groupby('LC2014').count()
        group14['index1'] = group14.index
        group14 = group14[['pointid','index1']]
        group14 = group14.rename(columns={'pointid':'ha_2014','index1':'landcover'})
        group14['ha_2014'] = (group14['ha_2014']*900)/10000
        pcadict['Base_2014'] = group14
        
        #Loop through the reporting dataframes and merge them into one dataframe
        tlist = list(pcadict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
        temp.fillna(0, inplace = True)
        temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
        #Export the reporting dataframe to a csv
        temp.to_csv(outpath+'pca_cover_change.csv', index = False)       
        
    def aqua(df, outpath):
        """
        This function reports on general landcover change in the to 20% of important watersheds for aquatic habitat.
        
        """
        
        
        def aquahabfunct(name, field, dev , df):        
            """
            This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
            name: The name of the scenario being processed
            field: The 2030 reporting field to use
            dev: Development scenario to use in the report
            df: The dataframe the report is based on
            """
            
            #Create the initial dataframe and change landcovers as necessary for reporting
             
            if x in ['base', 'dev','cons', 'trt']:
                if 'hpl' in df.columns:
                    flist = ['LC2014','pointid','c_abf75_rnk', field,'hplselected']
                else: 
                    flist =  ['LC2014','pointid','c_abf75_rnk', field]
                td = df[flist]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                if 'trt' in field:
                    if 'hpl' in flist:
                        td.loc[(td['hplselected'] == 1), field] = 'Forest'
            else:
                if 'hpl' in df.columns:
                    td = df[['LC2014','pointid','c_abf75_rnk', field, 'LC2030_bau','hplselected']]
                else:
                    td = df[['LC2014','pointid','c_abf75_rnk', field, 'LC2030_bau']]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Forest'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), field] = 'Forest'
                if 'hpl' in td:
                    td.loc[(td['hplselected'] == 1), field] = 'Forest'
                    
                    
            Helpers.pmes('Aquatic Habitat Reporting: ' + name + ', ' + dev)
            
            # Create the 2014 general landcover dataframe
            tempdf14 = td.loc[td['c_abf75_rnk'] > 0.59] #Select pixels that are in important aquatic watersheds
            tempdf14 = pd.merge(gclass,tempdf14, how = 'outer', left_on = 'landcover', right_on = 'LC2014')
            group14 = tempdf14.groupby('gen_class', as_index = False).count()
            group14 = group14[['pointid','gen_class']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            # Create the 2030 general landcover dataframe
            tempdf30 = td.loc[td['c_abf75_rnk'] > 0.59] #Select pixels that are in important aquatic watersheds
            tempdf30 = pd.merge(gclass,tempdf30, how = 'outer', left_on = 'landcover', right_on = field)
            group30 = tempdf30.groupby('gen_class', as_index = False).count()
            group30 = group30[['pointid','gen_class']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            if len(group30.index) == 0 | len(group14.index) == 0:
                Helpers.pmes('Empty rows in ' + i)
                
            #If there are rows in the dataframe, merge the tables, create a change field and add the reporting dataframe to the dataframe list
            else:
                tempmerge = pd.merge(group14,group30, on = 'gen_class', how = 'outer')
                tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
                tempmerge['change'] = tempmerge['change']*.09 #Convert to hectares
                if name in ['base','trt']:
                    tempmerge = tempmerge[['gen_class', 'change','count30']]
                    tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                    tempmerge['ha_' + name +'_'+ dev] = tempmerge['ha_' + name +'_'+ dev]*.09 #Convert to hectares
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name +'_'+ dev})
                    
                #For other scenarios and activities, do this section
                else:
                    tempdf302 = td.loc[td['c_abf75_rnk'] > 0.59] #Select pixels that are in important aquatic watersheds
                    tempdf302 = pd.merge(gclass,tempdf302, how = 'outer', left_on = 'landcover', right_on = 'LC2030_bau')
                    group302 = tempdf302.groupby('gen_class', as_index = False).count()
                    group302 = group302[['pointid','gen_class']]
                    group302 = group302.rename(columns={'pointid':'count302'})
                    
                    tempmerge = pd.merge(group30,group302, on = 'gen_class', how = 'outer')
                    tempmerge['count302'].fillna(0, inplace = True)
                    tempmerge['count30'].fillna(0, inplace = True)
                    tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                    tempmerge['change'] = tempmerge['change']*.09 #Convert to hectares
                    tempmerge = tempmerge[['change','gen_class']]
                    tempmerge = tempmerge.rename(columns = {'change':'ha_change_' + name})

                #Add the reporting dataframe to the dictionary of dataframes
                scendict[name + dev] = tempmerge
            
        scendict = {}
        
        #Loop through the scenarios and activities to create reporting dataframes
        for x in keylist:
            if x in ['base', 'trt']:
                if x == 'base':
                    for i in devlist:
                        aquahabfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        aquahabfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
                        
            else:
                if x == 'urb':
                    pass
                else:
                    aquahabfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
                
        #Create 2014 baseline reporting dataframe
        td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','c_abf75_rnk']]
        tempdf14 = td.loc[td['c_abf75_rnk'] > 0.59]
        tempdf14 = pd.merge(tempdf14,gclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
        group14 = tempdf14.groupby('gen_class', as_index = False).count()
        group14 = group14[['pointid','gen_class']]
        group14 = group14.rename(columns={'pointid':'ha_2014'})
        group14['ha_2014'] = group14['ha_2014']*.09 #Convert to hectares
        scendict['Base_2014'] = group14
        tlist = list(scendict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        
        #Loop through the reporting dataframes and merge into one dataframe
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'gen_class', how = 'outer' )
            count = count + 1
        temp.fillna(0, inplace = True)
        temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
        #Export the merged dataframe as a csv
        temp.to_csv(outpath + 'aquatic.csv', index = False)
        
        
    def termovement(df, outpath):
        """
        This function reports on movement resistance change for the county and essential connectivity areas.
        
        """
        
        
        arealist = ['county','eca']
        def movefunct(name, field, dev, df, area): 
            """
            This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
            name: The name of the scenario being processed
            field: The 2030 reporting field to use
            dev: Development scenario to use in the report
            df: The dataframe the report is based on
            area: Area to report on, either county or essential connectivity area
            """
            
            #Create the initial dataframe and change landcovers as necessary for reporting

            
            if x in ['base', 'dev','cons', 'trt']:
                if 'hpl' in df.columns:
                    flist = ['LC2014','pointid','eca_val', field,'hplselected']
                else: 
                    flist =  ['LC2014','pointid','eca_val', field]
                td = df[flist]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                if 'trt' in field:
                    if 'hpl' in flist:
                        td.loc[(td['hplselected'] == 1), field] = 'Forest'
            else:
                if 'hpl' in df.columns:
                    td = df[['LC2014','pointid','eca_val', field, 'LC2030_bau','hplselected']]
                else:
                    td = df[['LC2014','pointid','eca_val', field, 'LC2030_bau']]
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Forest'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), field] = 'Forest'
                if 'hpl' in td:
                    td.loc[(td['hplselected'] == 1), field] = 'Forest'
            if area == 'eca':
                td = td.loc[td['eca_val'] == 1]
            
                
            Helpers.pmes('Terrestrial Resistance Reporting: ' + area + ','+ name + ', ' + dev)
            #  Create the 2014 movement resistance dataframe
            tempdf14 = pd.merge(rclass,td, how = 'outer', left_on = 'landcover', right_on = 'LC2014')
            group14 = tempdf14.groupby('res_val', as_index = False).count()
            group14 = group14[['pointid','res_val']]
            group14 = group14.rename(columns={'pointid':'count14'})
            
            
            #  Create the 2030 movement resistance dataframe
            tempdf30 = pd.merge(rclass,td, how = 'outer', left_on = 'landcover', right_on = field)
            group30 = tempdf30.groupby('res_val', as_index = False).count()

            group30 = group30[['pointid','res_val']]
            group30 = group30.rename(columns={'pointid':'count30'})
            
            tempmerge = pd.merge(group14,group30, on = 'res_val', how = 'outer')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = tempmerge['change']*.09 #Convert to hectares
            
            #Merge the dataframes and create a change field, also clean up the names and fields in the dataframe
            if name in ['base','trt']:
                tempmerge = tempmerge[['res_val', 'change','count30']]
                tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
                tempmerge['ha_' + name +'_'+ dev] = tempmerge['ha_' + name +'_'+ dev]*.09 #Convert to hectares
                tempmerge = tempmerge.rename(columns = {'res_val':'movement_potential','change':'ha_change_' + name +'_'+ dev})
                
            #For other scenarios and activities, do this section
            else:
                tempdf302 = pd.merge(rclass,td, how = 'outer', left_on = 'landcover', right_on = 'LC2030_bau')
                group302 = tempdf302.groupby('res_val', as_index = False).count()
                group302 = group302[['pointid','res_val']]
                group302 = group302.rename(columns={'pointid':'count302'})
                
                tempmerge = pd.merge(group30,group302, on = 'res_val', how = 'outer')
                
                tempmerge['count302'].fillna(0, inplace = True)
                tempmerge['count30'].fillna(0, inplace = True)
                tempmerge['change'] = tempmerge['count30']-tempmerge['count302']
                tempmerge['change'] = tempmerge['change']*.09 #Convert to hectares
                tempmerge = tempmerge[['change', 'res_val']]
                tempmerge = tempmerge.rename(columns = {'res_val':'movement_potential','change':'ha_change_' + name})
                
            #Add the reporting dataframe to the dictionary of dataframes
            movedict[name + dev] = tempmerge
        
        #Loop through the reporting areas and the scenarios/activities to create the reporting dataframes
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
                    if x == 'urb':
                        pass
                    else:
                        movefunct(x, 'LC2030_trt_bau', 'bau', dfdict[x], y)
                    
            #Create a 2014 baseline dataframe
            td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','eca_val']]
            tempdf14 = pd.merge(td,rclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('res_val').count()
            group14['index1'] = group14.index
            group14 = group14[['pointid','index1']]
            group14 = group14.rename(columns={'pointid':'ha_2014','index1':'movement_potential'})
            group14['ha_2014'] = group14['ha_2014']*.09 #Convert to hectares
            movedict['Base_2014'] = group14
            
            #Loop through the reporting dataframes and merge them for export
            tlist = list(movedict.values())
            l = len(tlist)
            count = 1
            temp = tlist[0]
            while count < l:
                temp = pd.merge(temp,tlist[count],on = 'movement_potential', how = 'outer' )
                count = count + 1
            temp.fillna(0, inplace = True)
            temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
            #Export the merged reporting dataframe to a csv
            temp.to_csv(outpath+y+'movement.csv', index = False)   
    
    
    def cropvalue(df, outpath):
        """
        This function reports on changes in crop value from landcover change.
        
        """
        
        def cropfunct(name, field, dev, df): 
            """
            This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
            name: The name of the scenario being processed
            field: The 2030 reporting field to use
            dev: Development scenario to use in the report
            df: The dataframe the report is based on
           
            """
            
            #Create the initial dataframe and change landcovers as necessary for reporting
            if x in ['base', 'trt']:
                td = df[['LC2014','pointid', field]]
            else:
                td = df[['LC2014','pointid', field, 'LC2030_bau']]
                td.loc[(td['LC2030_bau'] == 'Young Forest'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Young Shrubland'), 'LC2030_bau'] = 'Shrubland'
                td.loc[(td['LC2030_bau'] == 'Woody Riparian'), 'LC2030_bau'] = 'Forest'
                td.loc[(td['LC2030_bau'] == 'Oak Conversion'), 'LC2030_bau'] = 'Forest'
                
            # Create the 2014 crop value dataframe
            tempdf14 = pd.merge(cclass,td, how = 'outer', left_on = 'landcover', right_on = 'LC2014')
            group14 = tempdf14.groupby('landcover', as_index = False).sum()
            group14 = group14[['crop_val','landcover']]
            group14 = group14.rename(columns={'crop_val':'crop14'})
            Helpers.pmes('Crop Value Reporting: ' + name + ', ' + dev)
            
            # Create the 2030 crop value dataframe
            tempdf30 = pd.merge(cclass,td, how = 'outer', left_on = 'landcover', right_on = field)
            group30 = tempdf30.groupby('landcover', as_index = False).sum()
            group30 = group30[['crop_val','landcover']]
            group30 = group30.rename(columns={'crop_val':'crop30'})
            
            tempmerge = pd.merge(group30,group14, on = 'landcover', how = 'outer')
            tempmerge['change'] = tempmerge['crop30']-tempmerge['crop14']
            
            #Merge the dataframes and create a change field
            if name in ['base','trt']:
                tempmerge = tempmerge[['landcover', 'change','crop30']]
                tempmerge = tempmerge.rename(columns = {'crop30':'usd_' + name +'_'+ dev})
                tempmerge = tempmerge.rename(columns = {'change':'usd_change_' + name +'_'+ dev})
                
            #For other scenarios and activities, do this section to compare 2030 baseline bau to 2030 trt bau
            else:
                tempdf302 = pd.merge(cclass,td, how = 'outer', left_on = 'landcover', right_on = 'LC2030_bau')
                group302 = tempdf302.groupby('landcover', as_index = False).sum()
                group302 = group302[['crop_val','landcover']]
                group302 = group302.rename(columns = {'crop_val':'crop302'})
                tempmerge = pd.merge(group30,group302, on = 'landcover', how = 'outer')
                tempmerge['crop302'].fillna(0, inplace = True)
                tempmerge['crop30'].fillna(0, inplace = True)
                tempmerge['change'] = tempmerge['crop30']-tempmerge['crop302']
                tempmerge = tempmerge[['change','landcover']]
                tempmerge = tempmerge.rename(columns = {'change':'usd_change_' + name})
            
            #Add the reporting dataframe to the dictionary of reporting dataframes
            cropdict[name + dev] = tempmerge
            
        cropdict = {}
        
        #Loop through the scenarios and activities to create reporting dataframes
        for x in keylist:
            if x in ['base', 'cdev','cons', 'trt']:
                if x == 'base':
                    for i in devlist:
                        cropfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        cropfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
 
            else:
                if x == 'vp':
                    pass
                elif x == 'urb':
                    pass
                else:
                    cropfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x])
        td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid']]
        
        # Create a 2014 baseline reporting dataframe
        tempdf14 = pd.merge(cclass,td, how = 'outer', left_on = 'landcover', right_on = 'LC2014')
        group14 = tempdf14.groupby('landcover', as_index = False).sum()
        group14 = group14[['crop_val','landcover']]
        group14 = group14.rename(columns={'crop_val':'cropvalue_usd_2014'})
        group14['cropvalue_usd_2014'] = group14['cropvalue_usd_2014']
        cropdict['Base_2014'] = group14
        tlist = list(cropdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        
        #Loop through the reporting dataframes and merge them into a reporting dataframe
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
        temp.fillna(0, inplace = True)
        temp = temp.loc[temp['landcover'].isin(['Annual Cropland','Rice','Orchard','Vineyard','Irrigated Pasture'])]
        temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
        #Export the reporting dataframe to a csv
        temp.to_csv(outpath+'cropvalue.csv', index = False)              
            
    
    def groundwater(df, outpath):
        """
        This function reports on changes in groundwater recharge.
        
        """
        

        def gwfunct(name, field, dev, df): 
            """
            This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
            name: The name of the scenario being processed
            field: The 2030 reporting field to use
            dev: Development scenario to use in the report
            df: The dataframe the report is based on
           
            """
            
            #Create the initial dataframes
            if name in ['base', 'trt']:
                td = df[['LC2014','pointid', 'bcm_val', field]]
            else:
                td = df[['LC2014','pointid', 'bcm_val', 'LC2030_bau', 'LC2030_trt_bau']]

            #Convert the bcm value from millimeters to acre feet per pixel per year
            td['bcm_val'] =  (td['bcm_val']*.0032808) * .222394 #Turn into ac/ft/pixel/year - These calculattions change the value from mm per year to feet per year, and then convert from feet per year to acre feet per year.
            Helpers.pmes('Groundwater Recharge Reporting: ' + name + ', ' + dev)
            # do 2014
            td2 = td.loc[((td[field] != td['LC2014']) & (td[field].isin(['Urban', 'Developed', 'Developed_Roads'])))]
            
            #For baseline and treatment, use this section to create a reporting dataframe
            if name in ['base', 'trt']:
                
                group30 = td2.groupby([field], as_index = False).sum()
                group30 = pd.merge(lc,group30, left_on = 'landcover', right_on = field, how = 'outer')
                group30 = group30[['landcover', 'bcm_val']]
                group30 = group30.rename(columns = {'bcm_val':'ac_ft_rec_lst_' + name +'_'+ dev})
                group30['ac_ft_rec_lst_' + name +'_'+ dev].fillna(0, inplace = True)
                gwdict[name + dev] = group30
            
            #For other scenarios and activities, use this section to compare 2030 bau to 2030 treatment bau groundwater recharge
            else:
                td2 = td.loc[((td['LC2030_trt_bau'] != td['LC2030_bau']) & (td['LC2030_trt_bau'].isin(['Urban', 'Developed', 'Developed_Roads'])))]
                
                #Create a dataframe for 2030 baseline bau
                group30 = td2.groupby(['LC2030_bau'], as_index = False).sum()
                group30 = pd.merge(lc,group30, left_on = 'landcover', right_on = 'LC2030_bau', how = 'outer')
                group30 = group30[['landcover', 'bcm_val']]
                group30 = group30.rename(columns = {'bcm_val':'bcm_val_30'})
                group30['bcm_val_30'].fillna(0, inplace = True)
                
                #Create a dataframe for 2030 treatment bau
                group302 = td2.groupby(['LC2030_trt_bau'], as_index = False).sum()
                group302 = pd.merge(lc,group302, left_on = 'landcover', right_on = 'LC2030_trt_bau', how = 'outer')
                group302 = group302[['landcover', 'bcm_val']]
                group302 = group302.rename(columns = {'bcm_val':'bcm_val_302'})
                group302['bcm_val_302'].fillna(0, inplace = True)
                
                #Merge the dataframes together to get change from 2030 baseline bau to 2030 trt bau
                temp = pd.merge(group30,group302, on = 'landcover', how = 'outer')
                temp['change'] = temp['bcm_val_302'] - temp['bcm_val_30']
                temp = temp[['landcover','change']]
                temp = temp.rename(columns = {'change':'ac_ft_rec_avd_' + name})
                gwdict[name] = temp

        gwdict = {}
        
        # Loop through the scenarios and activities to create reporting dataframes
        for x in keylist:
            if x in ['base', 'trt']:
                if x == 'base':
                    for i in devlist:
                        gwfunct(x, 'LC2030_' + i, i, dfdict[x])
                else:
                    for i in devlist:
                        gwfunct(x, 'LC2030_trt_' + i, i, dfdict[x])
                        
            else:
                if x == 'vp':
                    pass
                elif x == 'urb':
                    pass
                else:
                    gwfunct(x, 'LC2030_bau', 'bau', dfdict[x])
        tlist = list(gwdict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        
        #Loop through the reporting dataframes and merge them into one dataframe
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
        temp.fillna(0,inplace = True)
        temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
        #Export the combined dataframes to a csv
        temp.to_csv(outpath+'groundwater.csv', index = False)       

    def nitrates(df, outpath):
        """
        This function reports on changes in nitrate leaching and runoff.
        
        """

        
        xlist = ['runoff','leach']
        
        def nitfunct(name, field, dev, df, y): 
                """
                This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
                name: The name of the scenario being processed
                field: The 2030 reporting field to use
                dev: Development scenario to use in the report
                df: The dataframe the report is based on
                y: Which field to report on, either runoff or leaching
                """
                
                #Create the initial dataframes
                if x in ['base', 'trt']:
                    td = df[['LC2014','pointid', field]]
                else:
                    td = df[['LC2014','pointid', field, 'LC2030_bau']]
                    td.loc[(td['LC2030_bau'] == 'Young Forest'), 'LC2030_bau'] = 'Forest'
                    td.loc[(td['LC2030_bau'] == 'Young Shrubland'), 'LC2030_bau'] = 'Shrubland'
                    td.loc[(td['LC2030_bau'] == 'Woody Riparian'), 'LC2030_bau'] = 'Forest'
                    td.loc[(td['LC2030_bau'] == 'Oak Conversion'), 'LC2030_bau'] = 'Forest'
                    
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                Helpers.pmes('Nitrate Reporting: ' + y + ',' + name + ', ' + dev)

                # Create 2014 nitrate reporting dataframe
                group14 = td.groupby('LC2014', as_index = False).count()
                tempdf14 = pd.merge(nclass,group14, how = 'outer', left_on = 'landcover', right_on = 'LC2014')
                tempdf14[y+'2'] = tempdf14[y]*tempdf14['pointid']
                group14 = tempdf14[[y+'2','landcover']]
                group14 = group14.rename(columns={y+'2':y + '14'})

                # Create 2030 nitrate reporting dataframe
                group30 = td.groupby(field, as_index = False).count()
                tempdf30 = pd.merge(nclass,group30, how = 'outer', left_on = 'landcover', right_on = field)
                tempdf30[y+'2'] = (tempdf30[y]*tempdf30['pointid'])/1000
                group30 = tempdf30[[y+'2','landcover']]
                group30 = group30.rename(columns={y+'2':y + '30'})
                tempmerge = pd.merge(group14,group30, on = 'landcover', how = 'outer')
                tempmerge['change'] = (tempmerge[y+'30']-tempmerge[y+'14'])/1000
                
                # Merge the dataframes and create a change field for the report
                if name in ['base','trt']:
                    tempmerge = tempmerge[['landcover', 'change',y+'30']]
                    tempmerge = tempmerge.rename(columns = {y + '30':'tons_no3_' + name +'_' + dev })
                    tempmerge = tempmerge.rename(columns = {'change':'tons_no3_change_' + name + '_' + dev})
                    
                #For other scenarios and activities, use this section to compare 2030 bau to 2030 treatment bau nitrate change
                else:
                    group302 = td.groupby('LC2030_bau', as_index = False).count()
                    tempdf302 = pd.merge(nclass,group302, how = 'outer', left_on = 'landcover', right_on = 'LC2030_bau')
                    tempdf302[y+'2'] = tempdf302[y]*tempdf302['pointid']
                    group302 = tempdf302[[y+'2','landcover']]
                    group302 = group302.rename(columns={y+'2':y + '302'})
                    tempmerge = pd.merge(group30,group302, on = 'landcover', how = 'outer')
                    
                    #Merge the 2030 dataframes to create a change field
                    tempmerge[y + '302'].fillna(0, inplace = True)
                    tempmerge[y + '30'].fillna(0, inplace = True)
                    tempmerge['change'] = (tempmerge[y+'30']-tempmerge[y+'302'])/1000
                    tempmerge = tempmerge[['change', 'landcover']]
                    tempmerge = tempmerge.rename(columns = {'change':'tons_no3_change_' + name})
                
                # Add the reporting dataframe to the dictionary of reporting dataframes
                nitdict[name + dev] = tempmerge
        
        
        #Loop through the types of nitrate loss, scenarios and activities to create reporting dataframes for each combination
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
                    if x == 'eda':
                        pass
                    elif x == 'urb':
                        pass
                    else:
                        nitfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x],y)
                    
            #Create a reporting dataframe for 2014 baseline
            td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid']]        
            tempdf14 = pd.merge(td,nclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
            group14 = tempdf14.groupby('LC2014').sum()
            group14['index1'] = group14.index
            group14 = group14[[y,'index1']]
            group14[y] = (group14[y])/1000
            group14 = group14.rename(columns={y:'tons_no3_14','index1':'landcover'})
            nitdict['Base_2014'] = group14
            
            tlist = list(nitdict.values())
            l = len(tlist)
            count = 1
            temp = tlist[0]
            
            #Loop through the dataframes and combine them into a single reporting dataframe
            while count < l:
                temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
                count = count + 1
            temp.fillna(0, inplace = True)
            temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
            #Export the merged reporting dataframe to a csv
            temp.to_csv(outpath+y+'_nitrates.csv', index = False)                       
 
    
    def airpol(df, outpath):
        """
        This function reports on changes in nitrate leaching and runoff.
        
        """

        
        xlist = ['no2_val',	'so2_val','pm10_val', 'pm2_5_val','co_val',	'o3_val']
        
        def airfunct(name, field, dev, df, y, gridcode): 
                """
                This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
                name: The name of the scenario being processed
                field: The 2030 reporting field to use
                dev: Development scenario to use in the report
                df: The dataframe the report is based on
                y: Which field to report on, either runoff or leaching
                """
                td = df
                #Create the initial dataframes
#                if 'trt' in field:
#                    
#                    td.loc[(td['urb2selected'] == 1), field] = 'Forest'

                if x in ['base', 'trt']:
                    # 
                    
                    if 'hplselected' in td:
                        if 'urb' in td.columns:
                            td = td[['LC2014','pointid', field, 'gridcode14', gridcode, 'urbselected', 'hplselected']]
                        else:
                            td = td[['LC2014','pointid', field, 'gridcode14', gridcode, 'hplselected']]
                    elif 'urb' in td.columns:
                        td = td[['LC2014','pointid', field, 'gridcode14', gridcode, 'urbselected']]
                        
                        
                    else:
                        td = td[['LC2014','pointid', field, 'gridcode14', gridcode]]
                    td.loc[(td[field] == 'Oak Conversion'), gridcode] = 3
                    td.loc[(td[field] == 'Young Forest'), gridcode] = 3
                    td.loc[(td[field] == 'Woody Riparian'), gridcode] = 3
                    td.loc[(td[field] == 'Young Shrubland'), gridcode] = 5

                    td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                    td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                    td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                    td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'

                    td = pd.merge(td,cover14, how = 'left', left_on = 'gridcode14', right_on = 'gridcode14')
                    td = pd.merge(td,cover30, how = 'left', left_on = gridcode, right_on = 'gridcode30')
                    if 'hplselected' in td:
                        td.loc[td['hplselected'] == 1, 'cover30'] = td['cover30'] + .20
                    td = td.rename (columns = {'cover30':'cover2', 'cover14':'cover1'})
                else:
                    if 'hplselected' in td:
                        if 'urb' in td.columns:
                            td = td[['LC2014','pointid', field, 'LC2030_bau', gridcode, 'gridcode30_bau', 'urbselected', 'hplselected']]
                        else:
                            td = td[['LC2014','pointid', field, 'LC2030_bau', gridcode, 'gridcode30_bau', 'hplselected']]
                    elif 'urb' in td.columns:
                        td = td[['LC2014','pointid', field, 'LC2030_bau', gridcode, 'gridcode30_bau', 'urbselected']]
                       
                       
                    else:
                        td = td[['LC2014','pointid', field, 'LC2030_bau', gridcode, 'gridcode30_bau']]
                    td.loc[(td[field] == 'Oak Conversion'), gridcode] = 3
                    td.loc[(td[field] == 'Young Forest'), gridcode] = 3
                    td.loc[(td[field] == 'Woody Riparian'), gridcode] = 3
                    td.loc[(td[field] == 'Young Shrubland'), gridcode] = 5
                    td.loc[(td['LC2030_bau'] == 'Oak Conversion'), 'gridcode30_bau'] = 3
                    td.loc[(td['LC2030_bau'] == 'Young Forest'), 'gridcode30_bau'] = 3
                    td.loc[(td['LC2030_bau'] == 'Woody Riparian'), 'gridcode30_bau'] = 3
                    td.loc[(td['LC2030_bau'] == 'Young Shrubland'), 'gridcode30_bau'] = 5
                    
                    td.loc[(td['LC2030_bau'] == 'Young Forest'), 'LC2030_bau'] = 'Forest'
                    td.loc[(td['LC2030_bau'] == 'Young Shrubland'), 'LC2030_bau'] = 'Shrubland'
                    td.loc[(td['LC2030_bau'] == 'Woody Riparian'), 'LC2030_bau'] = 'Forest'
                    td.loc[(td['LC2030_bau'] == 'Oak Conversion'), 'LC2030_bau'] = 'Forest'
                    td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                    td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                    td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                    td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                    
                    td = pd.merge(td,cover30, how = 'left', left_on = 'gridcode30_trt_bau', right_on = 'gridcode30')
                    if 'hplselected' in td:
                        td.loc[td['hplselected'] == 1, 'cover30'] = td['cover30'] + .20
                    td = td.rename (columns = {'cover30':'cover2'})
                    td = pd.merge(td,cover30, how = 'left', left_on = gridcode, right_on = 'gridcode30')
                    if 'hplselected' in td:
                        td.loc[td['hplselected'] == 1, 'cover30'] = td['cover30'] + .20
                    td = td.rename (columns = {'cover30':'cover1'})

                Helpers.pmes('Air Pollution Reporting: ' + y + ',' + name + ', ' + dev)
                
                # Create 2014 nitrate reporting dataframe
                tempdf14 = pd.merge(td,aclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
                tempdf14.loc[tempdf14['LC2014'].isin(['Developed','Urban','Developed Roads']), 'cover1'] = .102
                tempdf14[y+'2'] = (tempdf14[y]*tempdf14['cover1'])/1000000 #Convert grams tons
                group14 = tempdf14.groupby('landcover', as_index = False).sum()
                group14 = group14[[y+'2','landcover']]
                group14 = group14.rename(columns={y+'2':y + '14'})

                # Create 2030 nitrate reporting dataframe
                tempdf30 = pd.merge(td,aclass, how = 'left', left_on = field, right_on = 'landcover')
                tempdf30.loc[tempdf30[field].isin(['Developed','Urban','Developed Roads']), 'cover2'] = ucc
                
                tempdf30[y+'2'] = (tempdf30[y]*tempdf30['cover2'])/1000000 #Convert grams tons
                group30 = tempdf30.groupby('landcover', as_index = False).sum()
                group30 = group30[[y+'2','landcover']]
                group30 = group30.rename(columns={y+'2':y + '30'})
                tempmerge = pd.merge(group14,group30, on = 'landcover', how = 'outer')
                tempmerge['change'] = tempmerge[y+'30']-tempmerge[y+'14']
                
                # Merge the dataframes and create a change field for the report
                if name in ['base','trt']:
                    tempmerge = tempmerge[['landcover', 'change',y+'30']]
                    tempmerge = tempmerge.rename(columns = {y + '30':'tons_' + name +'_' + dev })
                    tempmerge = tempmerge.rename(columns = {'change':'tons_change_' + name + '_' + dev})
                    
                #For other scenarios and activities, use this section to compare 2030 bau to 2030 treatment bau nitrate change
                else:

                    tempdf302 = pd.merge(td,aclass, how = 'left', left_on = 'LC2030_bau', right_on = 'landcover')
                    tempdf302.loc[tempdf302['LC2030_bau'].isin(['Developed','Urban','Developed Roads']), 'cover2'] = ucc
                    tempdf302[y+'2'] = (tempdf302[y]*tempdf302['cover2'])/1000000 #Convert grams tons
                    group302 = tempdf302.groupby('landcover', as_index = False).sum()
                    group302 = group302[[y+'2','landcover']]
                    group302 = group302.rename(columns={y+'2':y + '302'})
                    tempmerge = pd.merge(group30,group302, on = 'landcover', how = 'outer')
                    
                    #Merge the 2030 dataframes to create a change field
                    tempmerge[y + '302'].fillna(0, inplace = True)
                    tempmerge[y + '30'].fillna(0, inplace = True)
                    tempmerge['change'] = tempmerge[y+'30']-tempmerge[y+'302']
                    tempmerge = tempmerge[['change', 'landcover']]
                    tempmerge = tempmerge.rename(columns = {'change':'tons_change_' + name})
                    
                # Add the reporting dataframe to the dictionary of reporting dataframes
                nitdict[name + dev] = tempmerge
        
        
        #Loop through the types of nitrate loss, scenarios and activities to create reporting dataframes for each combination
        for y in xlist:
            nitdict = {}
            for x in keylist:
                if x in ['base', 'trt']:
                    if x == 'base':
                        for i in devlist:
                            airfunct(x, 'LC2030_' + i, i, dfdict[x],y, 'gridcode30_' + i)
                    else:
                        for i in devlist:
                            airfunct(x, 'LC2030_trt_' + i, i, dfdict[x],y, 'gridcode30_trt_' + i)
                else:
                    if x == 'vp':
                        pass
                    else:
                        airfunct(x, 'LC2030_trt_bau', 'bau', dfdict[x],y, 'gridcode30_trt_bau')
                        
                    
            #Create a reporting dataframe for 2014 baseline
            td = df[['LC2014','gridcode14','pointid']]   
            td = pd.merge(td,cover14, how = 'left', left_on = 'gridcode14', right_on = 'gridcode14')
            tempdf14 = pd.merge(td,aclass, how = 'left', left_on = 'LC2014', right_on = 'landcover')
            tempdf14.loc[tempdf14['LC2014'].isin(['Developed','Urban','Developed Roads']), 'cover14'] = .102
            tempdf14[y] = (tempdf14[y]*tempdf14['cover14'])/1000000  #Convert grams tons

            group14 = tempdf14.groupby(['landcover'], as_index = False).sum()
            group14 = group14.rename(columns={y:'tons_14'})
            group14 =  group14[['landcover','tons_14']]
            nitdict['Base_2014'] = group14
            
            tlist = list(nitdict.values())
            l = len(tlist)
            count = 1
            temp = tlist[0]
            
            #Loop through the dataframes and combine them into a single reporting dataframe
            while count < l:
                temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
                count = count + 1
            temp.fillna(0, inplace = True)
            temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
            #Export the merged reporting dataframe to a csv
            temp.to_csv(outpath+y+'_airpollute.csv', index = False)
    

    def watershedintegrity(df, outpath):
        """
        This function reports on changes in watershed integrity based on landcover change.
        
        """
        
        
        def intfunct(name, field, dev, df):
            """
                This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
                name: The name of the scenario being processed
                field: The 2030 reporting field to use
                dev: Development scenario to use in the report
                df: The dataframe the report is based on
            """
            
            #Create the initial dataframes
            
            if 'hplselected' in df.columns:            
                td = df[['LC2014','pointid', 'HUC_12', 'near_rivers','near_streams', field, 'hplselected']]
                td.loc[(td['hplselected'] == 1), field] = 'Forest'
            else:
                td = df[['LC2014','pointid', 'HUC_12', 'near_rivers','near_streams', field]]
            if 'trt' in field:
                td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
                td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
                td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
                td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
                
                
                
            import pandas as pd
            tdf = pd.DataFrame()
                
            Helpers.pmes('Watershed Integrity Reporting: ' + name + ', ' + dev)
            
            #Set empty variables for naturalness flag, riparian flag and watershed integrity label
            td['natural14'] = 0
            td['natural30'] = 0
            
            td['riparian'] = 0 #Riparian flag
            
            td.loc[(td['near_streams'] < 30.48) | (td['near_rivers'] < 304.8),'riparian'] = 1 #Set riparian flag to 1, Units are in meters for distance requirements
            
            td['watint14'] = 'na'
            td['watint30'] = 'na'

            #Create a list of HUC_12 codes
            huclist =  td['HUC_12'].tolist()
            huclist = list(set(huclist))
            
            # Create a dataframe for 2014 where the landcover is natural
            td.loc[td['LC2014'].isin(['Forest', 'Shrubland', 'Young Forest', 'Young Shrubland', 'Barren', 'Wetland', 'Water', 'Grassland']),'natural14'] = 1

            # Create a 2030 dataframe of natural landcovers
            td.loc[td[field].isin(['Forest', 'Shrubland', 'Young Forest', 'Young Shrubland', 'Barren', 'Wetland', 'Water','Grassland']),'natural30'] = 1
            tdict = {}
            
            #Loop through HUC_12s to calculate the watershed integrity label for each watershed
            for i in huclist:
                tdict[i] = {}
                
                #Create a dataframe queried on the huc12
                temp = td.loc[td['HUC_12'] == i]
                
                #Create a dataframe for 2014 grouped on the natural and riparian flag
                ctemp14 = temp.groupby(['natural14','riparian', 'HUC_12'], as_index = False).count()
                ctemp14huc = temp.groupby(['natural14'], as_index = False).count()
                
                #Create a dataframe for 2030 grouped on the natural and riparian flag
                ctemp30 = temp.groupby(['natural30','riparian'], as_index = False).count()
                ctemp30huc = temp.groupby(['natural30'], as_index = False).count()
                
                #Create a dataframe from the 2014 grouped dataframe for riparian flagged pixels
                ctemp14perc = ctemp14.loc[(ctemp14['riparian'] == 1)]
                ctemp14perc.reset_index(inplace = True)
                
                #Create a dataframe from the 2030 grouped dataframe for riparian flagged pixels
                ctemp30perc = ctemp30.loc[(ctemp30['riparian'] == 1)]
                ctemp30perc.reset_index(inplace = True)
                
               #Create variables and set to 0
                rip14nat = 0 #Number of natural landcover pixels in the riparian zone in 2014 
                rip14unnat = 0 #Number of unnatural landcover pixels in the riparian zone in 2014 
                rip30unnat = 0 #Number of unnatural landcover pixels in the riparian zone in 2030 
                rip30nat = 0 #Number of natural landcover pixels in the riparian zone in 2030
                
                nat14 = 0 #Number of natural landcover pixels in the watershed in 2014 
                unnat14 = 0 #Number of natural landcover pixels in the watershed in 2014 
                unnat30 = 0 #Number of natural landcover pixels in the watershed in 2030
                nat30 = 0 #Number of natural landcover pixels in the watershed in 2030
                
                #For Riparian Variables, fill in the above variables with the number of pixels in each category
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
                    
                #For Watershed Variables, fill in the above variables with the number of pixels in each category
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
                    
                #If there are any riparian pixels, create a naturalness ratio.
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
                
                
                #If there are any Watershed pixels, create naturalness ratio
                hucpcent14 = nat14/(nat14+unnat14)
                hucpcent14 = float(hucpcent14)
                
                hucpcent30 = nat30/(nat30+unnat30)
                hucpcent30 = float(hucpcent30)

                #Calculate Riparian Integrity Class for the Watershed in 2014
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
                    
                #Calculate watershed integrity Class for the Watershed in 2030
                if tempripint30:

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
            
            #Create a reporting table for 2014 
            temp14 = tdf.groupby(['watint14'], as_index = False).count()
            temp14 = temp14[['pointid','watint14']]
            temp14 = temp14.rename(columns = {'pointid':'count14'})
            if 'Base_2014' not in intdict:
                temp15 = temp14
                temp15 = temp15.rename(columns={'watint14':'Integrity_Class','count14':'ha_2014'})
                temp15['ha_2014'] = temp15['ha_2014']*.09 #Convert to hectares
                intdict['Base_2014'] = temp15
            
            #Create a reporting table for 2030 
            temp30 = tdf.groupby(['watint30'], as_index = False).count()
            temp30 = temp30[['pointid','watint30']]
            temp30 = temp30.rename(columns = {'pointid':'count30'})
            tempmerge = pd.merge(temp14,temp30, left_on = 'watint14',right_on='watint30', how = 'outer')
            tempmerge['change'] = tempmerge['count30']-tempmerge['count14']
            tempmerge['change'] = tempmerge['change']*.09 #Convert to hectares
            
            

            tempmerge = tempmerge[['watint14', 'change','count30']]
            tempmerge = tempmerge.rename(columns = {'count30':'ha_' + name +'_'+ dev})
            tempmerge['ha_' + name +'_'+ dev] = tempmerge['ha_' + name +'_'+ dev]*.09 #Convert to hectares

            tempmerge = tempmerge.rename(columns = {'watint14':'Integrity_Class','change':'ha_change_' + name +'_'+ dev})
            intdict[name + dev] = tempmerge
            

        intdict = {}
        #Loop through the development scenarios to create reporting dataframes
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
        
        #loop through the reporting datframes and merge into a single dataframe
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'Integrity_Class', how = 'outer' )
            count = count + 1
        temp.fillna(0, inplace = True)
        temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
        #Export merged dataframe to a csv
        temp.to_csv(outpath+'watint.csv', index = False)      
    def thab_func(df, outpath, lupath):
        """
        This function reports on terrestrial habitat quality. Each pixel is evaluated for the species which can utilize that landcover, and depending on lancover change, a pixel is categorized as improved, degraded or unchanged.
        
        
        
        
        """
        global pts
        import pandas as pd
        import Helpers
        rids = pd.read_csv(lupath + '/env_rids.csv')
        
        def subfunc(name, field, dev, df, gridcode, gridcode2):
            """
            This function is used to calculate the acres of improved and degraded habitat for the four animal guilds.
            """
            
            Helpers.pmes('Doing Terrestrial Habitat for : ' + name + ' and ' + dev)
            
            #Select the fields needed for the analysis
            if name in ['base', 'dev','cons', 'trt']:
                        td = df[['LC2014','pointid', 'rid', gridcode2,gridcode, field]]
                        td.loc[(td[gridcode] == 14), gridcode] = 3
                        td.loc[(td[gridcode] == 15), gridcode] = 5
                        td.loc[(td[gridcode2] == 14), gridcode2] = 3
                        td.loc[(td[gridcode2] == 15), gridcode2] = 5
                        
                        
                        td = td.loc[td['LC2014'] != td[field]]
                        
            else:
                td = df[[gridcode2,'pointid', 'rid',gridcode,'LC2030_bau','LC2030_trt_bau']]
                td.loc[(td[gridcode] == 14), gridcode] = 3
                td.loc[(td[gridcode] == 15), gridcode] = 5
                td.loc[(td[gridcode2] == 14), gridcode2] = 3
                td.loc[(td[gridcode2] == 15), gridcode2] = 5
                
                
                td = td.loc[td['LC2030_bau'] != td['LC2030_trt_bau']]
            
            habsuit = pd.read_csv(lupath + '/lut_habsuit.csv')
            lut_uf14 = pd.read_csv(lupath + '/lut_urbanfootprint14.csv')
            lut_uf30 = pd.read_csv(lupath + '/lut_urbanfootprint30.csv')
            tespp = pd.read_csv(lupath + '/list_threatened_endangered.csv')
            mcount = 0
            bcount = 0
            acount = 0
            tcount = 0
            countdict = {'m':mcount, 'b':bcount,'a':acount,'t':tcount,}
                
            specieslist = []
            
            #This function gets the species list and breaks up species using commas.
            def initialize_dict(row):
                species_string = rids.loc[rids['rid']==row['rid'], 'species_ranges'].values[0]
                species_string = species_string[1:-1]
                for i in [i for i in species_string.split(',')]:
                    if not i in dev_dict.keys():
                        dev_dict[i]={}
                        dev_dict[i]['degraded'] = 0
                        dev_dict[i]['improved'] = 0
                        
            #This function adds habitat suitability to a dictionary using the whr code. 
            def initialize_suit_lu(row):
                if row['cwhr_id'] not in suit_dict.keys():
                    suit_dict[row['cwhr_id']] = {}
                else:
                    suit_dict[row['cwhr_id']][row['whr13_code']] = row['habitat_suitability']
            
            #This function adds the ufcode to each row based on the gridcode for 2014
            def initialize_uf_lu14(row):
                uf_dict14[row['gridcode14']] =  row['ufcode']
                
            #This function adds the ufcode to each row based on the gridcode for 2030
            def initialize_uf_lu30(row):
                uf_dict30[row['gridcode30']] =  row['ufcode']    
                        
            def tally(row):
                """
                This function goes through each combination of rid/species and tallies up the acres of improved and degraded for each species.
                
                It then finds the average improved/degraded acres for each guild (mammals, birds, amphibians and threatened/endangered)
                """
                
                species_string = rids.loc[rids['rid']==row['rid'], 'species_ranges'].values[0]
                species_string = species_string[1:-1]
                
                for i in [i for i in species_string.split(',')]:
                    if i.upper() in suit_dict.keys():
                        
                        #Make a list of unique species in each guild, used to get the average acreage later
                        if i not in specieslist:
                            specieslist.append(i)
                            if 'm' in i:
                                countdict['m'] = countdict['m'] + 1
                            elif 'b' in i:
                                countdict['b'] = countdict['b'] + 1
                            elif 'a' in i:
                                countdict['a'] = countdict['a'] + 1
#                            elif 't' in i:
#                                countdict['t'] = countdict['t'] + 1
#                                Helpers.pmes ('TE Count: ' + str(countdict['t']))
                        
                        #This section goes through each species in each rid/species combination, finds the suitability based on the landcover, and decides whether the suitability has improved or degraded.
                        if row[gridcode2] in uf_dict14.keys():
                            lc14 = uf_dict14[row[gridcode2]]
                        else:
                            lc14 = -9999
                        if row[gridcode] in uf_dict30.keys():
                            lc30 = uf_dict30[row[gridcode]]
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
            
                        if cust30suit < cust14suit:
                            dev_dict[i]['degraded'] = dev_dict[i]['degraded'] + row['pointid']
                        
            def summarize(first_letter, guild):

                if guild=='tes':
                    
                    new_dict = {x: v for x,v in dev_dict.items() if x in list(tespp['species']) }
                    Helpers.pmes(new_dict)
                    tescount = len(new_dict)
                else:
                    new_dict = {x: v for x,v in dev_dict.items() if x.startswith(first_letter) }
                    
                if guild != 'tes':
                    deg= (pd.DataFrame.from_dict(new_dict, orient = 'index')['degraded'].sum()*.09)/countdict[first_letter]
                    imp = (pd.DataFrame.from_dict(new_dict, orient = 'index')['improved'].sum()*.09)/countdict[first_letter]
                else:
                    deg= (pd.DataFrame.from_dict(new_dict, orient = 'index')['degraded'].sum()*.09)/tescount
                    imp = (pd.DataFrame.from_dict(new_dict, orient = 'index')['improved'].sum()*.09)/tescount
                
                summary_dict[guild + '_avg_deg_ha']=deg
                summary_dict[guild + '_avg_imp_ha']=imp
                
                
            a = td.groupby(['rid', gridcode, gridcode2], as_index = False).count()
            if a.empty:
                pass
            else:
                suit_dict = {}
                dev_dict = {}
                uf_dict14 = {}
                uf_dict30 = {}
                summary_dict = {}
                Helpers.pmes ('Initializing 2014')
                lut_uf14.apply(initialize_uf_lu14, axis=1)
                Helpers.pmes ('Initializing 2030')
                lut_uf30.apply(initialize_uf_lu30, axis=1)
                habsuit.apply(initialize_suit_lu, axis=1)
                Helpers.pmes ('Applying to df')
                a.apply(initialize_dict, axis=1)
                Helpers.pmes ('Tallying the DF')
                a.apply(tally, axis = 1)
                summarize('m', 'mammals')
                summarize('b', 'birds')
                summarize('a', 'amphibians')
                summarize('t', 'tes')
                Helpers.pmes(a.head(10))
                a = pd.DataFrame.from_dict(summary_dict, orient='index')
                a.reset_index(inplace=True)
                Helpers.pmes(a.head(10))
                if a.empty:
                    Helpers.pmes('Dataframe is empty')
                else:
                    a.columns=['guild', 'ha_' + name + '_' + dev]
                    thab_dict[name + dev] = a
            
            


        thab_dict = {}
        for x in keylist:
            
            if x in ['base', 'trt']:
                if x == 'base':
                    for i in devlist:
                        subfunc(x, 'LC2030_' + i, i, dfdict[x], 'gridcode30_' + i, 'gridcode14')
                else:
                    for i in devlist:
                        subfunc(x, 'LC2030_trt_' + i, i, dfdict[x],'gridcode30_trt_' + i, 'gridcode14')
                pass
            else:
                if x == 'eda':
                    pass
                elif x == 'urb':
                    pass
                else:
                    subfunc(x, 'LC2030_trt_bau', 'bau', dfdict[x],'gridcode30_trt_bau', 'gridcode30_bau')
        
        tlist = list(thab_dict.values())
        l = len(tlist)
        count = 1
        if tlist:
            temp = tlist[0]
            
            #Loop through the dataframes and combine them into a single reporting dataframe
            while count < l:
                temp = pd.merge(temp,tlist[count],on = 'guild', how = 'outer' )
                count = count + 1
            temp.fillna(0, inplace = True)
            temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
            #Export the merged reporting dataframe to a csv
            temp.to_csv(outpath+'terrhab.csv', index = False)    
        else:
            Helpers.pmes('DF List is Empty')

    
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
    airpol(df,outpath)
    if cproc == 0:
        watershedintegrity(df,outpath)
    else:
        pass
    aqua(df,outpath)
    if terflag == 1:
        thab_func(df,outpath, lupath)
    
    
def carbreport(df, outpath,activitylist,carb14, carb30,acdict = 'None', cd = 0 , cm = 0, ucc = 0):
    """
    This function reporting on carbon totals and carbon changes for the development scenarios and activities
    
    Arguments-
    df: The dataframe, passed from the main program
    outpath: The folder to which reporting csvs will be exported
    activitylist: List of activities selected from the main program module
    carb14: The location of the 2014 carbon table, from the Generic Module
    carb30: The location of the 2030 carbon table, from the Generic Module
    acdict: If avoided conversion activities were selected, this dictionary holds them
    cd: Custom Development flag
    cm: Conservation Mask flag
    """
    
    import pandas as pd
    import Helpers
    lclist = ['Orchard','Annual Cropland','Vineyard', 'Rice', 'Irrigated Pasture','Forest', 'Shrubland', 'Wetland', 'Barren', 'Water','Developed','Urban','Developed Roads', 'Grassland']
    lc = pd.DataFrame({'landcover':lclist})
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    #Change treatment labels for riparian restoration, oak conversion and grass restoration to bau values for carbon reporting
    
    
    if 'rreselected' in df.columns:
        df.loc[(df['rreselected'] == 1), 'gridcode30_trt_med'] = df['gridcode30_med']
        df.loc[(df['rreselected'] == 1), 'gridcode30_trt_max'] = df['gridcode30_max']
        df.loc[(df['rreselected'] == 1), 'LC2030_trt_max'] = df['LC2030_max']
        df.loc[(df['rreselected'] == 1), 'LC2030_trt_med'] = df['LC2030_med']
        df.loc[(df['rreselected'] == 1), 'LC2030_trt_bau'] = df['LC2030_bau']
        df.loc[(df['rreselected'] == 1), 'gridcode30_trt_bau'] = df['gridcode30_bau']
    
    if 'oakselected' in df.columns:
        df.loc[(df['oakselected'] == 1), 'gridcode30_trt_bau'] = df['gridcode30_bau']
        df.loc[(df['oakselected'] == 1), 'gridcode30_trt_med'] = df['gridcode30_med']
        df.loc[(df['oakselected'] == 1), 'gridcode30_trt_max'] = df['gridcode30_max']
        df.loc[(df['oakselected'] == 1), 'LC2030_trt_bau'] = df['LC2030_bau']
        df.loc[(df['oakselected'] == 1), 'LC2030_trt_med'] = df['LC2030_med']
        df.loc[(df['oakselected'] == 1), 'LC2030_trt_max'] = df['LC2030_max']

    #Create dataframes for each scenario and activity
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
    
    #Read in the carbon tables
    c30 = pd.read_csv(carb30)
    c14 = pd.read_csv(carb14)
        
    collist = []
    def carbrepfull(df, name, dev, field):
        """
            This subfunction create a dataframe which is added to a dataframe dictionary (all will be merged at the end of the parent function to create a csv report)
            name: The name of the scenario being processed
            field: The 2030 reporting field to use
            dev: Development scenario to use in the report
            df: The dataframe the report is based on
        """
        Helpers.pmes ('Calculating Carbon For: ' + name)
        
        #Create a dataframe for reporting based on which scenario/activity is being reported
        if dev in devlist:
            if name == 'base':
                td = df[['LC2030_'+dev, 'LC2014', 'gridcode14', 'gridcode30_' + dev]]
            elif name == 'trt':
                td = df[['LC2030_trt_'+dev, 'LC2014', 'gridcode14', 'gridcode30_trt_' + dev]]
            else:
                td = df[['LC2030_bau', 'LC2030_trt_bau', 'LC2014', 'gridcode14', 'gridcode30_bau', 'gridcode30_trt_bau']]
                
        if name in activitylist:
            if (name + '_carbred') in df:
                td = df[['LC2030_bau', 'LC2030_trt_bau', 'LC2014', 'gridcode14', 'gridcode30_bau', 'gridcode30_trt_bau', name + '_carbred']]
            else:
                Helpers.pmes('Activity Carbon Rates not in Dataframe')
                
        if name in ['con']:
            td = df[['LC2030_bau', 'LC2030_trt_bau', 'LC2014', 'gridcode14', 'gridcode30_bau', 'gridcode30_trt_bau']]
            
        if 'ac' in name:
            td = df[['LC2030_bau', 'LC2030_trt_bau','gridcode30_bau', 'gridcode30_trt_bau']]
        
        
        #Calculate carbon differently for each scenario/activity
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
            if (name + '_carbred') in df:
                lct = td.groupby(['LC2030_trt_bau'], as_index = False).sum()
                lct = lct[['LC2030_trt_bau', name + '_carbred']]
                lct = lct.rename(columns = {'LC2030_trt_bau':'landcover',name + '_carbred':'carbon_' + name}) 
                collist.append('carbon_' + name)
                intdict[name] = lct
            else:
                Helpers.pmes('Activity Carbon Rates not in Dataframe')
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
        
        #If the activity is avoided conversion, then this function will show the change between baseline and treatment carbon totals
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
            
            lct['change'] = lct['sumtrt'] - lct['sumbase']
            temp = lct[['landcover', 'change']]
            
            temp = temp.rename(columns = {'change':'carbon_avoided_' + name}) 
            intdict[name] = temp
            
            
    intdict= {}
    
    #Loop through the list of scenarios/activities and calclulate carbon dataframes
    for i in keylist:
        Helpers.pmes(i)
        
        if i in ['base', 'trt']:
            if i == 'base':
                for x in devlist:
                    carbrepfull(dfdict[i],i, x, 'LC2030_' + x)
            else:
                for x in devlist:
                    carbrepfull(dfdict[i],i, x, 'LC2030_trt_' + x)
            
        else:

            carbrepfull(dfdict[i],i, 'bau', 'LC2030_trt_bau')

            
    c14 = pd.read_csv(carb14)
    
    #Calculate the 2014 carbon total
#    def do2014(df, c14):
#        td = df[['LC2014', 'gridcode14']]
#        temp = pd.merge(td,c14, how = 'left', on = 'gridcode14')
#        lct = temp.groupby(['LC2014'], as_index = False).sum()
#        return lct
#    lct = do2014(df, c14)
#      
#    lct = lct[['LC2014', 'carbrate14']]
#    lct = lct.rename(columns = {'LC2014':'landcover','carbrate14':'carbon2014'})
#    intdict['Carbon2014'] = lct

    tlist = list(intdict.values())
    l = len(tlist)
    count = 1
    temp = tlist[0]
#    Helpers.pmes('List of tables: ' + str(tlist))
    Helpers.pmes('Combining Dataframes')

    #Loop through the carbon reporting dataframes and merge into one dataframe
    while count < l:
            temp = pd.merge(temp,tlist[count],on = 'landcover', how = 'outer' )
            count = count + 1
    temp.fillna(0, inplace = True)
    
    
    temp['trt_bau_total'] = 0
    temp['trt_med_total'] = 0
    temp['trt_max_total'] = 0
    temp['trt_bau_total'] = temp['carbon_trt_bau'] + temp['trt_bau_total']
    temp['trt_med_total'] = temp['carbon_trt_med'] + temp['trt_med_total']
    temp['trt_max_total'] = temp['carbon_trt_max'] + temp['trt_max_total']
    
    for i in collist:
        temp['trt_med_total'] = temp[i] + temp['trt_med_total']
        temp['trt_max_total'] = temp[i] + temp['trt_max_total']
        temp['trt_bau_total'] = temp[i] + temp['trt_bau_total']
    temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
    #Export the dataframe to a csv
    temp.to_csv(outpath+'carbon.csv', index = False)  
    
    
    
def report_acres(df, activitylist, outpath):
    """
    This function reports the number of acres adopted for each activity.
    
    
    """
    
    import Helpers
    import pandas as pd
    acredict= {}
    
    
    if activitylist:
        for i in activitylist:
            temp = df.loc[df[i + 'selected'] == 1]
            temp = temp.groupby([i + 'selected'], as_index = False).count()
            temp = temp [[i + 'selected', 'pointid']]
            temp['pointid'] = temp['pointid'] * 0.222395
            temp = temp[['pointid']]
            temp = temp.rename(columns = {'pointid':i + '_acres'})
            
            acredict[i] = temp
            
        
        tlist = list(acredict.values())

        temp = tlist[0]

        
        Helpers.pmes('Combining Dataframes')
        result = pd.concat(tlist, axis=1)
        result = result.loc[:, ~result.columns.str.contains('^Unnamed')]    
        result.to_csv(outpath+'act_acres.csv', index = False)  
    
    
    