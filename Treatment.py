

#def create_treatment_scenario(treatment, treatment_input):
def create_treatment_scenario(treatment_list, user_treatment_area):
    """Function creates TREATMENT raster ...
    """
    import arcpy
    import Generic
    import os

    arcpy.env.overwriteOutput = True
 #   Generic.set_paths_and_workspaces('D:/temp/carbon_scratch/scratch.gdb', 'D:/CLOUD/Shared/Open Space/', 25000, 7500, 'D:/temp/carbon_scratch/scratch.gdb/ZZZZ', 'Carbon Framework/GIS Data/MASTER_DATA/', 'D:/temp/carbon_scratch/scratch.gdb' )

    arcpy.env.workspace = Generic.ArcWorkspace
    arcpy.env.scratchWorkspace = Generic.ArcScratchWorkspace

    #Treatment options
    #"None"
    all_masks = os.path.join(arcpy.env.workspace, "ALL_TREAT0")
    all_masks1 = os.path.join(arcpy.env.workspace, "ALL_TREAT1")
    all_masks2 = os.path.join(arcpy.env.workspace, "ALL_TREAT")
    for c in [all_masks, all_masks1, all_masks2]:
        if arcpy.Exists(c):
            arcpy.Delete_management(c)

    if not (treatment_list):
        Generic.add_to_logfile("No treatments selected for this run...")
    else:
        count = 0
        for i in treatment_list:

            if i[1] == Generic.Zoning:
                treatment_query = 'TP = 1'
                treatment_lut = Generic.TP_TREATMENT_LUT

            elif i[1] == Generic.FireHazard:
                treatment_query = 'OBJECTID = 285'
                treatment_lut = Generic.FIRE_TREATMENT_LUT

            elif i[1] == Generic.BuckeyeRRD:
                treatment_query = 'TP = 1'
                treatment_lut = Generic.URBAN_CONVERSION_LUT

            elif i[1] == Generic.PresRanchVineyards:
                treatment_query = 'VINEYARD = 1'
                treatment_lut = Generic.VINEYARD_CONVERSION_LUT

            elif i[1] == Generic.PresRanchEstates:
                treatment_query = 'TP = 1'
                treatment_lut = Generic.URBAN_CONVERSION_LUT

            elif i[1] == Generic.RiparianRestoration:
                treatment_query = 'OBJECTID >= 0'
                treatment_lut = Generic.RIPARIAN_TREATMENT_LUT

            elif i[1]  == Generic.OakRestoration:
                treatment_query = 'OBJECTID >= 0'
                treatment_lut = Generic.OAK_TREATMENT_LUT

            elif i[1] == Generic.UrbanTree:
                treatment_query = 'CENSUS_URBAN = 1 AND BUILDING_ROAD_FLAG = 0'
                treatment_lut = Generic.URBAN_TREE_LUT

            # User Defined Treatment Area
            polys2 = 0
            if user_treatment_area != "None":
                arcpy.MakeFeatureLayer_management (i[1], "temp_trt1")
                arcpy.SelectLayerByAttribute_management("temp_trt1", "NEW_SELECTION", treatment_query)
                arcpy.Intersect_analysis(["temp_trt1", user_treatment_area], "temp_trt2")
                res = arcpy.GetCount_management("temp_trt2")
                polys2= int(res[0])


            polys = Generic.check_for_overlap(Generic.VECTOR_MASK, i[1], treatment_query)


            if polys >0 and polys2 >0 and user_treatment_area!="None":
                Generic.treatments_with_overlap.append(i[0])
            elif polys >0 and user_treatment_area=="None":
                Generic.treatments_with_overlap.append(i[0])
            if polys == 0:
                Generic.add_to_logfile ("No overlap between treatment layer " + i[1] + " and user selected processing region " + Generic.VECTOR_MASK + " - skipping treatment module...")

            elif polys >0 and polys2 ==0 and user_treatment_area!="None":
                Generic.add_to_logfile ("No overlap between user defined treatment area " + user_treatment_area + " and processing area " + Generic.VECTOR_MASK + " inside of the treatment mask - skipping treatment module...")


            else:
                masks_to_mosaic= []
                Generic.add_to_logfile ("STARTING TREATMENT MODULE-->\n")
                Generic.add_to_logfile("Running treatments for " + i[1])
                import os
                from arcpy import env
                from arcpy.sa import *
                import Generic
                arcpy.CheckOutExtension("Spatial")
                arcpy.env.overwriteOutput = True

                arcpy.env.extent = Generic.MASK
                arcpy.env.cellSize = Generic.LANDFIRE
                arcpy.env.mask = Generic.MASK
                arcpy.env.snapRaster = Generic.LANDFIRE

                #Create mask of treatment zone (eg. parcels zoned as timberland)
                        #Create local variables
                Generic.add_to_logfile("Selecting treatment areas ...")

                if user_treatment_area != "None":
                    arcpy.MakeFeatureLayer_management("temp_trt2", "treatment")

                else:
                    arcpy.MakeFeatureLayer_management (i[1], "treatment")
                    arcpy.SelectLayerByAttribute_management("treatment", "NEW_SELECTION", treatment_query)

                treatment_mask = os.path.join(arcpy.env.workspace, "TREATMENT_MASK" + "_" + str(count) )
                treatment_mask_dub = os.path.join(arcpy.env.workspace, "TREATMENT_MASK_DUB" + "_" + str(count) )
                treatment_mask_rep = os.path.join(arcpy.env.workspace, "TREAT" + "_" + str(count) )

                #treatment_final = os.path.join(arcpy.env.workspace, "TREATMENT_FINAL" + "_" + str(count))
                treatment_final = os.path.join(arcpy.env.workspace, "TREATMENT_FINAL" + "_" + str(count) + "_30")
                treatment_final2 = os.path.join(arcpy.env.workspace, "TREATMENT_FINAL" + "_" + str(count) + "_50")


