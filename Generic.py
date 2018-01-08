from __future__ import unicode_literals #Can Delete This
def set_paths_and_workspaces(workspace = 'P:/Temp', root_data_path = 'E:/mercedtool', mask_fc = 'D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Vectors.gdb/Test_Mask', CVA_List_L = '', midpath = 'MASTER_DATA', output_file_loc = 'P:/Temp', run_name = 'Test', conservation_fc = ''):
    """Workspace must be a file .gdb and is the place where all temp files and outputs will be placed.
    root_data_path -->  This path the top level folder for the data files (e.g., D:/CLOUD/Shared/Open Space/)
    midpath -->  This path is the path to the data files from roopath down the tree (e.g., Carbon Framework/GIS Data/SAMPLE_DATA/)
    """

    import arcpy
    import os
    import sys
    import pandas as pd
    arcpy.env.overwriteOutput = True


    arcpy.env.workspace = output_file_loc
    arcpy.env.scratchWorkspace = output_file_loc


    global ArcWorkspace
    ArcWorkspace = output_file_loc

    global ArcScratchWorkspace
    ArcScratchWorkspace = output_file_loc


    all_layers = []

    global LANDFIRE2001
##    LANDFIRE2001 = os.path.join(root_data_path, midpath, 'Rasters.gdb/LF2001_Combined')
    LANDFIRE2001 ='D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Landcover_Rasters/Landcover_2001.tif'
    all_layers.append(LANDFIRE2001)

    global LANDFIRE2014
##    LANDFIRE2014 = os.path.join(root_data_path, midpath, 'Rasters.gdb/LF2014_Combined')
    LANDFIRE2014 ='D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Landcover_Rasters/Landcover_2014.tif'
    all_layers.append(LANDFIRE2014)

    global SPATIAL_REFERENCE_TEXT
    SPATIAL_REFERENCE_TEXT = "PROJCS['NAD_1983_California_Teale_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',-4000000.0],PARAMETER['Central_Meridian',-120.0],PARAMETER['Standard_Parallel_1',34.0],PARAMETER['Standard_Parallel_2',40.5],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
    arcpy.env.cellSize = LANDFIRE2014
    arcpy.env.snapRaster = LANDFIRE2014

    global pts
    #Set Local Variables
    ##
    #Paths

    global tempwork
    tempwork = workspace

    global RDP
    RDP = root_data_path

    global MP
    MP = midpath

    global Root_Mid_Path
    Root_Mid_Path = os.path.join(RDP, MP)

    global tempgdb
    tempgdb = os.path.join(root_data_path,midpath,'temppts.gdb')

    global MBTABS
    MBTABS = os.path.join(root_data_path,midpath,'Tables/MBATables')

    global neartabs
    neartabs = os.path.join(root_data_path,midpath,'Tables/NearTables')

    global vects
    vects = os.path.join(root_data_path,midpath,'Vectors.gdb')

    global lutables
    lutables = os.path.join(root_data_path,midpath,'LUTables')

    global valuetables
    valuetables = os.path.join(root_data_path,midpath,'Tables')

    global WS
    WS = workspace



    #Vectors
    global Points
    Points = os.path.join('D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Vectors.gdb/LFC_Points_Merged')
    all_layers.append(Points)

    #Tables
    global Points_Table
    Points_Table = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'pointsmerged.csv')
    all_layers.append(Points_Table)

    global Carbon2001
    Carbon2001 = os.path.join(root_data_path, midpath, 'Tables/CarbonTables/Carb01.csv')
    all_layers.append(Carbon2001)

    global Carbon2014
    Carbon2014 = os.path.join(root_data_path, midpath, 'Tables/CarbonTables/Carb14.csv')
    all_layers.append(Carbon2014)

    global Carbon2030
    Carbon2030 = os.path.join(root_data_path, midpath, 'Tables/CarbonTables/Carb30.csv')
    all_layers.append(Carbon2030)

    global calenviro
    calenviro = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_calenviro.csv')
    all_layers.append(calenviro)

    global fmmp
    fmmp = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_fmmp.csv')
    all_layers.append(fmmp)

    global genplan
    genplan = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_genplan.csv')
    all_layers.append(genplan)

    global hydrovuln
    hydrovuln = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_hydrovuln.csv')
    all_layers.append(hydrovuln)

    global slope
    slope = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_slope.csv')
    all_layers.append(slope)

    global scenic
    scenic = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_scenic.csv')
    all_layers.append(scenic)


    global lc
    lc = os.path.join(root_data_path,midpath,'Tables/ValueTables', 'env_landcovers.csv')
    all_layers.append(lc)


    #Near Tables
    global near_river
    near_river = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_rivers.csv')
    all_layers.append(near_river)

    global near_rip
    near_rip = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_riparian.csv')
    all_layers.append(near_rip)

    global near_streams
    near_streams = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_streams.csv')
    all_layers.append(near_streams)

    global near_cpad
    near_cpad = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_cpad.csv')
    all_layers.append(near_cpad)

    global near_nwi
    near_nwi = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_nwi.csv')
    all_layers.append(near_nwi)

