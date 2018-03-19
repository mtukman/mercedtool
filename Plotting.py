def crop_value_plot_tables(csv='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/cropvalue.csv', outpath='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/plot_tables/'):
    import os
    import pandas as pd 
    
    df =pd.read_csv(csv)
    df2 = df[df['landcover'].isin(['Annual Cropland', 'Orchard', 'Vineyard', 'Rice', 'Irrigated Pasture'])]
    df3 =df2.fillna(0)
    
    # Annual Croplands
    orchard = pd.DataFrame(columns=['Untreated', 'Treated'])
    orchard.loc[len(orchard)] = [float(df3.loc[df3['landcover']=='Orchard', 'usd_change_base_bau']), float(df3.loc[df3['landcover']=='Orchard', 'usd_change_trt_bau'])]
    orchard.loc[len(orchard)] = [float(df3.loc[df3['landcover']=='Orchard', 'usd_change_base_med']), float(df3.loc[df3['landcover']=='Orchard', 'usd_change_trt_med'])]
    orchard.loc[len(orchard)] = [float(df3.loc[df3['landcover']=='Orchard', 'usd_change_base_max']), float(df3.loc[df3['landcover']=='Orchard', 'usd_change_trt_max'])]
    orchard['scenario'] = ['ref', 'med', 'max']
    orchard.to_csv(os.path.join(outpath, 'plt_cropvalue_orchards.csv'))
    
    annual = pd.DataFrame(columns=['Untreated', 'Treated'])
    annual.loc[len(annual)] = [float(df3.loc[df3['landcover']=='Annual Cropland', 'usd_change_base_bau']), float(df3.loc[df3['landcover']=='Annual Cropland', 'usd_change_trt_bau'])]
    annual.loc[len(annual)] = [float(df3.loc[df3['landcover']=='Annual Cropland', 'usd_change_base_med']), float(df3.loc[df3['landcover']=='Annual Cropland', 'usd_change_trt_med'])]
    annual.loc[len(annual)] = [float(df3.loc[df3['landcover']=='Annual Cropland', 'usd_change_base_max']), float(df3.loc[df3['landcover']=='Annual Cropland', 'usd_change_trt_max'])]
    annual['scenario'] = ['ref', 'med', 'max']
    annual.to_csv(os.path.join(outpath, 'plt_cropvalue_annual.csv'))
    
    
    all_acts = pd.DataFrame(columns=['Untreated', 'Treated'])
    all_acts.loc[len(all_acts)] = [df3.sum(axis=0)['usd_change_base_bau'], df3.sum(axis=0)['usd_change_trt_bau']]
    all_acts.loc[len(all_acts)] = [df3.sum(axis=0)['usd_change_base_med'], df3.sum(axis=0)['usd_change_trt_med']]
    all_acts.loc[len(all_acts)] = [df3.sum(axis=0)['usd_change_base_max'], df3.sum(axis=0)['usd_change_trt_max']]
    all_acts['scenario'] = ['ref', 'med', 'max']
    all_acts.to_csv(os.path.join(outpath, 'plt_cropvalue_all.csv'))

#groundwater recharge
def groundwater_plot_tables(csv='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/groundwater.csv', outpath='D:/TGS/projects/64 - Merced Carbon/Reports/Draft Reports/plot_tables/'):
    import os
    import pandas as pd 
    
    df = pd.read_csv(csv)
    df3 =df.fillna(0)
    gwrc = pd.DataFrame(columns=['Untreated', 'Treated'])
    gwrc.loc[len(gwrc)] = [df3.sum(axis=0)['ac_ft_rec_lst_base_bau'], df3.sum(axis=0)['ac_ft_rec_lst_trt_bau']]
    gwrc.loc[len(gwrc)] = [df3.sum(axis=0)['ac_ft_rec_lst_base_med'], df3.sum(axis=0)['ac_ft_rec_lst_trt_med']]
    gwrc.loc[len(gwrc)] = [df3.sum(axis=0)['ac_ft_rec_lst_base_max'], df3.sum(axis=0)['ac_ft_rec_lst_trt_max']]
    gwrc['scenario'] = ['ref', 'med', 'max']
    gwrc.to_csv(os.path.join(outpath, 'plt_groundwater.csv'))

    return gwrc

crop_value_plot_tables()
tt = groundwater_plot_tables()