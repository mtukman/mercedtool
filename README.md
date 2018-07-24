# TerraCount

## Full Tool Guide
The full tool guide (MS Word Document) for TerraCount is available here:  http://carb.press/manual


## Files to Download 

The TerraCount and its supporting data are available at:

* TerraCount Python Scripts and Toolbox:

	https://github.com/mtukman/mercedtool

* TerraCount Supporting Data:

	https://carb.press/master_data
  
## System Requirements
To use the tool on your local computer, first make sure that you meet the following system requirements:
* ArcMap, version 10.3 or greater OR ArcGIS Pro
* 16 GB Memory
* 10 GB hard drive Space
* 64-bit background geoprocessing must be installed and enabled and the tool must be run in the background (this requirement applies to ArcMap only, ArcGIS Pro will run the tool by default)
* _ArcGIS Pro is Recommended for Running this tool_

## Installing the Tool in ArcMap
1.	Download the Github Repository and the supporting data from https://github.com/mtukman/mercedtool.  
2.	Extract the contents of “mercedtool-master.zip” (which contains a folder called mercedtool-master) to a folder on your hard drive.  The extracted folder contains a number of python modules and an ArcGIS toolbox called TerraCount. Download and extract the Master_Data folder from https://carb.press/master_data to anywhere on your hard drive.
3.	Add the Merced Conservation Carbon Accounting Tool to the ArcMap Toolbox window within ArcMap.  To do this, right-click the Arc Toolbox folder and click 'Add Toolbox'.  Browse to the location containing the toolbox that you extracted above in step 1 and select the “Terra Count ArcMap 10_5” toolbox. After adding the toolbox, navigate to the tool’s properties and make sure the “Always run in foreground” box is NOT checked.
4.	To have the tool automatically create charts and plots, you will need to have the Plotly package installed and to have a valid Plotly API key.  Install Plotly using your preferred package manager (or see step 5 below if you are unfamiliar with installing packages).  Obtain a Plotly API key by setting up a free Plotly account and generating a key in your user settings. 
5. 	To install Plotly in ArcMap, try using pip from the command line. From a command prompt, navigate to the ‘Scripts’ folder of the 64-bit python that ArcMap uses.  Then install plotly (see below for an example of what this command looked like on our machine):
_C:\Python27\ArcGISx6410.5\Scripts>   pip.exe install plotly_ 


Once your .mxd is saved, the contents of the Arc Toolbox window are also saved within the map document. The next time you open the document, the Toolbox window will be the same as when you saved the document.

## Installing the Tool in ArcGIS Pro
1.	Download the Github Repository and the supporting data from https://github.com/mtukman/mercedtool.  
2.	Extract the contents of “mercedtool-master.zip” (which contains a folder called mercedtool-master) to a folder on your hard drive.  The extracted folder contains a number of python modules and an ArcGIS toolbox called Terra Count. Download and extract the Master_Data folder from https://carb.press/master_data anywhere on your hard drive.
3.	To add the toolbox to ArcPro, open an ArcPro project and navigate to the catalog tab. Find the project tab in the catalog, and under it right click on the Toolboxes label. Choose “Add Toolbox” and select the "Terra Count Pro" toolbox to add. Save the ArcPro project and the toolbox will stay in the map.
4.	To have the tool automatically create charts and plots, you will need to have the Plotly package installed and to have a valid Plotly API key.  Install Plotly using the python package manager in ArcGIS Pro.  Obtain a Plotly API key by setting up a free Plotly account and generating a key in your user settings. 

Once your project is saved, the contents of the Arc Toolbox window are also saved within the map document. The next time you open the document, the Toolbox window will be the same as when you saved the document.