#    global near_fema
#    near_fema = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_fema.csv')
#    all_layers.append(near_fema)

    global near_roads
    near_roads = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_roads.csv')
    all_layers.append(near_roads)

    global near_woodyrip
    near_woodyrip = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_woodyrip.csv')
    all_layers.append(near_woodyrip)

    global near_woodycrop
    near_woodycrop = os.path.join(root_data_path, midpath, 'Tables/NearTables/env_near_woodycrop.csv')
    all_layers.append(near_woodycrop)

    #Lookup Tables
    global NitrateLU
    NitrateLU = os.path.join(root_data_path, midpath, 'Tables/LUTables/lut_nitrates.csv')
    all_layers.append(NitrateLU)

    global WaterUse
    WaterUse = os.path.join(root_data_path, midpath, 'Tables/LUTables/lut_wateruse.csv')
    all_layers.append(WaterUse)

    global Resistance
    Resistance = os.path.join(root_data_path, midpath, 'Tables/LUTables/lut_resistance.csv')
    all_layers.append(Resistance)

    global Crop_Value_LUT
    Crop_Value_LUT = os.path.join(root_data_path, midpath, 'Tables/LUTables/lut_crop_value.csv')
    all_layers.append(Crop_Value_LUT)

    global Air_Pollution
    Air_Pollution = os.path.join(root_data_path, midpath, 'Tables/LUTables/lut_air_pollution.csv')
    all_layers.append(Air_Pollution)

    global Activity_LUT
    Activity_LUT = os.path.join(root_data_path, midpath, 'Tables/trt/trt_reductions.csv')
    all_layers.append(Activity_LUT)




    #MISC
    global run_
    run = run_name
    #Outputs
    global CarbonRaster
    CarbonRaster = os.path.join(output_file_loc, run_name + "_CARBON_ALL")
    global CarbonStats
    CarbonStats = os.path.join(output_file_loc, run_name + "_CARBON_STATS")
    global CarbonStatsDetail
    CarbonStatsDetail = os.path.join(output_file_loc, run_name + "_CARBON_STATS_DETAIL")
    global CarbonStatsUrban
    CarbonStatsUrban = os.path.join(output_file_loc, run_name + "_CARBON_STATS_URBAN")

    #other vars
    vineyard_count =0
    global rr_count
    rr_count =0

    global treatments_with_overlap
    treatments_with_overlap =[]

    global output_gdb
    output_gdb = output_file_loc
    #parse CVA_list

    #send error if any of the above layers don't exist on their specified path
    for layer in all_layers:
        if not arcpy.Exists(layer):
            print("Layer or dataset: " + layer + " doesn't exist")
            arcpy.AddMessage("Layer or dataset: " + layer + " doesn't exist")
            sys.exit()

    #set mask
    global MASK
    global VECTOR_MASK
    if mask_fc == "None":
        arcpy.AddMessage("Using county boundary as processing area...")
        MASK = os.path.join(root_data_path, midpath, 'Vectors.gdb/Mask_Dissolved')
        VECTOR_MASK = os.path.join(root_data_path, midpath, 'Vectors.gdb/Mask_Dissolved')
    else:
        VECTOR_MASK = mask_fc
        arcpy.AddMessage("Using user-defined data area as processing area...")
        #first check coordinate system and project if necessary
        desc= arcpy.Describe(mask_fc)
        desc2 = arcpy.Describe(LANDFIRE2014)
        sr_mask = desc.spatialReference
        sr_landfire =  desc2.spatialReference

        if sr_mask.Name != sr_landfire.Name:
            arcpy.AddMessage ("Projecting user-defined processing area...")
            arcpy.Project_management(mask_fc, os.path.join(arcpy.env.workspace,"MASK"), SPATIAL_REFERENCE_TEXT)
            MASK = os.path.join(arcpy.env.workspace,"MASK")
            all_layers.append(MASK)

        else:
            MASK = mask_fc

    all_layers.append(MASK)
    all_layers.append(VECTOR_MASK)



    #create logfile
    global logfile
    logfile = open(os.path.join(output_file_loc, "logfile.txt"), "w")
    logfile.close()
    logfile = os.path.join((output_file_loc), "logfile.txt")


# Slope_threshold Function
# Creates percent slope and binary raster based on a specified threshold
# A value of 1 represents a pixel that exceeds the threshold

#Join data
#Create new layer
def join_layers(inLayer,LayerName, LayerJoinField, JoinTableName, TableJoinField,Output):
    arcpy.MakeFeatureLayer_management (inLayer, LayerName)
    arcpy.AddJoin_management( LayerName, LayerJoinField, JoinTableName, TableJoinField)
    arcpy.CopyFeatures_management( LayerName, Output)


#Check if field name exists
def check_field(layer_name, fieldname):
    """check to see if a field exists, returns 1 if it does"""
    res = 0
    for i in arcpy.ListFields(layer_name):
        if i.name==fieldname:
            res = res + 1
        else:
            res = res

    return res

#Check if index exists
def check_index(layer_name, indexname):
    """check to see if an index exists, returns 1 if it does"""
    res = 0
    for i in arcpy.ListIndexes(layer_name):
        if i.name==indexname:
            res = res + 1
        else:
            res = res

    return res

