def create_policy_knockouts(tpz, stream_buffer_dist='500 Feet',slope_threshold=55):
    """Creates a vector ("knockout" = 1) for all policy knockout areas.
    These include areas within a user defined distance from streams (default is 500 ft.)
    and areas of very steep slope (default threshold is 55%). Other knockout
    areas include Timber Protection Zones (TPZs), easements, and lands owned by public
    agencies or conservation organizations.

    tpz is 1 or 0 - 0 is the default.  If 1 is selected, tpz areas will be developed
    with vineyards and rural residences.

    Output feature class is in Teale Albers.

    """

    #Import System Modules
    import arcpy
    import sys
    import os
    import pandas as pd
    from arcpy import env
    import Generic
    arcpy.env.workspace = Generic.ArcWorkspace
    arcpy.env.scratchWorkspace = Generic.ArcScratchWorkspace
    #arcpy.env.scratchFolder = ArcScratchFolder
    #arcpy.env.scratchGDB= ArcScratchGDB


    #Figure out what csvs we need


    #create the flag


    arcpy.env.overwriteOutput = True
    arcpy.env.extent = Generic.MASK
    #arcpy.env.mask = Generic.MASK

    Generic.add_to_logfile("STARTING POLICY MODULE-->\n")
    Generic.add_to_logfile("**CREATING POLICY KNOCKOUTS WHERE CONVERSIONS WON'T OCCUR**")

    #Create processing table
    Generic.create_processing_table(Generic.Points,mask,scratch_folder)


    #Create and Calculate Flag Fields
    Generic.add_to_logfile("FLAGGING PIXELS")
    Generic.Make_Flags (Generic.Points_Table,Generic.Wet_Flag,'Wet_Flag')
    Generic.Make_Flags (Generic.Points_Table,Generic.Rip_Flag,'Rip_Flag')
    Generic.Make_Flags (Generic.Points_Table,Generic.Rec_Flag,'Rec_Flag')
    Generic.Make_Flags (Generic.Points_Table,Generic.CPAD_Flag,'CPAD_Flag')
    Generic.Slope_Flag (20,Generic.Points_Table,'Slope_Flag')

    #Flag pixels for knockout
    Generic.KnockoutFinish(['Wet_Flag','Rip_Flag','Rec_Flag','CPAD_Flag','Slope_Flag'])
    Generic.add_to_logfile("MERGE MASTER DATAFRAME")
    carb01 = pd.read_csv(Generic.Carbon2001)
    carb14 = pd.read_csv(Generic.Carbon2014)
    carb30 = pd.read_csv(Generic.Carbon2030)
    carb01 = pd.read_csv(Generic.Carbon2001)

    #Create Full Dataframe
    Generic.MergeTables()

    Generic.add_to_logfile ("ENDING POLICY MODULE-->\n")



