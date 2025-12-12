
# imports
import os

# must set this variable so r5py can access JDK reliably
os.environ['JAVA_HOME'] = r"C:\Program Files\Java\jdk-25\bin"

try:
    import geopandas as gpd 
except:
    %pip install geopandas
    import geopandas as gpd

try:
    import r5py # multimodal network isochrone generator library
except:
    %pip install r5py
    import r5py

try:
    import datetime # need this to work with dates for r5py
except:
    %pip install datetime
    import datetime

# get a clean CT shapefile
toronto_ct_no_centroid = gpd.read_file('./Toronto CT for Isochrone Creator/Toronto_Census_Tracts_No_Centroid_Final.shp') 

# get the study area for later calculation
study_area = toronto_ct_no_centroid.union_all().area

# get centroid shapefile to fetch origins
centroids_gdf = gpd.read_file('./Toronto CT for Isochrone Creator/Toronto_Centroids_Final.shp')
toronto_ct_no_centroid['centroid'] = centroids_gdf.geometry

# subset to only what is needed 
toronto_ct = toronto_ct_no_centroid[['DGUID', 'geometry', 'centroid']]

# path to walking network
pbf_path = "./toronto_again.pbf"

# path to 2015 gtfs data - DO NOT UNPACK ZIP
gtfs_path1 = "./gtfs_2015.zip"

# create transportation network object from r5py (this takes a while)
tn1 = r5py.TransportNetwork(pbf_path, gtfs = gtfs_path1)


def generate_iso_2015(point, time, tn):
    # Generates a <time> minute isochrone around <point> using a combination transit-walking network
    # returns the isochrone as one polygon
    
    point_gdf = gpd.GeoDataFrame({'id': [1], 'geometry': point}, crs = toronto_ct.crs)

    # create the isochrones as gdf using r5py function, using date from gtfs calendar file
    iso = r5py.Isochrones(
        tn,
        origins = point_gdf,
        departure=datetime.datetime(2015, 11, 22, 8, 30),
        transport_modes= [r5py.TransportMode.TRANSIT, r5py.TransportMode.WALK],
        isochrones=[time]
    )
    # ensure the crs matches
    iso = iso.to_crs(toronto_ct.crs)

    # turn the multilines into polygons and put them all together to make one multipart geometry
    return iso.geometry.polygonize().union_all()



def calc_percentage(iso):
    # Calculate the percentage of the study area covered by the isochrone area
    p = iso[0].geometry.area / study_area
    return p

toronto_ct_2015_skimmed = toronto_ct[['DGUID', 'geometry', 'centroid']]

# create the isochrones for every row (CT)! The time value was changed between runs when I decided to also generate 15 minute versions
toronto_ct_2015_skimmed['geometry'] = toronto_ct_2015_skimmed.apply(lambda row: generate_iso_2015([row['centroid']], 30, tn1), axis=1)

# calculate area coverage and assign into gdf
toronto_ct_2015_skimmed['area_percentage'] = toronto_ct_2015_skimmed.geometry.area/study_area

# ensure crs is still up to date
toronto_ct_2015_skimmed=toronto_ct_2015_skimmed.to_crs(toronto_ct.crs)

# write the output of this to a shapefile!
writable1 = toronto_ct_2015_skimmed[['DGUID', 'geometry', 'area_percentage']]
writable1.to_file('DGUID_ISO_30min_2015.shp')
print('2015 file made successfully')

########################################## DO IT ALL AGAIN FOR 2025 ########################################################
def generate_iso_2025(point, time, tn):
    # Generates a <time> minute isochrone around <point> using a combination transit-walking network
    # returns the isochrone as one polygon

    # analagous to 2015
    # separate function made because date had to be different
    
    point_gdf = gpd.GeoDataFrame({'id': [1], 'geometry': point}, crs = toronto_ct.crs)

    iso = r5py.Isochrones(
        tn,
        origins = point_gdf,
        departure=datetime.datetime(2025, 11, 14, 8, 30),
        transport_modes= [r5py.TransportMode.TRANSIT, r5py.TransportMode.WALK],
        isochrones=[time]
    )
    iso = iso.to_crs(toronto_ct.crs)

    return iso.geometry.polygonize().union_all()

gtfs_path2 = "./gtfs_2025.zip"
tn2 = r5py.TransportNetwork(pbf_path, gtfs = gtfs_path2)


toronto_ct_2025_skimmed = toronto_ct[['DGUID', 'geometry', 'centroid']]
toronto_ct_2025_skimmed['geometry'] = toronto_ct_2025_skimmed.apply(lambda row: generate_iso_2025([row['centroid']], 15, tn2), axis=1)

toronto_ct_2025_skimmed['area_percentage'] = toronto_ct_2025_skimmed.geometry.area/study_area
toronto_ct_2025_skimmed=toronto_ct_2025_skimmed.to_crs(toronto_ct.crs)
writable2 = toronto_ct_2025_skimmed[['DGUID', 'geometry', 'area_percentage']]
writable2.to_file('DGUID_ISO_15min_2025.shp')

print('2025 shapefile created successfully')