def create_rectangular_buffer(in_points, vineyard_fc_name, conversion_type, acreage_cap, threat_outlines):
    """This function creates rectangular polygons for all points in input fc.
    The input point feature class can be of type point or mulitpoint.
    The input point feature class must be in a projected coordinate system,
    and the polygon feature class will be created with the same spatial reference.
    Each new polygon will have a RefID attribute with the ObjectID of the point that it was created from.
    The height and width of the polygons are supplied by the user when the tool is run.
    Height and width parameters are to be entered in the units used by the projected coordinate system.
    The optional rotation angle parameter is to be entered in degrees [-360, 360].
    Required Inputs: Existing point feature class in a projected coordinate system,
    Output path for the new polygon feature class of type workspace,
    New polygon feature class name,
    New polygon height in units of the projected coordinate system,
    New polygon width in units of the projected coordinate system

    calling -->  create_rectangular_buffer('D:/temp/carbon_scratch/scratch.gdb/TEST_POINTS2',
    'D:/temp/carbon_scratch/scratch.gdb', 'VINNY', 200, 500) """


    import arcpy, sys, math, os

    def return_geometry(rectangle_height, rectangle_width, rotation=0):
        try:
            #Height for the rectangle
            global ht
            ht = rectangle_height
            #Width for the rectangle
            global width
            width = rectangle_width
            #Optional rotation parameter
            global delta
            delta = rotation
            #Calculate the length of the radius of the circumcircle
            r = math.sqrt(((float(ht)/2))**2 + ((float(width))/2)**2)
            #Calculate the angle in quadrant 1 for a nonrotated rectangle
            theta = math.degrees(math.atan((float(ht)/2)/((float(width))/2)))
            #Calculate the four angles made by the rectangle's diagonals once the rectangle is rotated by delta
            angles = (theta - delta, -theta - delta, 180 + theta - delta, 180 - theta - delta)
            #Calculate the x,y coordinates of a rotated rectangle's vertices when the rectangle is centered on the origin (0,0)
            xylist = [(r*math.cos(math.radians(a)), r*math.sin(math.radians(a))) for a in angles]
            return xylist
        except:
            sys.exit("Math errors")


    #first do nearest on in_points
    arcpy.Near_analysis(in_points, threat_outlines, "#", "#", "ANGLE", "GEODESIC")

    #if it's urbanization, do an identity with the zoning layer
    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    if conversion_type == "URBAN":
        zoning_identity = os.path.join(arcpy.env.workspace, "ZONING_IDENTITY")
        arcpy.Identity_analysis(in_features=in_points, identity_features=Zoning,out_feature_class=zoning_identity,join_attributes="ALL",cluster_tolerance="#",relationship="NO_RELATIONSHIPS")
        in_points = zoning_identity

    #Point Feature Class that the rectangular buffers will be created around
    ptfc = in_points
    #Path for Output Polygon Feature Class

    #Name for new polygon feature class
    pgnfcname = os.path.basename(vineyard_fc_name)
    #Polygon feature class
    pgnfcpath = os.path.split(vineyard_fc_name)[0]

    pgnfc=  vineyard_fc_name

    ####Get the field name for the object id field of the point feature class

    oidfldname = arcpy.Describe(ptfc).OIDFieldName


    ####Delete the polygon feature class if it already exists

    if arcpy.Exists(pgnfcname):
    	arcpy.Delete_management(pgnfc)
    	arcpy.AddMessage("Existing feature class " + pgnfc + " succesfully deleted.")

    ####Create the new polygon feature class

    has_m = "DISABLED"
    has_z = "DISABLED"
    template = ""
    sr = arcpy.Describe(LANDFIRE2014).SpatialReference
    arcpy.CreateFeatureclass_management(pgnfcpath, pgnfcname, "POLYGON", template, has_m, has_z, sr)
    arcpy.AddMessage ("New polygon feature class created succesfully.")



    ####Add reference field to the polygon feature class

    arcpy.AddField_management(pgnfc,"RefID","LONG","#","#","#","#","NON_NULLABLE","NON_REQUIRED","#")
    arcpy.AddMessage("Reference field successfully added to the new polygon feature class.")
    arcpy.AddField_management(pgnfc,"XCentroid","DOUBLE","#","#","#","#","NON_NULLABLE","NON_REQUIRED","#")
    arcpy.AddMessage("XCentroid field successfully added to the new polygon feature class.")
    arcpy.AddField_management(pgnfc,"YCentroid","DOUBLE","#","#","#","#","NON_NULLABLE","NON_REQUIRED","#")
    arcpy.AddMessage("YCentroid field successfully added to the new polygon feature class.")
    arcpy.AddField_management(pgnfc,"Height","DOUBLE","#","#","#","#","NON_NULLABLE","NON_REQUIRED","#")
    arcpy.AddMessage("Height field successfully added to the new polygon feature class.")
    arcpy.AddField_management(pgnfc,"Width","DOUBLE","#","#","#","#","NON_NULLABLE","NON_REQUIRED","#")
    arcpy.AddMessage("Width field successfully added to the new polygon feature class.")
    arcpy.AddField_management(pgnfc,"Rotation","DOUBLE","#","#","#","#","NON_NULLABLE","NON_REQUIRED","#")
    arcpy.AddMessage("Rotation field successfully added to the new polygon feature class.")


    ####Instantiate an arcpy point object and an arcpy array

    #Instantiate an arcpy Point Object
    point = arcpy.Point()
    #Instantiate an arcpy Array Object
    array = arcpy.Array()


    ####Instantiate cursors

    #if conversion_type=="VINEYARDS":
    #    sf="PVINE D"
    #elif conversion_type=="URBAN":
     #   sf="RURALRES D"
    #Instantiate a Search Cursor on the point feature class
    #pntfcrows = arcpy.SearchCursor(ptfc, sort_fields=sf)
    pntfcrows = arcpy.SearchCursor(ptfc)
    #Instantiate an Insert Cursor on the new polygon feature class
    pgnfcrows = arcpy.InsertCursor(pgnfc)


    ####Instantiate a new row for the polygon feature class
    newpgn = pgnfcrows.newRow()
    acreage = 0
    count = 0
    ####Loop through each point and create the polygons in the polygon feature class

    for eachrow in pntfcrows:
        if (acreage < (int(acreage_cap)+(int(acreage_cap) * 0.25))):
            if eachrow.getValue("NEAR_DIST") < 45 and conversion_type=="URBAN":
                    continue
            elif eachrow.getValue("NEAR_DIST") < 70 and conversion_type=="VINEYARDS": #Potential to miss large core areas that should have more than one vineyard on them?
                    continue
            #Retrieve the point geometry object from the shape field
            ptgeom = eachrow.getValue("Shape")
            #Retrieve the ObjectID from the ObjectID field
            oid = eachrow.getValue(oidfldname)
            #Grab rotation, width and height to pass to xylist function above
            pt_rot = round(eachrow.getValue("NEAR_ANGLE"), 2)
            if pt_rot < 0:
                pt_rot = pt_rot +360
            else:
                pt_rot = pt_rot

            if conversion_type=="VINEYARDS":
                pt_height= eachrow.getValue("NEAR_DIST")*1.25
                pt_width= (eachrow.getValue("NEAR_DIST")*1.25)*1.25
            elif conversion_type=="URBAN":

                if not eachrow.getValue("UnitsAllowed_int"):
                    if eachrow.getValue("NEAR_DIST") < 60:
                        pt_height= 80
                        pt_width= 80
                    else:
                        pt_height= 110
                        pt_width= 110
                elif int(eachrow.getValue("UnitsAllowed_int")) <= 1:
                    if eachrow.getValue("NEAR_DIST") < 60:
                        pt_height= 80
                        pt_width= 80
                    else:
                        pt_height= 110
                        pt_width= 110
                elif int(eachrow.getValue("UnitsAllowed_int")) > 1:
                    if eachrow.getValue("UnitsAllowed_int")*110 < eachrow.getValue("NEAR_DIST")*1.3:
                        pt_height= eachrow.getValue("UnitsAllowed_int")*110
                        pt_width = eachrow.getValue("UnitsAllowed_int")*110
                    else:
                        pt_height= eachrow.getValue("NEAR_DIST")*1.3
                        pt_width= eachrow.getValue("NEAR_DIST")*1.3
                pt_rot = 0


            acreage = acreage + ((pt_height*pt_width)/4047)
            count = count + 1

            #Now create xylist from function above
            xylist = return_geometry(pt_height, pt_width, pt_rot)

            #Get the number of points in the point geometry object
            numpts = ptgeom.pointCount
            #Loop through each point in the point geometry
            for eachpt in range(numpts):
                #Retrieve the point object from the point geometry object
                pt = ptgeom.getPart(eachpt)
                #Create the point list for the vertices
                if not (math.isnan(pt.X) or math.isnan(pt.Y)):
                	ptlst = [(x+ pt.X, y + pt.Y) for (x,y) in xylist]
                	#Assign the x and y coordinates to the arcpy point object and add the point to the array
                	for polypt in ptlst:
                		point.X = polypt[0]
                		point.Y = polypt[1]
                		array.add(point)
                	#Create an arcpy polygon object from the arcpy array
                	polygon = arcpy.Polygon(array)
                	#Clear the array so that the next polygon can be built
                	array.removeAll()
                	#Set the values of the shape field and the reference id field for the new polygon row
                	newpgn.setValue("Shape", polygon)
                	newpgn.setValue("RefID", oid)
                	newpgn.setValue("XCentroid", pt.X)
                	newpgn.setValue("YCentroid", pt.Y)
                	newpgn.setValue("Height", ht)
                	newpgn.setValue("Width", width)
                	newpgn.setValue("Rotation", delta)
                	#Add the new polygon row to the feature class
                	pgnfcrows.insertRow(newpgn)


    #add_to_logfile("New polygons successfully created.")
    del pgnfcrows, newpgn


    pgnview = pgnfcname + "_Layer"
    pgnlayer = arcpy.MakeFeatureLayer_management(pgnfc, pgnview).getOutput(0)


    #Set the output feature layer
    arcpy.SetParameter(6, pgnlayer)
    arcpy.AddMessage("New polygon layer created.")
    return (acreage, count)


