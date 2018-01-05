import Generic

def carbon_change(scenario_name, run_name, treatment_list, urban, urban_conversion=Generic.urban_out_raster, vineyard_conversion=Generic.vineyard_out_raster):
    """Function creates a CARBON_ALL raster in the scratch folder that includes total carbon per pixel for
    1990, 2010, and 2030.  For 2030, carbon is presented in the table for conversions/scenarios as well
    as for business as usual (BAU).  BAU only includes business as usual urbanization and vineyard conversion.

    This function also applies scenarios, by 'flipping pixels' in the areas that are overlapped by
    scenario rasters.  The pixel values of the scenario rasters should be set to the 'to' EVT, which
    looks up to the VALUE_10 field in 'tbl_cht_90_10_atts_gen_class_stock_change_lut'
    """
    import os
    import arcpy
    import Generic
    arcpy.CheckOutExtension("Spatial")
    import arcpy.sa

    Generic.add_to_logfile ("STARTING CARBON CHANGE MODULE-->")
    arcpy.env.overwriteOutput = True

    arcpy.env.workspace = Generic.ArcWorkspace
    arcpy.env.scratchWorkspace = Generic.ArcScratchWorkspace
    #arcpy.env.scratchFolder = ArcScratchFolder
    #arcpy.env.scratchGDB= ArcScratchGDB

    arcpy.env.extent = Generic.MASK
    arcpy.env.mask = Generic.MASK
    arcpy.env.cellSize = Generic.LANDFIRE
    arcpy.env.snapRaster = Generic.LANDFIRE

    if urban == 0:
        arcpy.CopyRaster_management(Generic.LANDFIRE, "temp_ras")
    elif urban == 1:
        arcpy.CopyRaster_management(Generic.LANDFIRE_URBAN, "temp_ras")

    arcpy.JoinField_management("temp_ras",in_field="CHT90_10",join_table=Generic.Carbon_Values,join_field="VALUE",fields="VALUE_90; VALUE_10;Mg_ac90;Mg_ac10;Mg_ac30;Mg_ac50")

    Generic.add_to_logfile("Extracting information from the landfire rasters and associated carbon tables...")

    #first create rasters - BL is the 30 BAU
    raster_dates =['90','10', '30NC','30BAU', '50NC', '50BAU']

    for i in raster_dates:
        if i in ('10', '30BAU', '30NC', '50BAU', '50NC'):
            outRaster = arcpy.sa.Lookup("temp_ras", "VALUE_" + '10' )
        else:
            outRaster = arcpy.sa.Lookup("temp_ras", "VALUE_" + i )

        outRaster2 = arcpy.sa.Int(outRaster)
        outRaster2.save("LU_" + i)
        arcpy.BuildRasterAttributeTable_management("LU_" + i, "Overwrite")

    if urban == 1:
        denras = arcpy.sa.Lookup("temp_ras", "DENSITY" )
        denras2 = arcpy.sa.Int(denras)
        denras2.save("DENSITY")
        arcpy.BuildRasterAttributeTable_management("DENSITY", "Overwrite")

    #this is where we flip pixels to create the 2030 raster.  First apply the BAU conversions
    #use generic->flip_pixels to create the to pixel values used here.
    Generic.add_to_logfile("Flipping pixels for urban and vineyard conversions and freezing pixels slated for conservation...")


    if arcpy.Exists(vineyard_conversion):
        outRaster= arcpy.sa.Con(arcpy.sa.IsNull(vineyard_conversion), "LU_30BAU", vineyard_conversion)
        outRaster_= arcpy.sa.Con(arcpy.sa.IsNull(vineyard_conversion), "LU_50BAU", vineyard_conversion)
    else:    #this just sets outraster to LUBAU since vineyard conversion doesn't exist
        outRaster = arcpy.sa.Raster("LU_30BAU")
        outRaster_ = arcpy.sa.Raster("LU_50BAU")

    if arcpy.Exists(urban_conversion):
        outRaster2= arcpy.sa.Con(arcpy.sa.IsNull(urban_conversion), outRaster, urban_conversion)
        outRaster2_= arcpy.sa.Con(arcpy.sa.IsNull(urban_conversion), outRaster_, urban_conversion)
    else:   #this just sets outraster 2 to outraster since urban conversion doesn't exist
        outRaster2 = outRaster
        outRaster2_ = outRaster_

    if (Generic.treatments_with_overlap):
        outRaster2.save("LU_temp")
        outRaster2_.save("L_U_temp")
        arcpy.Delete_management("LU_30BAU")
        arcpy.Delete_management("LU_50BAU")
        arcpy.CopyRaster_management("LU_temp", "LU_30BAU")  #replace BAU with raster just created that includes vineyard and urban conversions, will also be used downstream for scenarios
        arcpy.CopyRaster_management("L_U_temp", "LU_50BAU")
        # if the urban forestry inventory is selected on tool GUI, return all rasters with the urban forestry values instead of LandFire inventory
    else:
        outRaster2.save("LU_30")
        outRaster2_.save("LU_50")
        arcpy.Delete_management("LU_30BAU")
        arcpy.Delete_management("LU_50BAU")
        arcpy.CopyRaster_management("LU_30", "LU_30BAU")
        arcpy.CopyRaster_management("LU_50", "LU_50BAU")
        # if the urban forestry inventory is selected on tool GUI, join table and multiply

    counter = 1
    for i in Generic.treatments_with_overlap:
        Generic.add_to_logfile("Flipping pixels for the scenario...")
        treatment_raster = "TREATMENT_FINAL_" + str(counter-1) + "_30"
        treatment_raster2 = "TREATMENT_FINAL_" + str(counter-1) + "_50"

        if counter == 1:
            outRaster= arcpy.sa.Con(arcpy.sa.IsNull(treatment_raster), "LU_temp", treatment_raster)
            outRaster_= arcpy.sa.Con(arcpy.sa.IsNull(treatment_raster2), "L_U_temp", treatment_raster2)
        elif counter > 1:
            outRaster= arcpy.sa.Con(arcpy.sa.IsNull(treatment_raster), "LU_temp_" + str(counter-1), treatment_raster)
            outRaster_= arcpy.sa.Con(arcpy.sa.IsNull(treatment_raster2), "L_U_temp_" + str(counter-1), treatment_raster2)
        if counter == len(Generic.treatments_with_overlap):
            outRaster.save("LU_30")
            outRaster_.save("LU_50")
        else:
            outRaster.save("LU_temp_" + str(counter))
            outRaster_.save("L_U_temp_" + str(counter))
        counter = counter + 1

    final_outraster = Generic.CarbonRaster  #os.path.join(output_file_location, run_name + "_CARBON_ALL")
    final_outtable = Generic.CarbonStats   #os.path.join(output_file_location, run_name + "_CARBON_STATS")
    final_outtable_detail = Generic.CarbonStatsDetail
    final_outtable_urban = Generic.CarbonStatsUrban

    #combine the four rasters - 1990, 2010, 2030 BAU, and 2030 with conversions and scenarios applied
    Generic.add_to_logfile("**CALCULATING CARBON CHANGE**")
    ras_base_list = "LU_10;LU_90;LU_30;LU_50;LU_30BAU;LU_30NC;LU_50BAU;LU_50NC"
    if arcpy.Exists(os.path.join(arcpy.env.workspace, "ALL_TREAT")):
        ras_base_list = ras_base_list + ";ALL_TREAT"
    if urban == 1:
        ras_base_list = ras_base_list + ";DENSITY"
    outRaster = arcpy.sa.Combine(ras_base_list)
    outRaster.save(final_outraster)


    raster_dates.append('30')
    raster_dates.append('50')

    Generic.add_to_logfile("Adding carbon information to carbon change raster.")
    count_90 = 0
    count_10 = 0

    for i in raster_dates:
        #add and calc per acre and total carbon fields
        if i in ('90'):
            if count_90 == 0 and urban == 1:
                arcpy.JoinField_management(final_outraster,in_field="LU_" + i,join_table=Generic.Carbon_Values,join_field="VALUE_90",fields=['Gen_Class1990', "Mg_ac" + i])
            else:
                arcpy.JoinField_management(final_outraster,in_field="LU_" + i,join_table=Generic.Carbon_Values,join_field="VALUE_90",fields=["Mg_ac" + i])
            #arcpy.AlterField_management(final_outraster, 'tbl_cht_90_10_atts_gen_class_stock_change_lut.Gen_Class1990', 'GENCLASS' )
            count_90 = count_90 + 1

        else:
            if count_10 == 0 and urban == 1:
                arcpy.JoinField_management(final_outraster,in_field="LU_" + i,join_table=Generic.Carbon_Values,join_field="VALUE_10",fields=['gen_class2010_revised', "Mg_ac" + i ])

            #arcpy.AlterField_management(final_outraster, 'tbl_cht_90_10_atts_gen_class_stock_change_lut.Gen_Class1990', 'GENCLASS' )
            else:
                arcpy.JoinField_management(final_outraster,in_field="LU_" + i,join_table=Generic.Carbon_Values,join_field="VALUE_10",fields=["Mg_ac" + i])
            count_10 = count_10 + 1


        arcpy.AddField_management(final_outraster, "Tot_C_" + i, "FLOAT")
        if urban == 0:

            if i in('30', '50', '30BAU', '50BAU'):  #for these calculate them with area weighted numbers if they haven't flipped, otherwise give them base tons/acre
                arcpy.MakeTableView_management(final_outraster, "FORR" + i)
                arcpy.SelectLayerByAttribute_management("FORR" + i, "NEW_SELECTION", "LU_" + i + "<> LU_10")
                arcpy.CalculateField_management("FORR" + i, "Tot_C_" +i, "!Mg_ac" +i +"!*(0.222395*!COUNT!)", "PYTHON_9.3" )
                arcpy.SelectLayerByAttribute_management("FORR" + i, "NEW_SELECTION", "LU_" + i + "= LU_10")
                arcpy.CalculateField_management("FORR" + i, "Tot_C_" +i, "!Mg_ac" +i[0:2] +"NC!*(0.222395*!COUNT!)", "PYTHON_9.3" )

            else:
                arcpy.CalculateField_management(final_outraster, "Tot_C_" +i, "!Mg_ac" +i +"!*(0.222395*!COUNT!)", "PYTHON_9.3" )
        elif urban == 1:
            arcpy.MakeTableView_management(final_outraster, "FORR" + i)
            if i == '90':
                arcpy.SelectLayerByAttribute_management("FORR" + i, "NEW_SELECTION", "gen_class2010_revised = 'Urban'")
                arcpy.CalculateField_management("FORR" + i, "Tot_C_" +i, "168.73*(0.222395*!COUNT!*!DENSITY!*.01)", "PYTHON_9.3" )
                arcpy.CalculateField_management("FORR" + i, "Mg_ac" +i, "168.73*(!DENSITY!*.01)", "PYTHON_9.3" )
                arcpy.SelectLayerByAttribute_management("FORR" + i, "NEW_SELECTION", "gen_class2010_revised <> 'Urban'")
                arcpy.CalculateField_management("FORR" + i, "Tot_C_" +i, "!Mg_ac" +i +"!*(0.222395*!COUNT!)", "PYTHON_9.3" )
            else:
                #!!!add carbon here so that if new landfire class is urban to grow, then the calculation increases density**
                arcpy.SelectLayerByAttribute_management("FORR" + i, "NEW_SELECTION", "gen_class2010_revised = 'Urban'")
                arcpy.CalculateField_management("FORR" + i, "Tot_C_" +i, "168.73*(0.222395*!COUNT!*!DENSITY!*.01)", "PYTHON_9.3" )
                arcpy.CalculateField_management("FORR" + i, "Mg_ac" +i, "168.73*(!DENSITY!*.01)", "PYTHON_9.3" )
                #just added the above - 2/6/15

                #now calculate total carbon and tons/acre for areas in the urban forest treatment (LU_10 = 999) - this overwrites the step above for just
                #randomly selected treatment pixels in 2030 and 2050 (non-BAU and non-NC)
                if i == '30':
                    arcpy.SelectLayerByAttribute_management("FORR" + i, "NEW_SELECTION", "LU_30 = 999")
                    arcpy.CalculateField_management("FORR" + i, "Tot_C_" +i, "(168.73*(0.222395*!COUNT!*(!DENSITY!*1.15)*.01))", "PYTHON_9.3" )
                    arcpy.CalculateField_management("FORR" + i, "Mg_ac" +i, "(168.73*(!DENSITY!*1.15)*.01)", "PYTHON_9.3" )
                if i == '50':
                    arcpy.SelectLayerByAttribute_management("FORR" + i, "NEW_SELECTION", "LU_30 = 999")
                    arcpy.CalculateField_management("FORR" + i, "Tot_C_" +i, "(168.73*(0.222395*!COUNT!*(!DENSITY!*1.3)*.01))", "PYTHON_9.3" )
                    arcpy.CalculateField_management("FORR" + i, "Mg_ac" +i, "(168.73*(!DENSITY!*1.3)*.01)", "PYTHON_9.3" )


                if i in('30', '50', '30BAU', '50BAU'):  #below cals just for non-urban areas - for these calculate them with area weighted numbers if they haven't flipped, otherwise give them base tons/acre
                    arcpy.SelectLayerByAttribute_management("FORR" + i, "NEW_SELECTION", "gen_class2010_revised <> 'Urban'")
                    arcpy.SelectLayerByAttribute_management("FORR" + i, "SUBSET_SELECTION", "LU_" + i + "<> LU_10")
                    arcpy.CalculateField_management("FORR" + i, "Tot_C_" +i, "!Mg_ac" +i +"!*(0.222395*!COUNT!)", "PYTHON_9.3" )
                    arcpy.SelectLayerByAttribute_management("FORR" + i, "NEW_SELECTION", "gen_class2010_revised <> 'Urban'")
                    arcpy.SelectLayerByAttribute_management("FORR" + i, "SUBSET_SELECTION", "LU_" + i + "= LU_10")
                    arcpy.CalculateField_management("FORR" + i, "Tot_C_" +i, "!Mg_ac" +i[0:2] +"NC!*(0.222395*!COUNT!)", "PYTHON_9.3" )

                else:
                    arcpy.SelectLayerByAttribute_management("FORR" + i, "NEW_SELECTION", "gen_class2010_revised <> 'Urban'")
                    arcpy.CalculateField_management("FORR" + i, "Tot_C_" +i, "!Mg_ac" +i +"!*(0.222395*!COUNT!)", "PYTHON_9.3" )
            #first create final out raster
            #then multi
            #multiply by new field that is canopy cover - this raster just has the 1-6440 values combined with land cover (97000 + values)
            #arcpy.Selec
        arcpy.Delete_management("LU_" + i)
    arcpy.Delete_management("temp_ras")



    #first create an urban table output (shows just urban areas) - and a summary table for all areas
    arcpy.MakeTableView_management(final_outraster,'URB', 'LU_10 IN (173, 19, 25, 24, 9, 34, 26, 21, 118, 92, 95, 100, 91)')
    arcpy.Statistics_analysis(in_table='URB',out_table= final_outtable_urban,statistics_fields="Tot_C_10 SUM;Tot_C_30BAU SUM;Tot_C_30NC SUM;Tot_C_30 SUM;Tot_C_50BAU SUM;Tot_C_50NC SUM;Tot_C_50 SUM",case_field="#")
    arcpy.Statistics_analysis(in_table= final_outraster,out_table= final_outtable,statistics_fields="Tot_C_90 SUM;Tot_C_10 SUM;Tot_C_30BAU SUM;Tot_C_30NC SUM;Tot_C_30 SUM;Tot_C_50BAU SUM;Tot_C_50NC SUM;Tot_C_50 SUM",case_field="#")

    #now create a detail table if there was treatment
    if arcpy.Exists(os.path.join(arcpy.env.workspace, "ALL_TREAT")):
        arcpy.Statistics_analysis(in_table= final_outraster,out_table= final_outtable,statistics_fields="Tot_C_90 SUM;Tot_C_10 SUM;Tot_C_30NC SUM;Tot_C_30BAU SUM;Tot_C_30 SUM;Tot_C_50NC SUM;Tot_C_50BAU SUM;Tot_C_50 SUM",case_field="#")
        arcpy.Statistics_analysis(in_table= final_outraster,out_table= final_outtable_detail,statistics_fields="Tot_C_90 SUM;Tot_C_10 SUM;Tot_C_30BAU SUM;Tot_C_30NC SUM;Tot_C_30 SUM;Tot_C_50BAU SUM;Tot_C_50NC SUM;Tot_C_50 SUM",case_field="ALL_TREAT")




    layers_to_delete_at_finish = ["LU_temp", "LU_temp_1", "LU_temp_2", "L_U_temp", "L_U_temp_1", "L_U_temp_2"]
    for i in layers_to_delete_at_finish:
        try:
            if arcpy.Exists(i):
                arcpy.Delete_management(i)
        except:
            Generic.add_to_logfile ("Unable to delete " + i)