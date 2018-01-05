#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Dylan
#
# Created:     27/11/2017
# Copyright:   (c) Dylan 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import calculations, arcpy, os, zipfile, pandas, MercedRasterProcessing
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
ws = "D:/TGS/projects/64 - Merced Carbon/MBA/Deliverables from TNC/Urban Footprint/data/rasters/Clipped"
arcpy.env.workspace = calculations.rev_slash(ws)
arcpy.env.overwriteOutput = 1

import arcpy
first = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/ViewPoints.gdb/Points1'
second = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/ViewPoints.gdb/Points2'
third = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/ViewPoints.gdb/Points3'
fourth = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/ViewPoints.gdb/Points4'
fifth = 'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Vector/ViewPoints.gdb/Points5'
def ObsPts (inObsPoints, outputpath):
    # Set local variables'
    inRaster = "D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/DEM/Merced_DEM_Clipped.tif"
    zFactor = 1
    useEarthCurv = "CURVED_EARTH"
    refractionVal = 0.13

    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    # Execute ObserverPoints
    outObsPoints = ObserverPoints(inRaster, inObsPoints, zFactor,
                                  useEarthCurv, refractionVal)

    # Save the output
    outObsPoints.save(outputpath)

##ObsPts(first,'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/Viewsheds/Viewsheds.gdb/First')
##ObsPts(second,'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/Viewsheds/Viewsheds.gdb/Second')
##ObsPts(third,'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/Viewsheds/Viewsheds.gdb/Third')
ObsPts(fourth,'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/Viewsheds/Viewsheds.gdb/Fourth')
ObsPts(fifth,'D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/Viewsheds/Viewsheds.gdb/Fifth')
arcpy.env.workspace = calculations.rev_slash('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/Viewsheds/Viewsheds.gdb')

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "First"
arcpy.AddField_management(in_table="First", field_name="Total", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table="Second", field_name="Total", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table="Third", field_name="Total", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table="Fourth", field_name="Total", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table="Fifth", field_name="Total", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "First"
arcpy.CalculateField_management(in_table="First", field="Total", expression="!OBS1!+ !OBS2!+ !OBS3!+ !OBS4!+ !OBS5!+ !OBS6!+ !OBS7!+ !OBS8!+ !OBS9!+ !OBS10!+ !OBS11!+ !OBS12!+ !OBS13!+ !OBS14!+ !OBS15!+ !OBS16!", expression_type="PYTHON_9.3", code_block="")
arcpy.CalculateField_management(in_table="Second", field="Total", expression="!OBS1!+ !OBS2!+ !OBS3!+ !OBS4!+ !OBS5!+ !OBS6!+ !OBS7!+ !OBS8!+ !OBS9!+ !OBS10!+ !OBS11!+ !OBS12!+ !OBS13!+ !OBS14!+ !OBS15!+ !OBS16!", expression_type="PYTHON_9.3", code_block="")
arcpy.CalculateField_management(in_table="Third", field="Total", expression="!OBS1!+ !OBS2!+ !OBS3!+ !OBS4!+ !OBS5!+ !OBS6!+ !OBS7!+ !OBS8!+ !OBS9!+ !OBS10!+ !OBS11!+ !OBS12!+ !OBS13!+ !OBS14!+ !OBS15!+ !OBS16!", expression_type="PYTHON_9.3", code_block="")
arcpy.CalculateField_management(in_table="Fourth", field="Total", expression="!OBS1!+ !OBS2!+ !OBS3!+ !OBS4!+ !OBS5!+ !OBS6!+ !OBS7!+ !OBS8!+ !OBS9!+ !OBS10!+ !OBS11!+ !OBS12!+ !OBS13!+ !OBS14!+ !OBS15!+ !OBS16!", expression_type="PYTHON_9.3", code_block="")
arcpy.CalculateField_management(in_table="Fifth", field="Total", expression="!OBS1!+ !OBS2!+ !OBS3!+ !OBS4!+ !OBS5!+ !OBS6!+ !OBS7!+ !OBS8!+ !OBS9!+ !OBS10!+ !OBS11!+ !OBS12!+ !OBS13!+ !OBS14!+ !OBS15!+ !OBS16!", expression_type="PYTHON_9.3", code_block="")

temp = Lookup("First","Total") + Lookup("Second","Total") + Lookup("Third","Total") + Lookup("Fourth","Total") + Lookup("Fifth","Total")
temp.save('D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Raster/Viewsheds/Viewsheds.gdb/Combined')