def find_correct_rectangular_number(vineyard_rectangles, vineyard_rectangles_dissolve, conversion_type, acreage_cap):
    import arcpy, sys, math, os

    print ("Finding correct amount of vineyard acres...")
    arcpy.MakeTableView_management(vineyard_rectangles, "rectangleTableView")
    rectangle_count = int(arcpy.GetCount_management("rectangleTableView").getOutput(0))
    print ("Rectangle count = " + str(rectangle_count))
    arcpy.Delete_management("rectangleTableView")

    whileCount = 0
    targetReached = "False"
    change_value = int(rectangle_count * 0.1)
    guess_number = (rectangle_count * 0.8) + change_value
    mini = 0
    maxi = 0

    while targetReached == "False" and whileCount < 20:
        whileCount += 1
        arcpy.MakeFeatureLayer_management(vineyard_rectangles, 'rectangles_layer')
        print ("Guess Number = " + str(guess_number))
        print ("Change Value = " + str(change_value))
        where1 = "OBJECTID <= " + str(guess_number)
        arcpy.SelectLayerByAttribute_management('rectangles_layer', 'NEW_SELECTION', where1)
        arcpy.Dissolve_management('rectangles_layer', vineyard_rectangles_dissolve)

        rectangle_acreage = 0
        for row in arcpy.SearchCursor(vineyard_rectangles_dissolve):
            rectangle_acreage = rectangle_acreage + (row.getValue('Shape_Area') * 0.000247105)

        if ((rectangle_acreage-10) <= int(acreage_cap) and (rectangle_acreage+10) >= int(acreage_cap)): #need to change to a percent of total acreage that you can be over and still acceptable and update in second seed loop also!
            targetReached = "True"
            print ("Found Correct number of vineyards  ")
            print ("Final Guess Number = " + str(guess_number))
            print ("Final Change Value = " + str(change_value))
            print ("Rectangle Acrage = " + str(rectangle_acreage))

        elif rectangle_acreage < int(acreage_cap):
            mini = guess_number
            if (mini + change_value) == maxi:
                change_value = change_value - (change_value * .5)
            guess_number = guess_number + change_value

        elif rectangle_acreage > int(acreage_cap):
            maxi = guess_number
            if (maxi - change_value) == mini:
                change_value = change_value - (change_value * .5)
            guess_number = guess_number - change_value

    arcpy.MultipartToSinglepart_management(vineyard_rectangles_dissolve, 'temp_vineyard_rectangles_sp')
    arcpy.MakeTableView_management('temp_vineyard_rectangles_sp', "recTableView")
    final_rectangle_count = int(arcpy.GetCount_management("recTableView").getOutput(0))
    arcpy.Delete_management("recTableView")
    arcpy.Delete_management('temp_vineyard_rectangles_sp')


    return (rectangle_acreage, final_rectangle_count, whileCount)

