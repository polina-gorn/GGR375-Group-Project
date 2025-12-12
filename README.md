# GGR375-Group-Project
TTC Mobility Potentials and Equity:
Quantifying the Change in Travel Potential and Transit Reliability over Time & Space

This project investigates whether changes in public transit accessibility across Toronto census tracts (2015-2025) are equitably distributed or associated with socioeconomic factors like income, homeownership, and minority status. Using spatial statistics and geospatial analysis, we identify patterns of transit improvement/decline and examine potential equity implications.

The intermediate outputs and final visual deliverables of the project can be found in the folder **figures**. The code for unsuccessful reliability data can be explored **INSERT NAME**. 

In order to run these files, you will need to download a .pbf file of Toronto's walking network (too large to store on github) as well as gtfs zip files (also too large to store on github).
The .pbf file can be downloaded from here: https://download.bbbike.org/osm/bbbike/Toronto/
The GTFS zips are accessible from Open Data Toronto and TransitLand - note : A ZIPPED VERSION IS REQUIRED TO RUN SOME OF THESE FILES
If you are reading this and are our professor/TA, you will be emailed a link to a google drive containing these files.

To run the isochrone_creator.py file you will need the following:
- A JDK installation. We used this: https://www.oracle.com/ca-en/java/technologies/downloads/
- GTFS zips STILL ZIPPED
- run your code editor with Administrator permissions
- A VERY LONG TIME AND LOTS AND LOTS OF MEMORY. Multiple hours per year and isochrone size.

While all the code files should be runnable as-is assuming data files are stored in alignment with the github repo, the following run stages are how these shapefiles, figures, and text files were created in our workflow:
(code within the same stage could be run in any order)

STAGE 1:
geocode_intersections.ipynb
TTC_delays_processed.ipynb

STAGE 2:
bus_delay_Levenshtein.ipynb
create_isochrone_gdf.ipynb

STAGE 3:
create_isochrone_visuals.ipynb
create_morans_i_maps.ipynb
create_bivariate_maps.ipynb