##                global treatment_final
##                treatment_final = os.path.join(arcpy.env.workspace, "TREATMENT_FINAL")
                #make sure areas already converted to vineyard or rural residential aren't treated

                #Create updated LANDFIRE dataset with VALUE_10 field
                Generic.add_to_logfile("Setting up rasters ...")
                arcpy.CopyRaster_management(Generic.LANDFIRE, "temp_ras")
                arcpy.JoinField_management("temp_ras",in_field="CHT90_10",join_table=Generic.Carbon_Values,join_field="VALUE",fields="VALUE_10")

                #first create raster
                outRaster = arcpy.sa.Lookup("temp_ras", "VALUE_" + '10' )
                outRaster2 = arcpy.sa.Int(outRaster)
                outRaster2.save("LU_" + '10')
                arcpy.BuildRasterAttributeTable_management("LU_" + '10', "Overwrite")

                #If this is improved forest management, modify treatment mask
                #so that includes random selection of subset of pixels
                if i[0] in ("Improved Conifer Forest Management", "Riparian Area Restoration", "Valley Oak Restoration", "Urban Tree Planting"):
                    arcpy.JoinField_management("temp_ras",in_field="VALUE_10",join_table=treatment_lut,join_field="VALUE_2010",fields="PCT_PIX")
                    PorMask = arcpy.sa.Lookup("temp_ras", "PCT_PIX")
                    PorMask2 = arcpy.sa.ExtractByMask(PorMask, "treatment")
                    Por_In= os.path.join(arcpy.env.workspace, "POR_IN" + str(count))
                    Por_Out = os.path.join(arcpy.env.workspace, "POR_OUT" + str(count))
                    PorMask2.save(Por_In)
                    Generic.create_random_raster(Por_In, Por_Out)
                    #now mask out areas not randomly selected
                    random_sel = arcpy.sa.Con(((arcpy.sa.Raster(Por_Out) == 1) & (arcpy.sa.Raster("LU_10") >= 0)), arcpy.sa.Raster("LU_10"))
                    random_sel_dub = arcpy.sa.Con(((arcpy.sa.Raster(Por_Out) >= 1) & (arcpy.sa.Raster("LU_10") >= 0)), arcpy.sa.Raster("LU_10"))
                    random_sel.save("tr1")
                    random_sel_dub.save ("tr1_dub" + str(count))

                else:    #Extract raster by treatment mask only, no need for random raster
                    Generic.add_to_logfile("Extracting raster by treatment mask ...")
                    arcpy.gp.ExtractByMask_sa("LU_" + '10', "treatment", "tr1")
                    arcpy.gp.ExtractByMask_sa("LU_" + '10', "treatment", "tr1_dub" + str(count))



                #Erase converted vineyards/urban areas
                if arcpy.Exists(Generic.vineyard_out_raster):
                    tr2 = arcpy.sa.Con(arcpy.sa.IsNull(Generic.vineyard_out_raster), "tr1")
                    tr2_dub = arcpy.sa.Con(arcpy.sa.IsNull(Generic.vineyard_out_raster), "tr1_dub" + str(count))
                else:
                    tr2 = arcpy.sa.Raster("tr1")
                    tr2_dub =arcpy.sa.Raster("tr1_dub" + str(count))
                if arcpy.Exists(Generic.urban_out_raster):
                    tr3 = arcpy.sa.Con(arcpy.sa.IsNull(Generic.urban_out_raster), tr2)
                    tr3_dub =arcpy.sa.Con(arcpy.sa.IsNull(Generic.urban_out_raster), tr2_dub)
                else:
                    tr3 = tr2
                    tr3_dub = tr2_dub

                tr3.save(treatment_mask)
                tr3_dub.save(treatment_mask_dub)



                if i[0] == "Improved Conifer Forest Management":
                    tr4 = arcpy.sa.Con(arcpy.sa.IsNull(arcpy.sa.Raster(treatment_mask_dub)), 0, arcpy.sa.Raster(treatment_mask_dub))
                else:
                    tr4 = arcpy.sa.Con(arcpy.sa.IsNull(arcpy.sa.Raster(treatment_mask)), 0, arcpy.sa.Raster(treatment_mask))

                tr5 = arcpy.sa.Con(tr4>0, count + 1, tr4)
                tr5.save("HH" + str(count))



                #new grid used to flip pixels based on lookup table
                Generic.add_to_logfile("Grab to and from EVTs for chosen treatment ...")
                arcpy.AddMessage(treatment_mask)
                arcpy.AddMessage(treatment_final)
                arcpy.AddMessage(treatment_lut)
                Generic.flip_pixels(treatment_mask, treatment_final, treatment_lut, lut_field="VALUE_2030")
                if i[0] <> "Improved Conifer Forest Management":
                    Generic.flip_pixels(treatment_mask, treatment_final2, treatment_lut, lut_field="VALUE_2050")
                else:
                    Generic.flip_pixels(treatment_mask_dub, treatment_final2, treatment_lut, lut_field="VALUE_2050")


                Generic.add_to_logfile ("ENDING TREATMENT MODULE-->\n")
                count = count +1

            if count == 1:
                arcpy.CopyRaster_management("HH0", all_masks)
            elif count == 2:
                st1 = arcpy.sa.Con(arcpy.sa.Raster("HH1")==2, arcpy.sa.Raster("HH1"), arcpy.sa.Raster("HH0") )
                st1.save(all_masks)
            elif count == 3:
                st1 = arcpy.sa.Con(arcpy.sa.Raster("HH2")==3, arcpy.sa.Raster("HH2"), arcpy.sa.Raster("HH1") )
                st2 = arcpy.sa.Con(st1>0, st1, arcpy.sa.Raster("HH0") )
                st2.save(all_masks)
            if arcpy.Exists(Generic.vineyard_out_raster) and count>0:
                lov = arcpy.sa.Con(arcpy.sa.IsNull(Generic.vineyard_out_raster), 0, 5)
                st3 = arcpy.sa.Con(lov ==5, lov, arcpy.sa.Raster(all_masks))
                st3.save(all_masks1)
            elif count>0:
                #all_masks1 = all_masks
                arcpy.Rename_management(all_masks, all_masks1)
            if arcpy.Exists(Generic.urban_out_raster) and count>0:
                lov2 = arcpy.sa.Con(arcpy.sa.IsNull(Generic.urban_out_raster), 0, 5)
                st4 = arcpy.sa.Con(lov2 ==5, lov2, arcpy.sa.Raster(all_masks1))
                st4.save(all_masks2)
            elif count>0:
                #all_masks2 = all_masks1
                arcpy.Rename_management(all_masks1, all_masks2)

        layers_to_delete_at_finish = ["HH0", "HH1", "HH2", "tr1", "tr1_dub0", "tr1_dub1", "tr1_dub2", "POR_IN0", "POR_OUT0","POR_OUT0_","POR_OUT", "POR_OUT_", "POR_OUT1", "POR_OUT1_", "POR_OUT2", "POR_OUT2_"]

        for i in layers_to_delete_at_finish:
            try:
                if arcpy.Exists(i):
                    arcpy.Delete_management(i)
            except:
                Generic.add_to_logfile ("Unable to delete " + i)