def find_correct_urban_number(urban_seeds_full, urban_circles, urban_circles_dissolve, conversion_type, acreage_cap):
    import arcpy, sys, math, os
    arcpy.env.overwriteOutput = 1

    print ("Finding correct amount of urban acres...")
    arcpy.MakeTableView_management(urban_circles, "rectangleTableView")
    rectangle_count = int(arcpy.GetCount_management("rectangleTableView").getOutput(0))
    print ("Urban Circle count (not accounting for overlaps) = " + str(rectangle_count))
    arcpy.Delete_management("rectangleTableView")

    whileCount = 0
    targetReached = "False"
    if (rectangle_count  < 10):
        change_value = 1
    else:
        change_value = int(rectangle_count * 0.1)
    guess_number = (rectangle_count * 0.88) + change_value
    mini = 0
    maxi = 0

    #Testing to see if the max possilbe acreage is less than the total acreage target, if so, skip the iteration and just return the max possible circles
    arcpy.Dissolve_management(urban_circles, urban_circles_dissolve, 'flag_')
    max_rectangle_acreage = 0
    for row in arcpy.SearchCursor(urban_circles_dissolve):
        max_rectangle_acreage = max_rectangle_acreage + (row.getValue('Shape_Area') * 0.000247105)

    if (max_rectangle_acreage <= int(acreage_cap)):
        rectangle_acreage = max_rectangle_acreage

    elif (max_rectangle_acreage > int(acreage_cap)):

        while targetReached == "False" and whileCount < 10:
            whileCount += 1
            arcpy.MakeFeatureLayer_management(urban_circles, 'rectangles_layer')
            print ("Guess Number = " + str(guess_number))
            print ("Change Value = " + str(change_value))
            where1 = "OBJECTID <= " + str(guess_number)
            arcpy.SelectLayerByAttribute_management('rectangles_layer', 'NEW_SELECTION', where1)
            arcpy.Dissolve_management('rectangles_layer', urban_circles_dissolve, "flag_")

            rectangle_acreage = 0
            for row in arcpy.SearchCursor(urban_circles_dissolve):
                rectangle_acreage = rectangle_acreage + (row.getValue('Shape_Area') * 0.000247105)

            if (rectangle_acreage <= int(acreage_cap) and (rectangle_acreage+2) >= int(acreage_cap)): #could to change to a percent of total acreage that you can be over and still acceptable and update in second seed loop also!
                targetReached = "True"
                print ("Found Correct number of vineyards  ")
                print ("Final Guess Number = " + str(guess_number))
                print ("Final Change Value = " + str(change_value))
                print ("Rectangle Acrage = " + str(rectangle_acreage))

            elif rectangle_acreage < int(acreage_cap):
                mini = guess_number
                if (mini + change_value) == maxi:
                    change_value = change_value - (change_value * .5)
                guess_number = guess_number + change_value

            elif rectangle_acreage > int(acreage_cap):
                maxi = guess_number
                if (maxi - change_value) == mini:
                    change_value = change_value - (change_value * .5)
                guess_number = guess_number - change_value

    arcpy.MultipartToSinglepart_management(urban_circles_dissolve, 'temp_urban_circles_sp')
    arcpy.MakeTableView_management('temp_urban_circles_sp', "circleTableView")
    final_circle_count = int(arcpy.GetCount_management("circleTableView").getOutput(0))
    arcpy.Delete_management("circleTableView")
    try:
        arcpy.Delete_management('temp_urban_circles_sp')
    except:
        add_to_logfile("could not delete temp_urban_circles")


    return (rectangle_acreage, final_circle_count, whileCount)



def make_and_set_flag(feature_class, fieldname="flag", value=1):
    """This function makes a short integer field called flag
    and calcs it to 1.  If such a field exists already, it is
    deleted"""
    import arcpy
    import sys
    if not arcpy.Exists(feature_class):
        arcpy.AddError(feature_class + "doesn't exist")
        sys.exit()
    try:
        if fieldname in [i.name for i in arcpy.ListFields(feature_class)]:
            arcpy.DeleteField_management(feature_class, fieldname)
        arcpy.AddField_management(feature_class, fieldname, "SHORT")
        arcpy.CalculateField_management(feature_class, fieldname, value, "PYTHON_9.3")
    except:
        arcpy.AddError("Error creating flag.")
        print("Error creating flag.")
        sys.exit()


def flip_pixels(inraster, outname, jointable, joinfield="VALUE", destfield="VALUE_2010", lut_field="VALUE_2030"):
    """Takes an input raster and a look up table.  Input rater pixel values are VALUE_10 from
    tbl_cht_90_10_atts_gen_class_stock_change_lut.  Lookup table should contain a 'from' and a 'to'
    lookup (both relate to VALUE_10 in tbl_cht_90_10_atts_gen_class_stock_change_lut).
    The function creates a new grid with pixel values of the lookup table's VALUE_30 field.

    An example lookup table is: D:/CLOUD/Shared/Open Space/Carbon Framework/GIS Data/MASTER_DATA/CarbonTables.gdb/VINEYARD_CONVERSION_LUT
    All values in the VALUE_10 field will be looked up to the vineyard value in the VALUE_30 field.
    """
    import arcpy
    import arcpy.sa
    #first remove fields from the input raster if there are additional fields
    for i in arcpy.ListFields(inraster):
            if i.name.upper() not in('OBJECTID', 'VALUE', 'COUNT'):
                arcpy.DeleteField_management(inraster, i.name)
    arcpy.JoinField_management(inraster,joinfield,jointable,destfield,fields=lut_field)
    OutRaster = arcpy.sa.Lookup(inraster,lut_field)
    OutRaster.save(outname)


