# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 14:20:14 2018

@author: Dylan
"""

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
            if 'hplselected' in df:
                td = df[['LC2014','pointid','eca_val', field,'hplselected']]
            else: 
                td = df[['LC2014','pointid','eca_val', field]]
            td.loc[(td[field] == 'Young Forest'), field] = 'Forest'
            td.loc[(td[field] == 'Young Shrubland'), field] = 'Shrubland'
            td.loc[(td[field] == 'Woody Riparian'), field] = 'Forest'
            td.loc[(td[field] == 'Oak Conversion'), field] = 'Forest'
            if 'trt' in field:
                if 'hplselected' in td:
                    td.loc[(td['hplselected'] == 1), field] = 'Shrubland'
        else:
            if 'hplselected' in df:
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
            if 'hplselected' in td:
                td.loc[(td['hplselected'] == 1), field] = 'Shrubland'
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
            tempmerge = tempmerge.rename(columns = {'res_val':'resistance_class','change':'ha_change_' + name +'_'+ dev})
            
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
            tempmerge = tempmerge.rename(columns = {'res_val':'resistance_class','change':'ha_change_' + name})
            
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
        group14 = group14.rename(columns={'pointid':'ha_2014','index1':'resistance_class'})
        group14['ha_2014'] = group14['ha_2014']*.09 #Convert to hectares
        movedict['Base_2014'] = group14
        
        
        td = df[['LC2014','dcode_medinfill','dcode_maxinfill','pointid','eca_val']]
        td = td.loc[td['eca_val'] == 1]
        tempdf14 = pd.merge(td,rclass, how = 'outer', left_on = 'LC2014', right_on = 'landcover')
        group14 = tempdf14.groupby('res_val').count()
        group14['index1'] = group14.index
        group14 = group14[['pointid','index1']]
        group14 = group14.rename(columns={'pointid':'ha__eca_2014','index1':'resistance_class'})
        group14['ha__eca_2014'] = group14['ha__eca_2014']*.09 #Convert to hectares
        movedict['ECA_2014'] = group14
        
        #Loop through the reporting dataframes and merge them for export
        tlist = list(movedict.values())
        l = len(tlist)
        count = 1
        temp = tlist[0]
        while count < l:
            temp = pd.merge(temp,tlist[count],on = 'resistance_class', how = 'outer' )
            count = count + 1
        temp.fillna(0, inplace = True)
        temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]    
        #Export the merged reporting dataframe to a csv
        temp.to_csv(outpath+y+'movement.csv', index = False) 