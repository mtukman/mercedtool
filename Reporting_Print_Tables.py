
def create_reports ():

    import Generic
    import arcpy
    arcpy.CheckOutExtension("Spatial")

    Generic.set_paths_and_workspaces("D:/temp/B100.gdb", "D:/CLOUD/Shared/Open Space/", 10000, 10000, "None", "", 'Carbon Framework/GIS Data/MASTER_DATA/', "D:/temp/B100.gdb", "MIN", "No lands" )

    output_folder = "D:/temp2/"

    import os
    import arcpy
    arcpy.CheckOutExtension("Spatial")
    arcpy.env.extent = Generic.MASK
    arcpy.env.mask = Generic.MASK
    arcpy.env.cellSize = Generic.LANDFIRE
    arcpy.env.snapRaster = Generic.LANDFIRE

    carbon_raster = Generic.CarbonRaster
    table_carbon = Generic.CarbonStats

    conversion_only_ras = arcpy.sa.Con(carbon_raster, carbon_raster,"#", "LU_30 in (19, 151)")
    conversion_only_ras.save(os.path.join(Generic.userworkspace, "CARB_CONV"))

    print("Creating reports...")

    print "line 57"
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



    #BEGIN BAR CHART THAT SHOWS ACRES OF VINEYARD/RR EXPANSION IN the context of headwater stream index
    vineyard_per_strind, urb_per_strind = create_dict_of_vals(["CARB_CONV", Generic.StreamForest_Raster], Generic.StreamForest_Raster, Generic.StreamForest_Quint, "Rank", "Quintile")



    for i in vineyard_per_strind.keys():
        if i not in vineyard_per_strind.keys():
            vineyard_per_strind[i] = 0

    for i in urb_per_strind.keys():
        if i not in urb_per_strind.keys():
            urb_per_strind[i] = 0

    tf = open ('D:/temp/vineyard_by_streamindex.csv', 'w')
    tf.write("Stream Forest Index Class, Acres\n")
    for i in vineyard_per_strind.keys():
        tf.write(i + "," + str(vineyard_per_strind[i]/4046.86) + "\n")
    tf.close()

    tf = open ('D:/temp/urban_by_streamindex.csv', 'w')
    tf.write("Stream Forest Index Class, Acres\n")
    for i in urb_per_strind.keys():
        tf.write(i + "," + str(urb_per_strind[i]/4046.86) + "\n")
    tf.close()


    #BEGIN BAR CHART THAT SHOWS ACRES OF VINEYARD/RR EXPANSION INTO PRIME FARMLAND
    vineyard_per_fmmp, urb_per_fmmp = create_dict_of_vals(["CARB_CONV", Generic.FMMP_R], Generic.FMMP_R, Generic.FMMP, "DESC_")

    for i in vineyard_per_fmmp.keys():
        if i not in vineyard_per_fmmp.keys():
            vineyard_per_fmmp[i] = 0

    for i in urb_per_fmmp.keys():
        if i not in urb_per_fmmp.keys():
            urb_per_fmmp[i] = 0


    tf = open ('D:/temp/vineyard_by_farmland.csv', 'w')
    tf.write("Farmland Type, Acres\n")
    for i in vineyard_per_fmmp.keys():
        tf.write(i + "," + str(vineyard_per_fmmp[i]/4046.86) + "\n")
    tf.close()

    tf = open ('D:/temp/urban_by_farmland.csv', 'w')
    tf.write("Farmland Type, Acres\n")
    for i in urb_per_fmmp.keys():
        tf.write(i + "," + str(urb_per_fmmp[i]/4046.86) + "\n")
    tf.close()



 #BEGIN BAR CHART THAT SHOWS ACRES OF VINEYARD/RR EXPANSION IN the context of terrestrial habitat
    vineyard_per_th, urb_per_th = create_dict_of_vals(["CARB_CONV", Generic.TerrestrialHabitat_Raster], Generic.TerrestrialHabitat_Raster, Generic.TerrestrialHab_Quint, "Rank", "Quintile")

    for i in vineyard_per_th.keys():
        if i not in vineyard_per_th.keys():
            vineyard_per_fmmp[i] = 0

    for i in urb_per_th.keys():
        if i not in urb_per_th.keys():
            urb_per_th[i] = 0

    tf = open ('D:/temp/vineyard_by_terr_hab.csv', 'w')
    tf.write("Terrestrial Habitat Type, Acres\n")
    for i in vineyard_per_th.keys():
        tf.write(i + "," + str(vineyard_per_th[i]/4046.86) + "\n")
    tf.close()

    tf = open ('D:/temp/urban_by_terr_hab.csv', 'w')
    tf.write("Terrestrial Habitat Type, Acres\n")
    for i in urb_per_th.keys():
        tf.write(i + "," + str(urb_per_th[i]/4046.86) + "\n")
    tf.close()


#BEGIN BAR CHART THAT SHOWS ACRES OF VINEYARD/RR EXPANSION IN the context of Groundwater Recharge
    vineyard_per_gwr, urb_per_gwr = create_dict_of_vals(["CARB_CONV", Generic.GroundWaterRecharge_Raster], Generic.GroundWaterRecharge_Raster, Generic.GroundWaterRecharge_Quint, "Rank", "Quintile")

    for i in vineyard_per_gwr.keys():
        if i not in urb_per_gwr.keys():
            urb_per_gwr[i] = 0

    for i in urb_per_gwr.keys():
        if i not in urb_per_gwr.keys():
            urb_per_gwr[i] = 0

    tf = open ('D:/temp/vineyard_by_gw.csv', 'w')
    tf.write("Groundwater Recharge Class, Acres\n")
    for i in vineyard_per_gwr.keys():
        tf.write(i + "," + str(vineyard_per_gwr[i]/4046.86) + "\n")
    tf.close()

    tf = open ('D:/temp/urban_by_gw.csv', 'w')
    tf.write("Groundwater Recharge Class, Acres\n")
    for i in urb_per_gwr.keys():
        tf.write(i + "," + str(urb_per_gwr[i]/4046.86) + "\n")
    tf.close()



#BEGIN BAR CHART THAT SHOWS ACRES OF VINEYARD/RR EXPANSION IN the context of Water Yield
    vineyard_per_wy, urb_per_wy = create_dict_of_vals(["CARB_CONV", Generic.WaterYield_Raster], Generic.WaterYield_Raster, Generic.WaterYield_Quint, "Rank", "Quintile")



    for i in vineyard_per_wy.keys():
        if i not in vineyard_per_wy.keys():
            vineyard_per_wy[i] = 0

    for i in urb_per_wy.keys():
        if i not in urb_per_wy.keys():
            urb_per_wy[i] = 0

    tf = open ('D:/temp/vineyard_by_wy.csv', 'w')
    tf.write("Water Yield Class, Acres\n")
    for i in vineyard_per_wy.keys():
        tf.write(i + "," + str(vineyard_per_wy[i]/4046.86) + "\n")
    tf.close()

    tf = open ('D:/temp/urban_by_wy.csv', 'w')
    tf.write("Water Yield Class, Acres\n")
    for i in urb_per_wy.keys():
        tf.write(i + "," + str(urb_per_wy[i]/4046.86) + "\n")
    tf.close()