def check_for_overlap(treatment_or_threat_fc, mask_fc, query="None"):
    """Query is optional and can be "None"""
    import arcpy
    arcpy.env.overwriteOutput = True
    arcpy.MakeFeatureLayer_management(treatment_or_threat_fc, "lyr1")
    arcpy.MakeFeatureLayer_management(mask_fc, "lyr2")
    if query != "None":
        arcpy.SelectLayerByAttribute_management("lyr2", "NEW_SELECTION", query)
    arcpy.SelectLayerByLocation_management("lyr1", "INTERSECT", "lyr2")

    result = arcpy.GetCount_management("lyr1")
    return int(result.getOutput(0))


def add_to_logfile(string_to_add):
    import arcpy
    lf = open(logfile, "a")
    lf.write(string_to_add + "/n")
    lf.close()
    arcpy.AddMessage(string_to_add)
    print (string_to_add)


def get_dict_for_seeds(table):
    import arcpy, os
    sc = arcpy.da.SearchCursor(table, ['ID', 'OBJECTID', 'Shape_Area'])
    dict_big = {}
    for row in sc:
        ID = int(row[0])
        OID = row[1]
        Area =  row[2]
        if not ID in dict_big.keys():
            dict_big[ID] = [OID, Area]
        elif Area > dict_big[ID][1]:
            dict_big[ID] = [OID, Area]
    del sc
    return dict_big

def ylim(max_vin, max_urb):
    if max_vin > max_urb:
        if max_vin >=1000:
            return round((max_vin+500), -3)
        else:
            return round((max_vin+50), -2)
    else:
        if max_urb >=1000:
            return round((max_urb+500), -3)
        else:
            return round((max_urb+50), -2)


def check_extensions(ext='Spatial'):
    import arcpy
    import sys
    from arcpy import env

    try:
        if arcpy.CheckExtension(ext) == "Available":
            arcpy.CheckOutExtension(ext)
            return 1
        else:
            #print ext + " license is unavailable"
            #add_to_logfile ("Spatial Analyst Extension isn't installed or turned on")
            return 0

    except:
        #print "3D Analyst license is unavailable"
        #add_to_logfile ("Spatial Analyst Extension isn't installed or turned on")
        return 0

def create_cons_knockouts(input_fl):
        import arcpy
        import os
        from arcpy import env
        #Combine with policy knockouts to create final knockout
        #Union  Layers (conservation scenarion and policy knockout)
        add_to_logfile("Union ...")

        arcpy.env.extent = VECTOR_MASK
        policy_knockouts_with_slope = os.path.join(arcpy.env.workspace,"POLICY_KNOCKOUT_TEMP")
        conservation_knockout = os.path.join(arcpy.env.workspace,"POLICY_KNOCKOUT")
        inputs = [input_fl, policy_knockouts_with_slope]
        arcpy.Union_analysis(inputs, "Temp1")

        #Calculate knockout field, dissolve on knockout field (remove overlapping polygons),
        #project to Teale Albers
        add_to_logfile("Calculating field for knockout ...")
        arcpy.CalculateField_management("Temp1", "knockout", "1", "PYTHON_9.3", "")
        add_to_logfile("Dissolving and projecting ...")
        arcpy.Dissolve_management("Temp1", "Temp2", "knockout", "#","SINGLE_PART")

        sr = arcpy.CreateSpatialReference_management(SPATIAL_REFERENCE_TEXT)
        arcpy.Project_management("Temp2",conservation_knockout, sr)

        for i in range(1, 100):
            if arcpy.Exists("temp" + str(i)):
                arcpy.Delete_management("temp" + str(i))

def create_random_raster(input_raster, out_raster):
    """Function uses input raster for mask, extent, and cell size.  Function
    then creates a random raster with uniformly random pixel values across the
    extent of the input, it then creates an output raster whose pixel values
    are between 0 and 100 with a uniformly random distribution."""
    import arcpy
    import arcpy.sa
    import os
    temp = os.path.join(out_raster + "_")

    arcpy.env.extent = input_raster
    arcpy.env.snapRaster = input_raster
    arcpy.env.cellSize = input_raster

    print ("Creating random raster...")
    RanRas = arcpy.sa.CreateRandomRaster()
    RanRas.save(temp)
    #print ("Running Con...")

    TreatMask = arcpy.sa.Con(arcpy.sa.Raster(temp) <= arcpy.sa.Raster(input_raster), 1, arcpy.sa.Con(arcpy.sa.Raster(temp) <= (arcpy.sa.Raster(input_raster)*2), 2))

    TreatMask.save (out_raster)





"""
Initialization
"""
def create_processing_table(InPoints,inmask):
    """
    This function takes a point feature class (InPoints) and the user-defined processing area (inmask), selects by location
    abd exports a CSV file and reads the file into a global variable as a Pandas DF.
    """
    import arcpy
    import os
    import pandas as pd
    import Generic
    if inmask == 'D:/TGS/projects/64 - Merced Carbon/Python/MercedTool/Deliverables/MASTER_DATA/Vectors.gdb/Mask_Dissolved':
        pts = pd.read_csv(Generic.Points_Table)
        return pts
    else:
        pass
##        arcpy.MakeFeatureLayer_management(InPoints,'temp')
##        arcpy.SelectLayerByLocation_management('temp','INTERSECT',inmask)
##        #copy featureclass
##        arcpy.CopyFeatures_management('temp',os.path.join(Generic.tempgdb,'' )
##        #fctocsv
##        pts = pd.read_csv(os.path.join(Generic.RDP, Generic.MP,'Temp/temp.csv'))
##        return pts


