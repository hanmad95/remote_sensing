# -*- coding: utf-8 -*-
import os 
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import pickle


#============================================================================
# 2. Load LULC Classes
#============================================================================


filename = r'\C3S-LC-L4-LCCS-Map-300m-P1Y-2019-v2.1.1.nc'
path_to_file = r'C:\Users\hanne\Desktop\Hannes\Uni\Master EI\2020-2021 WS Masterarbeit\11_2020_Data_Read\01_Experiments' + r"\esa_lulc" + filename
area_of_interest = {"lat_min_area":47,"lat_max_area":49,"lon_min_area":10.5,"lon_max_area":12.5}

flag_meanings = """no_data cropland_rainfed cropland_rainfed_herbaceous_cover cropland_rainfed_tree_or_shrub_cover cropland_irrigated mosaic_cropland mosaic_natural_vegetation tree_broadleaved_evergreen_closed_to_open 
tree_broadleaved_deciduous_closed_to_open tree_broadleaved_deciduous_closed tree_broadleaved_deciduous_open tree_needleleaved_evergreen_closed_to_open tree_needleleaved_evergreen_closed tree_needleleaved_evergreen_open 
tree_needleleaved_deciduous_closed_to_open tree_needleleaved_deciduous_closed tree_needleleaved_deciduous_open tree_mixed mosaic_tree_and_shrub mosaic_herbaceous shrubland shrubland_evergreen shrubland_deciduous grassland 
lichens_and_mosses sparse_vegetation sparse_tree sparse_shrub sparse_herbaceous tree_cover_flooded_fresh_or_brakish_water tree_cover_flooded_saline_water shrub_or_herbaceous_cover_flooded urban bare_areas bare_areas_consolidated 
bare_areas_unconsolidated water snow_and_ice""".split(" ")


flag_values = [0, 10, 11, 12, 20, 30, 40, 50, 60, 61, 62, 70, 71, 72, 80, 81, 82, 90, 100, 110, 120, 121, 122, 130, 140, 150, 151, 152, 153, 160, 170, 180, 190, 200, 201, 202, 210, 220]

               
#============================================================================
# Load the Variables
#============================================================================
nc_file = Dataset(path_to_file, mode='r')


# Load lat and lat bounds
lat = np.array(nc_file.variables['lat'])
lat_indexes = np.where((lat>area_of_interest["lat_min_area"]) & (lat<area_of_interest["lat_max_area"]))[0]
lat = lat[lat_indexes]
lat_bounds = np.array(nc_file.variables["lat_bounds"])[lat_indexes]
# Load lon and lon bounds
lon = np.array(nc_file.variables['lon'])
lon_indexes = np.where((lon>area_of_interest["lon_min_area"]) & (lon<area_of_interest["lon_max_area"]))[0]
lon = lon[lon_indexes]
lon_bounds = np.array(nc_file.variables["lon_bounds"])[lon_indexes]

# Load Classes
lccs_class = np.array(nc_file.variables['lccs_class'])[0,:,:]
lccs_class = lccs_class[lat_indexes,:]
lccs_class = lccs_class[:, lon_indexes]

# close nc file
nc_file.close()

#============================================================================
# 3. Save the variables
#============================================================================

with open('lulc.pkl', 'wb') as f:
    pickle.dump([lat,lat_bounds,lon,lon_bounds,lccs_class,flag_meanings,flag_values], f)
    