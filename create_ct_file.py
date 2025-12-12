# imports
import geopandas as gpd

# get census tract for shapefile and ID
ct_gdf = gpd.read_file('./Census tract - Percentage of visible minority/Census tract - Percentage of visible minority, n.i.e..shp')

# DAs help isolate the Toronto City
da_home = gpd.read_file('./Dissemination area - Homeownership rate (%)/Dissemination area - Homeownership rate (%).shp')

# get the overall shape of the city as shown in DA file
city_bound = gpd.GeoSeries(da_home.geometry.union_all())

# make it a GDF with the right projection
city_boundary_gdf = gpd.GeoDataFrame({'id': [1], 'geometry': city_bound}, crs = ct_gdf.crs)

# overlay it onto CTs to isolate necessary CTs only
toronto_ct = ct_gdf.overlay(city_boundary_gdf, how = 'intersection')
#toronto_ct['centroid'] = toronto_ct.geometry.centroid

# Write this and the centroids to files for later use
toronto_ct.to_file('Toronto_Census_Tracts_No_Centroid_Final.shp')
toronto_ct['geometry'] = toronto_ct.geometry.centroid
toronto_ct.to_file('Toronto_Centroids_Final.shp')