def MergeLCValues():
    import functools
    import pandas as pd
    global pts
    landcover = pd.read_csv(lc)
    def MergeMultiDF(Listofdfs, JoinField):
        mba = functools.reduce(lambda left,right: pd.merge(left,right,on=JoinField), Listofdfs)
        global pts
        pts = mba.loc[:, ~mba.columns.str.contains('^Unnamed')]
        return pts
    MergeMultiDF([landcover,pts],'pointid')
    del pts['OBJECTID']
    return pts

"""
Suitability Flagging
"""

def  LoadSuitabilityData():
    import pandas as pd
    import functools
    suitlist = []
    temp = []
    for i in suitlist:
        temp.append(pd.read_csv(i))
    suitdf = functools.reduce(lambda left,right: pd.merge(left,right,on='pointid'), temp)
    return suitdf

#PREPROCESSING FUNCTIONS

def FCstoCSVs (inputgdb,Outpath):
    """
    This function takes a workspace with vector feature classes and writes out their tables as CSVs
    to a user defined folder.
    Workspace_FCs is a geodatabase with feature classes.
    Outpath is the folder where the CSVs are written to.
    """
    import arcpy
    import csv
    #Set the Variables
    arcpy.env.workspace = inputgdb
    arcpy.env.overwriteOutput = 1
    flist = arcpy.ListFeatureClasses()
    for i in flist:
        table = i
        outfile = Outpath + i + '.csv'

    #--first lets make a list of all of the fields in the table
        fields = arcpy.ListFields(table)
        field_names = [field.name for field in fields]
        print (fields)
        print (field_names)
        # Now we create the output file and write the table to it
        with open(outfile,'w') as f:
            dw = csv.DictWriter(f,field_names, lineterminator = '\n')
            #--write all field names to the output file
            dw.writeheader()

            #--now we make the search cursor that will iterate through the rows of the table
            with arcpy.da.SearchCursor(table,field_names) as cursor:
                for row in cursor:
                    dw.writerow(dict(zip(field_names,row)))
def FCtoCSV (inputfc,Outpath):
    """
    This function takes a workspace with vector feature classes and writes out their tables as CSVs
    to a user defined folder.
    Workspace_FCs is a geodatabase with feature classes.
    Outpath is the folder where the CSVs are written to.
    """
    import arcpy
    import csv
    #--first lets make a list of all of the fields in the table
    fields = arcpy.ListFields(inputfc)
    field_names = [field.name for field in fields]
    print (fields)
    print (field_names)
    # Now we create the output file and write the table to it
    with open(Outpath,'w') as f:
        dw = csv.DictWriter(f,field_names, lineterminator = '\n')
        #--write all field names to the output file
        dw.writeheader()

        #--now we make the search cursor that will iterate through the rows of the table
        with arcpy.da.SearchCursor(inputfc,field_names) as cursor:
            for row in cursor:
                dw.writerow(dict(zip(field_names,row)))
def Make_Flags (Flags,Fieldname):
    """

    """
    import pandas as pd
    import Generic
    FLG = pd.read_csv(Flags)
    Generic.pts[Fieldname] = 0
    Generic.pts.loc[Generic.pts['pointid'].isin (FLG['pointid']), Fieldname] = 1


def KnockoutFinish (list):
    import Generic
    Generic.pts['policy_knockout'] = 0
    for i in list:
        pts.loc[(pts[i] == 1), 'policy_knockout'] =1
def create_policy_knockouts(slope, outputcsv):
    """
    This function takes the point feature class (center points of landfire cells),
    applies a selection using the processing area mask,
    adds binary flags using pre-created csvs and creates a combined 'Knockout_Flag'.

    It then joins the carbon tables together, and the carbon table to the kockout table.
    The end result is a large csv with carbon and flag fields.

    Creates a vector ("policy_knockout" = 1)

    """

    #Import System Modules
    import arcpy
    import pandas as pd
    import Generic
    arcpy.env.overwriteOutput = True
    arcpy.env.extent = Generic.MASK

    #Create processing table
    Generic.create_processing_table(Generic.Points,Generic.MASK)


    #Create and Calculate Flag Fields- MUST RUN IN ORDER OR IT WILL NOT WORK
    print ('Creating Flags')
    Generic.add_to_logfile("FLAGGING PIXELS")
    Generic.Make_Flags (Generic.Wet_Flag,'Wet_Flag')
    Generic.Make_Flags (Generic.Rip_Flag,'Rip_Flag')
    Generic.Make_Flags (Generic.Rec_Flag,'Rec_Flag')
    Generic.Make_Flags (Generic.CPAD_Flag,'CPAD_Flag')
    Generic.pts.to_csv('E:/Temp/flags.csv')
    #Calculate the slope flag based on the slope value argument
    def SlopeFlag (Degree,Fieldname):
        import pandas as pd
        import Generic
        slp = pd.read_csv("D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/Other/Slope.csv")
        query = slp[slp['RASTERVALU'] > Degree]
        Generic.pts[Fieldname] = 0
        Generic.pts.loc[Generic.pts['pointid'].isin (query['pointid']), Fieldname] = 1
        del slp
        del query

    SlopeFlag(slope,'Slope_Flag')
    #Flag pixels for knockout
    print ('Calculating Knockout Flags')
    Generic.KnockoutFinish(['Wet_Flag','Rip_Flag','Rec_Flag','CPAD_Flag','Slope_Flag'])
    Generic.pts = Generic.pts.loc[:, ~Generic.pts.columns.str.contains('^Unnamed')]
    Generic.pts.to_csv('E:/Temp/test2.csv')
    #Read the
    df1 = pd.read_csv(Generic.Carbon2001)
    df2 = pd.read_csv(Generic.Carbon2014)
    df3 = pd.read_csv(Generic.Carbon2030)
    print ('Combining Carbon Data')
    DFname = Generic.pts.join(df1, on='gridcode01',rsuffix='_other')
    DFname2 = DFname.join(df2, on='gridcode14',rsuffix = 'other')
    Final = DFname2.join(df3, on = 'gridcode14', rsuffix = 'other')
    print ('Outputting csv')
    Final.to_csv(outputcsv)


