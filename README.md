# Merced Conservation and Carbon Accounting Tool

## Full Tool Guide
The full tool guide (MS Word Document) for the Merced Tool is available here:  http://rebrand.ly/box4ba8b


## Files to Download 

The MC-CAT and its supporting data are available at:

* MC-CAT Python Scripts and Toolbox:

	https://github.com/mtukman/mercedtool

* MC-CAT Supporting Data:

	http://goo.gl/A1H6BB
  
## System Requirements
To use the tool on your local computer, first make sure that you meet the following system requirements:
* ArcGIS, version 10.2.2 or greater OR ArcPro
* 16 GB Memory
* 5 GB hard drive Space

### ArcGIS Pro is Recommended for Running this tool

## Installing the Tool in ArcMap
1.	Download the Github Repository and the supporting data from https://github.com/mtukman/mercedtool.  
2.	Extract the contents of “mercedtool-master.zip” (which contains a folder called mercedtool-master) to a folder on your hard drive.  The extracted folder contains a number of python modules and an ArcGIS toolbox called MC-CAT. Download and extract the Master_Data folder from http://www.goo.gl/A1H6BB to anywhere on your hard drive.
3.	Add the Merced Conservation Carbon Accounting Tool to the ArcMap Toolbox window within ArcMap.  To do this, right-click the Arc Toolbox folder (see below) and click Add Toolbox.  Browse to the location containing the toolbox that you extracted above in step 1 and select the “MC_CAT_ArcMap_10_5” toolbox. After adding the toolbox, navigate to the tool’s properties and make sure the “Always run in foreground” box is NOT checked.
4.	To have the tool automatically create charts and plots, you will need to have the Plotly package installed and to have a valid Plotly API key.  Install Plotly using your preferred package manager.  Obtain a Plotly API key by setting up a free Plotly account and generating a key in your user settings. 

Once your .mxd is saved, the contents of the Arc Toolbox window are also saved within the map document. The next time you open the document, the Toolbox window will be the same as when you saved the document.

## Installing the Tool in ArcGIS Pro
1.	Download the Github Repository and the supporting data from https://github.com/mtukman/mercedtool.  
2.	Extract the contents of “mercedtool-master.zip” (which contains a folder called mercedtool-master) to a folder on your hard drive.  The extracted folder contains a number of python modules and an ArcGIS toolbox called MC-CAT. Download and extract the Master_Data folder from http://www.goo.gl/A1H6BB anywhere on your hard drive.
3.	To add the toolbox to ArcPro, open an ArcPro project and navigate to the catalog tab. Find the project tab in the catalog, and under it right click on the Toolboxes label. Choose “Add Toolbox” and select the “MC_CAT_Pro” toolbox to add. Save the ArcPro project and the toolbox will stay in the map.
4.	To have the tool automatically create charts and plots, you will need to have the Plotly package installed and to have a valid Plotly API key.  Install Plotly using the python package manager in ArcGIS Pro.  Obtain a Plotly API key by setting up a free Plotly account and generating a key in your user settings. 

Once your project is saved, the contents of the Arc Toolbox window are also saved within the map document. The next time you open the document, the Toolbox window will be the same as when you saved the document.
