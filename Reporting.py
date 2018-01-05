#-------------------------------------------------------------------------------
#
# Author:      Mark Tukman
#
# Created:     10/07/2014
# Copyright:   (c) Tukman Geospatial LLC 2014
# Unauthorized copying of this file, via any medium is strictly prohibited
#
# Proprietary and confidential
#
# Written by Mark Tukman (mark@tukmangeospatial.com)
# If you'd like to use this code to support land conservation or
# do something else cool, contact me - maybe I can help
#-------------------------------------------------------------------------------
def create_reports (treatments, conserved_acreage, output_folder, vineyard_count, rr_count):
#for unit testing
#def create_reports():
    import Generic


    layers_to_delete_at_finish=["CARB_CONV", "CMB67"]
    #set title font size
    tsize = 11
    #comment out the below 6 lines when not debugging
    #Generic.set_paths_and_workspaces("D:/temp/scratch.gdb", "D:/CLOUD/Shared/Open Space/", 10000, 10000, "None", "", 'Carbon Framework/GIS Data/MASTER_DATA/', "D:/temp/scratch.gdb", "PLACKARD" )
    #treatments = (["Preservation Ranch Vineyards",Generic.PresRanchVineyards], ["Preservation Ranch Estates",Generic.PresRanchEstates])
    #conserved_acreage = "120K Acres Conserved Next 20 Yrs."
    #output_folder = "D:/temp/"
    #vineyard_count = 10
    #rr_count = 6

    Generic.add_to_logfile("Creating reports...")
    import numpy as np
    import os
    import arcpy


    arcpy.env.workspace = Generic.ArcWorkspace
    arcpy.env.scratchWorkspace = Generic.ArcScratchWorkspace
    #arcpy.env.scratchFolder = ArcScratchFolder
    #arcpy.env.scratchGDB= ArcScratchGDB

    arcpy.CheckOutExtension("Spatial")
    import Generic
    import matplotlib.pyplot as plt
    import matplotlib.pyplot as plt2
    from matplotlib.backends.backend_pdf import PdfPages

    arcpy.env.extent = Generic.MASK
    #arcpy.env.mask = Generic.MASK
    arcpy.env.cellSize = Generic.LANDFIRE
    arcpy.env.snapRaster = Generic.LANDFIRE


    if os.path.isfile(os.path.join(output_folder, 'reports.pdf')):
        os.remove(os.path.join(output_folder, 'reports.pdf'))
    pp = PdfPages(os.path.join(output_folder, 'reports.pdf'))

    carbon_raster = Generic.CarbonRaster
    table_carbon = Generic.CarbonStats


    def create_dict_of_vals(input_raster_list_for_combine, combined_thematic_raster,   input_vector_for_join, thematic_vector_attribute, thematic_ras_joinfield = "OBJECTID" ):
        # Replace a layer/table view name with a path to a dataset (which can be a layer ) or create the layer/table view within the script
        # The following inputs are layers or table views: "CB_CW", "Calwater_TA"
        cmb1= arcpy.sa.Combine(input_raster_list_for_combine)
        cmb1.save("CMB67")
        arcpy.MakeTableView_management("CMB67" , "cw")
        arcpy.AddJoin_management(in_layer_or_view="cw",in_field=os.path.basename(combined_thematic_raster)[0:26],join_table=input_vector_for_join,join_field=thematic_ras_joinfield,join_type="KEEP_ALL")
        arcpy.AddJoin_management(in_layer_or_view="cw",in_field="CARB_CONV",join_table=carbon_raster,join_field="Value",join_type="KEEP_ALL")

        urb_per={}
        vineyard_per={}

        fields = []
        fields.append(os.path.basename(input_vector_for_join) + "." + thematic_vector_attribute)
        fields.append("VAT_CMB67." + "Count")
        fields.append("VAT_CMB67." + "Value")

        for i in ("151", "19"):
            if i == '151': ref = vineyard_per
            else: ref= urb_per
            where= "VAT_" + os.path.basename(carbon_raster)+ "." + "LU_30 = " + i + " and VAT_" + os.path.basename(carbon_raster)+ "." + "LU_10 <> " + i
            sc = arcpy.da.SearchCursor("cw", fields, where)
            count = 0
            for row in sc:
                if row[0] in ref.keys():
                    ref[row[0]] = ref[row[0]] + (row[1]*900)
                else:
                    ref[row[0]] = (row[1]*900)
            del sc

        return(vineyard_per, urb_per)


    dict_carbon_overall={}

    title = conserved_acreage

    c=1
    tm=""
    if len(treatments) >0 and c<len(treatments):
        for i in treatments:
            tm = tm + "Treatment " + str(c) + ": " + i[0] + "\n"
            c= c+1
    elif len(treatments) >0 and c==len(treatments):
        for i in treatments:
            tm = tm + "Treatment " + str(c) + ": " + i[0]
            c= c+1

    if len(treatments) >1:
        title = title + "\n" + tm

    def add_to_dict(dict_name, line_title, table, bau=1):
        vals = []
        fields_carbon = ["SUM_Tot_C_90", "SUM_Tot_C_10", "SUM_Tot_C_30",  "SUM_Tot_C_30BAU", "SUM_Tot_C_50",  "SUM_Tot_C_50BAU" ]
        for row in arcpy.da.SearchCursor(table, (fields_carbon)):
            if bau == 1:
                vals.append(row[0])
                vals.append(row[1])
                vals.append(row[3])
                vals.append(row[5])
            else:
                vals.append(row[0])
                vals.append(row[1])
                vals.append(row[2])
                vals.append(row[4])

        dict_name[line_title] = vals

    treatment_name_bau = "Business as Usual; Vineyard acreage cap: " + str(Generic.acreage_cap_vineyard) + ", Ruralres acreage cap: " + str(Generic.acreage_cap_urban)
    treatment_name = tm

    add_to_dict(dict_carbon_overall, treatment_name_bau, table_carbon, 1)
    if len(treatments) >0:
        add_to_dict(dict_carbon_overall, treatment_name, table_carbon, 0)

    years = [1990, 2010, 2030, 2050]
    colordict={"Business as Usual":"red","green""Improved Conifer Management":"green", "Fuels Management - Mayacamas":"yellow", "No Treatment":"black", \
    "40K Acres Conserved Next 20 Yrs.":"red", "80K Acres Conserved Next 20 Yrs.":"yellow", "120K Acres Conserved Next 20 Yrs.":"green" }
    colordict[treatment_name]="yellow"
    colordict[treatment_name_bau]="red"

    fig = plt.figure(figsize=(8.5, 11))
    for i in reversed(sorted(dict_carbon_overall.keys())):

        plt.subplot(3,1, 1)
        plt.plot(years, dict_carbon_overall[i], label=i, color=colordict[i])

    plt.xlabel('Year')
    plt.ylabel('Metric Tons Carbon')
    plt.legend(loc=2, prop={'size':8})
    plt.tight_layout()
    plt.title(title)

    if (rr_count>0 or vineyard_count>0):
        #first create just a raster of the vineyards and rr areas, so that the combine works
        conversion_only_ras = arcpy.sa.Con(carbon_raster, carbon_raster,"#", "LU_30 in (19, 151)")
        conversion_only_ras.save(os.path.join(Generic.ArcWorkspace, "CARB_CONV"))
        #BEGIN BAR CHART THAT SHOWS TOTAL ACRES OF VINEYARD AND RR BY WATERSHED
        vineyard_per_shed, urb_per_shed = create_dict_of_vals([os.path.join(Generic.ArcWorkspace, "CARB_CONV"), Generic.Calwater_R], Generic.Calwater_R, Generic.Calwater, "HANAME")

        for i in vineyard_per_shed.keys():
            if i not in urb_per_shed.keys():
                urb_per_shed[i] = 0

        for i in urb_per_shed.keys():
            if i not in vineyard_per_shed.keys():
                vineyard_per_shed[i] = 0


        x = [i for i in sorted(vineyard_per_shed.keys())]
        y = []
        k= []
        for i in x:
            y.append(vineyard_per_shed[i]/4046.86)
            k.append(urb_per_shed[i]/4046.86)
        ax= plt.subplot(3,1, 2)
        n = len(vineyard_per_shed)
        ind = np.arange(n)
        w = 0.3
        r1= ax.bar(ind, y,width=w,color='b',align='center')
        r2=ax.bar(ind+w, k,width=w,color='g',align='center')
        #ax.xaxis_date()
        ax.autoscale(tight=True)
        ax.set_title('Projected Vineyard and Rural Residential Development by Watershed', size=tsize)
        ax.set_xticks(ind + (.5*w))
        ax.set_ylabel('Acres')
        xTickMarks = x
        xtickNames = ax.set_xticklabels(xTickMarks, )
        plt.setp(xtickNames, rotation=40, ha='center', fontsize=8)
        ymax = Generic.ylim(max(vineyard_per_shed.values())/4047, max(urb_per_shed.values())/4047)
        plt.ylim(0, ymax)

        ax.legend((r1[0], r2[0]), ('Vineyard Conversion','Rural Residential Expansion'), prop={'size':8}, ncol=2)
        plt.tight_layout()
        #END CHART


        #BEGIN BAR CHART THAT SHOWS ACRES OF VINEYARD/RR EXPANSION INTO PRIME FARMLAND
        vineyard_per_fmmp, urb_per_fmmp = create_dict_of_vals(["CARB_CONV", Generic.FMMP_R], Generic.FMMP_R, Generic.FMMP, "DESC_")

        for i in vineyard_per_fmmp.keys():
            if i not in urb_per_fmmp.keys():
                urb_per_fmmp[i] = 0

        for i in urb_per_fmmp.keys():
            if i not in vineyard_per_fmmp.keys():
                vineyard_per_fmmp[i] = 0

        x = [i for i in sorted(vineyard_per_fmmp.keys())]

        y = []
        k= []
        for i in x:
            y.append(vineyard_per_fmmp[i]/4046.86)
            k.append(urb_per_fmmp[i]/4046.86)
        ax= plt.subplot(3,1, 3)

        n = len(vineyard_per_fmmp)
        ind = np.arange(n)
        w = 0.3
        r1= ax.bar(ind, y,width=w,color='b',align='center')
        r2=ax.bar(ind+w, k,width=w,color='g',align='center')
        #ax.xaxis_date()
        ax.autoscale(tight=True)
        ax.set_title('Projected Vineyard and Rural Residential Development by Farmland Type', size=tsize)
        ax.set_xticks(ind + (.5*w))
        ax.set_ylabel('Acres')
        xTickMarks = x
        xtickNames = ax.set_xticklabels(xTickMarks, )
        plt.setp(xtickNames, rotation=40, fontsize=8, ha='center')

        ymax = Generic.ylim(max(vineyard_per_fmmp.values())/4047, max(urb_per_fmmp.values())/4047)
        plt.ylim(0, ymax)
        ax.legend((r1[0], r2[0]), ('Vineyard Conversion','Rural Residential Expansion'), prop={'size':8}, ncol=2)
        plt.tight_layout()

        #END CHART

        pp.savefig()

        fig = plt.figure(figsize=(8.5, 11))

     #BEGIN BAR CHART THAT SHOWS ACRES OF VINEYARD/RR EXPANSION IN the context of terrestrial habitat
        vineyard_per_th, urb_per_th = create_dict_of_vals(["CARB_CONV", Generic.TerrestrialHabitat_Raster], Generic.TerrestrialHabitat_Raster, Generic.TerrestrialHab_Quint, "Rank", "Quintile")

        for i in vineyard_per_th.keys():
            if i not in urb_per_th.keys():
                urb_per_th[i] = 0

        for i in urb_per_th.keys():
            if i not in vineyard_per_th.keys():
                vineyard_per_th[i] = 0


        myorder = ['Highest','Mid-High','Mid','Mid-Low','Lowest']
        x=[]
        for i in myorder:
            if i in sorted(vineyard_per_th.keys()):
                x.append(i)
        y = []
        k= []
        for i in x:
            y.append(vineyard_per_th[i]/4046.86)
            k.append(urb_per_th[i]/4046.86)
        ax= plt.subplot(3,1, 1)

        n = len(vineyard_per_th)
        ind = np.arange(n)
        w = 0.3
        r1= ax.bar(ind, y,width=w,color='b',align='center')
        r2=ax.bar(ind+w, k,width=w,color='g',align='center')
        #ax.xaxis_date()
        ax.autoscale(tight=True)
        ax.set_title('Projected Vineyard and Rural Residential Development by Terrestrial Habitat Value', size=tsize)
        ax.set_xticks(ind + (.5*w))
        ax.set_ylabel('Acres')
        xTickMarks = x
        xtickNames = ax.set_xticklabels(xTickMarks, )
        plt.setp(xtickNames, rotation=40, fontsize=8, ha='center')

        ymax = Generic.ylim(max(vineyard_per_th.values())/4047, max(urb_per_th.values())/4047)
        plt.ylim(0, ymax)

        ax.legend((r1[0], r2[0]), ('Vineyard Conversion','Rural Residential Expansion'), prop={'size':8}, ncol=2)
        plt.tight_layout()

    #BEGIN BAR CHART THAT SHOWS ACRES OF VINEYARD/RR EXPANSION IN the context of Groundwater Recharge
        vineyard_per_gwr, urb_per_gwr = create_dict_of_vals(["CARB_CONV", Generic.GroundWaterRecharge_Raster], Generic.GroundWaterRecharge_Raster, Generic.GroundWaterRecharge_Quint, "Rank", "Quintile")

        for i in vineyard_per_gwr.keys():
            if i not in urb_per_gwr.keys():
                urb_per_gwr[i] = 0

        for i in urb_per_gwr.keys():
            if i not in vineyard_per_gwr.keys():
                vineyard_per_gwr[i] = 0


        myorder = ['Highest','Mid-High','Mid','Mid-Low','Lowest']
        x=[]
        for i in myorder:
            if i in sorted(vineyard_per_gwr.keys()):
                x.append(i)
        y = []
        k= []
        for i in x:
            y.append(vineyard_per_gwr[i]/4046.86)
            k.append(urb_per_gwr[i]/4046.86)
        ax= plt.subplot(3,1, 2)

        n = len(vineyard_per_gwr)
        ind = np.arange(n)
        w = 0.3
        r1= ax.bar(ind, y,width=w,color='b',align='center')
        r2=ax.bar(ind+w, k,width=w,color='g',align='center')
        #ax.xaxis_date()
        ax.autoscale(tight=True)
        ax.set_title('Projected Vineyard and Rural Residential Development by Groundwater Recharge Value', size=tsize)
        ax.set_xticks(ind + (.5*w))
        ax.set_ylabel('Acres')
        xTickMarks = x
        xtickNames = ax.set_xticklabels(xTickMarks, )
        plt.setp(xtickNames, rotation=40, fontsize=8, ha='center')

        ymax = Generic.ylim(max(vineyard_per_gwr.values())/4047, max(urb_per_gwr.values())/4047)
        plt.ylim(0, ymax)

        ax.legend((r1[0], r2[0]), ('Vineyard Conversion','Rural Residential Expansion'), prop={'size':8}, ncol=2)
        plt.tight_layout()

    #BEGIN BAR CHART THAT SHOWS ACRES OF VINEYARD/RR EXPANSION IN the context of Water Yield
        vineyard_per_wy, urb_per_wy = create_dict_of_vals(["CARB_CONV", Generic.WaterYield_Raster], Generic.WaterYield_Raster, Generic.WaterYield_Quint, "Rank", "Quintile")

        for i in vineyard_per_wy.keys():
            if i not in urb_per_wy.keys():
                urb_per_wy[i] = 0

        for i in urb_per_wy.keys():
            if i not in vineyard_per_wy.keys():
                vineyard_per_wy[i] = 0

        myorder = ['Highest','Mid-High','Mid','Mid-Low','Lowest']
        x=[]
        for i in myorder:
            if i in sorted(vineyard_per_wy.keys()):
                x.append(i)
        y = []
        k= []
        for i in x:
            y.append(vineyard_per_wy[i]/4046.86)
            k.append(urb_per_wy[i]/4046.86)
        ax= plt.subplot(3,1, 3)

        n = len(vineyard_per_wy)
        ind = np.arange(n)

        w = 0.3
        r1= ax.bar(ind, y,width=w,color='b',align='center')
        r2=ax.bar(ind+w, k,width=w,color='g',align='center')
        #ax.xaxis_date()
        ax.autoscale(tight=True)
        ax.set_title('Projected Vineyard and Rural Residential Development by Water Yield', size=tsize)
        ax.set_xticks(ind + (.5*w))
        ax.set_ylabel('Acres')
        xTickMarks = x
        xtickNames = ax.set_xticklabels(xTickMarks, )
        plt.setp(xtickNames, rotation=40, fontsize=8, ha='center')
        ymax = Generic.ylim(max(vineyard_per_wy.values())/4047, max(urb_per_wy.values())/4047)
        plt.ylim(0, ymax)

        ax.legend((r1[0], r2[0]), ('Vineyard Conversion','Rural Residential Expansion'), prop={'size':8}, ncol=2)
        plt.tight_layout()


    pp.savefig()

    pp.close()

    for i in layers_to_delete_at_finish:
        if arcpy.Exists(i):
            arcpy.Delete_management(i)
    #plt.show()