def Clean_Table (csv,idfield,length=5689373,keepfields = [], renamefields = [],valuefield = 'TEST'):
    """
    This function takes a csv and check it for consistency (and nulls) and drops fields
    that are unwanted, and renames fields that need to be renamed
    rename fields values must be in tuples where the first value is the existing field and the 2nd value is the new field name.
    example: renamefields = [('Value','Landcover')]
    """
    import pandas as pd
    import os
    import sys
    print ('reading csv ' + valuefield)
    if keepfields:
        df = pd.read_csv(csv, usecols = keepfields)
    else:
        df = pd.read_csv(csv)
    print (len(df))
    print ('Finished Loading DF, finding MAX')
    max = df[idfield].max()
    if (max != length) or (len(df) != length):
        print ("LENGTH IS WRONG")
        sys.exit()
    else:
        pass
    print ('Checking Uniqueness')
    unique = df[idfield].is_unique
    print (unique)
    if unique is True:
        pass
    else:
        print ("ID FIELD IS NOT UNIQUE")
        exit
    if valuefield in df:
        if df[valuefield].dtype == 'O':
            df[valuefield].fillna('None')
        else:
            df[valuefield].fillna(-9999)
    if not renamefields:
        print ("No fields to rename.")
    else:
        for i in renamefields:
            df = df.rename(columns={i[0]: i[1]})
    df.sort_values(idfield,inplace = True)
    os.rename (csv, os.path.join(os.path.dirname(csv), (os.path.basename(csv).split('.'))[0] + '_orig.csv'))
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]    
    df.to_csv(csv)

def MergeMultiDF(JoinField, dflist):
    '''Takes a list of dataframes and joins them on a common field'''
    #mba = pd.concat(temp, axis = 1)
    import pandas as pd
    import functools
    mba = functools.reduce(lambda left,right: pd.merge(left, right,on=JoinField), dflist)
    OutputDF = mba.loc[:, ~mba.columns.str.contains('^Unnamed')]
    return OutputDF


#Make MBA Raster
def MakeMBARaster(LUT,OutputPath,JoinKey,TargetKey,Lfield):
    """
    This function uses a lookup table and a raster to create a lookup raster.
    LUT = look up table CSV
    OutputPath = output raster
    JoinKey =
    """
    import arcpy
    import Generic
    from arcpy import env
    arcpy.CheckOutExtension("Spatial")
    #Set the Variables
    ws = 'E:/Temp'
    arcpy.env.workspace = ws
    arcpy.env.overwriteOutput = 1
    print ('Making Raster Layer')
    arcpy.MakeRasterLayer_management(raster,'temp')
    arcpy.AddJoin_management('temp',JoinKey,LUT,TargetKey)
    arcpy.CopyRaster_management('temp','temp2.tif')
    tempo = arcpy.sa.Lookup('temp2.tif',Lfield)
    print ('Saving Raster')
    tempo.save(OutputPath)

def RastersToPoints(Raster,ValueField,OutputName):
    """
    This function takes a raster, a value field and an output FC name, creates a point featureclass
    from the raster in the temp vector gdb in the Master Data Folder.
    """
    import arcpy
    print ('Doing: ' + Raster)
    arcpy.RasterToPoint_conversion(Raster,tempgdb+OutputName,ValueField)

def LoadCSVs(infolder):
    """
    This function takes a folder, and reads every csv in it into a dataframe
    and appends those dataframes to a list (dflist).
    """
    import arcpy
    import Generic
    import os
    from arcpy import env
    import pandas as pd
    #Set the Variables
    ws = infolder
    arcpy.env.workspace = ws
    arcpy.env.overwriteOutput = 1
    list1 = arcpy.ListTables()
    dflist = []
    print (list1)
    for i in list1:
        dflist.append(pd.read_csv(os.path.join(ws, i)))

    newlist = []
    for i in dflist:
        newlist.append(i.loc[:, ~i.columns.str.contains('^Unnamed')])
    print (newlist)
    return newlist


def Merge2csvs(inputcsv1,inputcsv2,mergefield,outputcsv,origcol = 'none',newcol = 'none'):
    """
    This function combines 2 CSVs into a new csv by reading them into pandas dataframes, renaming the
    column in one if necessary to match the key column names, then merging on the key field.

    The reulting merged dataframe is written to the specified CSV.
    """

    import arcpy
    import functools
    import pandas as pd
    ws = "D:/TGS/projects/64 - Merced Carbon/MBA/ToolData/Tables/MBTABLES"
    arcpy.env.workspace = ws
    arcpy.env.overwriteOutput = 1
    templist = [inputcsv1,inputcsv2]
    temp = []
    df1 = pd.read_csv(inputcsv1)
    df2 = pd.read_csv(inputcsv2)

    #if the column needs to be changed for the join to work rename it
    if origcol != 'none':
        df1 = df1.rename(columns={origcol : newcol})
    result = pd.merge(df2, df1, on=mergefield)
    result.to_csv(outputcsv)


#def CombineChangeFlag(list1, list2):
    #test comment
#  This is stubbed out for tukman to work on
#    from random import *
#    randBinList = lambda n: [randint(0,1) for b in range(1,n+1)]
#
#    a = randBinList(6000000)
#    b = randBinList(6000000)
#
#    L3 = [max(a, b) for a, b in zip(a, b)]

#def CreateSuitFlags(PandasQuery,TupleOut):
    #import pandas as pd


    #open_req_list = tuple(list(open_reqs['REQ_NUM']))


















